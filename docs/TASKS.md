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
The bounded local form, durable reports/images and field history are implemented.
Routing, AI, cases and real dataset import remain separate work.

## Evidence

UC-001 implementation and automated coverage are in place. The first targeted
integration run failed on the missing application entry point; after implementation,
`.venv/bin/python -m pytest tests/integration/test_intake.py -q` passed. A later
connection-lifecycle test failed before the SQLite connection closure fix; the
expanded integration and architecture selection passed (22 tests).

At handoff, `bash scripts/test.sh` passed: lifecycle checks and scenarios, 46
process-tooling tests and 22 pytest tests. The Uvicorn factory command documented
in the README started on loopback and shut down cleanly under a 3-second timeout
(exit 124 is the expected timeout). HTTP integration exercises form submission,
retrieval and history; a visual/manual browser journey has not been performed because
no browser is connected. No human implementation review or approval is claimed.

Parent verification: a temporary loopback Uvicorn server passed live HTTP form,
image submission, redirect, escaped report detail, prior finding/history, original
image retrieval and unknown-ID checks. Earlier startup attempts used the old entry
point or crossed sandbox network boundaries; the final check used the documented
factory in a single network context and passed. Temporary servers were stopped.
Parent code review and a Luna-medium read-only review found no blocking defects.
Neither constitutes human or visual acceptance.

## Next smallest step

Implementation review and shared project command alignment are complete. Try the
README run command and perform the manual browser journey when a browser is available;
record human acceptance before considering this phase done. Phase 3 remains
in-progress pending this visual/manual acceptance. Separately, the next data
inspection priority is BRACOT for a small, provenance-tracked field sample; source
selection and evaluation preparation remain outside UC-001 implementation. Follow
the [open-data plan](reference/OPEN-DATA.md) for the single source-selection
recommendation and its inspection limits. Offline capture remains a disclosed gap.

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
