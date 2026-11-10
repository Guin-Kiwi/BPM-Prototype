"""Standard-library preflight and effective containment checks for local inference."""
from pathlib import Path
import re
import socket

IMAGE_RE = re.compile(r'sha256:[a-f0-9]{64}')
CPU_LIMIT = 2
MEMORY_LIMIT = 6 * 1024**3
PID_LIMIT = 64
SCRATCH_BYTES = 64 * 1024**2
REQUIRED_MOUNTS = {'/', '/model', '/requests', '/results', '/tmp'}


def validate_container(info, image, uid, gid, sources):
    """Validate Docker inspect metadata before starting the container."""
    try:
        if (not isinstance(image, str) or not IMAGE_RE.fullmatch(image) or
                type(uid) is not int or uid <= 0 or type(gid) is not int or gid < 0 or
                info['Image'] != image or info['Config']['User'] != f'{uid}:{gid}'):
            raise ValueError('immutable image or non-root identity mismatch')
        host = info['HostConfig']
        expected = {
            'NetworkMode': 'none', 'ReadonlyRootfs': True, 'Privileged': False,
            'Memory': MEMORY_LIMIT, 'MemorySwap': MEMORY_LIMIT,
            'NanoCpus': CPU_LIMIT * 1_000_000_000, 'PidsLimit': PID_LIMIT,
            'PidMode': '', 'IpcMode': 'private',
        }
        if any(host.get(key) != value for key, value in expected.items()):
            raise ValueError('network, privilege or resource containment mismatch')
        if (host.get('CapAdd') or host.get('Devices') or
                {str(value).upper() for value in host.get('CapDrop', [])} != {'ALL'} or
                host.get('SecurityOpt') != ['no-new-privileges:true']):
            raise ValueError('capability, device or security policy mismatch')
        tmpfs = host.get('Tmpfs', {})
        if set(tmpfs) != {'/tmp'} or set(tmpfs['/tmp'].split(',')) != {
                'rw', 'noexec', 'nosuid', 'nodev', f'size={SCRATCH_BYTES}', 'mode=1777'}:
            raise ValueError('scratch containment mismatch')
        if not isinstance(sources, dict) or set(sources) != {'/model', '/requests', '/results'}:
            raise ValueError('expected only model, request and results bind mounts')
        mounts = info['Mounts']
        if (not isinstance(mounts, list) or len(mounts) != 3 or
                {mount.get('Destination') for mount in mounts} != set(sources)):
            raise ValueError('mount inventory mismatch')
        for mount in mounts:
            target = mount['Destination']
            writable = target == '/results'
            expected_mode = 'rw' if writable else 'ro'
            if (mount.get('Type') != 'bind' or mount.get('Source') != sources[target] or
                    mount.get('RW') is not writable or mount.get('Mode') != expected_mode or
                    mount.get('Propagation') != 'rprivate'):
                raise ValueError('mount source or permissions mismatch')
    except (KeyError, TypeError) as error:
        raise ValueError('container inspect data is incomplete or malformed') from error


def _status_values(path):
    values = {}
    for line in path.read_text(encoding='ascii').splitlines():
        key, separator, value = line.partition(':')
        if separator:
            values[key] = value.strip().split()
    return values


def _mount_options(mountinfo, targets):
    found = {}
    for line in mountinfo.splitlines():
        before, separator, after = line.partition(' - ')
        if not separator:
            raise ValueError('malformed /proc/self/mountinfo')
        left, right = before.split(), after.split()
        if len(left) < 6 or len(right) < 3:
            raise ValueError('malformed /proc/self/mountinfo')
        mountpoint = re.sub(r'\\([0-7]{3})',
                            lambda match: chr(int(match.group(1), 8)), left[4])
        if mountpoint in targets:
            if mountpoint in found:
                raise ValueError(f'duplicate effective mount: {mountpoint}')
            found[mountpoint] = {
                'readonly': 'ro' in left[5].split(','),
                'options': sorted(set(left[5].split(',') + right[2].split(','))),
                'filesystem': right[0],
            }
    if set(found) != targets:
        raise ValueError('required effective mounts are missing')
    return found


