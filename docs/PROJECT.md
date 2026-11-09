# Cooxupé P1 prototype

## Purpose

Build a local demonstrator of agricultural technical orientation (P1) for the BPM
coursework. Farmers submit an issue; an LLM proposes an assessment; explicit rules
select an action; advisory staff inspect evidence and handle cases requiring review.
Ayla leads implementation. This is a prototype, not a deployed agricultural service.

## Scope and current capability

Planned: text-first report entry, farm/field history, real LLM assessment, deterministic
routing, an advisory view, simulated communications and traceable experiment export.
Import a small licensed image sample separately; image assessment needs a suitable provider. Field aggregation
and sampling scenarios follow the first working path. Sales/time benefits are hypotheses.

Implemented: local browser intake with farm/field selection, text and optional image,
SQLite save/retrieve, fictional seed history and same-field chronology. Images are
stored with reports in one transaction. No model integration or routing exists yet;
no open-data images have been imported. See [UC-001](specs/UC-001-REPORT-INTAKE.md).

External messages, purchases and logistics handovers are simulated. Product recommendations
do not create orders. Model output is an inference, not a confirmed diagnosis. Review is
selective; do not impose universal review or invent routing thresholds.

## Architecture

Python 3.12 and FastAPI development profile. Business rules remain independent of the
web framework, model provider and persistence. Application services orchestrate domain
objects through interfaces; infrastructure supplies adapters. Provider,
rule execution and optional MCP integration remain design decisions.

For UC-001, [ADR-001](adr/ADR-001-local-report-persistence.md) selects local SQLite,
with each optional image stored transactionally with its report. Application services
use an application-owned repository boundary; domain and application do not depend
on SQLite. UC-001 implements this design.

| Location | Responsibility |
| --- | --- |
| `src/app/domain/` | Observations, rule inputs/results and sampling calculations |
| `src/app/application/` | Assessment/review workflows and adapter contracts |
| `src/app/interfaces/` | Planned HTTP/UI and experiment entrypoints |
| `src/app/infrastructure/` | Planned provider, storage and wiring adapters |
| `tests/unit/`, `tests/integration/`, `tests/e2e/` | Deterministic automated checks |
| `tests/fixtures/` | Small attributable fixtures when introduced |

## Resources

[Source map](reference/README.md) identifies the authoritative paper, assignment,
models and proposed refinements. Keep external references linked rather than copying
whole publications. Source changes require reconciliation, not silent replacement.
Set `BPM_DB_PATH` to select the local database; default `data/bpm.sqlite3` is ignored.
Runtime assets belong with their consuming layer. Keep secrets in local `.env` only;
large datasets and live experiment outputs go in ignored `data/` and `runs/` directories.
Track manifests and deliberately selected evidence separately.

## Commands

Run from the repository root. Setup requires Python 3.12 and package-index access.

| Activity | Command |
| --- | --- |
| Install | `PYTHON_BIN=python3.12 bash scripts/setup-python.sh` |
| Agent discovery | `bash scripts/setup-skills.sh codex` |
| Setup check | `bash scripts/check-setup.sh` |
| Targeted architecture check | `.venv/bin/python -m pytest tests/unit/test_architecture.py -q` |
| Full handoff checks | `bash scripts/test.sh` |
| Run locally | `PYTHONPATH=src .venv/bin/python -m uvicorn app.infrastructure.web:create_app --factory --host 127.0.0.1 --port 8000` |
| Release | No deployment/release workflow selected |

On this machine, system Python 3.12 lacks `ensurepip` (`python3.12-venv`). The local
`.venv` was created and populated using the existing template environment's pip;
no system packages were changed. A fresh host needs Python's venv support (or the
devcontainer). The resulting local environment passes setup and handoff checks.

Normal tests must not require paid calls or credentials. Live experiments will be
explicit opt-in runs, distinguished from test substitutes and replayed demo results.

## Dependencies

`requirements.txt` is the active manifest, initialized from the template Python profile:
.python-version selects Python 3.12; runtime/test packages include FastAPI, Uvicorn,
pytest, HTTPX, python-multipart and Pillow.
No model SDK or credentials are needed for intake. Dependency pinning is deferred
until the first working integration provides a tested environment to capture.
