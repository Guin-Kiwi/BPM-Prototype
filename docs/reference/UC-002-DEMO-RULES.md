# UC-002 demonstration rules and scenarios

This is a **proposal for owner review**, not approved policy, an agronomic protocol,
validated guidance or an executable DMN. It makes the routing worksheet's proposed
rule reviewable for the complete [UC-002 journey](../specs/UC-002-ASSESSMENT-HANDOFF.md).
The worksheet remains the authority for the selected direction and assessment boundary.
The labels and fixtures below are deliberately synthetic; they establish neither a
real report's risk nor eligibility for agronomic advice. Proposed windows below are
reversible demo assumptions, not agronomic thresholds.

## Proposed decision table: `uc002-demo-draft-1`

Evaluate top to bottom, taking the first match. Record the matched row, rule version,
input facts and reason. `unknown` includes unavailable or not established; it never
means `no`. The proposed facts are categorical, not direct model score thresholds:

| Order | Condition | Route | Recorded reason |
| --- | --- | --- | --- |
| 1 | Concerning risk, a repeat trigger or an unresolved-case trigger is established | Technician | List each established trigger. |
| 2 | Evidence is insufficient or unknown, or risk is uncertain or unknown | Technician | Identify the insufficient or unknown fact. |
| 3 | Applicable prepared guidance is absent, inapplicable or unknown | Technician | Guidance is not established as applicable. |
| 4 | Risk is low, evidence sufficient, applicable prepared guidance is identified, and repeat and unresolved-case triggers are both known absent | Communications | Routine eligibility established; identify the guidance entry. |
| 5 | Any remaining combination, including unknown history trigger | Technician | Specify the fact preventing routine eligibility. |

A technician route means human involvement, not an automatic visit or severe action.
An appropriate existing case is linked or a new case is created by a person when a
technician becomes involved. Communications records a person's relay of the identified
prepared guidance; the model does not generate treatment advice. Delivery, handling,
resolution and case closure are distinct. Severe actions retain human approval.

## Proposed connected demonstration configuration

One option for owner choice is that a presenter explicitly attaches a **scenario profile**
to a saved report before a live assessment. A profile supplies only the demo facts `risk` (`low`, `concerning`,
`uncertain`, `unknown`), `evidence` (`sufficient`, `insufficient`, `unknown`) and
`guidance_id` (an approved prepared entry identifier, or none/unknown). For the
recording fixture only, `G-DEMO` stands in for an entry and must be visibly labelled
as a test, not treated as applicable substantive guidance. The profile is hand-authored, versioned,
labelled synthetic on screen and in the record, and never derived from the model or
sent to either model. It is an operational simulation control, not reference truth,
source-label metadata or an evaluation label. The live image and interpretation calls
still run and their actual outputs are saved; a failure or invalid output is an error,
not a successful assessment or handoff. The presenter can choose a low/sufficient
profile for a routine demonstration without a technician reviewing every report.
Without a profile in this option the three facts are unknown, so the table selects
technician after a successful assessment. The structured guard below applies to every
profile; it can prohibit routine even when a profile says low/sufficient. Profile facts
are not a diagnosis or validated eligibility.

A separate option is **model-informed demo derivation**, not a profile supplying the
outcome: after successful inference and the guard, code assigns `low` and `sufficient`
only when the classifier's highest-scoring class is uniquely Rust, the interpretation
selects Rust, its warning is `none`, its note relationship is `consistent`, the estimate
exists, and the separately declared synthetic scenario facts establish Arabica and
possible rust as required by [the guidance candidate](UC-002-GUIDANCE-CANDIDATE.md).
Code maps that combination to `G-RUST-OBSERVE-1`; otherwise risk and evidence are
unknown and guidance is absent, except where the guard specifies insufficient evidence.
The history table still applies. Ties for highest score are not unique. This is an
explicitly **unvalidated demonstration assumption**, not an agronomic judgment or a
claim of real-world suitability: a leading score can result from a blank image, and no
leaf detector is available. The owner may choose either mechanism, or request a revised
proposal; neither is selected by this draft. The live assessment has a direct role in
this second option rather than merely accompanying supplied eligibility labels.

The farmer's count or percentage is stored and displayed with its original kind, unit
and area cue. Code records whether the estimate exists and includes its unchanged value
in the routing input record, but does not convert one kind to the other, compare their
magnitudes, infer a denominator or derive risk from either. A missing legacy estimate
makes evidence unknown regardless of the profile. No field-incidence or severity
threshold is implied. Other profile facts are overrides for demonstration, not measured
facts about the extent or image.

