# Cooxupé P1 prototype

BPM coursework prototype for agricultural technical orientation: LLM-assisted report
assessment, explicit decision rules and an evidence view for advisory staff.
The repository currently contains the development framework; the demo is not built yet.

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

See [project scope and commands](docs/PROJECT.md), [current work](docs/TASKS.md)
and [reference sources](docs/reference/README.md). Application run instructions will
be added with the first working slice.

## AI-SDLC development

Follow [CONTRIBUTING](CONTRIBUTING.md), the [working agreement](docs/WORKING-AGREEMENT.md),
[use cases](docs/specs/) and [decision records](docs/adr/).
Template attribution and the MIT licence for project material are in [LICENSE](LICENSE).
