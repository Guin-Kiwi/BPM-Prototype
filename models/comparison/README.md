# P1 AS-IS / TO-BE comparison proposals

Start with the previews, then open the editable models in your BPMN modeller.
Original group files remain unchanged. These are proposals for review, not approved
submission models or executable workflows.

| Model | Preview | Editable BPMN | Scalable A4 landscape image |
| --- | --- | --- | --- |
| P1 AS-IS | [PNG](p1_asis.png) | [BPMN](p1_asis.bpmn) | [SVG](p1_asis.svg) |
| P1 TO-BE | [PNG](p1_tobe.png) | [BPMN](p1_tobe.bpmn) | [SVG](p1_tobe.svg) |

[Comparison and source notes](NOTES.md) explain assumptions, the original TO-BE
comparison, scoped-out handovers and remaining lecturer questions. The cloud AS-IS
was unavailable; the new AS-IS is reconstructed from the working paper's P1 activity
analysis and explicitly labelled assumptions.

The TO-BE depicts the intended process, beyond the currently implemented intake.
It keeps routine reports independent of technician cases, makes context and human
communication explicit, and records guidance without assuming the issue is resolved.

## Verification

Both files passed the official OMG BPMN XML schemas and reference/scope checks;
SVG/PNG previews were visually inspected. These checks do not validate agronomic
policy, establish actual Cooxupé operating practice or replace modeler/print review.
The AS-IS has message start, intermediate timer and end events. Confirm whether the
rubric requires three event types in every individual diagram; the TO-BE core has no
artificial timer. Detailed severe-action approval remains outside the core diagram.

## Regeneration

`process-definitions.json` is the editable generation source; `build_diagrams.py`
produces XML/DI and previews with `lxml` and `cairosvg`. Install those in a separate
tooling environment, not the application requirements. Schema validation requires
the official `BPMN20.xsd`, `Semantic.xsd`, `BPMNDI.xsd`, `DC.xsd` and `DI.xsd` from
https://www.omg.org/spec/BPMN/20100501/ in `/tmp/cooxupe-bpmn-xsd/`; without them
the generator explicitly reports the schema check as not run. Editing BPMN directly
in a modeller is supported; do not regenerate over those edits without reconciling
the generation source. No deployment or engine execution is provided.
