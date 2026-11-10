"""Verify pinned Qwen text-model artifacts with the standard library only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

DEFAULT_MANIFEST = Path(__file__).with_name('model-manifest.json')
ARCHITECTURE = 'Qwen3ForCausalLM'
REPOSITORY = 'Qwen/Qwen3-0.6B'
EXPECTED_CONFIG = {
    'model_type': 'qwen3',
    'num_hidden_layers': 28,
    'hidden_size': 1024,
    'intermediate_size': 3072,
    'num_attention_heads': 16,
    'num_key_value_heads': 8,
    'head_dim': 128,
    'vocab_size': 151936,
    'tie_word_embeddings': True,
    'torch_dtype': 'bfloat16',
}
ALLOWED_FILES = {
    'config.json': 1024 * 1024,
    'generation_config.json': 1024 * 1024,
    'model.safetensors': 2 * 1024**3,
    'tokenizer.json': 64 * 1024**2,
    'tokenizer_config.json': 1024 * 1024,
    'vocab.json': 32 * 1024**2,
    'merges.txt': 32 * 1024**2,
}
MAX_TOTAL_BYTES = 2 * 1024**3 + 128 * 1024**2
MAX_SAFETENSORS_HEADER = 4 * 1024**2
ALLOWED_TOKENIZERS = {'Qwen2Tokenizer', 'Qwen2TokenizerFast'}


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def _load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'),
                          object_pairs_hook=_no_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f'{path.name} is not valid JSON: {error}') from error


def _reject_custom_loading(value):
    if isinstance(value, dict):
        if value.get('auto_map'):
            raise ValueError('artifact configuration requests custom loading (auto_map)')
        if value.get('trust_remote_code') is True or value.get('custom_load') is True:
            raise ValueError('artifact configuration requests custom loading')
        for item in value.values():
            _reject_custom_loading(item)
    elif isinstance(value, list):
        for item in value:
            _reject_custom_loading(item)


def _verify_safetensors_header(path):
    size = path.stat().st_size
    if size < 10:
        raise ValueError('model.safetensors is too short for a header and payload')
    with path.open('rb') as stream:
        prefix = stream.read(8)
        if len(prefix) != 8:
            raise ValueError('model.safetensors has a truncated header length')
        header_size = struct.unpack('<Q', prefix)[0]
        if not 0 < header_size <= MAX_SAFETENSORS_HEADER:
            raise ValueError('Safetensors header length exceeds the 4 MiB limit')
        if header_size > size - 8:
            raise ValueError('Safetensors header length exceeds file size')
        header_bytes = stream.read(header_size)
        if len(header_bytes) != header_size:
            raise ValueError('Safetensors header is truncated')
    try:
        header = json.loads(header_bytes, object_pairs_hook=_no_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f'Safetensors header is not valid JSON: {error}') from error
    if not isinstance(header, dict) or not any(key != '__metadata__' for key in header):
        raise ValueError('Safetensors header has no tensor entries')
    metadata = header.get('__metadata__')
    if metadata is not None and (not isinstance(metadata, dict) or
                                 any(not isinstance(k, str) or not isinstance(v, str)
                                     for k, v in metadata.items())):
        raise ValueError('Safetensors metadata must map strings to strings')
    for name, spec in header.items():
        if name == '__metadata__':
            continue
        if not isinstance(name, str) or not isinstance(spec, dict):
            raise ValueError('Safetensors tensor header entry is malformed')
        shape = spec.get('shape')
        offsets = spec.get('data_offsets')
        if (not isinstance(spec.get('dtype'), str) or not isinstance(shape, list) or
                any(type(dim) is not int or dim < 0 for dim in shape) or
                not isinstance(offsets, list) or len(offsets) != 2 or
                any(type(value) is not int for value in offsets) or
                offsets[0] < 0 or offsets[1] < offsets[0] or
                offsets[1] > size - 8 - header_size):
            raise ValueError('Safetensors tensor header entry is malformed')


def verify(folder, manifest_path):
    """Verify inventory, pinned hashes and architecture metadata; never load weights."""
    folder = Path(folder)
    manifest_path = Path(manifest_path)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError('artifact directory is missing or is a symlink')
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError('manifest is missing or is a symlink')
    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError('manifest must be a JSON object')
    if (manifest.get('repository') != REPOSITORY or
            manifest.get('architecture') != ARCHITECTURE or
            not isinstance(manifest.get('revision'), str) or
            not re.fullmatch(r'[a-f0-9]{40}', manifest['revision'])):
        raise ValueError('manifest repository, revision or architecture is invalid')
    classes = manifest.get('classes')
    if (not isinstance(classes, list) or len(classes) != 7 or
            any(not isinstance(label, str) or not label for label in classes) or
            len(set(classes)) != 7):
        raise ValueError('manifest must contain seven unique classifier labels')
    entries = manifest.get('files')
    if not isinstance(entries, list) or len(entries) != len(ALLOWED_FILES):
        raise ValueError('manifest must list exactly the seven allowed files')
    names = [item.get('name') if isinstance(item, dict) else None for item in entries]
    if set(names) != set(ALLOWED_FILES) or len(set(names)) != len(ALLOWED_FILES):
        raise ValueError('manifest file inventory differs from the allowlist')
    if {path.name for path in folder.iterdir()} != set(ALLOWED_FILES):
        raise ValueError('artifact inventory differs from the allowlist')

    total_bytes = 0
    file_entries = {item['name']: item for item in entries}
    for name, maximum in ALLOWED_FILES.items():
        path = folder / name
        entry = file_entries[name]
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'{name} must be a regular file, not a symlink')
        size = entry.get('size_bytes')
        digest_expected = entry.get('sha256')
        if type(size) is not int or not 0 < size <= maximum:
            raise ValueError(f'{name} manifest size is outside experiment limits')
        if not isinstance(digest_expected, str) or not re.fullmatch(r'[a-f0-9]{64}', digest_expected):
            raise ValueError(f'{name} manifest SHA-256 is invalid')
        if path.stat().st_size != size:
            raise ValueError(f'{name} size does not match manifest')
        total_bytes += size
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest() != digest_expected:
            raise ValueError(f'{name} SHA-256 does not match manifest')
    if total_bytes > MAX_TOTAL_BYTES:
        raise ValueError('combined artifact size exceeds experiment limit')

    config = _load_json(folder / 'config.json')
    if not isinstance(config, dict):
        raise ValueError('config.json must be an object')
    _reject_custom_loading(config)
    if config.get('architectures') != [ARCHITECTURE]:
        raise ValueError('config architecture differs from standard Qwen3ForCausalLM')
    for key, expected in EXPECTED_CONFIG.items():
        if config.get(key) != expected or type(config.get(key)) is not type(expected):
            raise ValueError(f'config {key} differs from pinned standard architecture')

    tokenizer_config = _load_json(folder / 'tokenizer_config.json')
    if not isinstance(tokenizer_config, dict):
        raise ValueError('tokenizer_config.json must be an object')
    _reject_custom_loading(tokenizer_config)
    if tokenizer_config.get('tokenizer_class') not in ALLOWED_TOKENIZERS:
        raise ValueError('tokenizer class is not on the standard tokenizer allowlist')
    template = tokenizer_config.get('chat_template')
    if not isinstance(template, str) or len(template.encode('utf-8')) > 256 * 1024:
        raise ValueError('chat template is missing or exceeds its metadata limit')

    _verify_safetensors_header(folder / 'model.safetensors')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    try:
        verify(args.directory, args.manifest)
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(f'Artifact verification failed: {error}', file=sys.stderr)
        return 1
    print('PASS: pinned artifact inventory and metadata; weights were not loaded')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
