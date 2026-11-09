# Farm history and technical case data model

**Status: working DESIGN draft.** This conceptual/logical model supports the selected
prototype direction; it is not a schema, an approved routing policy or a dataset
specification. [UC-001](../specs/UC-001-REPORT-INTAKE.md) owns intake requirements;
the [routing worksheet](../reference/DMN-RULE-WORKSHEET.md) owns the selected
routing direction and its open policy questions. Group paper and model alignment is
pending. This draft does not change the active lifecycle phase.

The prototype focuses one primary farmer’s view and one technician’s view on the
primary farm. Neighbouring farms, fields, reports and cases remain contextual data;
this is not a one-farm dataset. Multiaccount navigation and administration screens
are outside the current scope.

Farm is the history hub: one chronological view assembles reports, cases and typed
farm-history events, with optional filters. Original reports, photos and shared facts
remain in their source records; events do not duplicate them. A technical case is an
operational record created through technician involvement in P1, not a new C/F matrix business
case type. Communications is a responsibility for personalising and relaying established
advice; it does not assert a new Cooxupé department or make agronomic judgments.

## Source and decision trace

| Authority or status | What it establishes here |
| --- | --- |
| [Source map](../reference/README.md) and [group DOCX](<../../../Sharing is caring/The Case of the Brazilian Coffee Cooperative Cooxup├й.docx>) | The group paper owns the solution baseline and C/F matrix. Its P1 proposal uses optional GPS, photo/voice/text and a three-action DMN; it adds no department or C/F case type. The published case grounds organisation and AS-IS, not the proposed solution; its full chapter was unavailable and was not read for this draft. |
| Owner selections, including focused views and neighbouring context: [UC-001](../specs/UC-001-REPORT-INTAKE.md), [routing worksheet](../reference/DMN-RULE-WORKSHEET.md) | Focused farmer and technician views with neighbouring context; one proposed typed history-event table; camera-first intake with required location context and estimate; responsibility routing; independent reports and technician involvement for cases. These refinements differ from the group draft and need group alignment. |
| Agent proposals below | Field-scoped cases, link cardinalities, event type validation details, structure of relations, spatial representation and handoff. These are design recommendations, not owner or group decisions. The older [prototype concept](<../../../planning/PROTOTYPE-CONCEPT.md>) is supporting context, not authority over newer choices. |

The group paper also describes agronomic references, weather-zone event records,
optional pH and voice inputs. These are deferred integration/input extensions here,
not claims that they were absent from the solution baseline. Weather integration is
not required for the selected prototype routing direction.

## Entities and relationships

IDs below are conceptual keys, not prescribed columns. `0..*` means zero or more;
attributes marked optional may be unknown. The diagram shows the recommended case
cardinalities; geographic context and relation judgments are separate from membership.
The single typed event table is a proposal, not an implemented schema.

