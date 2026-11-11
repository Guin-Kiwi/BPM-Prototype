# Approved P1 process models

Ayla identified `AS-IS-BPMN.bpmn` and `TO-BE-BPMN.bpmn` in the surrounding
project folder as the approved pair on 11 November 2026. These repository copies
preserve their exact bytes and are the workflow authority for prototype alignment.
The published case and working paper retain their respective source/business scopes.
Approval selects the process models; it does not validate agronomic thresholds,
prove model accuracy or establish application completion. Embedded proposal caveats
remain unchanged rather than editing the approved artifacts.

| Editable model | SHA-256 at import |
| --- | --- |
| [AS-IS-BPMN.bpmn](AS-IS-BPMN.bpmn) | `ad932599ced7712e2ce1f82b8815fbad7f7f1b58bde17c3a031014f3792eb3bf` |
| [TO-BE-BPMN.bpmn](TO-BE-BPMN.bpmn) | `3b4e67360858369af26c3d0e6c6bc02188c600229e8c5affd3083cd72587bdfe` |

The approved TO-BE retains separate routine and technician paths, formal recording
and the visit-to-review loop. Its technical review permits preliminary guidance,
visit determination or both through an inclusive split/join. Optional P2/P3 message
referrals are human-controlled handovers, not automatic orders or pickup cancellation.
Visit findings have separate human entry and automated saving to case history.

Open these BPMNs in the modeller for their approved layout and subprocesses.
[Process trace and prototype boundaries](NOTES.md) explain the source mapping and
remaining implementation gaps. No generated preview or Camunda-import claim is made.

Import checks: both files parse as XML; IDs are unique, references resolve and sequence
flows stay within their process/subprocess. Full XSD, inclusive-gateway execution,
Camunda navigation and print checks have not been rerun for this pair.
