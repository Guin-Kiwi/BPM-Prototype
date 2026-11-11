# Current work

PHASE: 4
STATUS: in-progress

## Active objective

[UC-002: assessment and human handoff](specs/UC-002-ASSESSMENT-HANDOFF.md): connect
actual classifier and bounded interpreter outputs to deterministic routing and recorded
human handling. Use the [approved BPMNs](../models/approved/README.md) and the
pre-improvement case baseline. Weather is optional; leaf detection is deferred.

Validation of the supporting interpreter experiment is complete with output-contract
failure. The connected application journey remains unfinished.

## Current Use Case

docs/specs/UC-002-ASSESSMENT-HANDOFF.md

## Implemented capability

[UC-001](specs/UC-001-REPORT-INTAKE.md#design--revised-prototype) provides simulated
farmer intake: required photo, affected-plant estimate and browser GPS; optional note;
SQLite persistence, farm-wide history and legacy-preserving migration. Authentication,
mapped-field fallback and neighbouring context are not implemented.

## Evidence

- [Classifier results](../experiments/local-classifier/RESULTS.md): contained local
  inference works; unsuitable inputs can receive high disease scores.
- [Interpreter results](../experiments/local-interpreter/RESULTS.md): two contained
  trials, 0/12 accepted responses. Software checks passed 47 process tests and 134
  pytest tests; this does not establish interpretation quality or application completion.
- [Workflow experiment plan](../experiments/assessment-handoff/README.md): connected
  runs and measured operational benefits remain outstanding. Cost scenarios are hypothetical.

## Next step

Implement and evaluate the bounded constrained-output experiment specified in
[interpreter results](../experiments/local-interpreter/RESULTS.md#proposed-next-experiment--constrained-decisions-not-another-model).
Check structural validity and semantic usefulness separately before application integration.

## Remaining work and boundaries

- Follow the [routing worksheet](reference/DMN-RULE-WORKSHEET.md),
  [demo rules](reference/UC-002-DEMO-RULES.md) and sourced prepared guidance.
  Use actual assessment outputs and synthetic history; profiles test rules only.
- Preserve photo-only classification; interpretation receives scores, optional note
  and optional event weather. Connected history/extent remain with code/DMN and staff.
- Implement assessment persistence, responsibility routing, human handoff and cases.
  Visits, findings entry/save and conditional P2/P3 referrals remain later workflow gaps.
- Keep full available context accessible for human relevance judgment; absent issue
  links do not establish irrelevance. Interpreter agreement is not confirmation.
- [Weather](reference/EVENT-WEATHER.md), map boundaries, nearby context, permissions,
  offline capture and source-backed evaluation coverage require further work.

Responsibilities: [working agreement](WORKING-AGREEMENT.md).
