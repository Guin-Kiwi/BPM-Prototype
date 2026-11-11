# UC-002 assessment and handoff experiment plan

## Purpose and status

This document plans evidence for the [UC-002 assessment and handoff slice](../../docs/specs/UC-002-ASSESSMENT-HANDOFF.md).
It is a SPECIFY-phase evaluation plan, not an implementation, completed application
experiment, approved routing policy, or claim of agronomic validity. Record outcomes
in dated run reports linked from here; preserve failures and exclusions.

The [routing worksheet](../../docs/reference/DMN-RULE-WORKSHEET.md) owns the selected
business direction. The shared [UC-002 demonstration rules](../../docs/reference/UC-002-DEMO-RULES.md)
currently propose `uc002-demo-draft-2`; it remains unapproved. Use the exact rule
version under evaluation and record any later approved version explicitly. This plan
does not add desired-route labels or hand-entered eligibility facts. Actual model
outputs and separately declared synthetic history are inputs to routing; the route is
derived by the versioned deterministic rule, then compared with an independent
calculation from that same rule. The rule calculation is not a model input.

Interpreter agreement is not independent confirmation; the second model receives
the classifier scores, not independent visual evidence. Missing issue links do not
establish irrelevance: preserve all available context for human review. Profiles remain
permitted only for isolated rule tests, never connected-demo outcome selection.

## Questions and evidence boundaries

The evaluation separates four questions:

1. **Image inference feasibility:** does the selected image backend return a valid,
   traceable candidate-score vector from the photo alone? This is not diagnosis
   accuracy, confidence calibration, or evidence that an input is a coffee leaf.
2. **Bounded interpretation:** when selected, does the second model return the
   requested structured suspected issue, uncertainty, and optional weather
   interpretation from candidate scores, farmer note, and an optional saved weather
   snapshot? It must not turn inference into a confirmed finding or invent signs,
   guidance, or treatment.
3. **Deterministic routing and handoff:** does the recorded, versioned rule produce
   a reproducible route and reason from actual assessment outputs plus synthetic
   history, and does a person complete
   the applicable communications or technician handoff? A route is not a diagnosis,
   severe-action approval, delivery, resolution, or case closure.
4. **Operational feasibility:** what are actual machine/provider elapsed times,
   resource use and provider charges, and how do those compare with explicitly
   assumed staff-time scenarios? Model latency is not staff time saved.

Keep three evidence classes distinct in every report. **Source-backed agronomy** means
claims and data labels that retain their original source, definitions and limits, as
owned by the [open-data plan](../../docs/reference/OPEN-DATA.md) and selected guidance
references. **Prototype assumptions** means synthetic report/history/case records and
unvalidated demonstration mappings; identify each as synthetic or assumed. **Measured
results** means actual captured model outputs, timings, resource use, rule outputs and
human task observations from a named run. A source dataset label is not an agronomic
oracle for a route; an actual model output is an inference, not ground truth. Keep
history and the independent rule calculation out of image/interpretation requests.

## Scenario matrix

For each report, run image assessment on the original photo, then run the bounded text
interpretation on the recorded image scores, optional farmer note and optional weather
snapshot. Use those actual outputs with controlled synthetic history/case records to
exercise routing. Do not enter a target/expected route or synthetic risk label. Log
the assessment before routing; freeze a successful image and interpretation output
when making paired checks that vary history alone. Derive the route independently
from the rule version and recorded rule inputs. Compare application and independent
rule-calculation outputs, not the outcome against a hand-written route label. This
checks rule consistency for those inputs; it does not measure diagnostic truth or
real-world routing quality. Model/provider or storage failures remain failures and
must not be converted into successful routes.

