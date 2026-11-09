# Cooxupé P1 prototype

## Purpose

Build a local demonstrator of agricultural technical orientation (P1) for the BPM
coursework. Farmers submit an issue; an LLM proposes an assessment; explicit rules
select an action; advisory staff inspect evidence and handle cases requiring review.
Ayla leads implementation. This is a prototype, not a deployed agricultural service.

## Scope and current capability

Planned: text-first report entry, farm/field history, real LLM assessment, deterministic
routing, an advisory view, simulated communications and traceable experiment export.
Add a small licensed image sample after selecting a suitable provider. Field aggregation
and sampling scenarios follow the first working path. Sales/time benefits are hypotheses.

Implemented: Python package layers, architecture test, lifecycle tooling and development
environment. There is no application endpoint, model integration or runnable demo yet.

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
on SQLite. This accepted design is not yet implemented.

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
| Run locally / release | Not available until the first application slice exists |

On this machine, system Python 3.12 lacks `ensurepip` (`python3.12-venv`). The local
`.venv` was created and populated using the existing template environment's pip;
no system packages were changed. A fresh host needs Python's venv support (or the
devcontainer). The resulting local environment passes setup and handoff checks.

Normal tests must not require paid calls or credentials. Live experiments will be
explicit opt-in runs, distinguished from test substitutes and replayed demo results.

## Dependencies

`requirements.txt` is the active manifest, initialized from the template Python profile:
FastAPI, Uvicorn, pytest and HTTPX. `.python-version` specifies Python 3.12.
No model SDK or credentials are needed for bootstrap. Dependency pinning is deferred
until the first working integration provides a tested environment to capture.
