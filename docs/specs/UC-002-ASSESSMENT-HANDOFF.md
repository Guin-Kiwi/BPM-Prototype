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

A report with an image exists. Real model backend and configuration must be
selected before an assessment can run; a local classifier has completed a separate
[contained feasibility run](../../experiments/local-classifier/RESULTS.md) but is not
selected for integration. The [demo rule proposal](../reference/UC-002-DEMO-RULES.md) requires owner decisions
on scenario profiles versus model-informed demo derivation, substantive prepared guidance,
history and providers
before implementation. The acknowledgement fixture tests recording only and does not
complete the selected routine guidance journey.

## Trigger

Staff requests assessment of a saved report.

## Main flow

1. Load the photo for image classification under the
   [assessment boundary](../reference/DMN-RULE-WORKSHEET.md#assessment-and-routing-boundary).
2. Run the selected image model and save its candidate scores and model identity.
   Proposed second stage: interpret those scores with the farmer note and optional
   saved weather snapshot. Keep image results distinct from interpreted suspected
   issue and uncertainty; do not invent visible signs from class scores. Preserve
   original report evidence and identify every model/prompt and snapshot used.
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
  technician-routing rules; exact input definitions remain open below.
- Unknown prior history remains unknown, rather than evidence of no earlier issue.
- Missing weather permits an assessment without weather, explicitly marked unavailable.
  Model selection and interpretation-stage behavior remain open before implementation.

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
   [proposed table and synthetic fixtures](../reference/UC-002-DEMO-RULES.md) cover both
   branches, unknowns and precedence; scenario-profile versus unvalidated model-informed derivation requires owner approval.
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
run; no application assessment, routing or handoff journey has been implemented or tested.

## Open questions / assumptions

- Local classifier feasibility and selection; second-model choice and structured output.
  API credentials/billing are needed only if a hosted backend is selected.
- Weather endpoint/terms/coverage, alert archive and snapshot window; see the weather
  plan's source-backed limits. These remain unresolved; no weather integration exists.
- Owner decisions on scenario profiles versus model-informed demo derivation and the
  proposed substantive routine guidance, proposed
  history/case linkage and provider suitability are detailed in the
  [demo rule proposal](../reference/UC-002-DEMO-RULES.md#owner-decisions-before-implementation).
  Both routine and technician handoffs remain in scope; neither is implemented.

## Notes for implementation

Existing boundaries: domain reports, application intake/repository, SQLite and local
web adapters. Follow DESIGN and TDD after the slice's open behavior is resolved;
the owner has requested the connected demonstration, but this draft does not resolve
the pending behavior/provider choices or claim an implemented journey.
