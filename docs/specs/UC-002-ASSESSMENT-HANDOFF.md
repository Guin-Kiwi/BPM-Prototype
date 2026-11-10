# UC-002-ASSESSMENT-HANDOFF

## Goal

Extend saved report intake into a real image assessment, deterministic responsibility
route and recorded human handoff. This is a SPECIFY draft, not an implemented journey.

## Business value

Demonstrate the central TO-BE distinction: routine communication versus technician
attention, with an inspectable assessment and reason for each route.

## Scope

### In scope
- Reuse [UC-001](UC-001-REPORT-INTAKE.md) intake and stored report evidence.
- Real image assessment, structured saved output and explicit failure state.
- Optional [event weather](../reference/EVENT-WEATHER.md); proposed second-model
  interpretation of image scores, farmer note and that snapshot.
- Deterministic route with recorded rule version, input facts and reason.
- Minimal staff view of the report, image, assessment, route and available farm history.
- Recorded human handoff: routine guidance delivery or technician involvement.

### Out of scope
- Full visit scheduling, map interface, purchases and automatic farmer messaging.
- New datasets, production authentication and claims of agronomic validation.
- These exclusions bound this first slice; neighbouring context and later workflows
  remain in the wider prototype plan.

## Actors

Primary: simulated staff member opening a submitted report.
Secondary: farmer via existing intake; selected model backend and optional weather source.

## Preconditions

A saved report and photo exist. The recommended technical path is the pinned local
classifier, followed by a small offline text interpreter after its dependency, artifact,
containment and output-feasibility checks. The [guidance catalogue](../reference/UC-002-GUIDANCE-CANDIDATE.md)
records what each source supports; the [routing proposal](../reference/UC-002-DEMO-RULES.md)
separately defines administrative demonstration assumptions. No presenter-supplied
risk, eligibility or desired-route profile is an application input.

## Trigger

Staff requests assessment of a saved report.

## Main flow

1. Load the photo for image classification under the
   [assessment boundary](../reference/DMN-RULE-WORKSHEET.md#assessment-and-routing-boundary).
2. Run the selected image model and save its candidate scores and model identity.
   Proposed second stage: interpret those scores with the farmer note and optional
   saved weather snapshot. Keep image results distinct from interpreted suspected
   issue and uncertainty; do not invent visible signs from class scores. Preserve
   original report evidence and identify every model/prompt and snapshot used. Interpreter
   agreement is not independent confirmation of the image classification.
3. Code prepares defined history facts. Apply the versioned responsibility rules to
   those facts, assessment and extent estimate; save route and reason separately.
4. Staff sees the original evidence, assessment, route and available history.
5. Communications records relay of applicable prepared guidance, or technician
   involvement creates/links a technical case under the agreed linking rule.
6. Reload the report to inspect the recorded handoff. Delivery is not resolution,
   and handling recorded is not case closure.

## Alternate / edge flows

- Reassessment creates a separate assessment record rather than overwriting evidence.
- Unsupported guidance, missing evidence or uncertain assessment follows explicit
  technician-routing rules; the routing proposal records their concrete demonstration definitions.
- Unknown prior history remains unknown, rather than evidence of no earlier issue.
- Missing weather permits an assessment without weather, explicitly marked unavailable.
  Technical recommendations and the interpretation contract are in the routing proposal;
  their runtime feasibility remains to be measured.

## Errors / failure cases

Missing report/image, missing configuration, provider timeout/error, invalid model
output and storage failure remain visible. Do not fabricate a successful assessment,
route or handoff; the saved intake report remains retrievable.

## Acceptance criteria

Sources: selected [comparison pair](../../models/comparison/README.md),
[routing worksheet](../reference/DMN-RULE-WORKSHEET.md) and owner selection of a real
model for the first slice.

1. Image classification receives only the photo. Any second model receives candidate
   scores, farmer note and optional saved weather snapshot. Connected history,
   identities, earlier findings, extent and source-label metadata enter neither model.
2. Valid live output is saved as inference with provenance, not a confirmed finding.
3. Routing is reproducible from recorded inputs and versioned rules, with a reason.
   History changes can affect routing without changing the standalone assessment. The
   [proposed table](../reference/UC-002-DEMO-RULES.md) derives handling from actual
   image/interpretation outputs and ordinary synthetic history records. Hand-entered
   risk, eligibility or desired routes are excluded. Communications means relay of a
   scoped observation message, never a conclusion that agronomic risk is low.
4. Staff can inspect evidence/history and record the appropriate handoff. Routine
   reports create no technical case; technician involvement follows the agreed linking rule.
5. Results survive restart; errors never appear as completed assessment or delivery.
6. Weather provenance, units, time window and missing data remain inspectable. Later
   weather is excluded from the observation snapshot; simulated capture context is
   labelled. Weather never confirms damage or adds unsupported classifier classes.

## Security / trust-boundary notes

Before installing a local backend, follow the [candidate security review](../reference/LOCAL-MODEL-SECURITY.md).
The contained feasibility run records artifact, dependency and effective runtime checks;
unsupported-input behavior, diagnostic validity and provider selection remain unresolved.

Provider credentials stay server-side and outside Git. Treat farmer text and model
output as untrusted data. Explicit live requests may incur provider charges; ordinary
automated tests must not require paid calls. Simulated identity is not access control.

## Validation plan

### Tests
Unit: output validation, rule precedence, model-input boundaries and weather time/unit checks.
Integration: persistence, backend/weather failures, immutable snapshot links, routing facts and handoff consistency.
E2E: existing intake through a staff-recorded handoff and reload.

### Evidence

Planned: passing scoped checks and a deliberately run live example identifying model,
prompt/rule version, input report, actual output, route and handoff. A separate
[classifier feasibility experiment](../../experiments/local-classifier/RESULTS.md) has
run. The separate [interpreter experiment](../../experiments/local-interpreter/RESULTS.md)
completed loading/generation but accepted 0/12 responses; it does not establish provider
suitability. No application assessment, routing or handoff journey is implemented or tested.

## Open questions / assumptions

- Agronomic source support, project-authored message wording, routing assumptions and
  measured results have separate authorities. Ayla is not asked to validate agronomy.
- Local image preprocessing, local text candidate and exact interpretation schema are
  technical recommendations; interpreter feasibility and end-to-end results are pending.
- Explicit unresolved-issue links, history availability and human case linking are
  administrative prototype assumptions. Same-farm reports are not automatically repeats;
  absent links do not establish irrelevance. All available context remains inspectable.
- Weather acquisition/window remains optional and follows its existing source-backed
  plan. No weather API is required for this demonstration.
- Wider group paper/model alignment and real agronomic effectiveness remain distinct
  from demonstrating reproducible routing and human recording.

## Notes for implementation

Existing boundaries: domain reports, application intake/repository, SQLite and local
web adapters. Follow DESIGN and TDD after the slice's open behavior is resolved;
the owner has requested actual model-derived assessment and synthetic history, not
route profiles. This research/proposal work does not claim an implemented journey.
