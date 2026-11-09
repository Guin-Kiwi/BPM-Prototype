# Current work

PHASE: 3
STATUS: done

## Active objective

[UC-001: report intake](specs/UC-001-REPORT-INTAKE.md): implement the bounded
[revised prototype design](specs/UC-001-REPORT-INTAKE.md#design--revised-prototype).

## Current Use Case

docs/specs/UC-001-REPORT-INTAKE.md

## Current slice

Simulated farmer on farm-1; required uploaded photo, approximate affected-plant
estimate and usable browser GPS; optional text and area cue; simulated observation
time, separate receipt and fix time; farm-wide report history; legacy-preserving
SQLite migration with verified backup. Map fallback remains unavailable because no
field boundaries or map presentation are supplied. Routing, events, cases, AI,
authentication and dataset generation remain outside this slice.

## Evidence links

[Integration tests](../tests/integration/test_intake.py) and
[UC-001 DEVELOP evidence](specs/UC-001-REPORT-INTAKE.md#design--revised-prototype).

## Acceptance / validation cues

Targeted red: `.venv/bin/python -m pytest tests/integration/test_intake.py -q`
failed against the old implementation (5 failed, 15 passed). After implementation,
`.venv/bin/python -m pytest tests/integration/test_intake.py tests/unit/test_architecture.py -q`
passed (32 tests), including backup/restore and rollback on temporary databases.
Full handoff: `bash scripts/test.sh` passed lifecycle checks, 46 process tests and
32 pytest tests. A loopback Uvicorn startup against a temporary database shut down
cleanly under a three-second timeout (expected exit 124). No visual/manual browser
test has been performed.
Group paper/model alignment and human acceptance of the revised journey remain open.

## Next smallest step

Complete the map fallback only after
known boundaries, their provenance and a usable map presentation are supplied.

## Selected routing step

Ayla selected report-to-case routing as the next business specification step:
[consolidated routing worksheet](reference/DMN-RULE-WORKSHEET.md). This is the
prototype direction; alignment with the group paper and models is still pending.
The worksheet owns the terminology, routing proposal, open definitions and bounded
agent handoff. UC-001 remains intake/history only; no routing implementation yet.

## Deferred decisions / backlog

- LLM provider and image assessment, routing policy/execution and review criteria.
- Advisory guidance and handover, duplicate handling and experiment export.
- Offline capture remains a disclosed gap against the paper's assumption.

Implementation ownership: [working agreement](WORKING-AGREEMENT.md).
