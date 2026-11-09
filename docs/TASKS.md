# Current work

PHASE: 1
STATUS: in-progress

## Active objective

Specify [UC-002: assessment and handoff](specs/UC-002-ASSESSMENT-HANDOFF.md), the
barebones journey from saved report to real image assessment, deterministic route
and recorded human handoff. Provider choice and demo routing/guidance definitions
remain open; resolve them before DESIGN/implementation. UC-001 intake completion
and its existing evidence below are unchanged.

## Current Use Case

docs/specs/UC-002-ASSESSMENT-HANDOFF.md

## Existing implemented slice

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

Resolve the provider and bounded demo rules in the UC-002 draft, using the
[worksheet](reference/DMN-RULE-WORKSHEET.md#open-definitions-and-minimal-next-specify-task).
The selected work is SPECIFY; no application implementation is claimed.
The [local-model security review](reference/LOCAL-MODEL-SECURITY.md) records metadata
findings and containment conditions; no model installation or execution has begun.
[Experiment preparation](../experiments/local-classifier/README.md) supplies the manifest
and sandbox configuration. Next: dependency/loader review, isolated runtime build and
verified artifact acquisition in the next experiment session, as requested by Ayla.
Preparation is complete: manifest, artifact verifier and sandbox configuration are
committed. `bash scripts/test.sh` passed 46 process tests and 40 pytest tests, including
eight artifact-verifier checks; Compose configuration and manifest checks passed.
Effective container isolation and model loading remain unverified. No model packages,
weights or runtime image have been installed.

## Selected routing step

Ayla selected report-to-case routing as the next business specification step:
[consolidated routing worksheet](reference/DMN-RULE-WORKSHEET.md). This is the
prototype direction; the selected comparison pair is identified in the
[source map](reference/README.md), and group paper alignment remains pending.
The worksheet owns the terminology, routing proposal, open definitions and bounded
agent handoff. UC-001 remains intake/history only; no routing implementation yet.

## Deferred decisions / backlog

- Define routing inputs, uncertainty and reasons, guidance applicability, repeat handling,
  case linkage, severe approval, access and cross-farm context with the group. Preserve
  the [standalone assessment boundary](reference/DMN-RULE-WORKSHEET.md#assessment-and-routing-boundary):
  photo to image model; candidate scores, note and optional event weather to a proposed
  second model; extent and connected history to code/DMN. The [weather plan](reference/EVENT-WEATHER.md)
  records selected variables, sources, assumptions and open acquisition/window choices.
- Later code: AI/provider boundary, deterministic DMN, human guidance and case/visit
  workflows, technician view and traceable events/export. Map fallback needs known
  boundaries, provenance and usable presentation; manually verify the intake journey.
- Later data: inspect and attribute suitable image and illustrative guidance sources;
  design synthetic context and permissions without generating a dataset now.
- Later experiments: agree scenarios, reference truth, leakage controls and measured
  workload/outcomes; record actual runs. Offline capture remains a paper gap.

Implementation ownership: [working agreement](WORKING-AGREEMENT.md).
