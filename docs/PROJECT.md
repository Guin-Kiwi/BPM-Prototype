# Cooxupé P1 prototype

## Purpose

Build a local demonstrator of agricultural technical orientation (P1) for the BPM
coursework. Farmers submit an issue; AI assesses the evidence with uncertainty; deterministic
rules route responsibility to communications or a technician.
Ayla leads implementation. This is a prototype, not a deployed agricultural service.

## Scope and current capability

Selected concept: camera-first reporting with a required farmer estimate, automatic
identity/time and usable GPS or known-field fallback; one farmer view and one technician
view with neighbouring farms in scope. The [routing worksheet](reference/DMN-RULE-WORKSHEET.md)
sets out the selected responsibilities, proposed rule and open decisions. The selected
[comparison models](../models/comparison/README.md) do not replace the group paper.

Implemented: a local simulated farmer uploads a required image and estimate, obtains a
browser GPS fix, and saves/retrieves reports and farm-wide history in SQLite. Observation
time is simulated at photo selection; identity is fixed, not authenticated. Map fallback,
nearby history and the technician view are unavailable. See [UC-001](specs/UC-001-REPORT-INTAKE.md)
and [README](../README.md#run-the-local-demo) for details and limitations.

AI assessment, deterministic routing, technical cases, guidance, communications,
visit handling and experiment export are not implemented. No automatic farmer messaging
or product orders are planned. Model output is an inference, not a confirmed diagnosis;
review is selective and routing thresholds remain undecided.

## Architecture

Python 3.12 and FastAPI development profile. Business rules remain independent of the
web framework, model provider and persistence. Application services orchestrate domain
objects through interfaces; infrastructure supplies adapters. Provider,
rule execution and optional MCP integration remain design decisions.

For UC-001, [ADR-001](adr/ADR-001-local-report-persistence.md) selects local SQLite,
with images stored transactionally with their reports; new intake requires an image. Application services
use an application-owned repository boundary; domain and application do not depend
on SQLite. UC-001 implements this design.

| Location | Responsibility |
| --- | --- |
| `src/app/domain/` | Report representation; future business rules belong here |
| `src/app/application/` | Intake and repository boundary; assessment/review are future work |
| `src/app/interfaces/` | Reserved for future interfaces |
| `src/app/infrastructure/` | Local web and SQLite adapters; provider adapters are future work |
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