**History proposal:** use the same farm, independent of field or suspected issue, and
include any distinct report with observation time in the 30 days before the current
report's observation time (inclusive at the start, exclusive at the end). This broad
repeat trigger is deliberately conservative and the 30-day window is a demo assumption,
not disease biology. Exclude the current report and later or simultaneous observations.
A qualifying report establishes repeat even if other history is missing. Otherwise,
repeat is known absent only if the demo explicitly records the farm's report history as
complete for the entire window and all potentially relevant observation times are known;
otherwise it is unknown. The simulated capture time stays labelled as such.

An unresolved-case trigger is established if any same-farm case is recorded as open;
handling or advice recorded does not close it. It is known absent only when case history
is explicitly recorded complete and no open case exists; otherwise it is unknown. An
established trigger wins over an unknown one. On technician involvement, a person
inspects same-farm open cases and selects an appropriate existing case or creates a new
one, recording the choice and reason. The system proposes no automatic merge and does
not close a case. Completeness is a declared demo-data property, not an inference from
an empty result; no nearby-history completeness is assumed.

**Live model contract proposal:** recommend the pinned local classifier candidate in
the [feasibility run](../../experiments/local-classifier/RESULTS.md), pending suitability
review. Decode the uploaded image, convert to RGB, resize the shorter side to 224,
center-crop 224 × 224 with bilinear antialiasing, then apply the pinned configuration's
ImageNet normalization. Record artifact, class order and preprocessing version. Validate
exactly seven finite numeric scores (excluding booleans) in [0, 1], one per pinned
class in manifest order, with absolute difference from a sum of 1 no greater than `0.000001`;
save all candidates as uncalibrated scores, not disease probabilities. The classifier
sees only the photo. It has no invalid-image rejection and a blank scored Rust highly;
no new leaf detector is assumed and score validation does not establish image validity.

The text-only interpretation request contains only the candidate class names and scores,
the farmer note if present, and the selected optional weather snapshot. No report ID,
identity, extent, history, prior finding or source/evaluation label is sent. The response
must be one JSON object, at most 4096 UTF-8 bytes, with exactly these required keys and
no extra keys:

| Key | Required value |
| --- | --- |
| `schema_version` | Exact string `uc002-interpretation-1`. |
| `suspected_issue` | Exact supplied candidate name, or `unknown`. |
| `uncertainty` | `uncertain` or `unknown`; neither establishes eligibility. |
| `warning` | `none`, `insufficient_evidence`, `unsupported_issue`, or `unknown`. |
| `note_relation` | `consistent`, `contradictory`, `not_provided`, or `unknown`. |
| `limitations` | Array of 1–4 nonempty strings, each at most 200 Unicode characters. |
| `weather_used` | JSON boolean; must be false when no snapshot is supplied. |

`insufficient_evidence` means the supplied inputs are inadequate to interpret;
`unsupported_issue` means the note or weather suggests a possibility outside the
candidate list; `unknown` means the model cannot decide whether a warning applies.
`contradictory` means the note explicitly conflicts with the selected candidate;
`consistent` means the note explicitly supports the candidate without a conflicting
statement; `not_provided` is allowed only when the farmer note is absent or blank;
`unknown` covers all other cases. These model-reported categories are uncertain and
cannot detect an invalid photo, establish visible symptoms, or independently verify the
note. An absent or blank note must produce `not_provided`; a nonblank note must not.
Require limitations to describe uncertainty without treatment instructions, invented
visual observations, or unsupported diagnoses. Output violating these constraints,
including incorrect types, malformed JSON, duplicate keys, invalid enums, or unknown
fields, is an invalid output error; do not save a successful assessment or handoff.
A provider or classifier failure is likewise an error. Save the raw response and error
separately for inspection when available, without portraying it as an assessment.

For valid outputs, apply this deterministic guard before either proposed eligibility
mechanism: if `warning` is `insufficient_evidence` or `unsupported_issue`, or
`note_relation` is `contradictory`, set routing evidence to `insufficient`; if `warning`
is `unknown`, `note_relation` is `unknown` or `not_provided`, or `suspected_issue` is
`unknown`, set it to `unknown` unless already insufficient. Either prevents routine
eligibility. A profile cannot override this; record the original profile, guard result
and all triggering enum values. No free-text pattern matching is used to derive a guard
result. A structurally valid but semantically false model response may evade the guard;
no claim of guaranteed detection is made. Save validated fields, model/prompt versions
and snapshot reference separately from classifier output. The text backend/hosting and
cost remain a provider choice. Weather is optional; table decisions use the same explicit
facts whether it is present or absent, although weather may affect interpretation and
thus the guard.

