# P1 comparison trace

The [approved pair](README.md) governs the prototype workflow; the working
[group DOCX](<../../../Sharing is caring/The Case of the Brazilian Coffee Cooperative Cooxup├й.docx>)
remains the group solution baseline. The AS-IS is reconstructed from that paper and
group assumptions, including phone assessment and the visit decision; it is not a
verified account of actual Cooxupé practice. The published chapter spans printed pp. 163–172 (PDF pp. 167–176). The chapter's Table 1 reports visit scheduling and excessive monitoring
meetings as improvement opportunities, then proactive attendance scheduling based
on customer segmentation, process intelligence and standardized managerial meetings
as adopted solutions. It does not document the diagnosis workflow represented in the
group DOCX, which remains a group working model rather than a verified account.

## Selected pair

AS-IS receives and assesses a request, arranges and waits for a visit when needed,
provides guidance remotely or on site, and records guidance and progress. The visit
subprocess includes travel, inspection, on-site guidance and return.

TO-BE registers the report and retrieves farm and nearby history for routing and human
review. The image model receives the photo only; a proposed second model combines
its scores, farmer note and optional [event weather](../../docs/reference/EVENT-WEATHER.md).
DMN combines the assessment, extent estimate and code-derived history facts to route responsibility.
The subprocess sequence does not imply that retrieved history is passed to the LLM;
see the [assessment boundary](../../docs/reference/DMN-RULE-WORKSHEET.md#assessment-and-routing-boundary). Communications personally relays
established guidance for routine reports; technician involvement creates or links a
technical case. The technician reviews the full available context and judges relevance.
After clarification, the inclusive split always selects the visit decision and also
selects preliminary guidance when available. The join waits for the selected paths
before findings and case state are recorded.
The technician may then send a P2 referral or authorised P3 notice; both require
separate downstream messages if needed. Routine communications may optionally refer
a product need to P2. These are intermediate message-throw events, not orders or
an automatic pickup cancellation; downstream recipients/integration are not modeled
as participant message flows. Farmer message flows cover report, guidance and visit
arrangements/confirmation. A needed visit is planned with case status recorded, waits
for the appointment, and includes entering findings and saving them to case history
before return. It loops to review rather than case creation. The shared end records
report handling, not case closure. Official in-system guidance and recording are the
modeled work; incidental on-site conversation needs no new process step. Post-visit
review, advice and recording are intentional and may happen later, such as when the
farmer is unavailable.

## Existing TO-BE comparison and alignment

| Group baseline or earlier draft | Selected prototype direction / remaining alignment |
| --- | --- |
| Paper: photo, voice or text, optional GPS and farm test results; assumes offline capture. | Camera-first, required estimate and usable GPS or known-field fallback; voice, offline and extra inputs remain gaps or deferred. [UC-001](../../docs/specs/UC-001-REPORT-INTAKE.md) distinguishes target and demo. |
| Paper: per-farm, field and weather-zone event history plus agronomic references. | Full available farm and nearby history is retained for human relevance judgment; weather integration and exact scope/access remain open. |
| Paper: DMN chooses product recommendation, visit or severe bundle; technicians review diagnoses and approve severe actions. | DMN routes human responsibility, routine reports need no case, and product advice is optional. Severe approval and downstream P2/P3 handling remain outside core P1 and need group alignment; conditional referral events are modeled in the pair. |
| [Earlier group BPMN](<../../../Sharing is caring/3_Modelling/P1_technical_orientation_to-be(2).bpmn>) and [draft DMN](<../../../Sharing is caring/3_Modelling/DMN (Draft, not final)/P1_determine_action(1).dmn>) use case-first, repeat and action paths. | Technician involvement creates or links a case; visits loop to review. Define repeat handling, case linkage and closure with the group; no automatic farmer messaging, orders or pickup changes follow from routing. |

The real concept deliberately prepares routine guidance with technicians. The
prototype proposes illustrative observation guidance from attributable published
sources, subject to suitability and terms; no technician approval or validated treatment
is established. The [routing worksheet](../../docs/reference/DMN-RULE-WORKSHEET.md)
owns the proposed operational rule and open definitions. Communications is a role,
not an asserted department; a technical case is not a new C/F business case type.

## Review still needed

Walk the edited models and subprocesses in a BPMN modeller, check notation and
print legibility, and reconcile the table above with the group paper. Clarify the
assignment's event-type requirement rather than adding artificial process steps.
Quantified cost/benefit and process-policy evidence are still needed. Earlier
validation and generation evidence applies to earlier artifacts, not automatically
to the selected edited pair. No model execution is claimed.
