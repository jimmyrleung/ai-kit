---
description: Create a pragmatic-balance technical specification for integrating a new feature in an existing codebase. Single-approach variant of /integration-create-techspec.
argument-hint: Prefix of files to read.
---

# Goal

Create a pragmatic-balance technical specification based on:

- Feature description file(s)
- Integration analysis file(s) — or, if none exists, a lighter implementation plan

This is the single-approach variant of `/integration-create-techspec`. It skips the minimal / clean / pragmatic parallel exploration and commits directly to pragmatic. Use it when:

- The feature is small-to-medium and the 3-way exploration would be overkill, OR
- You already know pragmatic is the right fit and don't want to re-decide per feature.

If the feature has architectural uncertainty where comparing approaches would genuinely help, use `/integration-create-techspec` instead.

## Process

**MUST DO**: Execute Workflows 1 and 2.

Workflow 1 produces the techspec directly using the `@pragmatic-techspec` skill. Workflow 2 hands the produced techspec to an independent subagent for a fresh-eyes review against the same skill's contract.

### Workflow 1 - Build (skill, main thread)

1. Create a todo list with all steps for this workflow.
2. Read the feature description and integration analysis files to get context (all files starting with `$ARGUMENTS`). If no integration analysis is present, proceed with the lighter implementation plan and note this to the user so the skill's input-contract gap-flagging kicks in.
3. Use the `@pragmatic-techspec` skill with the input files above. The skill handles:
   - Reviewing inputs and mapping existing patterns in the target codebase.
   - Running the confidence gate (≥ 90% before writing; < 90% stops and asks clarifying questions).
   - Producing the techspec content.
4. Before writing the file, spot-check `file:line` references in the "Patterns reused" table against the current codebase to confirm they were verified, not guessed. Fix any that don't resolve.
5. Write the techspec to `{feature_name}_techspec.md` alongside the feature description and integration analysis.

### Workflow 2 - Review (subagent, fresh eyes)

The review uses an independent subagent so the doc gets checked by someone that didn't write it. The subagent reviews against `@pragmatic-techspec`'s contract — not against its own creation-mode defaults.

1. Create a todo list with all steps for this workflow.
2. Launch a single `@integration-techspec-creator-agent` in **review mode** with a prompt that:
   - States the task is **review**, not creation — the agent must not rewrite the techspec, only produce a review list.
   - Names the exact files the agent must read: the techspec from Workflow 1, the feature description, and the integration analysis (or lighter plan, if that's what was used).
   - Points the agent at the `@pragmatic-techspec` SKILL as the authoritative contract for what the techspec should contain. This overrides the agent's own internal `[Process]` and `[Output Guidance]` sections.
   - Asks the agent to check specifically:
     - All 8 **required sections** are present (Summary, Approach, Scope, Patterns reused, Implementation, Test plan, Files changed summary, Confidence score).
     - No section from the skill's **Do not include** list has been added.
     - No required section is a placeholder — if empty, a one-sentence "why this section has no substance" explanation is present.
     - Every `file:line` ref in the Patterns reused table resolves to real code (verify by reading, not by searching).
     - Every requirement from the feature description / integration analysis has a home in the techspec (implementation, test plan, or explicit out-of-scope).
     - Every design decision is traceable to either a reused pattern or a documented rationale.
     - Confidence score follows the global CLAUDE.md format: numeric score, "Why X%" bullets, "X% uncertainty" bullets.
   - Asks for a structured review output: misunderstandings, gaps, unverified `file:line` refs, violated section rules, unsupported claims, confidence-score gaps — plus a numeric reviewed-confidence score.
3. When the agent returns, read its review output and consolidate it into a single actionable list.
4. Confirm the list with the user before applying changes. Only edit the techspec after approval.
5. Ensure the post-review confidence score is ≥ 90% before completing.
6. Update the techspec to incorporate the approved review changes.
