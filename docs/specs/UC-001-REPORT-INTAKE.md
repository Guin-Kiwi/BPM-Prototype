# UC-001-REPORT-INTAKE

## Goal

A logged-in farmer records an observation primarily by taking a photo, with optional
supporting text and a required approximate affected-plant estimate for the observed
area. The report retains when and where the observation was made and is available
in the farm's history with useful nearby context.

## Business value

Make reporting quick for farmers while preserving attributable evidence and context
for later technician work, without treating a report as a confirmed finding or case.

## Scope

### In scope

- Camera-first report intake, optional text, account-derived farmer and farm, automatic
  observation time and preferred GPS, with mapped-field fallback when GPS is unusable.
- A required structured farmer estimate of affected plants as a count or percentage
  for the observed area; optional narrative remains separate.
- Durable original evidence, distinct capture and receipt times, report retrieval,
  farm history and geographic grouping where possible; location remains available
  for nearby context without requiring the farmer to name a field.
- Synthetic demo scenarios and attributable dataset images, with evaluation safeguards.

### Out of scope

- Implementing authentication, offline capture/sync or voice transcription. The target
  assumes a logged-in farmer; transcription is a future option, not implemented.
- Technician workflow, case creation, routing, relevance judgments, AI diagnosis,
  treatment guidance, messages and orders. A report becomes a case only through
  technician involvement; intake itself creates neither a case nor a finding.
- Measured incidence, aggregation policy and real farm history for the local demo.

## Actors

Primary: farmer recording an observation; presenter demonstrating synthetic reports.
Secondary: technician later involved with reports; evaluator preparing attributable
samples and synthetic history.

## Preconditions

Target: a valid authenticated account identifies the farmer and associated farm.
Location context is required for submission: usable GPS is preferred, with selection
of a known mapped field belonging to that farm as fallback. GPS permission is not a
login or farmer-workflow prerequisite. Authentication and account management are
dependencies outside this slice; actual field-boundary availability is for DESIGN.

Current demo: local application and writable storage, fictional data, no provider
credentials; it uses browser geolocation but has no authentication or mapped-boundary
fallback.
Its fictional identity is a simulation, not login or security.

## Trigger

A farmer opens report entry to record an observation.

## Main flow

1. Obtain farmer and farm from the signed-in account. Do not ask the farmer to name
   a field. Open the camera and ask the farmer to take a new photo.
2. Capture observation time and GPS automatically when the photo is taken; retain the
   original photo and any optional text. Use GPS when available and sufficiently
   accurate. Otherwise, including when permission is denied, ask the farmer to select
   a known field belonging to their farm on a map. Location context is required before
   submission; the farmer need not name the selected field.
3. Ask “About how many plants are affected?” Let the farmer choose an approximate
   count of plants or a percentage of plants in the area being observed. A brief area
   cue such as “the rows near the shed” is a recommended way to clarify scope, not a
   mandatory written description. No survey is required; optional narrative is separate.
4. Validate and save the complete report with a unique ID and a separate UTC receipt
   timestamp. Confirm only after the save succeeds.
5. Retrieve the report by ID and from the farm's history, including after restart.
   Retain the recorded point or field boundary for nearby context and derive geographic
   grouping when possible;
   clearly distinguish prior observations from confirmed findings. No intake step
   creates a case or makes a relevance or routing judgment.

## Alternate / edge flows

- **Proposed demo identity:** use one clearly labelled fixed fictional farmer/account
  and farm supplied by demo configuration. It simulates an already signed-in account;
  it provides no login, authentication or authorization. Do not infer identity or farm
  from GPS. Keep existing fictional data and history available through an explicit
  mapping to that farm; mapping and migration need design.
- **Prototype shortcut:** use a photo upload to represent a newly captured photo,
  solely to reduce implementation complexity. Recommend clearly labelled synthetic or
  manually supplied capture-time and location stand-ins, with their source recorded.
  Upload/receipt time is not the original photo capture time; do not claim a simulated
  value was automatically captured or obtained from GPS. Retain the uploaded evidence.