def _tmpfs_size_bytes(options):
    for option in options:
        match = re.fullmatch(r'size=(\d+)([kmgt]?)', option.lower())
        if match:
            value = int(match.group(1))
            suffix = match.group(2)
            return value * (1024 ** ('kmgt'.index(suffix) + 1)) if suffix else value
    return None


def _only_loopback(proc_root, interfaces):
    if interfaces is None:
        interfaces = [name for _, name in socket.if_nameindex()]
    names = sorted(set(interfaces))
    if names != ['lo']:
        raise ValueError('effective network interfaces must be loopback only')
    # Cross-check the kernel's interface table rather than relying only on the API.
    try:
        rows = [line.split(':', 1)[0].strip()
                for line in (proc_root / 'net/dev').read_text(encoding='ascii').splitlines()[2:]
                if ':' in line]
    except OSError as error:
        raise ValueError('cannot inspect /proc/net/dev') from error
    if sorted(rows) != ['lo']:
        raise ValueError('effective /proc network interfaces are not loopback only')
    return names


def effective_containment(proc_root=Path('/proc'), cgroup_root=Path('/sys/fs/cgroup'),
                          interfaces=None):
    """Inspect live Linux controls; return evidence or fail closed with ValueError."""
    proc_root = Path(proc_root)
    cgroup_root = Path(cgroup_root)
    try:
        status = _status_values(proc_root / 'self/status')
        uid_values = [int(value) for value in status['Uid']]
        gid_values = [int(value) for value in status['Gid']]
        if (len(uid_values) < 2 or len(gid_values) < 2 or uid_values[0] <= 0 or
                uid_values[0] != uid_values[1] or gid_values[0] != gid_values[1]):
            raise ValueError('effective process identity is root or inconsistent')
        cap_eff = status['CapEff'][0]
        if int(cap_eff, 16) != 0:
            raise ValueError('effective capabilities are not empty')
        no_new_privs = int(status['NoNewPrivs'][0])
        seccomp = int(status['Seccomp'][0])
        if no_new_privs != 1 or seccomp != 2:
            raise ValueError('no-new-privileges or seccomp is not effective')

        interfaces_seen = _only_loopback(proc_root, interfaces)
        mounts = _mount_options((proc_root / 'self/mountinfo').read_text(encoding='ascii'),
                                REQUIRED_MOUNTS)
        if not mounts['/']['readonly']:
            raise ValueError('effective root filesystem is writable')
        for target in ('/model', '/requests'):
            if not mounts[target]['readonly']:
                raise ValueError(f'{target} must be effectively read-only')
        if mounts['/results']['readonly']:
            raise ValueError('/results must be effectively writable')
        scratch = mounts['/tmp']
        scratch_options = set(scratch['options'])
        if (scratch['filesystem'] != 'tmpfs' or
                not {'noexec', 'nosuid', 'nodev'} <= scratch_options or
                _tmpfs_size_bytes(scratch_options) != SCRATCH_BYTES):
            raise ValueError('effective scratch mount controls mismatch')

        quota, period = (int(value) for value in
                         (cgroup_root / 'cpu.max').read_text(encoding='ascii').split())
        if period <= 0 or quota <= 0 or quota / period != CPU_LIMIT:
            raise ValueError('effective CPU quota differs from two CPUs')
        memory_max = int((cgroup_root / 'memory.max').read_text(encoding='ascii').strip())
        swap_max = int((cgroup_root / 'memory.swap.max').read_text(encoding='ascii').strip())
        pids_max = int((cgroup_root / 'pids.max').read_text(encoding='ascii').strip())
        if memory_max != MEMORY_LIMIT or swap_max != 0 or pids_max != PID_LIMIT:
            raise ValueError('effective memory, swap or process limit mismatch')
        return {
            'uid': uid_values[1], 'gid': gid_values[1], 'cap_eff': cap_eff.lower(),
            'no_new_privs': no_new_privs, 'seccomp': seccomp,
            'interfaces': interfaces_seen, 'mounts': mounts,
            'cpu_count': quota / period, 'memory_max': memory_max,
            'swap_max': swap_max, 'pids_max': pids_max,
        }
    except ValueError:
        raise
    except (OSError, KeyError, IndexError, TypeError, UnicodeError) as error:
        raise ValueError(f'cannot verify effective containment: {error}') from error
