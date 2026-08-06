---
description: Start the feature integration analysis process to help a developer to implement a new feature in an existing codebase.
argument-hint: File with high-level description of the feature to be built.
---

# Goal

Thoroughly understand what needs to be built — produce a reviewed integration analysis (a reference map of the codebase, not a design document).

This command is a thin shim: the `integration-analysis` skill owns the methodology and output contract; `review-artifact` owns the review sub-phase.

## Process

**MUST DO**: Execute Workflows 1 and 2.

### Workflow 1 — Initial Analysis (skill)

1. Create a todo list with all steps for this command.
2. Use the `integration-analysis` skill with:
   - the feature description in `$ARGUMENTS` as the requirement,
   - output file `{feature_name}_integration.md` (alongside the feature description).

   The skill handles the mandatory clarification questions, codebase exploration and code-flow tracing, consolidation (consensus / disagreement / confidence-weighted integration points — launching 1–3 `integration-analysis-agent` sub-agents for breadth where useful), the ≥ 90% confidence gate, and writing the file. It will not produce a design document — the litmus test is in the skill.

### Workflow 2 — Review Analysis (review-artifact)

Use the `review-artifact` skill with:

- `artifact_path`: `{feature_name}_integration.md`
- `artifact_label`: `integration analysis`
- `reviewer_agent`: `integration-review-agent`
- `creator_agent`: `integration-analysis-agent`
- `support_docs`: the feature description document written by the user
- `next_step`: end of command — no further phase

When the skill hands back, this command is complete.
