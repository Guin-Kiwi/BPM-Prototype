"""Fail-closed artifact and runtime gates; no model packages are imported."""
import hashlib
import importlib.util
import json
import struct
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
VERIFY = ROOT / 'experiments/local-interpreter/verify_artifacts.py'
RUNTIME = ROOT / 'experiments/local-interpreter/runtime_checks.py'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verify_module = load_module('interpreter_verify', VERIFY)
checks = load_module('interpreter_runtime_checks', RUNTIME)

CLASSES = ['Berry Blotch', 'Cercospora Brown Eye Spot', 'Healthy', 'Leaf Miner',
           'Phoma', 'Red Spider Mite', 'Rust']
NAMES = ['config.json', 'generation_config.json', 'model.safetensors',
         'tokenizer.json', 'tokenizer_config.json', 'vocab.json', 'merges.txt']


def safetensors_header(length=None):
    body = json.dumps({'weight': {'dtype': 'BF16', 'shape': [1],
                                  'data_offsets': [0, 2]}}).encode()
    if length is not None:
        body += b' ' * max(0, length - len(body))
    return struct.pack('<Q', len(body)) + body + b'\0\0'


@pytest.fixture
def artifact_set(tmp_path):
    folder = tmp_path / 'model'
    folder.mkdir()
    config = {
        'architectures': ['Qwen3ForCausalLM'], 'model_type': 'qwen3',
        'num_hidden_layers': 28, 'hidden_size': 1024, 'intermediate_size': 3072,
        'num_attention_heads': 16, 'num_key_value_heads': 8, 'head_dim': 128,
        'vocab_size': 151936, 'tie_word_embeddings': True, 'torch_dtype': 'bfloat16',
    }
    (folder / 'config.json').write_text(json.dumps(config))
    (folder / 'generation_config.json').write_text('{}')
    (folder / 'model.safetensors').write_bytes(safetensors_header())
    (folder / 'tokenizer.json').write_text('{}')
    (folder / 'tokenizer_config.json').write_text(json.dumps({
        'tokenizer_class': 'Qwen2Tokenizer',
        # The repository's tools branch is allowed as inert metadata, never executed.
        'chat_template': "{% if tools %}tools may be called{% endif %}",
    }))
    (folder / 'vocab.json').write_text('{}')
    (folder / 'merges.txt').write_text('\n')
    manifest = {
        'repository': 'Qwen/Qwen3-0.6B',
        'revision': 'c' * 40,
        'architecture': 'Qwen3ForCausalLM',
        'classes': CLASSES,
        'files': [{'name': name, 'size_bytes': (folder / name).stat().st_size,
                   'sha256': hashlib.sha256((folder / name).read_bytes()).hexdigest()}
                  for name in NAMES],
    }
    manifest_path = tmp_path / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest))
    return folder, manifest_path, manifest


