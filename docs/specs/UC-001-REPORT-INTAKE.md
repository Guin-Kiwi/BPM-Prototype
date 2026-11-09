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
- History is computed at retrieval: include same-field reports whose key
  `(observation date, receipt timestamp, report ID)` sorts before the current
  report’s key, newest first by that key. Dates use calendar-day precision; receipt
  timestamps are UTC instants and IDs break exact timestamp ties lexicographically.
  Exclude the current report and other fields. A later-submitted backdated report
  can therefore appear in history on a subsequent retrieval.
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
and history; the owner’s current request authorizes the bounded intake and synthetic
history scope. The concrete defaults below are implementation defaults accepted by Ayla for this prototype, not
group policy. The [source map](../reference/README.md) identifies the
paper as business-scope authority and the assignment as deliverables authority.

1. Offer at least two fictional farms with two fields each; each field belongs to one
   farm. Seed at least three earlier reports, including a fictional confirmed finding,
   and leave at least one field empty. Label scenario records synthetic.
2. Accept a selected farm and its field, a nonblank description, a valid observation
   date in ISO calendar format (not later than the application’s local current date),
   and zero or one image. Accept actual JPEG/PNG content up to and including 10 MiB;
   reject corrupt, unsupported or larger files. Save each valid submission as a
   distinct report with its original text, date, optional image, unique ID and UTC
   receipt timestamp; confirm receipt only after the complete save succeeds.
3. Retrieve by ID after restart, showing the saved evidence and image if present.
   Show history using the ordering and membership in Alternate / edge flows, including
   same-day ties and later-submitted backdated reports. An empty history is explicit
   and does not imply absence of disease.
4. Distinguish prior fictional confirmed findings from submitted observations; never
   present an observation or inference as a confirmation. Intake creates no finding.
5. For dataset-backed scenarios, make source attribution and synthetic context
   available. Keep current-image disease/severity scoring labels and label-bearing
   source names out of displayed attachment names, observations and diagnosis inputs.
   Identify reused images in provenance. Normal intake history may show prior
   confirmed findings even when an image repeats. For a future diagnosis evaluation,
   exclude history entries that reveal the current image’s answer, including findings
   tied to the same image or related images such as crops of one parent; record each
   exclusion. Keep scoring labels and source identifiers in separate restricted
   provenance/evaluation metadata, per the [open-data plan](../reference/OPEN-DATA.md).
6. Invalid required input, farm/field pairing or attachment yields an actionable error
   and leaves no partial report or image; a storage failure does not claim success and
   leaves no retrievable partial report. An unknown ID yields a not-found result.

## Security / trust-boundary notes

Treat uploads and text as untrusted: validate actual image content, escape rendered
text, generate neutral storage/display names, limit upload size and prevent path
traversal. Local synthetic data only; do not expose the unauthenticated prototype
publicly. Keep provenance and evaluation metadata out of diagnosis inputs.

## Validation plan

### Tests
- Unit: pairing, date and description validation, attachment boundaries and history
  ordering, including same-day ties and backdated submissions (criteria 2, 3, 6).
- Integration: seed coverage, atomic save/retrieve after restart, field isolation,
  evidence types, image validation, unknown ID and storage failure (criteria 1–6).
  For dataset-backed fixtures, check attribution, neutral names and repeat/related
  image leakage boundaries; future diagnosis-input exclusions are deferred to the
  evaluation slice (criterion 5).
- E2E: demonstrate selection, text-only and image submission, retrieval, confirmed
  history, empty history and errors; inspect synthetic labels and attribution
  where images are sourced (criteria 1–6).

### Evidence
Record executed application checks during VALIDATE. No application checks have run.

## Open questions / assumptions

- Working defaults accepted by Ayla for prototype implementation: one
  nonblank description, a nonfuture local calendar date, and at most one JPEG/PNG
  up to 10 MiB. These keep entry simple and storage bounded. The local date is the
  application host’s date; timezone and clock changes affect future-date validation.
