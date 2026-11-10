"""Lifecycle scenarios must neither copy nor retain local experiment assets."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class LifecycleFixtureTests(unittest.TestCase):
    def test_local_readonly_assets_are_excluded_from_scenarios(self):
        with tempfile.TemporaryDirectory() as tmp:
            scratch = Path(tmp)
            project = scratch / 'project'
            shutil.copytree(ROOT, project, ignore=shutil.ignore_patterns(
                '.git', '.venv', 'data', 'runs', '__pycache__', '.pytest_cache'))
            for name in ['data', 'runs']:
                folder = project / name / 'local-assets'
                folder.mkdir(parents=True)
                (folder / 'sentinel').write_text('must stay outside lifecycle fixtures')
                folder.chmod(0o555)
            fixtures = scratch / 'fixtures'
            fixtures.mkdir()
            try:
                result = subprocess.run(['bash', 'scripts/test-lifecycle.sh'], cwd=project,
                                        env={**os.environ, 'TMPDIR': str(fixtures)},
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stderr, '', result.stderr)
                self.assertEqual(list(fixtures.iterdir()), [], 'scenario cleanup left local assets')
            finally:
                # Permit cleanup even when testing the broken read-only copy behavior.
                for folder in scratch.rglob('*'):
                    if folder.is_dir():
                        folder.chmod(0o755)