def update_manifest(folder, manifest_path, manifest, name):
    path = folder / name
    entry = next(item for item in manifest['files'] if item['name'] == name)
    entry.update(size_bytes=path.stat().st_size,
                 sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    manifest_path.write_text(json.dumps(manifest))


def test_accepts_exact_pinned_artifacts_and_inert_template(artifact_set):
    folder, manifest_path, _ = artifact_set
    verify_module.verify(folder, manifest_path)


@pytest.mark.parametrize('problem', [
    'extra-file', 'missing-file', 'symlink', 'wrong-size', 'wrong-hash',
    'wrong-architecture', 'wrong-dimension', 'remote-code', 'wrong-tokenizer',
    'oversized-header', 'invalid-header', 'duplicate-manifest-file',
])
def test_rejects_untrusted_artifact_variations(artifact_set, problem, tmp_path):
    folder, manifest_path, manifest = artifact_set
    if problem == 'extra-file':
        (folder / 'loader.py').write_text('raise RuntimeError("must not execute")')
    elif problem == 'missing-file':
        (folder / 'merges.txt').unlink()
    elif problem == 'symlink':
        path = folder / 'model.safetensors'
        target = tmp_path / 'weights'
        path.rename(target)
        path.symlink_to(target)
    elif problem == 'wrong-size':
        (folder / 'config.json').write_text('{}')
        update_manifest(folder, manifest_path, manifest, 'config.json')
    elif problem == 'wrong-hash':
        path = folder / 'vocab.json'
        path.write_text('{"x":1}')
    elif problem in ('wrong-architecture', 'wrong-dimension', 'remote-code'):
        path = folder / 'config.json'
        config = json.loads(path.read_text())
        if problem == 'wrong-architecture':
            config['architectures'] = ['CustomQwen']
        elif problem == 'wrong-dimension':
            config['num_attention_heads'] = 17
        else:
            config['auto_map'] = {'AutoModel': 'repo.CustomModel'}
        path.write_text(json.dumps(config))
        update_manifest(folder, manifest_path, manifest, 'config.json')
    elif problem == 'wrong-tokenizer':
        path = folder / 'tokenizer_config.json'
        path.write_text(json.dumps({'tokenizer_class': 'CustomTokenizer',
                                    'chat_template': 'ordinary text'}))
        update_manifest(folder, manifest_path, manifest, 'tokenizer_config.json')
    elif problem == 'oversized-header':
        path = folder / 'model.safetensors'
        path.write_bytes(safetensors_header(4 * 1024 * 1024 + 1))
        update_manifest(folder, manifest_path, manifest, 'model.safetensors')
    elif problem == 'invalid-header':
        path = folder / 'model.safetensors'
        path.write_bytes(struct.pack('<Q', 9999) + b'{}')
        update_manifest(folder, manifest_path, manifest, 'model.safetensors')
    else:
        manifest['files'].append(dict(manifest['files'][0]))
        manifest_path.write_text(json.dumps(manifest))
    with pytest.raises((OSError, ValueError, KeyError, TypeError)):
        verify_module.verify(folder, manifest_path)


def container_info():
    image = 'sha256:' + 'a' * 64
    sources = {'/model': '/experiment/model', '/requests': '/experiment/requests',
               '/results': '/experiment/results'}
    info = {
        'Image': image,
        'Config': {'User': '1000:1000'},
        'HostConfig': {
            'NetworkMode': 'none', 'ReadonlyRootfs': True, 'Privileged': False,
            'CapDrop': ['ALL'], 'CapAdd': None,
            'SecurityOpt': ['no-new-privileges:true'],
            'Memory': 6 * 1024**3, 'MemorySwap': 6 * 1024**3,
            'NanoCpus': 2_000_000_000, 'PidsLimit': 64,
            'PidMode': '', 'IpcMode': 'private', 'Devices': [],
            'Tmpfs': {'/tmp': 'rw,noexec,nosuid,nodev,size=67108864,mode=1777'},
        },
        'Mounts': [
            {'Type': 'bind', 'Source': source, 'Destination': target,
             'RW': target == '/results', 'Mode': 'rw' if target == '/results' else 'ro',
             'Propagation': 'rprivate'}
            for target, source in sources.items()
        ],
    }
    return info, image, sources


def test_accepts_exact_container_configuration():
    info, image, sources = container_info()
    checks.validate_container(info, image, 1000, 1000, sources)


def test_accepts_structured_bind_mount_inspect_without_mode_string():
    # Docker Mounts API reports permissions through RW with an empty Mode string.
    info, image, sources = container_info()
    for mount in info['Mounts']:
        mount['Mode'] = ''
    checks.validate_container(info, image, 1000, 1000, sources)


@pytest.mark.parametrize('problem', [
    'network', 'rootfs', 'privileged', 'capabilities', 'no-new-privileges',
    'memory', 'swap', 'cpu', 'pids', 'pid-mode', 'ipc', 'device', 'scratch',
    'identity', 'mutable-image', 'extra-mount', 'writable-model', 'wrong-source',
])
def test_rejects_weakened_container_configuration(problem):
    info, image, sources = container_info()
    host = info['HostConfig']
    if problem == 'network': host['NetworkMode'] = 'bridge'
    elif problem == 'rootfs': host['ReadonlyRootfs'] = False
    elif problem == 'privileged': host['Privileged'] = True
    elif problem == 'capabilities': host['CapAdd'] = ['SYS_ADMIN']
    elif problem == 'no-new-privileges': host['SecurityOpt'] = []
    elif problem == 'memory': host['Memory'] = 2 * 1024**3
    elif problem == 'swap': host['MemorySwap'] = -1
    elif problem == 'cpu': host['NanoCpus'] = 3_000_000_000
    elif problem == 'pids': host['PidsLimit'] = 0
    elif problem == 'pid-mode': host['PidMode'] = 'host'
    elif problem == 'ipc': host['IpcMode'] = 'host'
    elif problem == 'device': host['Devices'] = [{'PathOnHost': '/dev/sda'}]
    elif problem == 'scratch': host['Tmpfs'] = {'/tmp': 'rw'}
    elif problem == 'identity': info['Config']['User'] = '0:0'
    elif problem == 'mutable-image': info['Image'] = 'qwen:latest'
    elif problem == 'extra-mount': info['Mounts'].append({'Destination': '/home'})
    elif problem == 'writable-model': info['Mounts'][0]['RW'] = True
    else: info['Mounts'][0]['Source'] = '/home/model'
    with pytest.raises(ValueError):
        checks.validate_container(info, image, 1000, 1000, sources)


def effective_fixture(tmp_path):
    proc = tmp_path / 'proc'
    (proc / 'self').mkdir(parents=True)
    (proc / 'net').mkdir()
    status = ('Uid:\t1000\t1000\t1000\t1000\nGid:\t1000\t1000\t1000\t1000\n'
              'CapEff:\t0000000000000000\nNoNewPrivs:\t1\nSeccomp:\t2\n')
    (proc / 'self/status').write_text(status)
    mounts = []
    for i, (point, opts, fstype) in enumerate([
        ('/', 'ro,relatime', 'overlay'), ('/model', 'ro,relatime', 'ext4'),
        ('/requests', 'ro,relatime', 'ext4'), ('/results', 'rw,relatime', 'ext4'),
        ('/tmp', 'rw,noexec,nosuid,nodev,size=65536k', 'tmpfs'),
    ], 1):
        mounts.append(f'{i} 0 0:1 / {point} {opts} - {fstype} {fstype} rw')
    (proc / 'self/mountinfo').write_text('\n'.join(mounts) + '\n')
    (proc / 'net/dev').write_text('Inter-| Receive\n face | bytes\nlo: 0 0\n')
    cgroup = tmp_path / 'cgroup'
    cgroup.mkdir()
    (cgroup / 'cpu.max').write_text('200000 100000\n')
    (cgroup / 'memory.max').write_text(str(6 * 1024**3))
    (cgroup / 'memory.swap.max').write_text('0')
    (cgroup / 'pids.max').write_text('64')
    return proc, cgroup


def test_effective_containment_returns_observed_controls(tmp_path):
    proc, cgroup = effective_fixture(tmp_path)
    evidence = checks.effective_containment(proc, cgroup, ['lo'])
    assert evidence['uid'] == evidence['gid'] == 1000
    assert evidence['cap_eff'] == '0000000000000000'
    assert evidence['no_new_privs'] == 1 and evidence['seccomp'] == 2
    assert evidence['interfaces'] == ['lo']
    assert evidence['cpu_count'] == 2
    assert evidence['memory_max'] == 6 * 1024**3
    assert evidence['swap_max'] == 0 and evidence['pids_max'] == 64
    assert evidence['mounts']['/']['readonly']
    assert evidence['mounts']['/model']['readonly']
    assert evidence['mounts']['/requests']['readonly']
    assert not evidence['mounts']['/results']['readonly']
    assert 'noexec' in evidence['mounts']['/tmp']['options']


@pytest.mark.parametrize('problem', ['root-user', 'capabilities', 'no-new-privs',
                                    'seccomp', 'network', 'cpu', 'memory', 'swap',
                                    'pids', 'writable-model', 'readonly-results',
                                    'scratch-exec', 'missing-control'])
def test_effective_containment_fails_closed(tmp_path, problem):
    proc, cgroup = effective_fixture(tmp_path)
    status_path = proc / 'self/status'
    status = status_path.read_text()
    if problem == 'root-user': status = status.replace('1000\t1000\t1000\t1000', '0\t0\t0\t0', 1)
    elif problem == 'capabilities': status = status.replace('0000000000000000', '0000000000000001')
    elif problem == 'no-new-privs': status = status.replace('NoNewPrivs:\t1', 'NoNewPrivs:\t0')
    elif problem == 'seccomp': status = status.replace('Seccomp:\t2', 'Seccomp:\t0')
    elif problem == 'network':
        (proc / 'net/dev').write_text('Inter-| Receive\n face | bytes\neth0: 0 0\nlo: 0 0\n')
    elif problem == 'cpu': (cgroup / 'cpu.max').write_text('300000 100000')
    elif problem == 'memory': (cgroup / 'memory.max').write_text(str(2 * 1024**3))
    elif problem == 'swap': (cgroup / 'memory.swap.max').write_text('1')
    elif problem == 'pids': (cgroup / 'pids.max').write_text('128')
    elif problem in ('writable-model', 'readonly-results', 'scratch-exec'):
        mount_path = proc / 'self/mountinfo'
        mounts = mount_path.read_text()
        if problem == 'writable-model': mounts = mounts.replace('/model ro,relatime', '/model rw,relatime')
        elif problem == 'readonly-results': mounts = mounts.replace('/results rw,relatime', '/results ro,relatime')
        else: mounts = mounts.replace('/tmp rw,noexec,nosuid,nodev', '/tmp rw,nosuid,nodev')
        mount_path.write_text(mounts)
    else:
        (cgroup / 'memory.swap.max').unlink()
    status_path.write_text(status)
    with pytest.raises(ValueError):
        checks.effective_containment(proc, cgroup, ['lo'])