| Scenario family | Input / expected evidence | Outcome to record |
| --- | --- | --- |
| Actual image and interpretation | Use a permitted report image, run the pinned image model, then the selected bounded interpretation model. Existing classifier JSON contains captured image scores; reuse those frozen vectors where useful. | Preserve full scores and validated interpretation output as observed. Record ambiguity, unsupported-input responses and errors. There is no expected diagnosis or route label; report clinical accuracy only if independent suitable diagnostic truth is later established. |
| Controlled history pairs | Hold report, source image, actual image output and actual interpretation output constant. Change only clearly marked synthetic report/case history and completeness metadata. Include history conditions relevant to the exact rule version. | Calculate routes from the recorded assessment and synthetic history using the rule version. Separately calculate them with an independent rule oracle derived from that version; compare outputs and reasons. No expected-route field is authored or passed to a model. |
| Rule conditions and precedence | Use actual inference cases that naturally exercise different rule inputs; add only synthetic history/case records as controlled variations. If a branch cannot be reached by available actual inference, mark it unexercised rather than fabricating a model output or desired route. | Verify deterministic evaluation order and traceable inputs/reason against the same versioned rule, without claiming the supplied scenario is agronomically correct. A route does not authorize severe action. |
| Weather boundary | Where a saved weather snapshot is available, compare separate actual interpretations with and without that snapshot. For history-only pairs, freeze interpretation output and vary history alone. | Record actual interpretation differences separately from route changes; route is derived from each saved assessment plus rule inputs. Do not infer weather causality or validity from this convenience comparison. |
| Failure and unsuitable input | Include missing report/image/configuration, invalid model output, timeout/provider failure, storage failure, blank and geometric controls, prompt-injection text and restart/reload. | Record actual observed output/error. Failure is not a completed route. Blank/geometry checks reveal implementation limitations only; an ordinary score is not a successful valid-leaf assessment. |

This is a scenario inventory, not a statistical sample. Record selection rationale,
exclusions and dependence. Multiple crops, perturbations or re-encodings from one
source image are related observations, not independent samples.

## Image inputs and source controls

The current licensed [BRACOL examples](../../docs/reference/EXAMPLE-IMAGES.md) are
three author-hosted detached-leaf JPEGs (original IDs 1, 21 and 90), kept under neutral
local filenames. Their source labels and hashes are in that manifest. They are useful
for upload and a controlled-condition comparison only; they are neither representative
field imagery nor an independent diagnosis benchmark. Do not use the source label as
a route oracle. The first classifier evidence already includes these images and blank
and geometric synthetic controls; this is an existing feasibility run, not UC-002
application evidence.

Before any later diagnostic scoring, document the chosen reference source, label
definitions, coverage, annotation provenance and relationship to model training data.
Check duplicates and related images against the available model/training provenance;
where that provenance is unavailable, state that overlap is unknown. A small convenience
sample cannot establish population performance. Do not claim independence or no training
overlap without evidence. Keep any later source-specific scores separate where labels or
severity scales differ. The [open-data plan](../../docs/reference/OPEN-DATA.md) remains
the authority for data-source inspection; this plan selects or downloads no data.

## Request boundary, traceability, and privacy

For every recorded run, verify what actually crossed each boundary:

- Image model request: photo only. No farmer note, identity, location, history,
  extent, prior finding, weather, source label or routing-oracle field.
- Optional interpretation request: candidate scores, farmer note, and only the
  optional versioned event-weather snapshot. No raw identity/coordinates, connected
  farm or nearby history, earlier assessment, extent, case data, source/evaluation
  labels, synthetic history, rule inputs or route oracle. The farmer note is untrusted user content
  and may itself contain personal details; do not duplicate it into experiment logs.
  Include a prompt-injection probe and verify the structured response contract.
- Code/rule: current-report facts derived under the authoritative rule plus controlled
  synthetic history/case records; record the inputs, matched rule, route and reason so a
  rerun can reproduce the decision. Do not enter a desired route as a test input.

Record random run IDs, neutral report/assessment IDs, source image hash/manifest ID,
model/provider and artifact/version, preprocessing, prompt and schema version, weather
snapshot/provider/version or unavailable state, synthetic-history record IDs and
completeness metadata, exact rule/guidance version, start/end
timestamps, elapsed duration, outcome/error, token usage and provider-reported charge
where available. Record CPU/RAM context for local timing. Never put credentials, raw
farmer identity, or unnecessary raw personal data in evidence. Do not log request
bodies, farmer-note text, raw model responses in experiment reports, or a hash of
payload text; even a digest can expose low-entropy or personal content. Use field-name
presence/absence checks, a schema-validation result and a random correlation ID to
show boundary compliance without copying values. If application storage retains the
response as required by the UC, keep it under the app's access controls and out of
shared experiment evidence.

