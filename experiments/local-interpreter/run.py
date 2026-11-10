"""Opt-in offline interpreter experiment; never imported by the application."""
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

from protocol import build_user_payload, validate_response
from runtime_checks import effective_containment
from verify_artifacts import verify

HERE = Path(__file__).resolve().parent
RESULT = Path('/results/first-run.json')


def write_result(result):
    temporary = RESULT.with_suffix('.tmp')
    with temporary.open('w', encoding='utf-8') as output:
        json.dump(result, output, ensure_ascii=False, indent=2, allow_nan=False)
        output.write('\n')
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, RESULT)


def load_model(manifest):
    import torch
    from safetensors import safe_open
    from safetensors.torch import load_file
    from transformers import PreTrainedTokenizerFast, Qwen3Config, Qwen3ForCausalLM

    if torch.version.cuda is not None:
        raise ValueError('CPU-only torch required')
    torch.set_num_threads(2)
    torch.set_num_interop_threads(1)
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True)
    if manifest['architecture'] != 'Qwen3ForCausalLM':
        raise ValueError('unexpected manifest architecture')
    config_data = json.loads(Path('/model/config.json').read_text())
    config = Qwen3Config.from_dict(config_data)
    if config.model_type != 'qwen3' or not config.tie_word_embeddings:
        raise ValueError('unexpected architecture or embedding tie')
    tokenizer = PreTrainedTokenizerFast(tokenizer_file='/model/tokenizer.json')
    for token, expected in [('<|im_start|>', 151644), ('<|im_end|>', 151645)]:
        if tokenizer.convert_tokens_to_ids(token) != expected or tokenizer.encode(token, add_special_tokens=False) != [expected]:
            raise ValueError('unexpected ChatML token')
    weights = Path('/model/model.safetensors')
    with weights.open('rb') as stream:
        raw = stream.read(8)
        if len(raw) != 8:
            raise ValueError('truncated tensor header')
        size = struct.unpack('<Q', raw)[0]
        if not 0 < size <= 1024 * 1024 or size + 8 > weights.stat().st_size:
            raise ValueError('tensor header outside bound')
    # Standard CPU initialization materializes non-persistent rotary buffers, which
    # are absent from the checkpoint and cannot be restored by load_state_dict.
    original_dtype = torch.get_default_dtype()
    try:
        torch.set_default_dtype(torch.bfloat16)
        model = Qwen3ForCausalLM(config)
    finally:
        torch.set_default_dtype(original_dtype)
    expected = {key: list(value.shape) for key, value in model.state_dict().items()}
    with safe_open(weights, framework='pt', device='cpu') as handle:
        specs = {name: (handle.get_slice(name).get_dtype(), handle.get_slice(name).get_shape()) for name in handle.keys()}
    names = set(specs)
    optional_head = 'lm_head.weight'
    if names not in (set(expected), set(expected) - {optional_head}):
        raise ValueError('unexpected tensor keys')
    for name, (dtype, shape) in specs.items():
        if dtype not in ('BF16', 'F16', 'F32') or shape != expected[name]:
            raise ValueError('unexpected tensor shape or dtype: ' + name)
    tensors = load_file(weights, device='cpu')
    if any(not torch.isfinite(value).all().item() for value in tensors.values()):
        raise ValueError('nonfinite weights')
    if optional_head in tensors and not torch.equal(tensors[optional_head], tensors['model.embed_tokens.weight']):
        raise ValueError('tied embedding and stored head differ')
    if optional_head not in tensors:
        tensors[optional_head] = tensors['model.embed_tokens.weight']
    model.load_state_dict(tensors, strict=True, assign=True)
    model.tie_weights()
    if model.lm_head.weight.data_ptr() != model.model.embed_tokens.weight.data_ptr():
        raise ValueError('embedding tie not preserved')
    model.eval()
    return model, tokenizer, {'header_bytes': size, 'tensor_count': len(specs), 'stored_head': optional_head in names, 'tied': True}


