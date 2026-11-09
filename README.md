# Cooxupé P1 prototype

BPM coursework prototype for agricultural technical orientation: LLM-assisted report
assessment, explicit decision rules and an evidence view for advisory staff.
The local demo supports simulated farmer report intake and farm-wide report history.

## Setup

```bash
cd BPM-Prototype
PYTHON_BIN=python3.12 bash scripts/setup-python.sh
bash scripts/setup-skills.sh codex
bash scripts/check-setup.sh
bash scripts/test.sh
```

Open this folder directly in VS Code. Use `.venv/bin/python` as the interpreter.
The devcontainer is an alternative Python 3.12 environment.

## Run the local demo

From the repository root, after setup:

```bash
PYTHONPATH=src .venv/bin/python -m uvicorn app.infrastructure.web:create_app --factory --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/ for the simulated farmer on Sunrise Farm (`farm-1`).
Choose a new-photo upload (JPEG or PNG, up to 10 MiB), give an approximate affected
plant count or percentage for the observed area, and obtain a browser GPS fix. Text
and an area cue are optional. Photo selection records a **simulated** observation time;
it does not establish when the photo was captured. GPS reports its own fix time and
accuracy and does not verify the photo location. The prototype accepts fixes no older
than five minutes, not in the future, and accurate to 100 metres or better. GPS is
required because map fallback is unavailable without supplied field boundaries. Retry
GPS if permission is denied or the fix is unusable; no draft is saved. Nearby grouping
is unavailable. The local, unauthenticated demo is for loopback use.

The database defaults to ignored `data/bpm.sqlite3` and persists between restarts.
Set `BPM_DB_PATH` to choose another local SQLite file. On first opening an older
database, the app creates and verifies a consistent SQLite backup alongside it before
transactionally migrating; keep that backup. If backup or migration fails, startup stops
and the original is unchanged. Unexpected report schemas, custom report indexes or
triggers, and foreign keys referencing reports require manual migration. Back up your
files separately as appropriate. The app needs write access to the database directory.
Legacy missing values remain unavailable, and legacy findings have unknown confirmation
provenance. Both existing farms and their records are preserved. Offline capture, AI
assessment, routing, cases, authentication and mapped-field fallback are not implemented.

See [project scope and commands](docs/PROJECT.md), [current work](docs/TASKS.md)
and [reference sources](docs/reference/README.md).

## AI-SDLC development

Follow [CONTRIBUTING](CONTRIBUTING.md), the [working agreement](docs/WORKING-AGREEMENT.md),
[use cases](docs/specs/) and [decision records](docs/adr/).
Template attribution and the MIT licence for project material are in [LICENSE](LICENSE).
