---
description: Create a detailed technical specification for integrating a new feature in an existing codebase.
argument-hint: Prefix of files to read.
---

# Goal

Create a reviewed technical specification by exploring three approaches in parallel — minimal-changes / clean-architecture / pragmatic-balance — and committing to one, based on:

- Feature description file(s)
- Integration analysis file(s)

(For a small feature where the 3-way comparison would be overkill, use `/integration-pragmatic-techspec` instead — it commits directly to pragmatic.)

This command is a thin shim: the `integration-techspec` skill owns the 3-way exploration, the consolidation, and the output contract; `review-artifact` owns the review sub-phase.

## Process

**MUST DO**: Execute Workflows 1 and 2.

### Workflow 1 — Build (skill)

1. Create a todo list with all steps for this command.
2. Read the feature description and integration analysis files (all files starting with `$ARGUMENTS`) to get context.
3. Use the `integration-techspec` skill with those inputs. The skill handles: launching the three `integration-techspec-creator-agent` variant workers (minimal-changes / clean-architecture / pragmatic-balance), comparing them, presenting the trade-offs and a recommendation, asking which approach you prefer, mapping existing patterns, the ≥ 90% confidence gate, and writing `{feature_name}_techspec.md`.

### Workflow 2 — Review Techspec (review-artifact)

Use the `review-artifact` skill with:

- `artifact_path`: `{feature_name}_techspec.md`
- `artifact_label`: `techspec`
- `reviewer_agent`: `integration-techspec-creator-agent` (review mode — review the existing techspec against the `integration-techspec` contract, don't author a new one)
- `creator_agent`: `integration-techspec-creator-agent`
- `support_docs`: the feature description document; the integration analysis document
- `next_step`: end of command — no further phase

When the skill hands back, this command is complete.
