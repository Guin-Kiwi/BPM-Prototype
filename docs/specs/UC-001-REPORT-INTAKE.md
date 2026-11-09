# UC-001-REPORT-INTAKE

## Goal
Select a fictional farm and field, submit a text observation with an optional image,
and retrieve the saved report alongside earlier reports for that field.

## Business value
Establish attributable intake and useful field context for the P1 demonstrator,
without presenting synthetic scenarios as real farm records.

## Scope

### In scope
- Local selection of a fictional farm and one of its fields; a small, explicitly
  synthetic seed history and an empty-history case.
- Observation date, required description and optional image; validation, save
  confirmation, retrieval by report ID and earlier reports for the selected field.
- Original submitted evidence, generated report ID and receipt timestamp; clear
  distinction between observations and any earlier confirmed findings.
- Attribution for any open-data images used in synthetic scenarios, with current
  sample evaluation answers kept separate.

### Out of scope
- AI diagnosis, action selection, treatment guidance, messages and orders.
- Creating confirmations or inferences during intake; routing and review policy.
- Voice, GPS/pH, offline sync, aggregation, measured incidence and real farm history.
- Authentication and deployment; this slice is a local demonstration.

## Actors

Primary: farmer role entering a report; Ayla demonstrating synthetic reports.
Secondary: evaluator preparing attributable dataset samples and synthetic history.

## Preconditions
Local application running with writable local storage and fictional farms, fields
and history available. Each field belongs to a selected farm. Dataset images, if used,
have source provenance and synthetic scenario context. No provider credentials required.

## Trigger
User opens report entry to record an observation for a field.

## Main flow

1. Select a fictional farm and one of its fields, enter the observation date and
   description, and optionally select a leaf image.
2. Validate the inputs and attachment; save the report and image with a unique ID and
   receipt timestamp, preserving the submitted evidence.
3. Show confirmation and saved report detail, clearly marked as synthetic/demo data.
4. Retrieve the report by ID, including after restart. Show earlier reports for the
   same field, separately identified as history; show any earlier confirmed findings
   as such and preserve their distinction from submitted observations.

## Alternate / edge flows

- Text-only reports are valid. A field with no earlier reports shows an empty history;
  missing history does not mean there was no disease.
- History contains only reports for the selected field that precede the current report;
  it excludes the current report and reports for other fields. The time basis for
  “earlier” must be explicit in DESIGN; receipt order alone may misorder backdated
  observations.
- Repeated submissions remain distinct; deduplication and aggregation are deferred.
- Dataset images may illustrate synthetic reports. Reuse is identified in scenario
  provenance and does not establish independent observations or real field incidence.

## Errors / failure cases

- Missing required values, invalid farm/field pairing or date, unsupported/corrupt
  image or oversized upload: explain the problem without a partially saved report.
- Unknown report ID: clear not-found result.
- Storage failure: report failure; do not claim successful receipt.

## Acceptance criteria

Sources: [main paper and concept](../reference/README.md) for field-linked reports
and history; agreed intake and synthetic-history scope in the current request. Image
limits are proposed defaults pending agreement, not established policy.

1. Given fictional farms and fields, the user can select a farm and a field belonging
   to it. Given valid date and description, submitting with or without an image saves
   a distinct report with matching evidence, unique ID and receipt timestamp.
2. Given a saved ID, detail retrieves the report and any saved image after restart;
   it shows only earlier reports for that same field, or an explicit empty history.
3. Given history with submitted observations and an earlier confirmed finding, the
   view distinguishes them and marks the scenario synthetic. It does not describe an
   observation or AI inference as a confirmed finding.
4. Given a dataset-backed scenario, source attribution and synthetic context are
   available. Current-sample disease/severity answers and label-bearing filenames
   are absent from the observation, displayed attachment name and future diagnosis
   inputs; earlier confirmed findings may be visible as history. See the
   [open-data plan](../reference/OPEN-DATA.md) for leakage controls.
5. Given an invalid farm/field pairing, input or attachment, the user sees an
   actionable error and no partial report. Given storage failure, no success is
   reported; an unknown ID gives a not-found result.
6. Subject to approval of the proposed attachment defaults, a valid JPEG/PNG is
   displayed on detail; corrupt, unsupported or over 10 MiB files are rejected.

## Security / trust-boundary notes

Treat uploads and text as untrusted: validate actual image content, escape rendered
text, generate neutral storage/display names, limit upload size and prevent path
traversal. Local synthetic data only; do not expose the unauthenticated prototype
publicly. Keep provenance and evaluation metadata out of diagnosis inputs.

## Validation plan

### Tests
- Unit: farm/field pairing, required inputs, report creation and history boundaries
  (criteria 1, 2, 5).
- Integration: save/retrieve and restart, field isolation and empty history, labelled
  evidence types, dataset provenance and current-answer/filename leakage, valid and
  invalid attachments, unknown ID and storage failure (criteria 1–6).
- E2E: demonstrate selection, text-only and image submissions, retrieval, earlier
  confirmed history, empty history and errors; inspect synthetic labels and attribution
  (criteria 1–6). Attachment-limit checks depend on agreement on defaults.

### Evidence
Record executed application checks during VALIDATE. No application checks have run.

## Open questions / assumptions

- Recommend one required description, one optional JPEG/PNG image and a 10 MiB
  maximum: simple for the first demo and bounded for local storage. These defaults
  require agreement; implementation of their exact limits awaits that decision.
- Recommend a small seed with two farms, two fields each and a few earlier reports,
  including one confirmed finding and one empty field; exact counts are not approved
  requirements. See the [open-data plan](../reference/OPEN-DATA.md).
- Local persistence and upload handling belong to DESIGN. Recommend observation
  date for history chronology, retaining receipt time separately; define ties and
  backdated entries before implementation. No images are downloaded.
- Offline capture is a paper assumption deferred beyond this slice; disclose the gap.

## Notes for implementation

Use existing domain/application/interface/infrastructure layers. Design selection,
report persistence and history retrieval; decide persistence in DESIGN and record
consequential decisions per the working agreement. Intake does not require a model
provider, routing policy or new review workflow.
