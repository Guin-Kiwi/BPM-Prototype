"""Verify pinned artifact integrity using only the standard library; never load weights."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

DEFAULT_MANIFEST = Path(__file__).with_name('model-manifest.json')


def verify(folder, manifest_path):
    manifest = json.loads(manifest_path.read_text())
    entries = {item['name']: item for item in manifest['files']}
    expected = {'config.json', 'model.safetensors'}
    if set(entries) != expected or len(manifest['files']) != 2:
        raise ValueError('manifest must allow only config.json and model.safetensors')
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError('artifact inventory directory is missing or is a symlink')
    if {p.name for p in folder.iterdir()} != expected:
        raise ValueError('artifact inventory differs from the manifest')
    for name, entry in entries.items():
        path = folder / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'{name} must be a regular file, not a symlink')
        size = entry['size_bytes']
        if type(size) is not int or not 0 < size <= 256 * 1024 * 1024:
            raise ValueError('manifest size is outside experiment limits')
        if name == 'config.json' and size > 128 * 1024:
            raise ValueError('config size exceeds experiment limit')
        if path.stat().st_size != size:
            raise ValueError(f'{name} size does not match manifest')
        if not re.fullmatch('[a-f0-9]{64}', entry['sha256']):
            raise ValueError('manifest SHA-256 is invalid')
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest() != entry['sha256']:
            raise ValueError(f'{name} SHA-256 does not match manifest')
    config = json.loads((folder / 'config.json').read_text())
    labels = manifest['classes']
    if (len(labels) != 7 or len(set(labels)) != 7 or
            config.get('num_classes') != len(labels) or config.get('label_names') != labels):
        raise ValueError('config class mapping does not match manifest')
    if config.get('architecture') != manifest['architecture']:
        raise ValueError('config architecture does not match manifest')

    def reject_custom(value):
        if isinstance(value, dict):
            if (value.get('custom_load') or value.get('trust_remote_code') or
                    value.get('auto_map')):
                raise ValueError('config requests custom loading')
            for item in value.values():
                reject_custom(item)
        elif isinstance(value, list):
            for item in value:
                reject_custom(item)

    reject_custom(config)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST,
                        help='trusted manifest; normally use the versioned default')
    args = parser.parse_args()
    try:
        verify(args.directory, args.manifest)
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(f'Artifact verification failed: {error}', file=sys.stderr)
        return 1
    print('PASS: pinned file integrity only; tensor safety and model behavior unverified')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
