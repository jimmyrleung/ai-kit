---
description: Start the refactoring/tech debt process to help a developer accomplish that in an existing codebase (intended for small to medium size refactors).
argument-hint: File with high-level description of the refactor/tech debt.
---

# Goal

- Thoroughly understand what needs to be refactored and/or what tech debt needs to be tackled.
- Craft a detailed refactoring plan with rollback points and success metrics.
- Break down the refactoring plan into implementation tasks.
- Create the tasks document for future implementation.

Intended for **small-to-medium** refactors — large/extra-large work routes to the detailed per-command workflow.

This command is a thin orchestrator: each phase invokes a skill that owns the methodology, output contract, and confidence gate. The orchestrator owns only the **workflow-specific glue** — the high-risk preamble, risk gates at each phase transition, abort criteria, success metrics required before planning, the anti-perfectionism block, the rollback decision tree, the post-refactor validation, the quality-gate table, and the output manifest.

## Critical Mindset: Refactoring is High-Risk

**Refactoring breaks things.** Unlike new features (additive) or bug fixes (targeted), refactoring touches working code and can introduce regressions across the system. This workflow has explicit risk gates and abort criteria — they are the reason it's a workflow, not just a skill.

### Risk Gates (Check at Each Phase Transition)

Before proceeding to the next phase, verify:

1. **Risk level is acceptable** — If risk is HIGH or CRITICAL, pause and get explicit user approval
2. **Blast radius is contained** — Changes affect only the intended scope
3. **Rollback is viable** — You can undo changes without data loss
4. **Tests exist** — Sufficient test coverage to catch regressions

### Abort Criteria (When to Stop Entirely)

**STOP the refactor and escalate to user if:**

- Risk level escalates to CRITICAL during any phase
- Discovered scope is 3x+ larger than initially estimated
- Core assumptions from the audit prove incorrect
- Required test coverage cannot be achieved before changes
- Dependencies on external systems make rollback impossible

### Success Metrics (How to Know the Refactor Worked)

Define these BEFORE starting Phase 3 (Planning):

| Metric              | How to Measure                          | Target               |
| ------------------- | --------------------------------------- | -------------------- |
| **Code Quality**    | Cyclomatic complexity, duplication %    | Reduced by X%        |
| **Test Coverage**   | Line/branch coverage of refactored code | ≥ 80%                |
| **Performance**     | Response time, memory usage             | No regression (± 5%) |
| **Maintainability** | Time to make a typical change           | Reduced by X%        |
| **Dependencies**    | Coupling between modules                | Reduced by X imports |

**Important:** If you can't define success metrics, the refactor goal is too vague. Go back and clarify.

### When to Stop Refactoring (Avoid Perfectionism Trap)

Refactoring is "done" when:

1. ✅ **Original pain points are addressed** — the specific problems in the request are solved
2. ✅ **Success metrics are met** — measurable targets achieved
3. ✅ **Tests pass** — all existing + new tests green
4. ✅ **Code review approved** — changes reviewed by team

**STOP even if:**

- ❌ You see other improvements you could make
- ❌ The code isn't "perfect"
- ❌ There's more tech debt nearby
- ❌ You want to refactor "just one more thing"

**Rule of thumb:** If a change wasn't in the original scope, it goes into a NEW refactoring request.

## Process

Create a todo list with all phases, then go through them in order.

### Phase 1 — Audit

1. Read the refactor description in `$ARGUMENTS` and classify its scope:
   - **S** (small) — single module, few files
   - **M** (medium) — multiple modules, moderate complexity
   - **L** (large) — system-wide, significant complexity
   - **XL** (extra large) — architectural change, high risk
2. If **L or XL**: recommend the detailed per-command workflow instead — `/audit-refactor-techdebt` → (review pass) → manual planning + task breakdown phase-by-phase — and stop here.
3. Otherwise, use the `refactor-audit` skill with:
   - the refactor description (`$ARGUMENTS`) as the input,
   - `{refactor_name}` derived from the description's filename,
   - the scope (S vs M) as a hint for breadth (S: do it on the main thread; M: the skill may launch 1–3 `audit-agent` sub-agents).

   The skill handles the clarification questions, codebase exploration, dependency mapping, scope definition, risk classification, consolidation (consensus / disagreement / confidence-weighted findings), the ≥ 90% confidence gate, and writing `{refactor_name}_audit.md`.

**Risk Gate Check:**

- If risk level is **HIGH**: present risk summary to user, get explicit approval to continue.
- If risk level is **CRITICAL**: recommend aborting or descoping. Do not proceed without user acknowledgment of the risks.
- If scope is L or XL: recommend the detailed workflow instead.

Proceed to [Phase 2] only after the risk gate passes.

### Phase 2 — Review Audit

Use the `review-artifact` skill with:

- `artifact_path`: `{refactor_name}_audit.md`
- `artifact_label`: `audit`
- `reviewer_agent`: `audit-reviewer-agent`
- `creator_agent`: `audit-agent`
- `support_docs`: the refactor description (`$ARGUMENTS`)
- `next_step`: `Phase 3 — Plan Refactor`

When the skill hands back, run the **Risk Gate Check** below, then proceed to [Phase 3].

**Risk Gate Check:**

- If the review found significant new risks: re-assess risk level and present to user.
- If scope expanded significantly (> 30% more files/changes): flag for user decision — continue or descope?
- Check abort criteria: is scope now 3x+ original? Are core assumptions still valid?

Proceed to [Phase 3] only after the risk gate passes.

### Phase 3 — Plan Refactor

**Pre-phase requirement:** Before planning, ensure success metrics are defined. Ask the user:

- "What specific metrics will prove this refactor succeeded?"
- "What is the minimum acceptable improvement?"

If the user cannot define metrics, the refactor scope is too vague — **go back to audit**.

Once success metrics are agreed, use the `refactor-plan` skill with:

- the refactor description (`$ARGUMENTS`) and the reviewed `{refactor_name}_audit.md` from Phase 2 as inputs,
- the user's success metrics,
- `{refactor_name}` as before.

The skill launches 1–3 `refactoring-planner-agent` workers in parallel (3-way: **minimal-risk / clean-architecture / pragmatic-balance**), consolidates trade-offs, presents the comparison + recommendation to the user, takes the user's choice, runs the ≥ 90% confidence gate, and writes `{refactor_name}_plan.md` with phases (each with goal, duration, changes, rollback point, success criteria), impact analysis, testing strategy, rollback strategy, and risk mitigation.

**Risk Gate Check:**

- Verify rollback strategy is viable for **every** phase in the plan.
- If any phase has no viable rollback: flag to the user, consider feature flags or an incremental approach.
- If the plan requires database migrations: extra scrutiny — data rollback is often impossible.
- Confirm success metrics are baked into the plan.

Proceed to [Phase 4] only after the risk gate passes.

### Phase 4 — Break Down Into Tasks

Use the `refactor-tasks` skill with:

- the refactor description (`$ARGUMENTS`), the reviewed `{refactor_name}_audit.md`, and the approved `{refactor_name}_plan.md` as inputs,
- `{refactor_name}` as before.

The skill launches 1–3 `refactoring-tasks-creator-agent` workers in parallel (3-way: **granular / balanced / pragmatic**), consolidates trade-offs, presents the comparison + recommendation to the user, takes the user's choice, runs the ≥ 90% confidence gate, and writes `{refactor_name}_tasks.md` (overview table + dependency graph + per-task detail with rollback + testing requirements).

When the skill hands back, this command is complete — implementation begins.

## Output Documents

At the end of this workflow you should have created (alongside the refactor description):

1. `{refactor_name}_audit.md` — comprehensive audit of the codebase (reviewed; carries a `## Review` section)
2. `{refactor_name}_plan.md` — detailed refactoring plan with phases and rollback strategies
3. `{refactor_name}_tasks.md` — implementation tasks with dependencies and acceptance criteria

Each document should include:

- **Risk level** (current assessment)
- **Success metrics** (how to measure completion)
- **Rollback strategy** (how to undo if needed)

## Quality Gates

| Transition     | Confidence | Risk Gate                          | User Approval |
| -------------- | ---------- | ---------------------------------- | ------------- |
| Phase 1 → 2    | ≥ 90%      | Risk ≤ HIGH (or explicit approval) | ✅ Required   |
| Phase 2 → 3    | ≥ 90%      | Scope not expanded > 30%           | ✅ Required   |
| Phase 3 → 4    | ≥ 90%      | Rollback viable for all phases     | ✅ Required   |
| Phase 4 → Done | N/A        | N/A                                | ✅ Required   |

## Rollback Decision Tree

During implementation, use this decision tree:

```
Task fails or causes issues
├─ Affects only this task? ──────→ Rollback task, investigate, retry
├─ Affects other completed work? ─→ Rollback to last stable phase
└─ Affects production data? ──────→ STOP. Assess damage. May need incident response.

Rollback triggers:
├─ Tests failing that passed before
├─ Performance degradation > 10%
├─ New errors in logs
├─ User-reported issues
└─ Confidence drops below 70%
```

## Post-Refactor Validation

After all tasks complete, verify:

1. **Success metrics met** — compare against targets defined in Phase 3
2. **No regressions** — all original tests still pass
3. **Performance acceptable** — within ± 5% of baseline (or improved)
4. **Code review complete** — changes reviewed by team member
5. **Documentation updated** — if APIs or patterns changed

**Only mark refactor complete when all validations pass.**
