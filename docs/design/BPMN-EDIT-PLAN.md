# P1 BPMN comparison edit plan

**Status:** This plan and its recorded checks describe earlier model work. Ayla’s
[selected edited pair](../../models/comparison/README.md) is now the prototype
comparison source; confirm its own notation, import and print checks separately.
The current task does not authorize further BPMN changes.

## Outcome

Produce one readable A4 landscape page for each P1 model. Make the proposed benefit
visible: routine reports need less technician handling, while technical work starts
with assembled evidence and history. Necessary visits remain part of both processes.

## Requirements and boundaries

- **R1 — Comparable scope and detail.** Both models run from the farmer's request/report
  to guidance and recorded progress. Use the same visible visit-planning, appointment
  wait and field-visit pattern. The comparison concerns proposed responsibilities and
  information availability, not a guaranteed reduction in activities or visits.
- **R2 — Readable, correct notation.** Retain the external farmer pool, appropriate
  Cooxupé lanes, exclusive routing, message flows between pools, sequence flows within
  Cooxupé, genuine subprocesses and the scheduled-visit timer. Show AI and deterministic
  DMN explicitly, even when their detail is collapsed.
- **R3 — Preserve meaning.** Routine reports do not create technical cases. Only the
  technician branch creates/links a case; loop back to review, never to case creation
  or initial AI routing. Scheduling and advice delivery do not automatically close a
  case. Save case state when progress changes; the shared ending completes the
  handling pass, not necessarily the technical case.
- **R4 — Retain the improvement mechanism.** Show routine human communication separately
  from technician work, farm/nearby context as available evidence, and technician
  relevance judgment. Communications relays established guidance without diagnosing;
  product advice is conditional. No new department or C/F business case type is implied.
- **R5 — Keep costs visible in analysis.** Include round-trip travel, on-site work and
  scheduling in field-visit time/cost assumptions; do not show travel/return as separate
  overview tasks. Quantify routine technician effort and context-preparation effort;
  also account for the communications handover. Benefits remain hypotheses until tested.
- **R6 — Source and scope discipline.** Use the [working paper/source map](../reference/README.md)
  and selected [AS-IS](<../../models/comparison/p1_asis (2).bpmn>) and
  [TO-BE](<../../models/comparison/p1_tobe (2).bpmn>). Phone diagnosis
  is a labelled group assumption, not verified published practice. Preserve existing
  assumptions and approval limits. Severe P2/P3 actions remain explicitly outside the
  core view; this plan neither approves nor silently removes them from the wider proposal.

The [HS26 assignment](<../../../Group work assignment -BPM HS26.pdf>), pp. 2–3,
requires reasonable complexity on A4, major BPMN elements, visible intelligent steps,
appropriate granularity, semantic consistency and cost/benefit justification. These
requirements support abstraction with traceability; they do not require one box per
cost component. The supplied FS26 grading template is supporting guidance; HS26 is
the current assignment. This plan changes no prototype code, dataset or group paper.

## Open choices

- Recommend a collapsed **AI-assisted report triage** subprocess with a brief visible
  annotation: “Register report; retrieve farm/nearby history; AI assessment; DMN routing.”
  Preserve its service/business-rule tasks inside the editable model. If a printed
  marker/annotation does not make automation sufficiently clear, expose AI assessment
  and DMN as two visible tasks before shrinking text. Confirm any remaining rubric
  interpretation with the lecturer; do not add decorative events to satisfy a count.
- The overview will show report handling, with technical case state retained. A complete
  case-closure/reopening lifecycle is separate detail; do not label the common end
  “case closed” without modelling that decision.
- Page fit is a proposed layout target, not a passed check. If legibility fails, move
  secondary explanations to a caption or expand a subprocess separately rather than
  removing decisions, state semantics or the visible visit path.

## Steps

### 1. Simplify AS-IS without changing the working baseline

- Keep **Receive and register request** and **Allocate available technician** visible.
- Group **Assess request**, the phone/visit choice, phone diagnosis and review of
  visit necessity inside **Assess request with farmer**. Keep the source assumptions
  in the caption and editable detail. Its visible result is **Visit needed?**
- Yes: **Arrange visit with farmer** (coordination) → **Agreed visit time** (timer)
  → **Conduct field visit** (field advisory). No: use the remote-guidance path.
- The visit subprocess includes on-site guidance. On the No path, show **Provide
  remote agronomic guidance**. Merge these mutually exclusive paths before **Document
  guidance and progress** → **Guidance recorded**. This avoids duplicating advice or
  implying the farmer must wait for the technician to return before receiving it.
- Remove **Visit occurred?**, **Return from farm** and their now-unneeded merge. Put
  relevant travel/return and on-site details inside the visit work; guidance may be
  provided during the visit. Do not turn this abstraction into a forced second trip
  or imply that guidance must wait until the technician returns.

