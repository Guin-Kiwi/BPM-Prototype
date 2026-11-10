"""Fail closed before untrusted tensor loading or accepting numeric output."""
import importlib.util
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[2] / 'experiments/local-classifier/runtime_checks.py'
spec = importlib.util.spec_from_file_location('runtime_checks', SOURCE)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


@pytest.fixture
def container():
    return {
        'Image': 'sha256:' + 'a' * 64,
        'Config': {'User': '1000:1000'},
        'HostConfig': {
            'NetworkMode': 'none', 'ReadonlyRootfs': True, 'Privileged': False,
            'CapDrop': ['ALL'], 'CapAdd': None,
            'SecurityOpt': ['no-new-privileges:true'],
            'Memory': 2147483648, 'MemorySwap': 2147483648,
            'NanoCpus': 2000000000, 'PidsLimit': 64,
            'PidMode': '', 'IpcMode': 'private', 'Devices': [],
            'Tmpfs': {'/tmp': 'rw,noexec,nosuid,nodev,size=67108864,mode=1777'},
        },
        'Mounts': [
            {'Type': 'bind', 'Source': '/experiment/' + name, 'Destination': target,
             'RW': writable, 'Propagation': 'rprivate'}
            for name, target, writable in [('model', '/model', False),
                                            ('inputs', '/inputs', False),
                                            ('results', '/results', True)]
        ],
    }


def validate(container):
    checks.validate_container(container, 'sha256:' + 'a' * 64, 1000, 1000,
                              {'/model': '/experiment/model',
                               '/inputs': '/experiment/inputs',
                               '/results': '/experiment/results'})


def test_accepts_declared_containment(container):
    validate(container)


@pytest.mark.parametrize('key,value', [
    ('NetworkMode', 'bridge'), ('ReadonlyRootfs', False), ('Privileged', True),
    ('CapDrop', []), ('CapAdd', ['SYS_ADMIN']), ('SecurityOpt', []),
    ('Memory', 0), ('MemorySwap', -1), ('NanoCpus', 0), ('PidsLimit', 0),
    ('PidMode', 'host'), ('IpcMode', 'host'), ('Devices', [{'PathOnHost': '/dev/sda'}]),
    ('Tmpfs', {'/tmp': 'rw'}),
])
def test_rejects_weakened_host_controls(container, key, value):
    container['HostConfig'][key] = value
    with pytest.raises(ValueError):
        validate(container)


@pytest.mark.parametrize('problem', ['root', 'image', 'extra', 'writable', 'source'])
def test_rejects_identity_or_mount_escape(container, problem):
    if problem == 'root':
        container['Config']['User'] = '0:0'
    elif problem == 'image':
        container['Image'] = 'moving:tag'
    elif problem == 'extra':
        container['Mounts'].append({'Destination': '/home'})
    elif problem == 'writable':
        container['Mounts'][0]['RW'] = True
    else:
        container['Mounts'][0]['Source'] = '/home'
    with pytest.raises(ValueError):
        validate(container)


@pytest.mark.parametrize('scores', [[1/7] * 7, [1, 0, 0, 0, 0, 0, 0]])
def test_accepts_seven_class_distribution(scores):
    checks.validate_scores(scores)


@pytest.mark.parametrize('scores', [[], [0.5, 0.5], [float('nan')] * 7,
                                   [float('inf')] * 7, [-1, 2, 0, 0, 0, 0, 0],
                                   [0.1] * 7])
def test_rejects_invalid_model_output(scores):
    with pytest.raises(ValueError):
        checks.validate_scores(scores)


@pytest.mark.parametrize('specs', [
    {}, {'head': ('F16', [1000, 768])},
    {'head': ('F64', [7, 768])},
    {'head': ('F16', [7, 768]), 'extra': ('F16', [1])},
])
def test_rejects_incompatible_tensor_specs(specs):
    with pytest.raises(ValueError):
        checks.validate_tensor_specs(specs, {'head': [7, 768]})


def test_accepts_expected_half_precision_head():
    checks.validate_tensor_specs({'head': ('F16', [7, 768])}, {'head': [7, 768]})
