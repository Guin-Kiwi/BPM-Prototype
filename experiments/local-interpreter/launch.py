"""Create, inspect, then supervise only this experiment's offline container."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

from runtime_checks import validate_container

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', help='inspected immutable local sha256 image ID')
    args = parser.parse_args()
    if not re.fullmatch(r'sha256:[a-f0-9]{64}', args.image) or os.getuid() == 0:
        parser.error('requires a full immutable image ID and non-root host user')
    output = ROOT / 'runs/local-interpreter'
    if (output / 'first-run.json').exists():
        parser.error('preserve the previous run separately before another launch')
    sources = {'/model': str(ROOT / 'data/local-interpreter/model'),
               '/requests': str(ROOT / 'data/local-interpreter/requests'), '/results': str(output)}
    if any(not Path(p).is_dir() or Path(p).is_symlink() for p in sources.values()):
        parser.error('all three scoped mount directories must already exist without symlinks')
    # Do not pass host environment/secrets into Compose interpolation or Docker.
    env = {name: os.environ[name] for name in ['PATH'] if name in os.environ}
    env.update(COFFEE_INTERPRETER_IMAGE=args.image, COFFEE_RUN_UID=str(os.getuid()),
               COFFEE_RUN_GID=str(os.getgid()))
    compose = ['docker', 'compose', '-f', str(HERE / 'compose.yaml')]

    def command(argv, **kwargs):
        return subprocess.run(argv, env=env, check=True, capture_output=True,
                              text=True, timeout=30, **kwargs).stdout

    # Refuse an existing service; never replace or remove someone else's container.
    if command(compose + ['ps', '--all', '--quiet', 'interpreter']).strip():
        parser.error('experiment service already exists; inspect it before cleanup')
    command(compose + ['create', '--pull', 'never', 'interpreter'])
    container = command(compose + ['ps', '--all', '--quiet', 'interpreter']).strip()
    if not re.fullmatch(r'[a-f0-9]{64}', container):
        raise ValueError('expected one created experiment container')
    try:
        info = json.loads(command(['docker', 'inspect', container]))[0]
        validate_container(info, args.image, os.getuid(), os.getgid(), sources)
        evidence = {k: info[k] for k in ['Id', 'Image', 'Config', 'HostConfig', 'Mounts']}
        (output / 'container-inspect.json').write_text(json.dumps(evidence, indent=2) + '\n')
        try:
            completed = subprocess.run(['docker', 'start', '--attach', container], env=env,
                                       capture_output=True, text=True, timeout=210)
            (output / 'container.log').write_text(completed.stdout + completed.stderr)
        except subprocess.TimeoutExpired:
            command(['docker', 'kill', container])
            raise TimeoutError('host supervisor exceeded 210 seconds; container killed')
        state = json.loads(command(['docker', 'inspect', container]))[0]['State']
        (output / 'container-state.json').write_text(json.dumps(state, indent=2) + '\n')
        if state['ExitCode'] != 0 or state['OOMKilled'] or state['Running']:
            raise RuntimeError('container failed; inspect local state and log')
        print('PASS: inspected containment, completed run, container removed on exit')
    finally:
        command(['docker', 'rm', '--force', container])


if __name__ == '__main__':
    main()