- **Location fallback:** when GPS is unavailable or insufficiently accurate, offer
  mapped-field selection for the account's farm. Preserve the farmer-selected field ID
  and boundary as the location context, with field-level precision and source; do not
  invent a point or centroid as the observed location. For usable GPS, preserve the
  device point and reported accuracy with device source. Prototype boundaries may be
  synthetic and must be labelled as such. DESIGN must define usable GPS and boundary
  availability. If neither usable GPS nor a selectable known field is available,
  recommend explaining and retrying without submission; exact handling remains open.
  This is not an approved exception or a claim of offline or durable draft support.
- Keep farm history even when a report cannot be assigned a geographic group. Grouping
  must not fabricate a field, and unavailable nearby context must be explicit. Existing
  farm-wide demo history and its ordering are implemented below; wider nearby history
  membership and proximity rules need a decision.
- The estimate describes affected plants within the area the farmer is estimating, not the
  proportion of land affected. A percentage is affected plants divided by all plants
  in that area, expressed as 0–100%; the denominator is conceptual and need not be
  counted. An approximate count is in plants, not plants per acre. Do not label the
  percentage “per acre”: an acre is an area unit, not a plant denominator. A GPS point
  supplies neither the area extent/acreage nor the number of plants. Neither estimate
  is systematic measured incidence or a confirmed finding. A selected field may be
  offered as an understandable area cue; it supplies neither a plant denominator nor
  proof that the estimate covers the whole field.
- Preserve the entered estimate, its kind, units, any supplied area context and
  farmer-reported provenance on retrieval; do not convert between count and percentage
  or infer acreage, a denominator or precision. Existing reports lacking an estimate retain an explicit
  unavailable value; do not invent one or alter their original evidence.
- Repeated submissions remain distinct; deduplication is deferred. Reused dataset
  images are identified in provenance and are not independent observations or incidence.

## Errors / failure cases

- Camera cancellation or capture failure: explain and allow retry; do not save without
  a photo. In the prototype, a failed upload can be retried.
- Unavailable, denied or insufficiently accurate GPS: offer selection of a known field
  for the account's farm. If neither usable GPS nor a selectable known field is available,
  the proposed behavior is explanation and retry without submission; DESIGN must resolve
  the exact path. No arbitrary point is invented.
- Missing or invalid estimate, invalid time, attachment or location: explain how to
  correct it; do not partially save. The farmer must supply an estimate, even when it
  is approximate; there is no “unable to estimate” submission alternative.
  Unknown report ID yields not found. Storage failure must not claim successful receipt
  or leave a retrievable partial report. No offline queuing is claimed.

## Acceptance criteria

Sources: the intake requirements below govern the farmer journey; the
[source map](../reference/README.md) identifies the paper as business-scope authority
and the assignment as deliverables authority. Proposed demo defaults and unresolved
choices below are not approved policy. The selected intake uses the photo-first
framing and requires an approximate affected-plant count or percentage. The currently
working demo and its evidence are described in [TASKS](../TASKS.md).

1. Given a signed-in farmer, obtain identity and farm from the account, open the
   camera and ask for a new photo. Text is optional, no field name is required, and
   intake does not offer or claim transcription. GPS permission is not a login or
   farmer-workflow prerequisite.
2. A successful report preserves the original photo and optional submitted text, a
   unique ID, observation time and separately recorded UTC receipt time. Capture and
   receipt must not be conflated. A report requires location context: use a usable
   device GPS point with its reported accuracy and source; when unavailable or
   insufficiently accurate, allow selection on a map of a known field for the account's
   farm, retaining its ID, boundary and farmer-selected source with field-level
   precision. Do not represent a boundary or its centroid as an observed GPS point.
   Define GPS usability and actual boundary availability in DESIGN.
3. The farmer can retrieve a saved report after restart and access farm history.
   Location is retained for nearby context; geographic grouping is derived only when
   possible; the farmer need not enter a field name. Empty history does not imply
   absence of disease. Observations and prior confirmed findings remain distinct.
4. Intake creates neither a confirmed finding nor a case, routing decision or relevance
   judgment. Only technician involvement can turn a report into a case; its process is
   outside this use case.
