# Reference sources

The approved BPMN pair governs the prototype workflow. The published case and
working group DOCX retain authority over their respective facts and group baseline;
assignment requirements govern deliverables. Reconcile remaining differences.

## Use each source for its scope

| Source | Authority |
| --- | --- |
| Published Cooxupé case, Ribeiro et al. (2025) | Organisation, reported problems, adopted improvements and outcomes; does not establish our proposed solution. |
| Main working group DOCX below | Group solution baseline, P1 scope and authoritative C/F matrix. |
| Assignment and grading material | Deliverables and assessment expectations. |
| [Approved prototype comparison pair](../../models/approved/README.md) | Prototype workflow; this approval does not establish agronomic thresholds or group policy. Differences from the group baseline require alignment. |
| Other working files | Supporting drafts; reconcile conflicts instead of choosing by modification date. |

The published chapter is [Toward the Full Application of BPM](https://doi.org/10.1007/978-3-031-80793-0_12),
pp. 163–172, in *Business Process Management Cases Vol. 3*, available in the
[local book PDF](<../../../Business Process Management Cases Vol. 3.pdf>).
Printed chapter pages 163–172 correspond to PDF pages 167–176 in this supplied file.

### What the primary case establishes

- Table 1, printed p. 169: agricultural technical orientation spans a member's need
  for technical support through receiving agronomic guidance. The named improvement
  opportunities are visit scheduling and excessive process-monitoring meetings.
- The same row reports adopted solutions: proactive attendance scheduling based on
  customer segmentation, process intelligence and standardized managerial meetings.
  Techniques include BPMN, RACI, OKRs and customer-segmentation analysis. It does not
  provide the actual segment definitions, allocation rules or operational RACI.
- Results, p. 168: the chapter reports shorter member-service lead time and improved
  allocation decisions for agricultural technicians/engineers. It gives no numerical
  baseline, effect size or diagnostic-performance measurements for our experiment.
- The chapter documents improvements already undertaken. Image-based assessment and
  report routing are our proposed extensions; they are not the case's implemented
  solution. The case does not specify phone-versus-visit diagnosis, triage thresholds,
  communications duties, treatment rules or our report/technical-case distinction.
- The self-service/knowledge-bank plans below Table 1 concern IT calls and developer
  capacity; do not attribute them to agricultural advice. Figs. 1–2 show the overall
  coffee chain and BPM project scope, not a detailed agricultural-advisory workflow.

The selected AS-IS baseline is the situation **before** the chapter's adopted
improvements. Customer segmentation, proactive attendance scheduling and the reported
improved management are comparison evidence, not assumed starting capabilities. The
prototype proposes its own TO-BE against that pre-improvement baseline.

Design implication: evaluate how the prototype could support member service,
responsibility allocation and process visibility. Status tracking is a proposed means
of addressing those goals, not proof that the original organisation had no status
records. Synthetic demonstrations cannot establish real reductions in visits or lead
time. Preserve the selected model-input and event-weather boundaries.

The prototype uses camera-first reporting, required location context, a mapped-field
fallback and responsibility routing. These are prototype choices to reconcile with the
working DOCX and earlier group BPMN/DMN; the selected comparison pair reflects the prototype direction. They do not establish a new Cooxupé department. A technical
case record is also distinct from the C/F matrix's business case types.

## Local source map

These links use the surrounding `bpm-project` reference folder. A standalone clone
will not contain those files; restore the same layout or update this map. Do not
mistake missing references for permission to invent requirements.

- [Main group paper (business scope and C/F matrix)](<../../../Sharing is caring/The Case of the Brazilian Coffee Cooperative Cooxup├й.docx>)
- [Assignment (deliverables)](<../../../Group work assignment -BPM HS26.pdf>)
- [Grading template (FS26; confirm HS26 applicability)](<../../../Sharing is caring/Grading - TEMPLATE BPM FS26.pdf>)
- [P1 to-be BPMN (working model)](<../../../Sharing is caring/3_Modelling/P1_technical_orientation_to-be(2).bpmn>)
- [P1 DMN (draft, not approved policy)](<../../../Sharing is caring/3_Modelling/DMN (Draft, not final)/P1_determine_action(1).dmn>)

## Alignment needed before coding policy

The paper describes selective review, including severe-case approval. Criteria for
routine guidance, repeat-case precedence, missing evidence and severe routing need
agreement. The draft DMN is not an approved treatment protocol. Do not infer harvest
cancellation or automatic orders from a disease label. The authoritative C/F matrix
is the one in the main paper; other spreadsheets are supporting drafts.

The intended submission includes a report (maximum 15 pages), two BPMN plus one DMN
or three BPMN models, actual AI prototype experiments, artefacts and a presentation.
Trace acceptance criteria to the assignment and rubric when writing UC-001. Confirm
ambiguous grading details and MCP expectations with the lecturer.

## Evidence conventions

Separate observed inputs, AI inferences, confirmed findings and synthetic scenarios.
Duplicate reports do not create independent samples. Leaf severity and field incidence
are different measures; incidence needs a defined sample denominator. Dataset labels
do not provide business action labels. Preserve dataset versions and attribution.

Public data and agronomic source candidates are listed in the linked prototype
concept. Verify suitability and reuse terms before importing samples. Source documents and datasets are not redistributed with the prototype.

First dataset preparation: [open-data intake plan](OPEN-DATA.md).

Selected prototype routing direction and next specification step:
[report-to-case routing worksheet](DMN-RULE-WORKSHEET.md). Group model alignment remains pending.

[Farm history and technical case data-model draft](../design/DATA-MODEL.md) traces
source-backed context, selected direction and unresolved design proposals.

[Approved P1 AS-IS / TO-BE comparison](../../models/approved/README.md)
links the canonical BPMNs. Source assumptions
and outstanding group alignment are explicit.

[Event weather context](EVENT-WEATHER.md) owns selected environmental variables,
source evidence, snapshot assumptions and the distinction from connected history.
