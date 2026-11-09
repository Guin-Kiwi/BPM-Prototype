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

The agreed journey and synthetic-history boundaries are drafted for human review.
Attachment defaults and exact seed counts are recommendations, not approved decisions.
SPECIFY remains in progress pending review and agreement on attachment limits; choose
whether to adopt the seed recommendation before preparing fixtures.

## Evidence

Bootstrap checks passed on 9 November: setup check, lifecycle scenarios, 46 tooling
tests and 3 pytest tests. Bootstrap committed as `ac10147`. No application has been
built or application acceptance checks run for this draft.

For this specification revision: `bash scripts/check-lifecycle.sh` and
`bash scripts/test-lifecycle.sh` passed; local links in the three edited documents
and `git diff --check` passed. Human review is outstanding.

## Next smallest step

Review the UC and attachment defaults. The agreed selection, persistence and history
journey can inform DESIGN; finalize attachment limits before implementing them.
After agreeing seed contents, prepare scenarios under the [open-data plan](reference/OPEN-DATA.md).

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
