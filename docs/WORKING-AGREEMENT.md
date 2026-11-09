# Working agreement

Team conventions; humans and agents both follow this file; change it by team agreement.

## Workflow
| Topic | Agreement |
| --- | --- |
| Solo or team | Ayla owns prototype implementation; this supports a group coursework submission. Sarah and Ayla review business alignment and evaluation conclusions. |
| Branches | Solo bootstrap work is committed directly to `main`, as authorized by Ayla. Other tooling branches use `chore/<short-name>`. One use case per branch and per PR, named `uc-NNN-<short-name>` (lowercase, same NNN as the UC file). |
| Review and merge | Ayla reviews and authorizes prototype merges. Do not assume a second code reviewer is available. GitHub ruleset enforcement has not been verified; imported requirements still apply if enabled. |
| Shared files | Shared files (`AGENTS.md`, `docs/PROJECT.md`, `docs/INDEX.json`, `.github/`) stay separate from feature work; solo bootstrap may include them directly on `main`. Otherwise use their own small PR. |

## Conventions
| Topic | Agreement |
| --- | --- |
| Decision records | Record a consequential decision that is hard to reverse or spans use cases (e.g. data store, auth approach, framework, a break in the layer rules) in an ADR; otherwise, record it in the use case. |
| UC numbering | The issue number zero-padded to three digits (issue #42 → 042), otherwise the next sequential number (001, 002, …). |

## ADR proposals and acceptance

Humans and agents may propose decisions; record the proposer. Exploratory ideas
remain Proposed. In solo work, an explicit owner decision counts as acceptance;
a request to explore an option does not.

Prepare PR documents to describe the resulting merged state. An ADR submitted
for acceptance may say Accepted on the branch; designated secondary human review
and merge establish acceptance in teamwork. No separate ADR approval or later
status-only PR is required. Review evidence belongs to the PR; do not invent an
approver or approval date before review occurs.

If the reviewer selects another option, align the Decision and Consequences
before merge. Approval covers the reviewed decision. This resulting-state
convention does not turn unrun or failed checks into successful validation.

## Coursework delivery

Ayla builds and fixes the prototype. Peter and Toby prepare scenarios, run experiments
and produce evaluation/cost-benefit evidence. Sarah integrates the report. Sarah and
Ayla review their conclusions. This division does not authorize changing group policy:
unresolved routing and review criteria require group agreement against the paper/models.

Use synthetic farm histories and licensed sample data with source manifests. Keep
credentials and unselected raw experiment outputs out of git. Live model experiments
are deliberate runs with model/prompt/rule versions and actual results recorded.
