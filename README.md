# Cooxupé P1 prototype

BPM coursework prototype for agricultural technical orientation: LLM-assisted report
assessment, explicit decision rules and an evidence view for advisory staff.
The local demo currently supports fictional report intake and field history.

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

Open http://127.0.0.1:8000/ to select a fictional farm and field, submit an
observation and view its saved detail and earlier field history. The seeded farms,
reports and confirmed finding are synthetic. No dataset images are included; uploaded
images remain original evidence. The local, unauthenticated demo is for loopback use.

The database defaults to ignored `data/bpm.sqlite3` and persists between restarts.
Set `BPM_DB_PATH` to choose another local SQLite file. The app needs write access to
its directory. The 10 MiB upload limit is per image; database growth and backups are
not managed. Offline capture, AI assessment, routing and authentication are not part
of this slice.

See [project scope and commands](docs/PROJECT.md), [current work](docs/TASKS.md)
and [reference sources](docs/reference/README.md).

## AI-SDLC development

Follow [CONTRIBUTING](CONTRIBUTING.md), the [working agreement](docs/WORKING-AGREEMENT.md),
[use cases](docs/specs/) and [decision records](docs/adr/).
Template attribution and the MIT licence for project material are in [LICENSE](LICENSE).