Use explicit opt-in live runs outside ordinary tests. Automated tests and routine
checks must not make paid provider calls. If the provider does not report tokens or
charge, record `unknown` with the reason; do not estimate it as an observed cost.
Do not retry silently: each attempt and charge belongs in the run record. A duplicate
submission/idempotence check should confirm whether it reuses an assessment or creates
a separately identified reassessment according to the approved behavior.

## Measurements and cost-benefit method

For each actual run, separate and label:

- model initialization/readiness, image preprocessing, inference, optional
  interpretation, routing/persistence, and end-to-end elapsed time;
- warm single-request measurements from cold startup, and local CPU/resource
  measurements from hosted provider latency; do not call either a concurrency or
  service-level result without that workload;
- staff active minutes (measured only from an observed task protocol) from elapsed
  waiting time; and
- provider-reported actual tokens/charges from scenario assumptions.

For a later transparent comparison, measure a manual baseline with the same defined
report and handoff tasks before attributing savings. No quantitative real-world
baseline exists yet. Use staff cost only as an explicitly supplied assumption. For
each low/base/high assumption scenario, show the inputs and compute:

`assisted total active minutes = intake + assessment review + routing/handoff + correction/rework + failure/retry handling`

`net staff minutes = manual active minutes - assisted total active minutes`

`net value per report = (net staff minutes / 60 * assumed loaded staff cost per hour) - observed or explicitly assumed AI cost per report`

`break-even reports = fixed setup cost / positive net value per report`

Count each assisted active task exactly once in `assisted total active minutes`;
correction/review/failure time is already included there and is not subtracted again.
If net value is zero/negative, report no break-even under that scenario. State whether
the assumed time savings were measured, elicited, or illustrative. Show latency
separately: waiting for a model is not labor saved unless the task protocol demonstrates
that the staff member can do other work. Mark hypothetical costs or missing provider
prices as assumptions/unknown. This calculation estimates prototype economics only;
it cannot establish realized cooperative savings or diagnostic value.

## Worked sensitivity example (assumptions only)

[Versioned inputs and derived values](cost-benefit-scenarios.json) provide a worked
comparison for the paper, separate from unrun application results. All numeric inputs
are arbitrary, project-authored illustrations: 100 reports/month, loaded staff value
BRL 30/hour, AI cost BRL 1/report, and setup cost BRL 600. None is a case-study fact,
quoted model price, measured staff time or actual prototype cost. A flat assumed AI
cost is used so the example does not imply free local compute or an authorized paid
provider. Replace assumptions only with properly labelled measured or sourced values.

| Assumption scenario | Manual active minutes | Assisted total active minutes | Net staff minutes | Net imputed value/report | Whole reports to break even |
| --- | ---: | ---: | ---: | ---: | ---: |
| Conservative | 10 | 12 | -2 | BRL -2.00 | None |
| Central | 15 | 10 | 5 | BRL 1.50 | 400 |
| Optimistic | 20 | 8 | 12 | BRL 5.00 | 120 |

The JSON decomposes assisted time into intake, assessment review, routing/handoff,
correction/rework and failure/retry handling; each is counted once. With the illustrative
monthly volume, the central case reaches its modeled break-even at 4 months and the
optimistic case at 1.2 months; the conservative case never does under those inputs.
These are arithmetic consequences of the assumptions, not benefit evidence. Staff
capacity released is an imputed value, not automatically cash saved. No avoided visit,
real service-time reduction, outcome improvement or diagnostic value is priced here.

## Technical recommendation

Recommend the local split path as the first candidate for implementation feasibility:
the already pinned image classifier followed by the official Qwen3-0.6B local text
candidate reviewed in [local-interpreter metadata notes](../local-interpreter/README.md).
The classifier has an actual contained feasibility run; two contained interpreter
trials completed with 0/12 accepted outputs. This path keeps farmer data local and provides a concrete input
boundary for image-only scoring followed by a text-only structured interpretation.
It is a technical recommendation, not a provider selection or suitability finding.

