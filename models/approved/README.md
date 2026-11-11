# Approved P1 process models

These BPMNs define the prototype workflow. The published case and group paper retain
their respective source and business scopes. Workflow approval does not establish
agronomic validity or implementation completion.

| Editable model | Current SHA-256 |
| --- | --- |
| [AS-IS-BPMN.bpmn](AS-IS-BPMN.bpmn) | `0f976373877ff5229b514a2d1eb7202edc721ebafe44e1390cff9de3f2f5170f` |
| [TO-BE-BPMN.bpmn](TO-BE-BPMN.bpmn) | `d28b8bf1f16e98a481f5e366e4c5a9026fbff764d93fc4e94ca74318cfc76ace` |

The approved TO-BE retains separate routine and technician paths, formal recording
and the visit-to-review loop. Its technical review always determines whether a visit is needed and also provides
preliminary guidance when available, using an inclusive split/join. Optional P2/P3 message
referrals are human-controlled handovers, not automatic orders or pickup cancellation.
Visit findings have separate human entry and automated saving to case history.

Open these BPMNs in the modeller for their approved layout and subprocesses.
[Process trace and prototype boundaries](NOTES.md) explain the source mapping and
remaining implementation gaps. No generated preview or Camunda-import claim is made.

Import checks: both files parse as XML; IDs are unique, references resolve and sequence
flows stay within their process/subprocess. Full XSD, inclusive-gateway execution,
Camunda navigation and print checks have not been rerun for this pair.