def main():
    start = time.perf_counter()
    RESULT.parent.mkdir(exist_ok=True)
    with RESULT.open('x', encoding='utf-8') as output:
        output.write('{}\n')
    result = {'status': 'starting', 'cases': [], 'semantic_adherence': 'not automatically established'}
    write_result(result)
    def timeout(_signum, _frame):
        raise TimeoutError('180 second wall limit')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(180)
    try:
        result['containment'] = effective_containment()
        verify(Path('/model'), HERE / 'model-manifest.json')
        manifest = json.loads((HERE / 'model-manifest.json').read_text())
        request_bytes = Path('/requests/requests.json').read_bytes()
        if len(request_bytes) > 100000:
            raise ValueError('requests exceed size limit')
        envelope = json.loads(request_bytes)
        if set(envelope) != {'cases'} or not isinstance(envelope['cases'], list) or not envelope['cases']:
            raise ValueError('invalid requests envelope')
        requests = envelope['cases']
        classes = manifest['classes']
        result['requests_sha256'] = hashlib.sha256(request_bytes).hexdigest()
        prompt = (HERE / 'prompt.txt').read_text().strip()
        if '<|' in prompt:
            raise ValueError('invalid system prompt')
        result['prompt_sha256'] = hashlib.sha256(prompt.encode()).hexdigest()
        result['model'] = manifest
        result['inventory'] = {d.metadata['Name']: d.version for d in importlib.metadata.distributions()}
        result['platform'] = {'python': sys.version, 'machine': platform.machine(), 'processor': platform.processor()}
        model, tokenizer, tensors = load_model(manifest)
        import torch
        result['tensor_inventory'] = tensors
        result['startup_seconds'] = time.perf_counter() - start
        result['status'] = 'running'
        write_result(result)
        for case in requests:
            case_result = {'id': case.get('id') if isinstance(case, dict) else None, 'status': 'starting'}
            result['cases'].append(case_result)
            write_result(result)
            try:
                if set(case) != {'id', 'request'} or not isinstance(case['id'], str):
                    raise ValueError('invalid case envelope')
                request = case['request']
                payload = build_user_payload(request, classes)
                chat = '<|im_start|>system\n' + prompt + '<|im_end|>\n<|im_start|>user\n' + payload + '<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
                input_ids = tokenizer.encode(chat, add_special_tokens=False, return_tensors='pt')
                count = input_ids.shape[1]
                if count > 1024:
                    raise ValueError('input exceeds token limit')
                before = time.perf_counter()
                with torch.inference_mode():
                    output = model.generate(input_ids, attention_mask=torch.ones_like(input_ids), max_new_tokens=384,
                        do_sample=False, use_cache=True, eos_token_id=151645, pad_token_id=151645)
                elapsed = time.perf_counter() - before
                generated = output[0, count:]
                raw = tokenizer.decode(generated, skip_special_tokens=False)
                if raw.endswith('<|im_end|>'):
                    raw = raw[:-len('<|im_end|>')]
                case_result.update(status='completed', input_tokens=count, output_tokens=len(generated), inference_seconds=elapsed,
                    raw_response=raw[:16384], validation_errors=validate_response(raw, classes, request))
            except TimeoutError:
                case_result['status'] = 'timeout'
                write_result(result)
                raise
            except Exception as error:
                case_result.update(status='error', error=f'{type(error).__name__}: {error}')
            write_result(result)
        result['status'] = 'completed'
    except Exception as error:
        result['status'] = 'error'
        result['error'] = f'{type(error).__name__}: {error}'
        result['traceback'] = traceback.format_exc(limit=8)
    finally:
        signal.alarm(0)
        result['elapsed_seconds'] = time.perf_counter() - start
        result['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        memory = Path('/sys/fs/cgroup/memory.peak')
        if memory.exists():
            result['cgroup_memory_peak_bytes'] = int(memory.read_text().strip())
        write_result(result)
    if result['status'] != 'completed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
