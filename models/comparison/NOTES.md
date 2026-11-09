# P1 comparison definitions — review draft

These are two new semantic definitions for the same P1 boundary: a farmer requests support, receives guidance, and Cooxupé records what is known. AS-IS is the group's working baseline, including its assumptions, not verified operating practice. TO-BE is a proposed design incorporating more recent prototype choices; it is not an implemented or group-approved process. The full published chapter was unavailable and was not read. The cloud AS-IS file was not available, so no direct comparison to it is asserted.

## Source register

- [Source map](../../docs/reference/README.md): source map and authority boundaries; the group paper owns the business-scope baseline.
- [Main working DOCX](<../../../Sharing is caring/The Case of the Brazilian Coffee Cooperative Cooxup├й.docx>): main group paper, especially P1 C/F matrix, A1–A5 and value-added activities 3–19, plus process-level P-a/P-b. Read via DOCX XML text. Its own source citations are not independent verification here. It calls the coordination/field split an inference and phone/visit diagnosis an assumption.
- [Data model](../../docs/design/DATA-MODEL.md): independent reports, technician involvement for cases, human relevance decisions, farm history and responsibility routing, all design draft choices.
- [Intake specification](../../docs/specs/UC-001-REPORT-INTAKE.md): target report inputs and prototype limitations; intake does not implement the wider proposed workflow.
- [Existing P1 TO-BE](<../../../Sharing is caring/3_Modelling/P1_technical_orientation_to-be(2).bpmn>): existing group TO-BE used for comparison only; untouched.

## Activity mapping and assumptions

| Group P1 activity | AS-IS definition |
| --- | --- |
| 3 | Receive and register request. |
| 4–5 | Check availability and allocate technician. |
| 6–8 | Assess request before the phone-or-visit gateway, phone diagnosis and visit-still-needed gateway. The branches and their sequence are working-draft assumptions. |
| 9–14 | Coordination arranges the visit in a collapsed subprocess with a slot-confirmation/rescheduling loop. An intermediate timer waits for the agreed date (explicit working assumption); field advisory then travels and inspects. Farmer waiting/hosting is abstracted by the black-box participant and notes. |
| 15–17 | Formulate and give guidance; message reaches the farmer. |
| 18–19 | An explicit visit-occurred gateway returns a visiting technician before the merged documentation path. Documentation can contain a known outcome; it does not imply resolution. |
| P-a / P-b | Status collection and monitoring meetings are process-level work across requests, shown as an annotation rather than a request step. Their participants and cadence require confirmation. |

TO-BE maps receipt to report registration, history/context assembly, uncertain AI assessment and DMN responsibility routing. A human communications responsibility personalises and relays established guidance on the routine path; an optional product recommendation is not a mandatory outcome. On the technician path, a human creates or links an appropriate technical case, reviews the full available context, decides relevance and membership, and uses phone or visit as needed. Both paths record guidance delivery and any known outcome in farm history. Report registration alone neither creates a case nor closes one; delivery is distinct from resolution. The technician's assigned farms supply minimum context, with access and cross-farm visibility still undecided. These are design choices for review, not new departments or C/F case types.

The new-report input annotation summarises the selected camera/photo, estimate and device-location or mapped-field fallback direction. Field selection conveys field-level precision, not a fabricated GPS point; what happens when neither usable location nor a mapped field exists is unresolved. Offline support in the group paper is an assumption, not implemented functionality. AI output is an uncertain assessment, not a confirmed finding; candidates from proximity do not establish case membership. Thin or unavailable history remains possible.

## Existing TO-BE comparison and alignment

The existing BPMN starts by creating a case, uses an LLM analysis and repeat-case decision before a three-action DMN, then depicts product recommendation, visit, or a human-approved severe bundle with parallel alerts and P2/P3 handovers, and records and closes a case on every path. The new proposal retains human involvement and approval but routes responsibility, keeps routine reports independent of cases, makes context and human relevance judgments explicit, allows phone or visit, and records delivery separately from known resolution. Severe alerts, pre-order and any P3 pickup change are outside the core diagram and require human approval and group agreement; diagnosis alone does not skip pickup. A route is not approval. This simplifies the earlier three-action model and needs reconciliation with the group paper, existing BPMN and draft DMN, not silent replacement of them.

Possible group-document updates after agreement: clarify report versus technical case; responsibility versus action routing and optional product advice; case membership and full-context review; communications as a role rather than a department; outcome versus delivery; and the exact approval and P2/P3 handover scope. Align intake choices with the group's broader photo/voice/text and optional GPS proposal; resolve whether offline capture and additional inputs are in scope. Preserve the original files during review.

## Open decisions and rendering checks

- Define routing criteria, uncertainty and low-confidence handling, how advice is established and who can approve severe actions. Confirm whether every technician route needs a case, case scope, multiple report membership, closure and reopening rules.
- Agree farm assignment, cross-farm access, relevance criteria, context availability, missing location and history handling, and how delivery or unresolved outcomes are recorded.
- Clarify the rubric's three-event-types requirement: whether each individual diagram needs three types or the comparison set as a whole. The AS-IS uses message start, scheduled-time intermediate catch and end events; the agreed visit timestamp is an explicit assumption. The TO-BE uses message start and end events. Do not add an irrelevant timer to satisfy the rubric; resolve whether the requirement applies per diagram or across the model set.
- SVGs target A4 landscape; PNG previews were visually inspected and adjusted for legible labels and routed messages. A physical print and import into the team’s modelling tool still need review. The visit-arrangement subprocess contains a hidden confirmed-slot/rescheduling loop; other collapsed subprocesses contain high-level internal summaries. They require elaboration before any execution use.
- `gateway` denotes exclusive decision/merge; named branch conditions are descriptive, not executable DMN expressions. The parent should render the farmer as a black-box pool, use message flows for the listed messages, and render subprocess steps as hidden internal start/tasks/end. The output includes BPMN XML/DI and matching SVG/PNG previews, but no new DMN or datasets. All models are non-executable comparison proposals.

## Checks and remaining review

Both BPMN files passed reference/scope checks and validation against the official
OMG BPMN 2.0 XSD set on generation. Gateway branch conditions are descriptive; no
engine execution is claimed. XML schema validation does not verify agronomic policy
or establish that the working AS-IS assumptions reflect actual Cooxupé practice.
The original files and cloud model were not overwritten. A Luna-medium semantic
review found no blocking defects; its scheduling-exchange observation is addressed
with explicit visit-arrangement and slot-confirmation messages to/from the farmer.
Modeler import and engine execution remain unverified.
