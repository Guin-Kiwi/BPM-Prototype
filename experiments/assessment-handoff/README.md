# UC-002 assessment and handoff experiment plan

## Purpose and status

This document plans evidence for the [UC-002 assessment and handoff slice](../../docs/specs/UC-002-ASSESSMENT-HANDOFF.md).
It is a SPECIFY-phase evaluation plan, not an implementation, completed application
experiment, approved routing policy, or claim of agronomic validity. Experiment
execution follows owner decisions, provider selection, and implementation. Record
outcomes in a dated run report linked from here; preserve failures and exclusions.

The [routing worksheet](../../docs/reference/DMN-RULE-WORKSHEET.md) owns the selected
business direction. The shared [UC-002 demonstration rules](../../docs/reference/UC-002-DEMO-RULES.md)
currently specify proposed version `uc002-demo-draft-1`, including the connected-demo
scenario profile and its proposed history facts. This proposal is unapproved. Use this
exact version when describing or exercising its proposed behavior; record any later
approved version explicitly rather than silently renaming the draft. It is an oracle
for whether implementation matches supplied demo facts, not for learned risk, clinical
quality, or real-report eligibility. The profile's synthetic risk/evidence/guidance
facts are simulation controls and must never be presented as model output, diagnostic
truth, or validated routing facts.

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
   the oracle route and reason from the supplied facts, and does a person complete
   the applicable communications or technician handoff? A route is not a diagnosis,
   severe-action approval, delivery, resolution, or case closure.
4. **Operational feasibility:** what are actual machine/provider elapsed times,
   resource use and provider charges, and how do those compare with explicitly
   assumed staff-time scenarios? Model latency is not staff time saved.

Record source/fixture truth by type: (a) source asset and attribution, (b) source
dataset labels with their original meaning, (c) synthetic scenario profile and
history-completeness facts, (d) the proposed/approved routing rule version, and (e) any
independent expert diagnostic reference, if one is later obtained. Keep source labels,
profile and routing-oracle fields out of images, filenames, model requests and other
inference inputs. Report an unavailable truth source as a limitation; do not promote a
model's own output to ground truth.

## Scenario matrix

Run each connected demonstration with live image and interpretation inference and an
explicit, versioned scenario profile attached to the saved report, as proposed in the
shared rules. Profile facts drive the demonstration route but are not derived from or
sent to either model. Log the actual live assessment independently from the profile
and route. The image and interpretation results can be evaluated for schema validity,
traceability, ambiguity and limitations; they must not be scored as matching profile
risk or as clinically correct. Rule conformance is checked separately: given the
recorded profile/history facts and exact rule version, does the deterministic decision
match that version's route and reason? Without a profile, assess the documented
unknown-fact path after a successful live assessment. A model or storage failure is a
failed run, not a completed route. These demonstrations do not measure real-world
routing quality.

