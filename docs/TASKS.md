# Current work

PHASE: 3
STATUS: in-progress

## Active objective

[UC-001: report intake](specs/UC-001-REPORT-INTAKE.md): select a fictional farm and
field, save and retrieve a report, and show earlier reports for that field. Routing
and model integration are deferred.

## Current Use Case

docs/specs/UC-001-REPORT-INTAKE.md

## Current slice

Ayla reviewed intake/history and accepted the SQLite design, then selected DEVELOP.
Implement the bounded local form, durable reports/images and field history with TDD.
Routing, AI, cases and real dataset import remain separate work.

## Evidence

Bootstrap checks passed on 9 November: setup check, lifecycle scenarios, 46 tooling
tests and 3 pytest tests. Bootstrap committed as `ac10147`. No application has been
built or application acceptance checks run for this draft.

Previous SPECIFY revision: `bash scripts/check-lifecycle.sh`,
`bash scripts/test-lifecycle.sh`, local links in both edited documents and
`git diff --check` passed. Human review is outstanding; no application acceptance
checks have run.

DESIGN revision: lifecycle check and lifecycle scenario tests passed; local Markdown
link targets in the spec, task record and ADR exist, and `git diff --check` passed.
These are document/process checks, not application acceptance evidence.

## Next smallest step

Implement UC-001 using the accepted design and targeted TDD. Run required handoff
checks; preserve actual check evidence and disclose unfinished acceptance work.

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
