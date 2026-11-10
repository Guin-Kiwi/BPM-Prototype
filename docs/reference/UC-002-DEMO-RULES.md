# UC-002 demonstration routing proposal

**Status: proposed**, for the [UC-002 journey](../specs/UC-002-ASSESSMENT-HANDOFF.md);
Selected direction for the first bounded observation demonstration; the detailed
software assumptions remain proposals, not measured behavior, agronomic validation or
an executable DMN. This
proposal replaces the worksheet's unresolved low-risk test for this narrowly scoped
demonstration: communications relays a matching prepared **observation** message, not
a clearance that risk is low. No model or rule prescribes treatment. The
[routing worksheet](DMN-RULE-WORKSHEET.md) retains the wider process and model boundary.

## Decision table: `uc002-demo-draft-2`

Interpreter agreement with the classifier is **not independent confirmation**: it
interprets the same scores and optional note/weather. It supplies no second image
examination or calibrated increase in confidence.

After successful valid image and interpretation calls, evaluate in order; save rule
version, input facts, matched row and reasons. The inputs come from actual model outputs,
report/farm data and synthetic history, not hand-entered desired routes, risks or
eligibility. Unknown means not established. No numerical model-score or field-severity
threshold is used.

| Order | Condition | Route | Reason |
| --- | --- | --- | --- |
| 1 | An explicit link to the same unresolved issue/episode is established | Technician | Record the relevant issue/case link. |
| 2 | Relevant history/relationship data unavailable | Technician | Record what could not be checked. |
| 3 | Interpretation unknown, contradictory or unsupported; classifier and interpreter disagree; or no unique leading class | Technician | Record the assessment condition. |
| 4 | No matching applicable prepared observation entry, including unknown crop context | Technician | No applicable entry. |
| 5 | Unique leading class equals interpreted candidate; interpretation has no warning or contradiction; an applicable prepared entry exists; no established relevant unresolved-issue trigger and history query available | Communications | Record candidate and entry ID for human relay. |

If either model call fails or output is invalid, record an error and retain the report;
do not fabricate a successful assessment, route, or handoff. A missing farmer estimate
also prevents mapping to an entry and routes to technician after a valid assessment.
The routine route permits only a person's relay of the fixed entry. It asserts neither
that the report is low risk nor that the inferred issue is confirmed. Technician
involvement means a person links an appropriate existing case or creates one, with a
reason. No case is created for routine communication. A visit is a human decision;
handling and delivery are not case closure or resolution. Severe actions still require
human approval; no automatic contact, product order or severe action follows routing.

## Assessment and guidance mapping

Recommend the pinned classifier from the [contained feasibility run](../../experiments/local-classifier/RESULTS.md),
subject to suitability review. Photo only enters the classifier. Decode to RGB, resize
the shorter side to 224, center-crop 224 × 224 with bilinear antialiasing, and apply
the pinned configuration's ImageNet normalization. Record artifact, class order and
preprocessing version. Validate exactly seven finite numeric scores excluding booleans,
one per pinned class in order, each in [0, 1] and sum within 0.000001 of 1. Scores
are uncalibrated model outputs, not probabilities of disease. Record the full vector;
a tie for highest score is not a unique leading class.

Recommend the already [metadata-reviewed pinned Qwen3-0.6B candidate](../../experiments/local-interpreter/README.md)
for the first offline interpretation feasibility check: it avoids API credentials and
charges and uses the existing CPU host. This is a recommendation, not a measured claim
of adequate JSON compliance, model quality or memory fit. Review/lock dependencies,
verify artifacts and tied-weight behavior, and measure a bounded local run before app
integration. Use an independent RAM/time limit appropriate to the interpreter; do not
assume the classifier's 2 GiB cap fits it. If it fails the structured-output checks,
review a larger local instruction model rather than hiding failures or substituting
hand-authored outputs. No technical provider choice is delegated to Ayla.
The request contains only the candidate names and scores, farmer note if provided and
optional selected event-weather snapshot. It excludes identity, report ID, extent,
history, earlier findings and source/evaluation labels. Do not infer visible signs from
scores. Persist classifier results, interpretation, prompt/model versions and weather
snapshot separately; weather is optional and never adds an unsupported class.

Proposed interpretation output is exactly one JSON object at most 4096 UTF-8 bytes,
with all keys below required and no extras or duplicate keys:

| Key | Allowed value |
| --- | --- |
| `schema_version` | `uc002-interpretation-1` |
| `suspected_issue` | Exact supplied classifier class or `unknown` |
| `warning` | `none`, `insufficient_evidence`, `unsupported_issue`, `unknown` |
| `note_relation` | `consistent`, `contradictory`, `not_provided`, `unknown` |
| `limitations` | Array of 1–4 nonempty strings, each at most 200 Unicode characters |
| `weather_used` | Boolean; false when no snapshot was supplied |