| Entity | Key, important attributes and cardinality |
| --- | --- |
| Farmer / account | `farmer_id`, `account_id`, account-to-farm association. A target account identifies a farmer and farm; exact multiplicity and real authentication/authorization are open. A demo identity is explicitly simulated. |
| Farm | `farm_id`, fictional identity and optional labelled boundary. One farm has zero or more fields, reports and technician assignments. |
| Field | `field_id`, `farm_id`, optional versioned boundary, boundary source and synthetic flag. A field belongs to one farm; a report need not be assigned to a field when a GPS point cannot be grouped. |
| Technician assignment | `assignment_id`, technician, farm, effective period. Each assignment links one technician and one farm; both can have many assignments. Assigned farms are the minimum scope; access and cross-farm sharing remain open. |
| Report | `report_id`, farm, farmer/account reference, observation time and source, separate receipt time, optional narrative, estimate and location context. One farm has many reports; each report is independently retained. One original photo is required for new target submissions; legacy reports may lack it. |
| Photo evidence | `evidence_id`, report, original content/reference, media type and provenance. One report has one photo in the current target; retained legacy reports may have none. Dataset reuse links to source asset identity without changing the original evidence. |
| Estimate | Report-owned value, kind (count or percentage), unit, farmer-reported provenance and any area cue. New reports have one; legacy reports may have none. Count is plants; percentage is affected plants among all plants in the observed area, not land area or measured incidence. |
| Location context | Report-owned device point with accuracy, source and capture time, **or** farmer-selected field and retained boundary with field-level precision and source. Each new report has one usable context; a point may yield zero or one derived field under a rule still to be agreed. No point is implied by a boundary. |
| Assessment | `assessment_id`, report, inference, uncertainty, evidence references, model/prompt version and time. Based on the current report evidence and optional versioned [event weather](../reference/EVENT-WEATHER.md), with model inputs separated under the [assessment boundary](../reference/DMN-RULE-WORKSHEET.md#assessment-and-routing-boundary). A report can have zero or more assessments; none is itself a confirmed finding. |
| Routing decision | `decision_id`, report, route, reason, rule/version, inputs and time. A report can have zero or more decisions over time; the route assigns responsibility, not relevance or a diagnosis. |
| Technical case | `case_id`, farm, optional field scope, status, technician involvement and dates. Recommended: one primary farm, optionally one field, with zero or more cases per farm/field. A case starts with technician involvement and at least one report; case scope and cardinality require agreement. |
| Case membership | `membership_id`, case, report, technician, time and reason. Recommended: a case has one or more reports; a report has zero or more memberships over time. Membership is a deliberate technician judgment, not a routing or proximity result. Whether simultaneous membership in multiple cases is allowed is open. |
| Geographic context | Same-farm and neighbouring farm/field/report/case candidates are derived from available geometry and other source records as needed. Persisting every adjacency or proximity link is not required; candidates do not establish relevance or membership. Unmatched records remain visible. |
| Confirmed/rejected relation | `relation_id`, two reports or cases, relation kind, confirmed/rejected judgment, technician, reason and time. These durable human judgments exist independently of automatic matches; a rejected relation does not make records generally irrelevant. |
| Farm-history event (proposed typed table) | `event_id`, type, farm, optional field/report/case links, occurred and recorded times, actor/source and type-specific details. One farm has zero or more events. Types have distinct meanings and validation: **finding** requires confirmation provenance for a confirmed finding; unknown provenance remains uncertain, and AI inference alone is not confirmation. **Guidance** records established or technician-prepared advice; **treatment** records an action and source; **communication** records personal relay and delivery status; **outcome** records what is known about resolution. Delivery does not establish resolution. Link to original evidence and shared facts instead of copying them. Purchase-history integration is outside scope. |
| Source asset / evaluation metadata | `asset_id`, dataset/version, original sample and parent IDs, attribution, licence status, transformations, labels and reuse links; synthetic scenario source and provenance are separately identified. Restricted labels and evaluation metadata are separated from operational report content and inference inputs. |

```mermaid
erDiagram
    FARM ||--o{ FIELD : contains
    FARM ||--o{ REPORT : history
    FARM ||--o{ TECHNICIAN_ASSIGNMENT : assigned
    FARM ||--o{ TECHNICAL_CASE : scopes
    REPORT ||--o| PHOTO_EVIDENCE : has
    REPORT ||--o| ESTIMATE : has
    REPORT ||--o| LOCATION_CONTEXT : has
    FIELD o|--o{ LOCATION_CONTEXT : selected_or_derived
    REPORT ||--o{ ASSESSMENT : assessed
    REPORT ||--o{ ROUTING_DECISION : routed
    TECHNICAL_CASE ||--|{ CASE_MEMBERSHIP : includes
    REPORT ||--o{ CASE_MEMBERSHIP : joins
    FARM ||--o{ FARM_HISTORY_EVENT : history
    REPORT o|--o{ FARM_HISTORY_EVENT : relates
    TECHNICAL_CASE o|--o{ FARM_HISTORY_EVENT : relates
    SOURCE_ASSET o|--o{ PHOTO_EVIDENCE : provenance
```

Diagram optionality permits legacy records; new intake has stricter requirements.
Derived context and durable human relation judgments can connect different kinds of
record and are described in the table rather than implying a single foreign-key target
in the diagram. Farmer/account and staff identity relationships await access design.

## Invariants and interpretation

- Target intake derives farmer and farm from the signed-in account; the prototype may
  use a labelled simulated identity. GPS permission is neither login nor workflow gate.
  Automatically record observation time for camera capture and separately record UTC
  receipt. Label manually supplied or synthetic prototype stand-ins and their sources;
  an upload represents a new photo, not proof of capture time or device GPS.
- Prefer usable device GPS with point, reported accuracy, source and capture time.
  Otherwise select a known mapped field of the account's farm and retain its boundary
  and source. Do not replace the field with a fictitious observed point or centroid.
  The bounded demo GPS rule is in UC-001; boundary availability and the target path
  when neither source is available remain open.
- Each new report has an approximate affected-plant count or percentage with an
  understandable observed-area basis. An optional area cue can help; no extra written
  narrative is mandatory. Do not invent area, acreage, a plant denominator, measured
  incidence or a conversion between count and percentage. Legacy missing values stay
  unavailable.
- A report is not a case, diagnosis or confirmed finding. Technician involvement creates
  or joins a suitable case; do not create a duplicate merely because a later report
  escalates. No rule requires every report to be consumed by a case or every routine
  report to be reviewed. A technician judges case membership and relevance; automatic
  non-matching, a DMN route or a rejected relation does not establish irrelevance.
- Assemble one chronological farm history from reports, cases and events, with optional
  filters; do not copy reports, original photos or shared facts into events. Define
  ordering for backdated and simultaneous records before implementation.
- Keep all available farm context visible to the appropriate technician, subject to
  access rules still to be agreed. Nearby or same-farm context is a candidate, not
  proof of relevance. Separate observations, assessments and confirmed findings;
  retain the provenance of decisions, guidance, treatment, communication and outcomes.
  Severe actions require human approval; a route alone does not authorise them.
- Preserve data source and synthetic scenario context separately from operational
  records. A reused photo or related crop is not independent evidence. Keep current
  scoring labels and label-bearing identifiers out of inference inputs. The current
  photo goes to the image model; its scores, farmer note and optional versioned
  event weather may feed a second model. Connected history is reserved for
  deterministic routing and human review. Record duplicate/related-image exclusions
  in evaluation; ordinary prior findings remain visible in history. See the
  [open-data plan](../reference/OPEN-DATA.md).

## Spatial framework for later dataset design

Future fictional scenarios may use plausible Brazilian coordinates and labelled
fictional owners, histories and boundaries. Contrast elongated farms with many
external and few internal field neighbours with compact farms having many internal
and few external neighbours; also include irregular boundaries, gaps and corner
contacts. These are scenario goals, not claims about real farms or commitments to
counts, volumes or generation.

Derive field relationships from boundary geometry: internal adjacency relates fields
of the same farm; external adjacency relates fields of different farms. Proximity is a
separate distance relationship and does not imply touching. Define coordinate system,
boundary versions, distance/radius and whether point-only contact counts as adjacency
before use. Query geometry to derive adjacency and proximity when needed; storing all
such links is not required. Durable technician-confirmed or rejected relations remain independent
of automatic matches. Geometry can suggest context; it cannot determine agronomic
relevance or case membership. Cross-farm access and privacy remain open.

## Agreed direction, recommendations and next scope

| Topic | Selected direction / recommendation | Remaining decision |
| --- | --- | --- |
| Cases | Technician involvement only; link to an appropriate existing case when warranted. Recommend primary farm and optional field scope, with explicit report membership and related cases across farms or fields. | Case scope, multiple memberships, closure/reopening and cross-farm relation/access rules. |
| History | One chronological view combines reports, cases and proposed typed events; optional filters, unmatched context and original records remain available. | Ordering ties and backdated records, nearby criteria, relevance workflow and permissions. |
| Prototype focus | One primary farmer view and one technician view focus on the primary farm, with neighbouring farm/field/report/case context. No multiaccount navigation or admin screens now. | Exact synthetic counts remain undecided; no dataset generation now. |
| Intake | Camera-first, location and estimate required for new reports; upload is a prototype shortcut. | Boundary availability and target no-location behavior; UC-001 records implemented demo defaults. |
| Routing | DMN selects responsibility with reason; communications personalises and relays established guidance. | Routing definitions, severe approval, actor/access boundaries and reconciliation with group DOCX/BPMN/DMN. |
| Data/evaluation | Label synthetic data and protect scoring metadata. | Source suitability/licences, evaluation exclusion policy and eventual scenario design; no dataset generation now. |

**Minimum now:** use this model to reconcile intake and the independent routing
specification, identify the report/farm/history and location boundaries, and preserve
existing data. The typed history table, assessment, routing, cases, spatial analysis
and evaluation are proposals or logical future interfaces, not implementation
commitments for UC-001. Real account
authentication, transcription, offline capture and external messages are not implemented.

**Implemented demo and preservation:** [UC-001](../specs/UC-001-REPORT-INTAKE.md#design--revised-prototype)
records the bounded intake, farm-wide report history and legacy-preserving migration.
Cases, events, nearby context and routing remain unimplemented. ADR-001 selects local
SQLite, not the wider conceptual model. Preserve legacy evidence and missing values
as described in UC-001 when planning future changes.

**Bounded handoff:** owners resolve the intake and case choices above and align the
paper/models; specify routing separately as the worksheet requests. Later DESIGN can
map the agreed routing and guidance slice to the existing intake
boundary and propose an ADR only if a consequential cross-use-case decision is ready
for review. Validate with acceptance
examples for location fallback, estimate scope, legacy preservation, farm history,
independent reports, case linking, typed-event validation, durable relation judgments,
neighbour context and evidence separation. These are planned checks,
not evidence of implementation or approval. No ADR is proposed for unresolved options.
