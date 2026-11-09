# Current work

PHASE: 0
STATUS: in-progress

## Active objective

Bootstrap the Cooxupé P1 prototype from the AI-SDLC template without implementing
unagreed business policy. No active use case yet; bootstrap is tooling/context work.

## Current slice

Project identity, source map, Python/FastAPI environment and inherited checks.

## Acceptance / validation cues

- Project documents distinguish implemented scaffold from proposed capabilities.
- References resolve locally and identify authority and open policy questions.
- Template identity is removed, attribution retained and project code licensed MIT.
- Setup and full handoff checks pass; record evidence below.

## Decisions and remaining work

Ayla approved MIT and template cleanup. Python/FastAPI follows the discussed profile.
First-slice decisions: provider access and image timing; routing/review criteria and
rule artifact/execution; whether a narrow MCP integration is needed. These do not
block environment setup, but behavior must be agreed before implementation.

## Evidence

Verified 9 November 2026:
- `bash scripts/check-setup.sh`: passed; Codex skill link and local Python environment resolve.
- `bash scripts/test.sh`: passed; lifecycle scenarios, 46 tooling tests and 3 pytest tests.
- Project navigation/source link check: passed; references use the surrounding folder.
- `git diff --check`: passed.

Corrected inherited setup path duplication and isolated licence/README regression
fixtures from project-specific content. Human review of bootstrap changes remains
outstanding; phase stays in-progress for that review.

## Next smallest step

Review bootstrap, then select SPECIFY for UC-001: assess and route one text report,
with explicit handling of unavailable history, invalid model output and model failure.

## Backlog

1. Assess and route one report with real LLM analysis and traceable rule output.
2. Advisory evidence view, review/corrections and simulated guidance/handover.
3. Synthetic field scenarios, duplicate handling and experiment export.

Implementation owner: [working agreement](WORKING-AGREEMENT.md).
Source scope: [project context](PROJECT.md) and [source map](reference/README.md).
