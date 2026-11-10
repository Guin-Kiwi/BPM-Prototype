# UC-002 source and group-model alignment

This is a trace between the published case, the working-group C/F matrix, the
selected P1 BPMN pair, the current application slice and the planned UC-002
evidence. It records alignment questions; it does not approve group policy or
claim that the prototype implements the case's adopted improvements.

## Source baseline

The supplied chapter, *Toward the Full Application of BPM*, describes a BPM
improvement initiative and reports improvements already adopted. Table 1 (printed
p. 169; PDF p. 173) identifies two P1 opportunities: scheduling technician visits
to cooperative members and excessive meetings required to monitor the process.
Its listed adopted solutions are a proactive attendance schedule based on customer
segmentation, process intelligence, and standardized managerial meetings. The
chapter does not provide the segment definitions, allocation rules, operational
RACI, or a detailed diagnosis and guidance workflow. It reports shorter member
service lead time and better technician/engineer allocation decisions (printed
p. 168), without numerical baselines or measured effects.

The group C/F matrix and AS-IS model supply a more detailed process hypothesis:
request registration, technician allocation, phone-or-visit diagnosis, scheduling,
field guidance and documentation. Treat these as the group's modeled baseline,
not as steps established by the chapter. The group's modeled AS-IS is the
pre-improvement baseline for this comparison. The chapter's adopted changes are
the real-world improvement reference, not the baseline that UC-002 claims to extend.
UC-002 proposes a digital assessment and responsibility handoff against that
pre-improvement baseline; it does not reconstruct the case's adopted scheduling
solution. The app demo does not implement segmentation, proactive scheduling or
process intelligence.

## Trace to existing model and app

| Source / C-F function | Selected BPMN nodes | Current app state and gap | Planned acceptance evidence |
| --- | --- | --- | --- |
| Case Table 1, P1: visit scheduling and process-monitoring meetings are improvement opportunities; adopted response is proactive attendance scheduling by customer segment, process intelligence and standardized managerial meetings. The group C/F matrix places visit scheduling, technician allocation and monitoring under **Advisory coordination**. | AS-IS: `A_Allocate`, `A_Schedule`, `A_Schedule_Rearrange`. TO-BE: `T_Context`, `T_Route`, `T_Case`, `Activity_07f6j9c`. The TO-BE depicts routing and recording a technical case, not the chapter's segmentation-based scheduling or its managerial meeting standardization. | UC-001 persists submitted reports and farm-wide report history. UC-002 assessment, responsibility routing, case linkage and handoff are not implemented. Scheduling and meeting analytics are outside this app slice. | UC-002 AC3–5: reproducible, versioned routing with reasons; staff records routine communication or technician involvement; state survives reload and failure does not fabricate a handoff. These demonstrate the proposed slice only, not reduced lead time or improved resource allocation. |
| Group C/F function **Field advisory**: diagnose by phone or visit and provide agronomic guidance (group DOCX matrix). The published chapter establishes the service end-to-end label, but not this diagnosis sequence. | AS-IS: `A_Assessment`, `A_Remote`, `A_Visit`, `A_Document`. TO-BE: `T_Assess`, `T_Review`, `T_ConductVisit`, `T_Record`. | The app saves original report evidence only; it has no image assessment, guidance or technician review. The demo's proposed AI inference must remain distinct from a confirmed finding. | UC-002 AC1–2 and AC4: enforce model-input boundaries, persist attributed inference, and let staff inspect evidence and record the human handoff. Any visit remains beyond the bounded first journey. |
| Group C/F function **Advisory coordination** includes the communications role in the selected TO-BE. Communications relays prepared guidance; it is a role in the coordination function, not a newly asserted department or C/F function. | TO-BE lane `T_Coord` is named “Advisory coordination / communications role”; `T_Routine` is “Relay established guidance.” The pool-level `T_App` lane represents the application/system, not a business function in the C/F matrix. | No communications action or guidance delivery is recorded by the current app. | UC-002 AC4–5: a staff member records the appropriate handoff and can inspect it after reload; a recorded delivery is not resolution. Confirm lane/function terminology in the group model review. |
| The group matrix's P1 case type is **Farm issue (a member's support request)**. The prototype's technical case is a record for technician involvement, not an additional business case type in the C/F matrix. | TO-BE `T_Case` creates or links a technical case; the report is registered at `T_Register`. The selected process ends at `T_End` “Report handling recorded,” not case closure. | Current persistence covers reports, not assessments, routes, technical cases or handoff events. | UC-002 AC3–5: keep route and handoff separate from assessment; routine reports do not create a technical case; technician involvement follows an agreed linking rule; handling does not assert closure. The linking policy remains open. |

## Decisions and boundaries to carry forward

- Keep the group's pre-improvement AS-IS baseline distinct from the chapter's
  adopted improvements and the prototype's proposed assessment/handoff. Cite the
  chapter only for what it states; use the group DOCX as the group's C/F and model
  baseline.
- Keep **Advisory coordination**, **Field advisory**, and **Application** distinct:
  the first two are business functions/lanes; communications is a role within
  advisory coordination; the application is a supporting system lane.
- Keep a report (the member's farm-issue request) distinct from an optional linked
  technical case record. A technical case does not create a new C/F case type.
- Preserve UC-002's boundaries: photo-only image model; proposed second model gets
  image candidate scores, farmer note and optional versioned weather; code/DMN gets
  separately prepared history facts. Human review remains selective and a severe
  action still needs human approval. Existing photo/note/model-input, weather and
  history boundaries should not be widened by this alignment note.
- Group alignment questions are decisions for model/paper reconciliation. They do
  not block every prototype draft: the app can specify its bounded report-to-handoff
  slice while explicitly labeling scheduling, visit planning and wider neighbor
  history workflows outside the demo. Do not claim the larger model or case solution
  is fully implemented.

See the [UC-002 draft](../specs/UC-002-ASSESSMENT-HANDOFF.md),
[selected BPMN comparison and trace](../../models/comparison/README.md), and
[source map](README.md). Acceptance criteria above are planned checks; no application
assessment, routing, delivery or case-linking evidence exists yet.
