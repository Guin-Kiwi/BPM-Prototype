"""Opt-in offline experiment; this module is never imported by the application."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import signal
import struct
import sys
import time
import traceback

from runtime_checks import validate_scores, validate_tensor_specs
from verify_artifacts import verify

HERE = Path(__file__).resolve().parent


def containment():
    status = dict(line.split(':', 1) for line in Path('/proc/self/status').read_text().splitlines()
                  if ':' in line)
    assert os.geteuid() != 0, 'root is forbidden'
    assert int(status['CapEff'].strip(), 16) == 0, 'effective capabilities'
    assert status['NoNewPrivs'].strip() == '1', 'privilege escalation enabled'
    assert status['Seccomp'].strip() == '2', 'seccomp filter absent'
    interfaces = sorted(p.name for p in Path('/sys/class/net').iterdir())
    assert interfaces == ['lo'], 'unexpected network interface'
    mounts = {}
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        fields = line.split()
        if fields[4] in {'/', '/model', '/inputs', '/results', '/tmp'}:
            mounts[fields[4]] = fields[5].split(',')
    for target in ['/', '/model', '/inputs']:
        assert 'ro' in mounts[target], f'{target} is writable'
    assert 'rw' in mounts['/results'], 'results unavailable'
    assert {'noexec', 'nosuid', 'nodev'} <= set(mounts['/tmp']), 'scratch flags'
    cgroup = Path('/sys/fs/cgroup')
    limits = {name: (cgroup / name).read_text().strip()
              for name in ['memory.max', 'memory.swap.max', 'pids.max', 'cpu.max']}
    assert limits['memory.max'] == str(2**31), 'memory limit'
    assert limits['memory.swap.max'] == '0', 'swap enabled'
    assert limits['pids.max'] == '64', 'process limit'
    quota, period = map(int, limits['cpu.max'].split())
    assert quota / period == 2, 'CPU limit'
    return dict(uid=os.geteuid(), gid=os.getegid(), interfaces=interfaces,
                status={k: status[k].strip() for k in ['CapEff', 'NoNewPrivs', 'Seccomp']},
                mounts=mounts, cgroup=limits, wall_timeout_seconds=180)


def run():
    start = time.perf_counter()
    result = {'containment': containment()}
    verify(Path('/model'), HERE / 'model-manifest.json')
    manifest = json.loads((HERE / 'model-manifest.json').read_text())
    result['model'] = manifest
    # Bound the header before invoking even the maintained Safetensors parser.
    weights = Path('/model/model.safetensors')
    with weights.open('rb') as stream:
        header_bytes = struct.unpack('<Q', stream.read(8))[0]
        if not 0 < header_bytes <= 1024 * 1024:
            raise ValueError('tensor header outside bounded experiment limit')

    import torch
    from timm.models.convnext import convnext_small
    from safetensors import safe_open
    from safetensors.torch import load_file
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
    from torchvision import transforms
    from torchvision.transforms import InterpolationMode

    assert torch.version.cuda is None, 'CPU-only build required'
    torch.set_num_threads(2)
    torch.set_num_interop_threads(1)
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True)
    imports_done = time.perf_counter()
    model = convnext_small(pretrained=False, num_classes=7).eval()
    expected = {name: list(tensor.shape) for name, tensor in model.state_dict().items()}
    with safe_open(weights, framework='pt', device='cpu') as handle:
        specs = {name: (handle.get_slice(name).get_dtype(), handle.get_slice(name).get_shape())
                 for name in handle.keys()}
    validate_tensor_specs(specs, expected)
    tensor_start = time.perf_counter()
    tensors = load_file(weights, device='cpu')
    if any(not torch.isfinite(tensor).all().item() for tensor in tensors.values()):
        raise ValueError('non-finite weights')
    # Standard FP32 CPU model; strict loading converts the published F16 tensors.
    model.load_state_dict(tensors, strict=True)
    del tensors
    ready = time.perf_counter()
    result['timing_seconds'] = dict(imports_and_preflight=imports_done-start,
                                  architecture_and_header=tensor_start-imports_done,
                                  tensor_load_and_validation=ready-tensor_start,
                                  startup_to_ready=ready-start)
    result['tensor_inventory'] = dict(count=len(specs), header_bytes=header_bytes,
                                     dtype='F16', runtime_dtype='float32',
                                     head_weight=specs['head.fc.weight'][1],
                                     head_bias=specs['head.fc.bias'][1])
    result['inventory'] = {d.metadata['Name']: d.version for d in importlib.metadata.distributions()}
    result['platform'] = dict(python=sys.version, machine=platform.machine(),
                              processor=platform.processor(), torch_threads=torch.get_num_threads())
    normalize = [transforms.ToTensor(), transforms.Normalize(
        [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]
    pipelines = {
        'config-center-crop': transforms.Compose([
            transforms.Resize(224, interpolation=InterpolationMode.BILINEAR, antialias=True),
            transforms.CenterCrop(224), *normalize]),
        'card-direct-resize': transforms.Compose([
            transforms.Resize((224, 224), interpolation=InterpolationMode.BILINEAR,
                              antialias=True), *normalize]),
    }
    result['preprocessing'] = dict(input='RGB', size=[224, 224], interpolation='bilinear',
        antialias=True, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225],
        modes=list(pipelines), note='Config crop_pct=1; direct resize follows model-card training note.')
    input_paths = sorted(Path('/inputs').iterdir())
    if [p.name for p in input_paths] != ['sample-01.jpg', 'sample-02.jpg', 'sample-03.jpg']:
        raise ValueError('only the three staged neutral-name examples are permitted')
    examples = []
    result['inputs'] = []
    for path in input_paths:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 1024 * 1024:
            raise ValueError('invalid image file')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with Image.open(path) as source:
            if source.size != (512, 256) or source.format != 'JPEG':
                raise ValueError('unexpected example dimensions/format')
            image = source.convert('RGB')
        result['inputs'].append(dict(name=path.name, sha256=digest, dimensions=list(image.size)))
        examples.extend([(path.name, 'original', image),
                         (path.name, 'rotate15', image.rotate(15, fillcolor='white')),
                         (path.name, 'dim50', ImageEnhance.Brightness(image).enhance(0.5)),
                         (path.name, 'blur2', image.filter(ImageFilter.GaussianBlur(2)))])
    examples.append(('blank', 'synthetic-white', Image.new('RGB', (224, 224), 'white')))
    geometry = Image.new('RGB', (224, 224), 'navy')
    draw = ImageDraw.Draw(geometry)
    draw.rectangle((20, 20, 100, 100), fill='red')
    draw.ellipse((120, 120, 210, 210), fill='yellow')
    examples.append(('non-coffee', 'synthetic-geometry', geometry))
    result['predictions'] = []
    with torch.inference_mode():
        warmup = time.perf_counter()
        model(torch.zeros(1, 3, 224, 224))
        result['timing_seconds']['warmup'] = time.perf_counter()-warmup
        for mode, transform in pipelines.items():
            for name, variant, image in examples:
                before = time.perf_counter()
                tensor = transform(image).unsqueeze(0)
                preprocessing_seconds = time.perf_counter()-before
                timings, repeated = [], []
                for _ in range(3):
                    before = time.perf_counter()
                    logits = model(tensor)
                    if logits.shape != (1, 7) or not torch.isfinite(logits).all().item():
                        raise ValueError('invalid logits')
                    scores = logits.softmax(-1)[0].tolist()
                    timings.append(time.perf_counter()-before)
                    validate_scores(scores)
                    repeated.append(scores)
                result['predictions'].append(dict(
                    input=name, variant=variant, preprocessing=mode,
                    preprocessing_seconds=preprocessing_seconds,
                    inference_seconds=timings, scores=repeated[0],
                    max_repeat_score_difference=max(abs(a-b) for values in repeated
                                                  for a, b in zip(values, repeated[0]))))
    result['memory'] = dict(method='Linux getrusage(RUSAGE_SELF).ru_maxrss KiB; cgroup v2 memory.peak bytes',
                            process_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                            cgroup_peak_bytes=int(Path('/sys/fs/cgroup/memory.peak').read_text()))
    result['timing_seconds']['total'] = time.perf_counter()-start
    result['status'] = 'completed'
    return result


def main():
    def expired(*_):
        raise TimeoutError('experiment exceeded 180 seconds')
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(180)
    try:
        result = run()
    except Exception as error:
        result = dict(status='failed', error=f'{type(error).__name__}: {error}')
        traceback.print_exc()
    finally:
        signal.alarm(0)
    # Exclusive creation prevents silent replacement of an earlier run.
    with Path('/results/first-run.json').open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(result['status'])
    return 0 if result['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