- The minimum seed and chronology above provide isolation, confirmed-history and
  empty-history examples with little setup. Observation date best represents when an
  event occurred; receipt time and ID give deterministic same-day order. Same-day
  ordering does not claim the events actually occurred in that order.
- No material intake policy question remains for DESIGN under these working defaults;
  Ayla reviewed the design and selected DEVELOP. Local persistence and upload handling belong to
  DESIGN. No images have been downloaded or scenarios imported.
- Offline capture is a paper assumption deferred beyond this slice; disclose the gap.

## Notes for implementation

Use existing domain/application/interface/infrastructure layers. Design selection,
report persistence and history retrieval; decide persistence in DESIGN and record
consequential decisions per the working agreement. Intake does not require a model
provider, routing policy or new review workflow.

## Design

Ayla reviewed and accepted this design for prototype development; the acceptance
criteria and working defaults govern this slice. The existing layer
structure is sufficient with the following small additions:

- **Domain:** fictional farms and their fields; reports retain submitted observations
  and optional original image evidence. A prior fictional confirmed finding is a
  distinct kind of history evidence, never created by intake.
- **Application:** an intake service validates the farm/field relationship and the
  specified inputs, then requests one complete save; a retrieval service gets a
  report and computes its same-field history under the specified ordering. These
  services own the use-case rules and depend on a modest repository boundary, not
  on HTTP or a database. The repository provides farm/field lookup, atomic report
  save, report lookup and field history; storage-specific representations stay behind it.
- **Interface:** a local form offers farm and dependent field selection, date,
  description and optional image. Validation errors identify the relevant input; after
  successful save it leads to synthetic-labelled report detail. Detail is addressable
  by report ID and shows the original evidence, distinct prior findings and ordered
  history or its explicit empty state; unknown IDs show not found. Render text safely
  and use neutral attachment names. FastAPI is the existing development profile;
  server-rendered HTML is a proposed simple journey, without choosing a template engine.
- **Infrastructure:** a local SQLite adapter owns durable fictional scenario and report
  records and stores an optional bounded original image with its report in one
  transaction, as accepted in [ADR-001](../adr/ADR-001-local-report-persistence.md).
  Image content must be decoded/verified as actual JPEG or PNG, not accepted solely
  from a filename or MIME type. Invalid input creates nothing; a failed transaction
  leaves no retrievable partial report or image and produces no confirmation.

Synthetic seed records use stable scenario-owned identities so initialization is
idempotent across restarts and does not overwrite user submissions or duplicate seed
history. Seed identities are not dataset identifiers. No raw dataset images are
currently present; add source-backed images only after selection and provenance work
in the [open-data plan](../reference/OPEN-DATA.md). Keep attribution and synthetic
context available separately from restricted original identifiers, paths and scoring
labels; neither label-bearing names nor current answers enter displayed observations,
attachment names or future diagnosis inputs. Track image reuse and relatedness in
provenance; future evaluation must record exclusions described in criterion 5.

SQLite keeps report and image atomic with few moving parts, at the cost of database
growth and a local writable file; it is a local demo choice, not a distributed store
or backup strategy. The 10 MiB limit bounds each image, not total storage. The local
host clock and deterministic same-day tie breaks retain the limitations stated above.
Minimal additions for DEVELOP are a multipart form parser and an image
verification library if needed (for example python-multipart and Pillow); neither
is installed yet, and no template engine, ORM or migration tool is selected.

Acceptance mapping: seed and idempotence cover **1**; form, validation and atomic
save cover **2 and 6**; durable lookup and history cover **3**; typed evidence
covers **4**; separated provenance and deferred evaluation exclusions cover **5**.
With DEVELOP selected, implement the smallest journey
using the existing TDD workflow. Exercise the spec's unit, integration and E2E plan,
especially image content/size boundaries, transaction failure, restart, seed reruns,
history ties/backdating and separation of findings and source labels. No application
behavior or acceptance checks are claimed in DESIGN.
