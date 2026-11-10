"""Standard-library gates for the contained, opt-in classifier experiment."""
import math
import re


def validate_container(info, image, uid, gid, sources):
    """Check Docker's actual created configuration before starting the container."""
    if (not re.fullmatch(r'sha256:[a-f0-9]{64}', image) or uid <= 0 or gid < 0 or
            info['Image'] != image or info['Config']['User'] != f'{uid}:{gid}'):
        raise ValueError('immutable image or non-root identity mismatch')
    host = info['HostConfig']
    expected = dict(NetworkMode='none', ReadonlyRootfs=True, Privileged=False,
                    Memory=2**31, MemorySwap=2**31, NanoCpus=2_000_000_000,
                    PidsLimit=64, PidMode='', IpcMode='private')
    if any(host.get(k) != v for k, v in expected.items()):
        raise ValueError('network, privilege or resource containment mismatch')
    if (host.get('CapAdd') or host.get('Devices') or
            {v.upper() for v in host.get('CapDrop', [])} != {'ALL'} or
            host.get('SecurityOpt') != ['no-new-privileges:true']):
        raise ValueError('capability, device or security policy mismatch')
    tmp = host.get('Tmpfs', {})
    if set(tmp) != {'/tmp'} or set(tmp['/tmp'].split(',')) != {
            'rw', 'noexec', 'nosuid', 'nodev', 'size=67108864', 'mode=1777'}:
        raise ValueError('scratch containment mismatch')
    mounts = info['Mounts']
    if len(mounts) != 3 or {m['Destination'] for m in mounts} != set(sources):
        raise ValueError('mount inventory mismatch')
    for mount in mounts:
        target = mount['Destination']
        if (mount.get('Type') != 'bind' or mount.get('Source') != sources[target] or
                mount.get('RW') != (target == '/results') or
                mount.get('Propagation') != 'rprivate'):
            raise ValueError('mount source or permissions mismatch')


def validate_scores(scores):
    if (len(scores) != 7 or any(not math.isfinite(x) or not 0 <= x <= 1 for x in scores)
            or not math.isclose(sum(scores), 1, abs_tol=1e-5)):
        raise ValueError('expected a finite seven-class probability distribution')


def validate_tensor_specs(specs, expected):
    if set(specs) != set(expected):
        raise ValueError('tensor key inventory differs from standard architecture')
    total = 0
    for name, (dtype, shape) in specs.items():
        if dtype != 'F16' or list(shape) != list(expected[name]):
            raise ValueError('tensor dtype or shape differs from standard architecture')
        total += math.prod(shape) * 2
    if total > 128 * 1024 * 1024:
        raise ValueError('tensor payload exceeds experiment limit')