## Recording-test fixture `G-DEMO`

This project-authored, non-treatment message is a UI and recording test fixture, not
sourced agronomic guidance or technician-approved advice. In a labelled simulated
recording test, a person can relay and record the following exact text and entry version
`G-DEMO-1`; it makes no claim about the condition, extent or actions needed on a real
farm:

> We received your report. This demonstration has recorded your photo and estimate for
> review. The automated assessment is uncertain and does not confirm a diagnosis. Please
> contact the cooperative if you need further assistance.

No model-generated treatment, diagnosis or product instruction is included. The message
is an acknowledgement and explanation, not agricultural guidance or evidence of a
resolved issue. It does not complete the selected routine branch. That branch requires
a real attributable illustrative prepared guidance entry, suitability and reuse checks,
and an explicit applicability mapping. The [Arabica rust observation candidate](UC-002-GUIDANCE-CANDIDATE.md)
now proposes `G-RUST-OBSERVE-1`, its exact wording, source, applicability and limits; it
remains unselected. Investigating and proposing suitable guidance remains
project work; the owner need not supply a validated agricultural policy.

## Deliberate synthetic scenarios

These are hand-authored decision inputs, not actual model outputs or validated cases.
Each assumes all unspecified facts needed for its stated row are established. They
exercise the proposed table and handoff, not diagnostic accuracy.

| Fixture | Explicit facts | Expected route and observable handoff |
| --- | --- | --- |
| Routine | Low risk; sufficient evidence; hypothetical applicable prepared entry; both history triggers known absent | Row 4 in the synthetic table; no case. `G-DEMO-1` can test recording only; full routine completion awaits substantive prepared guidance and its mapping. |
| Concerning | Concerning risk; other facts may be unknown | Row 1, technician involvement; person links or creates a case. Severe action still needs approval. |
| Insufficient | Evidence insufficient; risk unknown; history triggers absent | Row 2, technician involvement; record the missing evidence. |
| Unsupported | Low risk; sufficient evidence; no applicable prepared guidance; history triggers absent | Row 3, technician involvement; record unsupported guidance. |
| Repeat or unresolved | Low risk; sufficient evidence; applicable guidance; repeat or unresolved-case trigger established | Row 1, technician involvement; person links an appropriate case or creates one. |
| Unknown history | Low risk; sufficient evidence; applicable guidance; no established repeat or unresolved trigger, but history availability unknown | Row 5, technician involvement; record unknown history. |

For a paired boundary check, retain the same standalone assessment while changing only
history from known absent to an established repeat: the route changes from row 4 to
row 1. Another pair uses the same decision facts with weather present and unavailable;
the table gives the same route. These synthetic checks do not claim that real weather
can never influence an interpretation. Reassessment is a separate saved assessment.

## Owner decisions before implementation

1. Recommended: preserve substantive prepared guidance as the routine objective and
   use explicitly synthetic scenario facts to demonstrate routing, with the guard above.
   An acknowledgement-only routine branch is a scope reduction and is not recommended.
   Alternatively choose the explicitly unvalidated model-informed derivation above or
   request a revised proposal. Review the existing [attributable guidance candidate](UC-002-GUIDANCE-CANDIDATE.md)
   `G-RUST-OBSERVE-1` and its proposed applicability mapping; `G-DEMO-1` only tests recording.
2. Accept the proposed same-farm 30-day repeat rule, explicit completeness semantics,
   unresolved-case definition and human case-linking procedure, or supply alternatives.
3. Accept the local classifier/preprocessing and response contract as a limited demo
   candidate after considering unsupported images, review the proposed structured warning and
   contradiction guard, and select the text backend/hosting and cost. Resolve weather
   acquisition/window separately if weather is used.

Reconcile the selected process pair with group sources. Once definitions are approved,
version the authoritative rule table and guidance mapping, then check each DMN row,
ordering, output and reason against it using scenarios covering every row, unknowns and
overlaps. Verify the model-input boundaries, persistence, recorded human handoffs and
severe approval separately. No such implementation or validation has occurred.