| Scenario family | Input / expected evidence | Outcome to record |
| --- | --- | --- |
| Synthetic routine route | Attach the linked rule's explicit routine profile (including `G-DEMO`) to a saved report; run both live models; provide complete history with both triggers known absent. | Log actual model outputs separately. Check route/reason against `uc002-demo-draft-1` given the supplied profile/history; record the person's `G-DEMO-1` relay and no case. This is not evidence that a real report is low risk or eligible for advice. |
| Escalation and precedence | Use separate explicit profiles for concerning risk, insufficient/unknown evidence, and absent/unknown guidance; pair with controlled repeat, unresolved-case, and unknown-history facts, including overlaps. Run both live models for each profile. | Log assessment independently; check matched rule/precedence, route and reason against `uc002-demo-draft-1` from supplied facts. Record human technician involvement and case choice. This does not evaluate whether supplied profile facts describe the image or a farm. A route does not authorize severe action. |
| No-profile path | Run a successful live assessment with no profile attached; mark history completeness according to the scenario record. | Profile facts stay unknown per the linked proposal; check the resulting route against `uc002-demo-draft-1`. Do not treat model interpretation as a substitute profile or as established risk/evidence. |
| Boundary pairs | Hold report, live assessment and profile constant while varying only connected history; compare weather-present versus weather-unavailable when weather is used. | History may change route while leaving the standalone assessment unchanged. Optional/missing weather is traceable; route behavior is checked against the exact rule version. This does not establish clinical quality or a real weather effect. |
| Live assessment successes and ambiguity | Use only approved local examples and controls. Preserve source labels without treating them as diagnostic truth or scenario-profile facts. Include valid and ambiguous outputs if they occur. | Save finite schema-valid candidate scores and interpretation fields, model/prompt versions, preprocessing and timing. Describe ambiguity without inventing a universal confidence cutoff or claiming agreement with supplied risk. |
| Unsuitable inputs | Synthetic blank and geometric controls, plus the licensed example JPEGs that are detached leaves on plain backgrounds. These do not represent field reports. No new dataset is authorized by this plan. | Record ordinary scores, refusal/abstention if implemented, and resulting uncertainty. Existing blank overconfidence is a known limitation; do not count it as a successful diagnosis. |
| Failure paths | Missing report/image/configuration; malformed model output; timeout/provider unavailable; storage error; invalid/missing weather; restart/reload. Include bounded interpretation prompt-injection text as untrusted farmer content. | Visible failure state with no fabricated assessment, route, delivery or resolution; original report remains retrievable. Record retries and whether repeated requests create duplicate assessments/handoffs. |
| Handoff lifecycle | Routine communications record and technician involvement/case handoff; later reload and restart. Reassessment uses same report evidence. | Persisted provenance, route, reason, handoff and case link survive restart. Reassessment is a separate assessment; handling/delivery does not imply closure/resolution. |

The scenario inventory is not a statistical sample. If later work adds examples, record
selection rationale, exclusions and dependence. Multiple crops, perturbations or
re-encodings from one source image are related observations, not independent samples.

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
  extent, prior finding, weather, source label or scenario-profile/routing fact.
- Optional interpretation request: candidate scores, farmer note, and only the
  optional versioned event-weather snapshot. No raw identity/coordinates, connected
  farm or nearby history, earlier assessment, extent, case data, source/evaluation
  labels, scenario profile or route oracle. The farmer note is untrusted user content
  and may itself contain personal details; do not duplicate it into experiment logs.
  Include a prompt-injection probe and verify the structured response contract.
- Code/rule: separately prepared approved facts and the authoritative rule version;
  record inputs, matched rule, route and reason so a rerun can reproduce the decision.

Record random run IDs, neutral report/assessment fixture IDs, source image hash/manifest
ID, model/provider and artifact/version, preprocessing, prompt and schema version,
weather snapshot/provider/version or unavailable state, scenario-profile version and
synthetic marker, supplied synthetic `risk`, `evidence` and `guidance_id` values in a
separate profile record, history-completeness facts, exact rule/guidance version, start/end
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

The [first contained local-classifier run](../local-classifier/RESULTS.md) is actual
pre-application feasibility evidence: pinned artifacts loaded within its recorded
local limits, warmed CPU forward median was 77.07 ms on the documented machine, and
blank input returned a high Rust score. Its perturbation and preprocessing sensitivity,
absence of diagnostic truth, and unsupported-input limitations are also recorded.
It did not test UC-002 storage, interpretation model, route, human handoff, weather or
provider costs. Do not cite that run as E2E success or diagnostic performance.

The plan is ready to execute when the provider/assessment contract and real-report
fact definitions are decided, the routing/guidance oracle is approved for the scenarios
being exercised, and the application journey exists. Until then, mark those checks
pending; do not fill in fabricated outcomes. At execution, append a dated report and
link evidence for:

- run/environment and scenario IDs, selected/excluded inputs and known dependencies;
- actual successes, ambiguous outputs, unsuitable inputs and each failure path;
- request-boundary evidence, output validation, route reproducibility and handoff
  persistence/restart behavior;
- timings/resource use, actual provider token/cost data or explicit unknowns, and
  assumptions behind each low/base/high cost-benefit scenario; and
- deviations, limitations, unresolved decisions and the scope of any conclusion.

No application experiment or end-to-end success is claimed by this plan. The actual
check status and evidence belong in future dated run reports, not inferred from this
checklist.
