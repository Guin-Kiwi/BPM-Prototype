# Current work

PHASE: 1
STATUS: in-progress

## Active objective

[UC-001: report intake](specs/UC-001-REPORT-INTAKE.md): revise the specification for
camera-first farmer reporting, account-derived farm, automatic observation time,
preferred GPS with mapped-field fallback, a required approximate affected-plant count
or percentage for the observed area, farm history and nearby context. Routing and relevance are separate work.

## Current Use Case

docs/specs/UC-001-REPORT-INTAKE.md

## Current slice

SPECIFY is in progress. The owner requires a camera-first target, approximate
plant estimate and location context: usable GPS is preferred, with selection of a known
field on a map for the account's farm when GPS is unavailable or insufficiently
accurate. GPS permission is not a login or workflow gate. The revised target is not
implemented. The intended prototype uses an upload to represent a new photo and labelled
synthetic or manual capture-context stand-ins; synthetic boundaries must be labelled.
The working demo selects a fictional farm and field, requires text and date, accepts an
optional image, and shows same-field history. It does not collect the structured estimate
and has no login, automatic GPS, mapped-boundary fallback, offline capture or
transcription. Earlier acceptance of the SQLite demo design does not approve the revised
target.

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

Resolve the proposed demo identity and seed mapping, how to convey estimate scope
without requiring extra narrative, usable-GPS criteria, actual field-boundary availability,
and farm/nearby history and grouping rules. If neither usable GPS nor a selectable known
field is available, retry without submission is a working recommendation for DESIGN,
not an approved exception or a claim of offline draft persistence. Resolve behavior-
affecting choices and group alignment before marking SPECIFY done. DESIGN can inspect
affected components and alternatives, but implementation-ready DESIGN and a phase
transition await those decisions and explicit selection of DESIGN. The earlier visual/
manual demo acceptance remains outstanding; existing checks cover the old demo.
Separately, BRACOT remains the next data inspection priority under the
[open-data plan](reference/OPEN-DATA.md). Offline capture remains a disclosed gap.

## Data-model draft

[Farm history and technical case model](design/DATA-MODEL.md) is drafted for review,
with source/decision trace, relationships, spatial framework and legacy-data limits.
It does not approve case cardinalities or change the active SPECIFY phase. Review
those choices before implementation or dataset generation; no generation is authorised.

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
