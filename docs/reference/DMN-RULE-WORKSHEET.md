# P1 report routing worksheet

This records the owner's selected prototype direction and a proposed operational
rule for discussion and personal DMN editing. It is not approved group policy or an
implementation specification. The group DOCX, BPMN and draft DMN remain unchanged;
alignment with them is pending. Model assessments are inferences, not diagnoses.

## Sources and limits

- [Business paper](<../../../Sharing is caring/The Case of the Brazilian Coffee Cooperative Cooxup├й.docx>): P1 guidance, selective technician involvement and approval of severe actions; P2/P3 are handovers. See the [source map](README.md).
- [Original draft DMN](<../../../Sharing is caring/3_Modelling/DMN (Draft, not final)/P1_determine_action(1).dmn>) and [working BPMN](<../../../Sharing is caring/3_Modelling/P1_technical_orientation_to-be(2).bpmn>) are group drafts, not approved policy or this proposed routing rule.
- [Embrapa, Caixeta et al., *Manejo integrado de pragas e doenças do café arábica*, Circular Técnica 8, October 2024, 35 pages](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1167902/1/Circular-Tecnica-8-Manejo-integrado-de-pragas.pdf); [alternate official PDF](https://ainfo.cnptia.embrapa.br/digital/bitstream/doc/1167902/1/Circular-Tecnica-8-Manejo-integrado-de-pragas.pdf). The indexed management section describes about 25 plants × 4 leaves and incidence as diseased leaves divided by sampled leaves. Its 5% threshold concerns a specific chemical management context, not severe escalation, pickup cancellation or image leaf severity. Full PDF not reviewed; pages not verified.
- [WCR/CATIE manual landing page](https://worldcoffeeresearch.org/resources/prevention-and-control-of-coffee-leaf-rust) describes a technician-facing manual; the full manual has not been read and no detailed rules are attributed to it.
- [OMG DMN 1.4](https://www.omg.org/spec/DMN/1.4/PDF): FIRST selects the first matching rule; order matters.

## Selected prototype direction

1. A farmer who suspects something is wrong submits a **report**, even if it may
   ultimately turn out that there is no problem. Link it to its farm, field and
   available history. Receipt confirms submission, not advice or resolution.
2. An LLM assesses the report and available evidence; retain observations separately
   from its inference and any confirmed findings. Deterministic DMN routes the report
   to **routine advisory communication** or **technician required**, with a reason.
3. Only technician involvement creates a **case**; routine reports remain reports.
   If a report escalates later, link it to an appropriate existing case or create a
   new one. Do not require a duplicate case. The technician decides what follow-up,
   including clarification or a visit, is appropriate.
4. Technicians are assigned farms at minimum and can access their routine reports,
   communications, treatment and available sales information. Purchase-history
   integration is out of scope. A product purchase is optional, never automatic.
5. Communications staff personalise and relay established advice; they make no
   diagnostic or agronomic judgment. AI and DMN do not message farmers
   directly. Communication delivered and issue resolved are separate outcomes.

## Proposed operational routing rule

Route to communications only when **all** are established: low risk, applicable
established routine guidance, sufficient evidence, and no escalation trigger. Route
to a technician when risk is concerning or uncertain, evidence is insufficient or
uncertain, guidance is unsupported or inapplicable, or a repeat/unresolved trigger
applies. Missing or unknown inputs do not establish eligibility for routine advice.
Record the reason and relevant evidence for either route. The thresholds, repeat
window and other definitions below still need agreement; no numeric cutoff is set here.

Inputs should express evidence and history, risk, applicability of established
guidance and escalation triggers—not the circular conclusion `visitNeeded`. Model
self-confidence alone is not validated evidence of eligibility. Whether a cause is
controllable is not a routing criterion: a downpour may be uncontrollable while an
established routine response exists. A weather API is not required.

Concerning or severe indications require technician involvement. Routing itself
does not authorise a severe action or bundle: retain the existing human approval
step before any severe action, including the paper's proposed pickup, alert and
pre-order bundle. Risk context alone is not field severity; a photo's leaf severity
is not measured field incidence.

## Examples for discussion

These outcomes assume the stated facts can be established under definitions yet to
be agreed; they are illustrative, not agronomic protocols.

| Report and available evidence | Proposed route and reason |
| --- | --- |
| Suspected problem; low risk, sufficient evidence, applicable routine guidance, no trigger; no problem may ultimately be found | Communications relays established advice; no product is required. |
| Downpour; low risk and sufficient evidence, applicable routine response, no trigger | Communications; uncontrollable cause alone does not escalate. |
| Suspected rust with concerning risk or uncertain evidence | Technician required; risk or evidence prevents routine eligibility. |
| Apparently low risk but no applicable established guidance | Technician required; guidance is unsupported. |
| Repeat or unresolved report, including one with severe indications | Technician required; link to an appropriate existing case or create one; severe actions still require approval. |

## Open definitions and minimal next SPECIFY task

- Agree who defines and validates low/concerning risk, sufficient evidence and
  applicable established guidance, including handling uncertainty and missing data.
- Define repeat and unresolved triggers, their time window, farm/field scope,
  missing history, and when a later report links to an existing case.
- Define technician assignment and access boundaries, the communications handoff,
  and how severe approval and receipt, delivery and resolution are recorded.
- Reconcile the selected direction with the group's paper and models; the current
  draft has a repeat gateway and action paths that do not directly express this rule.

Next agent: prepare a minimal routing UC in SPECIFY, separate from
[UC-001 intake/history](../specs/UC-001-REPORT-INTAKE.md). Trace the owner direction,
proposed rule and unresolved choices to acceptance criteria; identify the authoritative
rule version and how consistency with the eventual DMN will be checked. Do not edit the
group models or implement routing. Agreed intake can progress independently; routing
implementation awaits the open operational definitions and alignment.

Planned acceptance evidence: demonstrate report receipt and farm/field history; exercise
both routes and each missing/uncertain or escalation condition with a recorded reason;
show routine reports without cases and later escalation linked or newly created; verify
staff handoff, assigned-farm access and severe approval; distinguish message delivery
from resolution. These are planned checks, not results or evidence of group approval.