The [interpreter results](../local-interpreter/RESULTS.md) record actual artifact,
dependency, containment, CPU and memory checks and both output-contract failures. One
constrained-output follow-up is proposed but has not been implemented or measured;
its success must not be assumed. Provider choice remains open.

## Existing evidence and planned completion

### Existing intake baseline (verified 10 November 2026)

Code inspection of `src/app/application/intake.py`, `src/app/domain/reports.py`,
`src/app/infrastructure/web.py` and `src/app/infrastructure/sqlite.py` confirms the
current reusable slice is report intake, storage, retrieval and farm-wide report
history. The web boundary decodes and verifies uploaded JPEG/PNG files and enforces
the 10 MiB cap; the integration suite covers valid JPEG/PNG examples and rejects
malformed image bytes. A direct check of the existing `verify_image` function accepted
generated blank white JPEG and PNG files. This verifies image-file validity only:
there is no leaf/coffee validity check, so a blank valid image is accepted. The app
stores and serves the uploaded image bytes as received; no assessment preprocessing
or transformation currently exists. This is compatible with a future image-only
adapter receiving the original photo, but does not implement one.

There is no application assessment, LLM interpretation, case, routing/handoff
behavior, or assessment/handoff UI in `src/app` today. The existing farmer intake and
report-detail pages are present. No manual or visual browser check was performed as
part of this baseline.

The scoped existing-intake and architecture command was run against the test suite:

```text
.venv/bin/python -m pytest tests/integration/test_intake.py tests/unit/test_architecture.py -q
32 passed in 0.33s
```

The intake test client creates its SQLite database under pytest's `tmp_path`; this
run did not use `data/bpm.sqlite3`. These results verify only the covered backend
intake/storage/restart/image-format and architecture checks. They do not verify the
browser visually or any UC-002 assessment, route, model, case, handoff or weather path.

The [first contained local-classifier run](../local-classifier/RESULTS.md) and its
[captured score vectors](../local-classifier/evidence/first-run.json) are actual
pre-application measurements, not synthetic expected outcomes. Under config
center-crop, `sample-02.jpg` yielded Rust 0.4353; its dimmed and blurred variants yielded
Phoma 0.5515 and 0.4689. A synthetic white blank image yielded Rust 0.7811. These are
observed model scores, not diagnoses or routing labels. The JSON records 28 image and
perturbation/preprocessing predictions; reuse selected vectors unchanged for later
history-pair routing checks rather than rerunning and describing the same image output
as independent. Its warmed CPU forward median was 77.07 ms on the documented machine.
The run also records preprocessing sensitivity, no independent diagnostic truth, and
unsupported-input limits. It did not test an interpretation model, application route,
human handoff, weather integration or provider costs. Do not cite it as E2E success or
diagnostic performance.

The two Qwen trials produced actual responses but no accepted output (0/12); see the
[interpreter results](../local-interpreter/RESULTS.md) for errors and limitations. No
paired-history route or end-to-end result is measured. Application work and route
evaluation await a usable interpretation path, remaining real-report rule/guidance
definitions and an implemented journey. Record future results or errors as observed.
At execution, append a dated report and link evidence for:

- run/environment and scenario IDs, selected/excluded inputs and known dependencies;
- actual image and interpretation outputs, ambiguous/unsuitable cases and each failure
  path, clearly separated from source labels and synthetic history assumptions;
- request-boundary evidence, output validation, route reproducibility and handoff
  persistence/restart behavior, with paired checks reusing frozen actual assessment
  outputs and deriving route only from synthetic history plus the exact rule version;
- timings/resource use, actual provider token/cost data or explicit unknowns, and
  assumptions behind each low/base/high cost-benefit scenario; and
- deviations, limitations, unresolved decisions and the scope of any conclusion.

No application routing, interpretation or end-to-end success is claimed by this plan.
Classifier scores and the failed interpreter trial outputs are actual model evidence;
accepted interpretation, route and end-to-end measurements remain outstanding.
Keep source-backed agronomy, prototype assumptions and measured results separate in
those reports.
