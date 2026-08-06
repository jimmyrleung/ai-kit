---
description: Run the audit phase of the refactoring/tech-debt workflow — codebase analysis + scope definition + risk classification, then a review pass — without committing to the full plan/tasks workflow.
argument-hint: File with high-level description of the refactor/tech debt.
---

# Goal

- Thoroughly understand the codebase area being refactored.
- Produce a reviewed audit (scope, dependencies, risks, anti-patterns) that's solid enough to plan against.

This command is the standalone Phase 1 + Phase 2 of `/refactor-techdebt-dev`. Use it when you want the audit (and its review) on its own — e.g. when you're not sure the work is worth doing yet, or when you'll plan + break down tasks manually afterward. For the full workflow (audit → review → plan → tasks), use `/refactor-techdebt-dev`.

## Process

### Phase 1 — Audit

Use the `refactor-audit` skill with:

- the refactor description (`$ARGUMENTS`) as the input,
- `{refactor_name}` derived from the description's filename,
- breadth hint: the skill may launch 1–3 `audit-agent` sub-agents.

The skill handles the clarification questions, codebase exploration, dependency mapping, scope definition, risk classification, consolidation (consensus / disagreement / confidence-weighted findings), the ≥ 90% confidence gate, and writing `{refactor_name}_audit.md`.

When the skill hands back, proceed to [Phase 2].

### Phase 2 — Review Audit

Use the `review-artifact` skill with:

- `artifact_path`: `{refactor_name}_audit.md`
- `artifact_label`: `audit`
- `reviewer_agent`: `audit-reviewer-agent`
- `creator_agent`: `audit-agent`
- `support_docs`: the refactor description (`$ARGUMENTS`)
- `next_step`: end-of-command (plan/tasks are deferred to a follow-up — `/refactor-techdebt-dev` for the full workflow, or invoke `refactor-plan` and `refactor-tasks` ad-hoc once you're ready)

When the skill hands back, this command is complete. The reviewed audit is in `{refactor_name}_audit.md` (with a `## Review` section appended).
