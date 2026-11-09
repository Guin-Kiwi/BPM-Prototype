# Current work

PHASE: 1
STATUS: in-progress

## Active objective

[UC-001: report intake](specs/UC-001-REPORT-INTAKE.md): select a fictional farm and
field, save and retrieve a report, and show earlier reports for that field. Routing
and model integration are deferred.

## Current Use Case

docs/specs/UC-001-REPORT-INTAKE.md

## Current slice

The bounded intake and synthetic-history journey has implementable working defaults
for attachments, seed coverage and chronology. They are recommendations, not owner
or group approvals. SPECIFY remains in progress for the required human review; no
routing, AI or case behavior is included.

## Evidence

Bootstrap checks passed on 9 November: setup check, lifecycle scenarios, 46 tooling
tests and 3 pytest tests. Bootstrap committed as `ac10147`. No application has been
built or application acceptance checks run for this draft.

For this revision, `bash scripts/check-lifecycle.sh`, `bash scripts/test-lifecycle.sh`,
local links in both edited documents and `git diff --check` passed. Human review is
outstanding; no application acceptance checks have run.

## Next smallest step

Human review of [UC-001](specs/UC-001-REPORT-INTAKE.md), then select DESIGN for the
agreed intake: define storage/atomicity, retrieval and image validation while preserving
history order and evaluation isolation. Scenario preparation follows the
[open-data plan](reference/OPEN-DATA.md); no dataset has been downloaded.

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
