# Current work

PHASE: 4
STATUS: in-progress

## Active objective

Complete the owner-selected six-step [UC-002 assessment and handoff](specs/UC-002-ASSESSMENT-HANDOFF.md)
work: reuse existing C/F and BPMN; define demonstration rules/scenarios; connect the
contained classifier and bounded LLM; record human handling in the app; run experiments;
prepare technical and cost/benefit evidence. The baseline is Cooxupé **before** the
published case's improvements. No leaf detector is being added; weather remains optional.

Current selected work is VALIDATE for the **supporting local-interpreter experiment**,
following its DEVELOP/TDD implementation and post-green review. This phase does not
mean UC-002's application journey has been implemented or completed. The sourced
observation direction is selected; interpreter agreement is not independent confirmation,
and missing issue links do not establish irrelevance. All available context remains
visible for human relevance judgment. Profiles are isolated-test fixtures only.

## Current Use Case

docs/specs/UC-002-ASSESSMENT-HANDOFF.md

## Existing implemented slice

Simulated farmer on farm-1; required uploaded photo, approximate affected-plant
estimate and usable browser GPS; optional text and area cue; simulated observation
time, separate receipt and fix time; farm-wide report history; legacy-preserving
SQLite migration with verified backup. Map fallback remains unavailable because no
field boundaries or map presentation are supplied. Routing, events, cases, AI,
authentication and dataset generation remain outside this slice.

## Evidence links

[Integration tests](../tests/integration/test_intake.py) and
[UC-001 DEVELOP evidence](specs/UC-001-REPORT-INTAKE.md#design--revised-prototype).

## Acceptance / validation cues

Targeted red: `.venv/bin/python -m pytest tests/integration/test_intake.py -q`
failed against the old implementation (5 failed, 15 passed). After implementation,
`.venv/bin/python -m pytest tests/integration/test_intake.py tests/unit/test_architecture.py -q`
passed (32 tests), including backup/restore and rollback on temporary databases.
Full handoff: `bash scripts/test.sh` passed lifecycle checks, 46 process tests and
32 pytest tests. A loopback Uvicorn startup against a temporary database shut down
cleanly under a three-second timeout (expected exit 124). No visual/manual browser
test has been performed.
Group paper/model alignment and human acceptance of the revised journey remain open.

## Next smallest step

Review the [existing-artifact alignment](reference/UC-002-ALIGNMENT.md),
[concrete demo-rule proposal](reference/UC-002-DEMO-RULES.md),
[prepared-guidance candidate](reference/UC-002-GUIDANCE-CANDIDATE.md) and
[acceptance/experiment plan](../experiments/assessment-handoff/README.md).
These are specifications and planned checks, not application results or approved
business policy. The user selected the bounded sourced observation demonstration and preserved the two
clarifications: interpreter agreement is not independent confirmation; no issue link
does not establish irrelevance. Two contained interpreter trials are complete; their output contract failed in all
12 responses. The next technical step is a reviewed local model/output-generation
comparison before app DESIGN/TDD, not weakening the contract. No owner
validation of agronomic rules or provider-detail choice is required for this proposal.

| Owner task | Current evidence / remaining work |
| --- | --- |
| Existing C/F and BPMN alignment | Primary case, group C/F table and selected XML models inspected; alignment draft linked above. No replacement matrix or group-model edits. |
| Demonstration rules and scenarios | Two sourced non-treatment observation messages and ordered model-output/history rules proposed. No hand-entered desired route or eligibility and no Rust=low-risk rule. |
| Classifier plus bounded LLM | [Contained classifier run](../experiments/local-classifier/RESULTS.md) completed; [Local LLM metadata candidate](../experiments/local-interpreter/README.md) [Contained interpreter results](../experiments/local-interpreter/RESULTS.md): loading/generation completed, 0/12 accepted outputs. Application adapter remains unimplemented. |
| Staff handoff and recording | UC-002 specifies it; no assessment, routing or handoff UI/storage implemented yet. |
| Actual workflow experiments | Experiment plan drafted; connected live model/UI runs remain outstanding. |
| Paper/presentation evidence and cost/benefit | Existing classifier evidence and a worked hypothetical cost comparison available in the experiment plan; end-to-end evidence and actual AI usage/cost remain outstanding. |

Classifier handoff checks passed lifecycle checks/scenarios, 47 process tests and
73 pytest tests; actual runtime inventory matched the 28 locked distributions.
The proposed LLM output contract now defines exact fields, bounds and warning guards;
routing uses actual output fields and synthetic history only. Local interpreter artifacts and runtime controls were verified in two trials; output
compliance and semantic usefulness remain unresolved (0/12 accepted responses). The experiment plan includes
a three-scenario arithmetic check, with every cost/time input labelled hypothetical.
Fresh baseline check: the existing intake and architecture command passed 32 tests
against temporary databases, as recorded in the experiment plan. SPECIFY checks passed
lifecycle validation, generated-view checks, local link/model-ID checks and whitespace
checks. Interpreter experiment full handoff passed 47 process and 134 pytest tests; 61 focused
protocol/guard tests passed. Terra/high completed post-green whole-file review; Luna/high
independently validates the actual runtime evidence. No UC-002 application tests, routing
results or live connected application runs are claimed.
These results establish their stated scopes only. Weather acquisition is a
separate optional check under the preserved [weather plan](reference/EVENT-WEATHER.md).

## Selected routing step

Ayla selected report-to-case routing as the next business specification step:
[consolidated routing worksheet](reference/DMN-RULE-WORKSHEET.md). This is the
prototype direction; the selected comparison pair is identified in the
[source map](reference/README.md), and group paper alignment remains pending.
The worksheet owns the terminology, routing proposal, open definitions and bounded
agent handoff. UC-001 remains intake/history only; no routing implementation yet.

## Deferred decisions / backlog

- Reconcile the proposed demonstration definitions and wider business policy with group
  models; clinical risk criteria and real-world validation remain outside current evidence. Preserve
  the [standalone assessment boundary](reference/DMN-RULE-WORKSHEET.md#assessment-and-routing-boundary):
  photo to image model; candidate scores, note and optional event weather to a proposed
  second model; extent and connected history to code/DMN. The [weather plan](reference/EVENT-WEATHER.md)
  records selected variables, sources, assumptions and open acquisition/window choices.
- Later code: AI/provider boundary, deterministic DMN, human guidance and case/visit
  workflows, technician view and traceable events/export. Map fallback needs known
  boundaries, provenance and usable presentation; manually verify the intake journey.
- Later data: inspect and attribute suitable image and illustrative guidance sources;
  design synthetic context and permissions without generating a dataset now.
- Later experiments: agree scenarios, reference truth, leakage controls and measured
  workload/outcomes; record actual runs. Offline capture remains a paper gap.

Implementation ownership: [working agreement](WORKING-AGREEMENT.md).
