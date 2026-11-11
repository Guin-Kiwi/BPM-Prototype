# P1 report routing worksheet

This records the selected prototype direction and a proposed operational
rule for discussion and personal DMN editing. It is not approved group policy or an
implementation specification. The selected [comparison pair](../../models/approved/README.md)
governs the prototype workflow; reconciliation with the group DOCX and draft DMN
remains pending. Model assessments are inferences, not diagnoses.

## Sources and limits

- [Business paper](<../../../Sharing is caring/The Case of the Brazilian Coffee Cooperative Cooxup├й.docx>): P1 guidance, selective technician involvement and approval of severe actions; P2/P3 are handovers. See the [source map](README.md).
- [Original draft DMN](<../../../Sharing is caring/3_Modelling/DMN (Draft, not final)/P1_determine_action(1).dmn>) and [working BPMN](<../../../Sharing is caring/3_Modelling/P1_technical_orientation_to-be(2).bpmn>) are group drafts, not approved policy or this proposed routing rule.
- [Embrapa, Caixeta et al., *Manejo integrado de pragas e doenças do café arábica*, Circular Técnica 8, October 2024, 35 pages](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1167902/1/Circular-Tecnica-8-Manejo-integrado-de-pragas.pdf); [alternate official PDF](https://ainfo.cnptia.embrapa.br/digital/bitstream/doc/1167902/1/Circular-Tecnica-8-Manejo-integrado-de-pragas.pdf). The indexed management section describes about 25 plants × 4 leaves and incidence as diseased leaves divided by sampled leaves. Its 5% threshold concerns a specific chemical management context, not severe escalation, pickup cancellation or image leaf severity. The rust and leaf-miner passages have now been reviewed; exact sections, pages and
  claim limits are recorded in the [guidance catalogue](UC-002-GUIDANCE-CANDIDATE.md).
- [WCR/CATIE manual landing page](https://worldcoffeeresearch.org/resources/prevention-and-control-of-coffee-leaf-rust) describes a technician-facing manual; the full manual has not been read and no detailed rules are attributed to it.
- [OMG DMN 1.4](https://www.omg.org/spec/DMN/1.4/PDF): FIRST selects the first matching rule; order matters.

## Selected prototype direction

1. A farmer who suspects something is wrong submits a **report**, even if it may
   ultimately turn out that there is no problem. Link it to its farm and available
   location and history; a field association is not always available. Receipt confirms
   submission, not advice or resolution.
2. Assess each report independently. The image model receives the photo only;
   a proposed second model combines its candidate scores with the farmer note and
   optional bounded [event weather](EVENT-WEATHER.md). Its structured assessment is
   inference, not a confirmed finding. Farm/nearby history, earlier assessments,
   treatments and cases are excluded from both models. Code derives history facts
   separately; deterministic DMN combines them with the assessment and farmer's
   extent estimate to route responsibility, with a reason.
3. Only technician involvement creates a **case**; routine reports remain reports.
   If a report escalates later, link it to an appropriate existing case or create a
   new one. Do not require a duplicate case. The technician decides what follow-up,
   including clarification or a visit, is appropriate.
4. Technicians are assigned farms at minimum and can access their routine reports,
   communications, treatment and available sales information. Purchase-history
   integration is out of scope. A product purchase is optional, never automatic.
5. Communications staff personally relay established guidance; they do not diagnose.
   In the real concept, technicians deliberately prepare this guidance. A prototype may
   illustrate it with attributable published sources, with its source and applicability
   recorded in the [guidance catalogue](UC-002-GUIDANCE-CANDIDATE.md). Published source
   support is not technician approval of an individual report. AI and DMN do not
   message farmers directly, and no product order is automatic.
6. Full available farm and nearby history remains accessible for technician judgment.
   Following clarification, an inclusive split always selects the visit decision and
   also selects preliminary guidance when available; selected paths join before
   recording findings and case state. A technician may then send a conditional P2/P3
   referral; routine staff may optionally refer a product need to P2. These message-throw events are not product
   orders or automatic pickup cancellation; P3 notices require authorisation and group
   alignment. A needed visit is planned with case status recorded, waits for the
   appointment, has findings entered and saved to case history, and returns to review.
   Official guidance and recording are captured in the system; incidental on-site conversation is not a separate modeled task. Review, advice
   and recording after the visit are intentional and may occur later, for example if the
   farmer was unavailable. Handling recorded does not mean the case is closed.

## Assessment and routing boundary

Event weather is the only selected context extension beyond the current photo and
farmer note; its variables, provenance, assumptions and source limits are owned by
[the weather plan](EVENT-WEATHER.md). Do not infer a data connection from BPMN task
order. Weather enrichment is not connected report history.

Keep the original report and its standalone AI assessment linked to the farm. Later
reports or history changes can affect routing and technician review without changing
that assessment. Reassessment of the same evidence must be recorded separately.

Code prepares defined history facts, such as repeat reports or an unresolved case;
DMN applies explicit rules. Guidance matching uses an explicit code/rule mapping to
prepared entries, not LLM-generated treatment. Mapping and history definitions remain
open. Technicians can inspect the underlying reports and judge connections the rules
have not captured. Neither model uncertainty nor deterministic execution guarantees
that an assessment or route is correct.

## Bounded demonstration routing

The demonstration uses actual image and interpretation outputs plus synthetic report
history, with no hand-entered desired route, risk or eligibility. The
[versioned demonstration proposal](UC-002-DEMO-RULES.md) owns the exact rule order,
model contract, history assumptions and entry mapping. Its communications route means
relay of a sourced, non-treatment observation message. It establishes neither low
agronomic risk nor that a technician is unnecessary. The earlier proposed generic
low-risk test is not supported by these sources and is not a demonstration input.

Agronomic content and its limits are owned by the
[prepared guidance catalogue](UC-002-GUIDANCE-CANDIDATE.md). Staff responsibility,
repeat window, history completeness and exact software output guards are prototype
assumptions. Class scores and interpretation are inferences; interpreter agreement is not
independent confirmation. Missing issue links do not establish that other reports are
irrelevant. The bounded demonstration has no farm-wide 30-day repetition rule. No score cutoff, source
sampling incidence threshold or disease name authorizes treatment, a product order,
pickup cancellation, a visit or severe action. Human approval remains necessary for
severe actions; technicians judge follow-up and case relevance.

## Open definitions and minimal next SPECIFY task

- For the wider concept, establish agronomic risk criteria through appropriate expertise;
  the bounded demo instead relays observation
  messages and tests its explicit software assumptions instead of claiming clinical triage.
- Define repeat and unresolved triggers, their time window, farm/field scope,
  missing history, and when a later report links to an existing case.
- Define technician assignment and access boundaries, the communications handoff,
  and how severe approval and receipt, delivery and resolution are recorded.
- Reconcile the selected pair with the group paper and earlier BPMN/DMN, including
  their repeat gateway, action paths, input modes, offline assumption and severe handovers;
  see the [comparison trace](../../models/approved/NOTES.md#existing-to-be-comparison-and-alignment).
- Use the researched illustrative guidance entries and their attribution, applicability
  and reuse notes; determine how the prototype presents its limits without implying
  technician validation or treatment approval.

Continue the draft [UC-002](../specs/UC-002-ASSESSMENT-HANDOFF.md), separate from
[UC-001 intake/history](../specs/UC-001-REPORT-INTAKE.md). Trace the selected requirements,
proposed rule and unresolved choices to acceptance criteria. Include an input-boundary
check: image model receives only the photo; any second model receives candidate
scores, farmer note and optional versioned weather snapshot. Farm/nearby history and
prior findings enter neither. Changing connected history can change routing while
leaving the standalone assessment unchanged.
Identify the authoritative
rule version and how consistency with the eventual DMN will be checked. Do not edit the
group models or implement routing. Agreed intake can progress independently; routing
implementation awaits the open operational definitions and alignment.

Planned acceptance evidence: demonstrate report receipt and farm/field history; exercise
both routes and each missing/uncertain or escalation condition with a recorded reason;
show routine reports without cases and later escalation linked or newly created; verify
staff handoff, full available context and severe approval; walk a planned visit back to
review including later advice, and distinguish handling and delivery from case closure
and resolution. These are planned checks, not results or evidence of group approval.
