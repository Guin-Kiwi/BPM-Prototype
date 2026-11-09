# Current work

PHASE: 2
STATUS: in-progress

## Active objective

[UC-001: report intake](specs/UC-001-REPORT-INTAKE.md): revise the specification for
camera-first farmer reporting, account-derived farm, automatic observation time,
preferred GPS with mapped-field fallback, a required approximate affected-plant count
or percentage for the observed area, farm history and nearby context. Routing and relevance are separate work.

## Current Use Case

docs/specs/UC-001-REPORT-INTAKE.md

## Current slice

DESIGN: the [revised UC-001 design](specs/UC-001-REPORT-INTAKE.md#design--revised-prototype)
sets working defaults for the next GPS-based prototype slice, farm history and a
non-destructive migration. The revised target is not implemented. The runtime has
saved non-seed reports and no field-boundary geometry; mapped fallback remains blocked
until known real or explicitly synthetic boundaries and map presentation are supplied.
The current demo and prior evidence below concern the older intake only. Group
paper/model alignment for the changed business journey remains pending; no revised
human acceptance is claimed.

## Evidence

For the revised DESIGN edits, `bash scripts/check-lifecycle.sh` and `git diff
--check` passed; local Markdown links and anchors in the two edited documents passed
a targeted link check. No revised implementation or human review is claimed.

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

Review the bounded UC design and its working assumptions. The next DEVELOP slice is
specified in its acceptance mapping: simulated primary farm, upload/manual time,
usable device GPS, required estimate, farm-wide report history, preservation migration
and focused tests. It must expose the boundary interface and report fallback as
unavailable; it cannot complete map fallback without supplied boundary geometry and
a map presentation. No dataset or business-record generation is authorized. The
full revised UC and group alignment remain open. DESIGN remains in progress pending
review and document checks; no phase transition or human approval is asserted.

The [data-model draft](design/DATA-MODEL.md) remains the wider direction: one primary
farmer and technician view with neighbouring context, and typed history events in a
later event-producing slice. Cases, spatial analysis and routing are not part of the
next intake implementation. BRACOT remains a separate data inspection priority under
the [open-data plan](reference/OPEN-DATA.md).

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