5. Demo scenarios are labelled synthetic. Dataset-backed scenarios provide attribution
   and context; original text, image and metadata are preserved. Keep current-image
   disease/severity scoring labels and label-bearing source names out of displayed
   attachment names, observations and diagnosis inputs. Separate restricted provenance
   and evaluation metadata as in the [open-data plan](../reference/OPEN-DATA.md).
   Record reuse and relatedness. Future image assessment receives only the photo;
   a proposed second model may combine its scores with the note and optional
   [event weather](../reference/EVENT-WEATHER.md). Connected history feeds routing and human review separately,
   under the [assessment boundary](../reference/DMN-RULE-WORKSHEET.md#assessment-and-routing-boundary).
   Record exclusions for duplicate/related evaluation images. Ordinary history may show
   prior findings for repeated images without presenting them as new confirmation.
6. Invalid or incomplete required evidence, invalid location/time, corrupt, unsupported
   or oversized image, and storage failure yield actionable errors without a partial
   report or false confirmation; unknown IDs yield not found. The existing demo's JPEG/
   PNG and 10 MiB limit remain the accepted bounds for the revised demo.
7. The future bounded demo uses an upload to represent a new photo and a clearly
   simulated fixed fictional identity. Label synthetic or manually supplied capture-time
   and location stand-ins and their source; never present upload time as actual capture
   time or a stand-in as GPS. Synthetic mapped field boundaries are explicitly labelled.
   The current demo obtains browser geolocation on request; mapped-field fallback is
   unavailable.
8. A new report requires a structured farmer estimate: either an approximate count
   of affected plants (unit: plants) or an approximate percentage of affected plants
   among all plants in the area being observed (unit: percent). Recommend a nonnegative
   whole-number count or a percentage from 0 to 100 inclusive; reject missing, nonnumeric
   or out-of-range values with an actionable error. No submission is allowed without
   an estimate. Save and retrieve the value, kind, unit and farmer-reported estimate
   provenance, and any area context supplied, without presenting them as measured
   incidence or a confirmed finding. Do not derive a denominator, acreage, area coverage
   or converted estimate from the GPS point. Historical reports without this input
   remain available and show it as unavailable.

## Security / trust-boundary notes

Treat image, metadata, location and text as untrusted: validate actual image content,
escape rendered text, generate neutral names, limit upload size and prevent path
traversal. Location and account association are sensitive; a fixed demo identity is not
security. Use synthetic data locally and do not expose the unauthenticated demo publicly.
Authorization and account-to-farm access are dependencies requiring design before real
data; do not trust client-supplied identity as proof. Keep restricted provenance and
scoring metadata out of diagnosis inputs.

## Validation plan

### Tests

- Unit: count/percentage selection, bounds, mandatory estimate and optional narrative;
  GPS usability and source/accuracy, mapped-field ownership and boundary handling,
  image content and size boundaries, grouping when available and no fabricated group
  (criteria 1–3, 6–8). Define history membership and ordering before testing them.
- Integration: account/farm association at its boundary, atomic save and restart
  retrieval, original evidence and distinct times, farm isolation, no case/finding,
  failure paths, estimate provenance and legacy missing estimates, and synthetic labels
  (criteria 1–4, 6–8). Use a clearly labelled fake
  account for demo tests, not a claim of authentication.
- E2E/manual: exercise camera-first target and labelled upload demo; usable GPS,
  denied/unavailable or inaccurate GPS with mapped-field selection, and neither source
  available; both estimate choices, optional narrative, photo failure, farm history, empty
  history and prior finding. Verify location source, precision, farm membership and
  device/map availability; record gaps (criteria 1–4, 6–8).
- Dataset fixtures: attribution, neutral names, reuse and related-image leakage;
  diagnosis-input exclusions belong to the future evaluation slice (criterion 5).

### Evidence

Existing automated and live HTTP evidence and manual review limits are recorded in
[TASKS](../TASKS.md); see the current [intake implementation](../../src/app/application/intake.py)
and [integration tests](../../tests/integration/test_intake.py). Implementation and
automated check evidence are recorded below. Full target acceptance and a visual/manual journey remain unverified.

## Open questions / assumptions

- The prototype uses one primary farmer view and one technician view focused on the
  primary farm, with neighbouring farm, field, report and case context. Exact synthetic
  counts and generation remain undecided. The demo uses the fixed simulated farm-1
  identity and preserves both farms and their original history associations. Real
  authentication, authorization and account/farm relationships need separate design.
- The bounded demo defines GPS usability below; future work must establish boundary
  availability, how farm
  ownership and field boundaries are verified and retained, and behavior if neither
  location source is available. Retry without submission is a working recommendation,
  not an approved exception; no offline draft persistence is implied.
- The demo uses the observed-area prompt and optional area cue; assess usability in
  manual review. Extra written narrative is not required. Do not require
  field naming, acreage or a survey.
- The demo history ordering is defined below. Decide wider event-history ordering,
  geographic grouping source and behavior when unavailable, and nearby radius,
  relevance and privacy boundaries with appropriate owners. Relevance policy is separate
  work; do not silently equate nearby with relevant or invent grouping boundaries.
- Reconcile the changed journey with the group paper/models. The accepted demo image
  bound remains one JPEG/PNG up to 10 MiB.

## Notes for implementation

DESIGN should assess impacts on the existing domain, intake/retrieval services, local
form, location sources, repository and SQLite data, including the structured estimate
and migration and preservation of prior reports, images, findings and synthetic
provenance. Keep synthetic seed initialization idempotent without overwriting reports.
[ADR-001](../adr/ADR-001-local-report-persistence.md)
remains the accepted local persistence decision; do not assume it resolves account,
location or migration design. Identify any consequential cross-use-case decision for
review under the [working agreement](../WORKING-AGREEMENT.md). Further implementation
requires its own selected and reviewed work.

## Design — revised prototype

This is a technical working design, not group approval of the changed journey. The
[data model](../design/DATA-MODEL.md) describes the intended wider history; ADR-001
continues to govern SQLite. No new ADR is needed for these reversible intake choices.

**Working defaults.** Bind the simulated farmer to the existing `farm-1` (Sunrise
Farm); label the identity simulated. Preserve both farms and every report's original
farm and field IDs, including farm-2 history; do not remap or relabel existing user
reports as seed data. The farm view shows farm-1 reports only. A field ID without
geometry is historical association, not location. The observed-area prompt itself
provides the estimate scope; an optional area cue is stored separately from narrative.

A device fix is usable when latitude and longitude are finite and in range, accuracy
is finite and between 0 and 100 metres inclusive, and the fix timestamp is no more
than five minutes old and not in the future when submitted. These are prototype
thresholds, not agronomic precision claims. Preserve the device fix time and accuracy;
never relabel manually entered coordinates as device GPS. With the upload shortcut,
record a clearly labelled simulated observation time when the farmer selects the
photo, without requiring date entry. It represents the new-photo scenario, not verified
photo capture metadata. Record receipt independently in UTC.
Reject invalid or future observation times. A device fix obtained for an upload is
location at fix time, not proof of the photo's capture location.

**Components and representation.** Extend the report domain and intake service with
validation independent of HTTP and SQLite. The form obtains browser geolocation,
asks for photo, estimate and optional area cue/narrative, records the simulated
observation time automatically,
and shows fix status and the simulated identity. The service binds the configured
farm server-side, validates the inputs, and saves atomically through the existing
repository boundary. Extend retrieval and farm-history queries; SQLite remains the
adapter. Keep original JPEG/PNG bytes and accepted size limits under ADR-001.

Store one report-owned estimate: kind `count` or `percentage`, numeric value, unit
`plants` or `percent`, source `farmer_reported`, and optional area cue. Count is a
nonnegative integer; percentage is 0–100 inclusive. Store observation timestamp with
source and precision, and separate UTC receipt timestamp. Record photo source as
`uploaded` and preserve any actually known provenance without inventing it. New
reports require these values; missing legacy estimate, capture time and provenance
remain explicitly unavailable, with the original date retained at date precision.

Store location as a discriminated report-owned record: `device` has WGS84 latitude,
longitude, accuracy in metres and fix timestamp; `selected_field` has the farm-owned
field ID and a snapshot of its polygon or multipolygon boundary, coordinate reference,
version/source and synthetic flag, with farmer-selected source and field precision.
A legacy field association is neither kind. Retain no fabricated point for a boundary.
A boundary-provider interface returns only known, validated, versioned geometries
for the configured farm; selection must be checked server-side and the selected
geometry snapshotted with the report. A GPS point need not resolve to a field. No
spatial grouping is inferred without geometry and an agreed rule.

**Journey and split.** For the next slice, a usable device fix permits submission;
missing, denied, stale or inaccurate GPS shows an actionable explanation and retry.
The map fallback is explicitly unavailable until real or explicitly synthetic known
field boundaries, provenance and a usable map presentation are supplied. The current
runtime fields contain only ID, farm and name: no boundaries are available. Do not
create boundary data as part of this work. Once that dependency is provided, implement
map selection through the same interface and validate ownership and retained geometry.
If neither location path works, keep the user on the form, explain and allow retry;
do not submit or claim a durable draft. Invalid photo, estimate, time or location and
storage failure must likewise leave no partial report or success confirmation.

**History and migration.** Show all reports belonging to the primary farm, including
ungrouped and legacy reports, newest observation day first; within a day sort known
observation timestamps newest first, then date-only records, with receipt time and ID
as descending deterministic ties. Show date-only precision and unavailable values
explicitly. Display legacy `finding` as a legacy finding with confirmation provenance
unknown, never as a newly confirmed finding. Indicate nearby context/grouping is
unavailable when no supported geometry/rules exist; do not imply no nearby reports.
A report-only history is the smallest useful first slice. The proposed typed event
model is the direction for a later event-producing slice: no new event table is needed
now, and cases or copied report events must not be invented to populate it.

Before migration, make a consistent SQLite backup using the SQLite backup API, verify
that it opens and passes integrity checks, and stop with an actionable error if backup
fails. Use a versioned, transactional migration, rebuilding the reports table if needed
to relax old required columns while preserving originals; use explicit column lists and
idempotent seed initialization. On failure roll back and retain the verified backup;
never delete or reset the database. Test on a copy containing saved non-seed reports:
compare IDs, farm/field associations, original dates, text, image bytes and media types,
receipt times and findings before/after; check row counts, foreign keys, integrity,
restart, repeated initialization and backup restoration. Legacy missing estimates,
location and provenance stay unavailable; never fabricate historical coordinates,
estimates, timestamps or confirmation. New validation must not prevent legacy retrieval.

**Acceptance mapping / next DEVELOP slice.** Criteria 1, 2, 6–8: simulated farm,
upload and simulated observation time, device GPS, required estimate, validation and atomic save;
map fallback remains blocked by the boundary dependency. Criteria 3–4: restart-safe
retrieval and farm-wide report history, explicit unavailable context, no finding or case
creation. Criterion 5: label the simulation and preserve known provenance; dataset
import and evaluation safeguards requiring dataset assets belong to later work. Tests
must cover both estimate kinds and invalid inputs, GPS thresholds and failure/retry,
optional text, image bounds, source/time distinctions, farm isolation, history ordering,
legacy preservation and migration rollback/restore. Manual browser verification covers
permission and device availability; lack of a suitable device is recorded as a gap.

In: report/domain and repository changes, browser GPS path, simulated identity,
upload form, farm history, migration and focused tests. Out: map UI until the stated
boundary dependency is met, generated records/data, authentication, technician UI,
cases/events, nearby analysis, AI, routing, voice, offline and weather. The full
revised UC remains incomplete until map fallback and remaining target/evaluation
criteria are implemented and validated. Group reconciliation of the changed business
journey with the paper/models remains pending; it is distinct from these technical
prototype defaults and does not constitute approval.


**DEVELOP evidence.** The bounded GPS intake and report-only farm history are
implemented with temporary-database migration tests, including verified backup,
restore and injected rollback. The original runtime database was not migrated during
development. Browser permission and device behavior have not been manually tested.
Mapped-field fallback remains unavailable, so the full revised UC remains incomplete;
group alignment and human acceptance remain pending.
