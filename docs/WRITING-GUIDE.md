# Clear, concise project writing

Use this guide when drafting or shortening requirements, plans and agent handoffs.
Use the existing UC and ADR templates for those artefacts; use the
[task-plan template](templates/TASK-PLAN.md) for bounded supporting work.
The [open-data plan](reference/OPEN-DATA.md) is a worked example.

## Preserve the decision

Before rewriting, identify what the reader must know to act correctly:

| Element | Preserve |
| --- | --- |
| Outcome | The observable result and why it matters |
| Requirement | What must happen, with its source or decision authority |
| Condition / exception | When it applies, when it does not, and which rule wins |
| Boundary | Limits, exclusions and deliberately deferred behavior |
| Uncertainty | What is unknown, its consequence and the next way to resolve it |
| Evidence | The checks and artefacts needed to establish completion |

Distinguish requirements, proposals, working assumptions and verified results.
Link the authority for shared facts instead of maintaining competing copies.
A recommendation can include a reason and proceed under an explicit working
assumption; unresolved choices block only the behavior they materially affect.
Follow existing approval rules rather than creating new review gates here.

## Write for action

- State the outcome first. Add background only when it explains a requirement,
  choice or consequence the reader needs for this task.
- Put one independently checkable requirement in each item. Keep its conditions
  and exceptions beside it; give stable IDs when several checks need to refer to it.
- Name the actor, input and observable result. Define terms that affect behavior.
  Replace “handle appropriately” with the action or explicit unresolved choice.
- Use headings matching the reader's questions and tables for parallel comparisons.
  Keep technical detail when it changes implementation or validation.
- Separate completion criteria from results. Record actual passes, failures and
  unavailable checks; planned checks are not evidence that work is complete.

## Review a rewrite

Compare the rewrite with the source, not just for readability. Account for every
requirement, condition, exception, precedence rule, boundary and completion check:
it is retained, linked to its authority, or explicitly deferred/superseded by a
named decision. Shortening alone never authorizes changing scope or meaning.

Check that a reader can tell what to do, what remains uncertain, what can proceed
and how to verify completion without needing the brainstorming conversation.
Use a short preservation checklist in the review or handoff; keep historical
rewrite commentary out of the maintained document.

## Example

Vague: “Validate the field images and use suitable labels.”

Actionable: “Before scoring diagnosis, record the image's source and reference
label. A leaf outline is not a disease label. If disease labels are unavailable,
use the image for upload/context testing only; diagnosis scoring remains pending.”
