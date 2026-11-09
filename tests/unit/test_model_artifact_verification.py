"""Artifact integrity checks must not import or load model runtimes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

VERIFY = Path(__file__).resolve().parents[2] / 'experiments/local-classifier/verify_artifacts.py'


@pytest.fixture
def artifacts(tmp_path):
    folder = tmp_path / 'model'
    folder.mkdir()
    config = {'architecture': 'convnext_small', 'num_classes': 7,
              'label_names': [f'class-{i}' for i in range(7)],
              'pretrained_cfg': {'custom_load': False}}
    (folder / 'config.json').write_text(json.dumps(config))
    (folder / 'model.safetensors').write_bytes(b'fixture weights, never loaded')
    manifest = {'architecture': config['architecture'], 'classes': config['label_names'],
                'files': [{'name': p.name, 'size_bytes': p.stat().st_size,
                           'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                          for p in folder.iterdir()]}
    source = tmp_path / 'manifest.json'
    source.write_text(json.dumps(manifest))
    return folder, source, manifest


def run_check(folder, source):
    return subprocess.run([sys.executable, str(VERIFY), str(folder), '--manifest', str(source)],
                          capture_output=True, text=True, timeout=5)


def test_verified_artifacts_are_not_loaded(artifacts):
    folder, source, _ = artifacts
    result = run_check(folder, source)
    assert result.returncode == 0, result.stderr
    assert 'integrity only' in result.stdout


@pytest.mark.parametrize('problem,message', [
    ('missing', 'inventory'), ('extra', 'inventory'), ('symlink', 'regular file'),
    ('size', 'size'), ('tampered', 'SHA-256'), ('labels', 'class mapping'),
    ('loader', 'custom loading'),
])
def test_rejects_untrusted_artifact_variations(artifacts, problem, message):
    folder, source, manifest = artifacts
    weights = folder / 'model.safetensors'
    if problem == 'missing':
        weights.unlink()
    elif problem == 'extra':
        (folder / 'loader.py').write_text('raise RuntimeError("must not execute")')
    elif problem == 'symlink':
        target = folder.parent / 'outside'
        weights.rename(target)
        weights.symlink_to(target)
    elif problem == 'size':
        weights.write_bytes(b'wrong length')
    elif problem == 'tampered':
        value = weights.read_bytes()
        weights.write_bytes(bytes([value[0] ^ 1]) + value[1:])
    else:
        config_path = folder / 'config.json'
        config = json.loads(config_path.read_text())
        if problem == 'labels':
            config['label_names'].reverse()
        else:
            config['pretrained_cfg']['custom_load'] = True
        config_path.write_text(json.dumps(config))
        entry = next(f for f in manifest['files'] if f['name'] == 'config.json')
        entry.update(size_bytes=config_path.stat().st_size,
                     sha256=hashlib.sha256(config_path.read_bytes()).hexdigest())
        source.write_text(json.dumps(manifest))
    result = run_check(folder, source)
    assert result.returncode != 0
    assert message in result.stderr