`insufficient_evidence` means interpretation cannot be made from the supplied inputs;
`unsupported_issue` means note or weather suggests an issue outside the candidates;
`unknown` means the model cannot determine the warning. `consistent` means the note
does not contradict the selected issue, not independent confirmation. `contradictory`
means explicit conflict; `unknown` means relationship cannot be determined. If the
note is absent or blank, require `not_provided`; otherwise prohibit it. A missing note
alone does not block an otherwise matching observation message; unknown or contradictory
content does. The selected issue must equal the unique leading classifier class, warning
must be `none`, and note relation must be `consistent` or `not_provided`; otherwise
row 3 applies. The structured values are model inferences, not verified observations.
Invalid JSON, types, enums, candidate names, lengths, input-dependent fields, or
prohibited extra fields are errors. The prompt prohibits treatment, fabricated visual
observations and confirmed diagnoses; semantic violations detected during validation
are errors, but schema checks cannot guarantee detecting them.

Mapping is exact and versioned, never generated by the model. For a matching `Rust`
candidate, use [G-RUST-OBSERVE-1](UC-002-GUIDANCE-CANDIDATE.md) only when its crop and
other documented applicability conditions are established from farm/scenario context;
its wording discusses **possible** rust. For a matching `Leaf Miner` candidate, map to `G-LEAF-MINER-OBSERVE-1` in the same
catalogue, under its documented Arabica/observation-only scope. Other
classes have no entry unless separately specified. A score or inferred candidate does
not establish Arabica or confirm an issue; missing crop or entry applicability routes
to a technician. Guidance research and reuse checks remain separate from the routing
logic. Exact entry identifiers and applicability are recorded with each handoff.

The farmer's count or percentage, kind, unit and optional area cue remain unchanged in
the report and routing record. No conversion, inferred denominator, field incidence,
severity assessment or comparison between count and percentage is made; neither model
receives extent. The classifier has no invalid-image rejection and rated a blank white
input Rust 78.11%; an interpreter seeing only scores cannot reliably detect the blank.
A matching message therefore demonstrates workflow, not dependable image validity,
diagnosis or safe real-world agricultural routing. No leaf detector is assumed.

## Synthetic history and cases

Seed ordinary reports, cases and explicit issue/episode relationships, not desired
routes or eligibility. An established link to the same unresolved issue/episode is a
repeat/open-issue trigger. Farm membership, disease-label similarity and a 30-day age
window alone do not establish repetition; no farm-wide time-window rule is selected.

Absence of an issue link does **not** establish that other reports are irrelevant.
Keep all available farm context visible to the technician, including unlinked reports;
a person may later judge relevance and record a link. Routing records only whether
an escalation trigger is established in the currently available data. A failed history
query or unavailable relevant relationship data remains unknown and routes to a
technician. A successful query with no established trigger is not proof of no related
problem, low risk or resolved illness.

On technician involvement, a person inspects available cases and links an appropriate
one or creates one, with a reason. Handling does not close the case. Scenario profiles
and synthetic model outputs may be used for isolated rule unit tests only. The connected
demonstration uses actual image/interpretation outputs and ordinary synthetic history;
no presenter field chooses the desired route, risk or eligibility.

## Planned checks and existing evidence

Software conformance checks will exercise: a valid matching issue and applicable entry
with complete empty history; each unsupported/missing entry and unknown/contradictory
interpretation; missing note; tied or mismatched candidates; explicitly linked unresolved issue,
unlinked reports remaining visible, unrelated same-farm reports, and unavailable history; missing estimate; and model failures. Check both count
and percentage without converting either. Compare identical assessment outputs with
changed history and with/without weather; weather can change interpretation, so only
identical assessment facts must produce the same table result. Check entry provenance,
human handoffs, persistence and severe approval separately. Test fixtures for rule
conformance are not evidence of diagnostic correctness or field suitability.

The actual [first-run evidence](../../experiments/local-classifier/evidence/first-run.json)
shows, under center-crop preprocessing, original sample-02 leading Rust at 43.53%,
sample-03 leading Rust at 90.77%, and a blank leading Rust at 78.11%. Those are
classifier observations only: no interpreter or routing run has been performed and no
route or text-model result is claimed. Sample-02's leading class changed under tested
perturbations; none of these examples establishes independent diagnostic truth.

Before implementation, reconcile this scope with the worksheet and group sources,
use the researched source/applicability records for the two observation messages, and perform
the text-model and classifier suitability checks. Version the approved rules and mapping,
then compare eventual DMN order, conditions, outputs and reasons against the table.
No implementation, live end-to-end run or validation is claimed here.