### 2. Simplify TO-BE while exposing who benefits

- Keep **Report received**, then replace the four visible registration/context/AI/DMN
  boxes with **AI-assisted report triage**. Retain those original operations inside it.
  Keep **Who handles report?** visible immediately afterwards.
- Routine: **Relay established guidance** in coordination/communications → shared
  recording step. This path visibly avoids technician assessment and case creation.
- Technician: **Create or link technical case** → **Review context and advise farmer**
  → existing **Field visit needed?**
- Yes: **Plan visit and record case status** (coordination) → **Agreed visit time**
  → **Conduct field visit** (field advisory) → loop to the existing review subprocess.
  Keep visit scheduling out of the review's internal detail to avoid duplicate work.
- No: continue to the shared **Record delivery / known outcome** → **Report handling
  recorded**. The review records current case state; the end does not close the case.
- Retain a short context note: full available farm history and neighbouring candidates
  remain accessible; the technician judges relevance. A photo's apparent mildness or
  an automatic non-match must not establish that surrounding reports are irrelevant.

### 3. Lay out the pair for comparison

- Use A4 landscape, the same font/style and consistent labels for matching activities.
  Align receipt, assessment, human response and recording as common visual stages.
- Use coordination and field advisory lanes in AS-IS. TO-BE adds the application lane
  for automation, with the same human responsibilities easy to locate below it.
- Aim for about 10–12 visible activities/events/gateways in AS-IS and 13–15 in TO-BE;
  these are layout guides, not targets that override correctness. Put the visit loop
  in the lower portion, with short orthogonal arrows and few crossings.
- Aim for 9–10 point or larger labels at actual print size. Use two or three lines per
  activity; move source caveats, cost detail and secondary notes to the figure caption.
  Fit by rearranging/collapsing detail before reducing text size.

### 4. Connect the figures to the argument

Use a short comparison paragraph: AS-IS allocates technician attention to incoming
requests; TO-BE prepares context and sends eligible routine guidance to communications.
Technicians retain judgment, visits and follow-up for technical work. Evaluate workload,
preparation time, total handling effort and visits; do not claim savings from hiding
travel or from having fewer diagram boxes.

## Completion evidence

| Check | Evidence required |
| --- | --- |
| R1/R3: equivalent scope and correct paths | Walk through phone-only AS-IS, visited AS-IS, routine TO-BE, technician remote advice and a visit returning to review. No dead ends, duplicate cases, forced unnecessary visits or automatic closure. |
| R2: notation and import | Both XML files pass schema/reference checks and open in Camunda. Farmer exchanges cross pools as messages; internal work uses sequence flows; collapsed detail remains editable. |
| R2/R4: visible intelligence and responsibility | At A4 size a reviewer can identify AI, DMN, routine human communication, technician review and planned visits without opening subprocesses. Check natural message-start, appointment timer and end events against the lecturer's wording. |
| R1/R6: no lost or invented requirements | Compare each moved/removed activity with the working paper and original diagram; record whether retained inside a subprocess, combined, or explicitly deferred. Confirm assumptions and group-document differences remain labelled. |
| R5: honest improvement argument | Cost/benefit notes include travel and the new handover, distinguish measurements from assumptions and use comparable AS-IS/TO-BE scenarios. |
| A4 fit | Export each overview to a single A4 landscape page, inspect at 100%/print size, and verify readable labels, no clipping/overlaps and traceable arrows. This is a required check, not yet a result. |

**Earlier-model evidence (9 November 2026):** the then top-level models implemented this
plan. These checks do not establish results for the selected edited pair. AS-IS has 12 overview nodes and four subprocess detail diagrams; TO-BE has
13 overview nodes and three detail diagrams. Assessment/phone choice, scheduling,
travel and on-site work remain in editable detail. TO-BE retains registration,
context retrieval, AI assessment and deterministic DMN routing inside triage.
The visit returns to technician review without repeating case creation.

Both files pass the official BPMN 2.0 XSD, unique-ID/reference checks,
sequence-flow scope and incoming/outgoing consistency checks. Every flow node is
reachable from a start and has a path to an end within its process/subprocess.
These structural checks do not establish routing-policy correctness.

The earlier AS-IS and TO-BE overview previews used A4 landscape
dimensions (297 × 210 mm), 9.5-point activity labels and 9-point secondary text.
Both earlier rendered PNGs were visually inspected for clipping, shape overlaps and arrow
routes; automated text-fit checks reported no warnings. Those earlier previews were derived
from the XML overview layout; current stable preview filenames refer to the selected pair. Camunda UI import, subprocess navigation and physical
print legibility remain unverified. Quantified cost/benefit evidence and group
acceptance of the proposed process remain outstanding. No application code changed.
