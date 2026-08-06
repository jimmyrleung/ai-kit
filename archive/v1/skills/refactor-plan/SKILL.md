---
name: refactor-plan
description: Produce a phased refactoring plan from a reviewed audit by exploring three approaches in parallel — minimal-risk / clean-architecture / pragmatic-balance — then committing to one with the user. Each phase has rollback points, success metrics, and testing strategy. Produces {refactor_name}_plan.md. Use ad-hoc, or as Phase 3 of /refactor-techdebt-dev.
---

# Refactor Plan Skill (3-way exploration)

You take a *reviewed* audit and produce a detailed, phased implementation plan with clear rollback points, success metrics, and a testing strategy. Refactoring breaks things — every phase needs a viable rollback and measurable success. This skill explores three approaches side by side and then commits to one with the user.

> **Litmus test:** if your plan has a phase without a rollback path, or a "success criterion" you can't measure, you're not done. Refactoring is high-risk by definition; the plan exists so the implementation is *safe*, not just possible.

## When to use

- **Ad-hoc**: you have a reviewed audit and need a phased plan with rollback and success metrics.
- **Orchestrated**: Phase 3 of `/refactor-techdebt-dev`.

## When NOT to use

- The audit isn't done / reviewed yet — run `refactor-audit` (and the orchestrator's `review-artifact` pass) first.
- Success metrics cannot be defined — if the user can't say what "this worked" means, the refactor scope is too vague; go back to audit.
- You want to break work into tasks — that's `refactor-tasks`, after the plan is approved.

## Coordinator vs worker

- **No mandate handed to you (default — you're on the main thread):** you're the *coordinator*.
  1. Read the inputs (refactor description + reviewed audit + any review notes) end to end.
  2. **Confirm success metrics with the user before planning.** Ask: "What specific metrics will prove this refactor succeeded?" and "What is the minimum acceptable improvement?" If the user cannot define metrics, **stop and return to audit** — the scope is too vague.
  3. Launch **1–3 `@refactoring-planner-agent` sub-agents in parallel**, each handed the inputs and one mandate:
     - **minimal-risk** — safest path, smallest changes, maximum backward compatibility.
     - **clean-architecture** — ideal end state, proper patterns, maintainability.
     - **pragmatic-balance** — speed + quality; acceptable trade-offs; ships safely.
  4. When they return, compare the three. Form your own opinion on which fits *this* refactor, considering: scope, urgency, risk tolerance, team context.
  5. Present to the user: a brief summary of each approach, a trade-offs comparison, your recommendation with reasoning, and the concrete implementation differences.
  6. Ask the user which approach they prefer.
  7. Build the final plan for the chosen approach (folding in anything worth keeping from the others), run the confidence gate, and write the file.
- **You were spawned as a `@refactoring-planner-agent` worker with a mandate:** you're a *worker*. Build the phased plan **for your assigned mandate only** and return your draft to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

## Input contract

Expect, in order of authority:
1. **Reviewed audit** (`{refactor_name}_audit.md` — the orchestrator's review phase updates it in place; look for its `## Review` section) — authoritative for scope, files affected, dependencies, risks. **Required.** If the audit isn't reviewed yet, say so and stop.
2. **Refactor description** — the requirement (pain points, desired end state, constraints, baseline metrics).
3. **Success metrics from the user** (gathered above) — required before you can plan.

Derive the `{refactor_name}` base name from the inputs; ask if not discoverable.

## Process (per approach — what each worker does, and what the coordinator does for the final)

1. **Understand the full context.** Re-read all pain points + the desired end state; absorb every dependency / constraint / risk in the audit.
2. **Design the refactoring approach for your mandate.** Choose appropriate patterns (e.g. strangler fig, branch-by-abstraction, big-bang, incremental). Plan the transition strategy. Consider backward compatibility. Design rollback mechanisms (feature flag? git revert? data migration with down-script?).
3. **Define phases.** Each phase must:
   - Deliver value **or** reduce risk on its own.
   - Be deployable independently.
   - Have a clear rollback point with method, data plan, and trigger.
   - Build on prior phases.
4. **Plan the testing strategy.** Identify test gaps (from the audit). Plan new unit / integration / E2E tests. Define the integration scenarios. Set test-coverage goals (current → target, with critical paths at 100%).
5. **Set success metrics.** Use the user's metrics + the audit's findings: code quality (complexity, duplication), test coverage (line/branch), performance (response time, memory), maintainability, dependencies (coupling). Each metric has a how-to-measure and a target.
6. **Plan the rollback strategy.** Immediate (< 5 min, git revert / feature flag toggle), data (forward + backward migrations), feature flags (named, with monitoring), and the decision tree (success → continue / minor → fix forward / major → rollback). If any phase has *no* viable rollback, flag it loudly — consider feature flags or incremental approach. If the plan requires DB migrations, apply extra scrutiny (data rollback is often impossible).
7. **Assess risks.** High-risk areas: probability + impact + mitigation + contingency-if-mitigation-fails. Unknowns: what needs investigation.
8. **Coordinator: present approaches & gate.** Present to the user: brief summary of each approach, trade-offs comparison, your recommendation, concrete differences. Ask which to take. Build the final plan.
9. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (≈ audit completeness 30% / pattern fit 25% / rollback viability 20% / metrics measurability 15% / risk realism 10%). **If < 90%: STOP and ask clarifying questions.** At ≥ 90%, present the consolidated plan to the user and ask if it's OK to proceed (to Phase 4 — tasks — or end-of-command); on confirmation, write the file.

## Required sections

The final plan includes:

- **Executive summary** — 2–3 sentences on the approach, plus:
  - **Refactor Level**: Low / Medium / High / Critical
  - **Number of phases**, **Estimated timeline**, **Deployment strategy** (all-at-once / phased / feature-flagged / canary).
- **Confidence score** — global CLAUDE.md format.
- **Refactoring approach** — name the chosen approach (minimal-risk / clean-architecture / pragmatic-balance) and why it won here, in one short paragraph. Key decisions (with reasoning). Patterns to follow / patterns to avoid.
- **Implementation phases** — for each phase: Goal, Duration, Changes, Dependencies (Requires / Blocks), **Rollback Point** (Method / Data / Trigger), **Success Criteria** (checklist).
- **Impact analysis** — side effects (per area + mitigation), performance impact (expected / acceptable range / how to measure), user impact (visible changes / behaviour / migration needed).
- **Testing strategy** — existing tests (expected behaviour, tests that need updates with file references, transitional failures), new tests required (unit / integration / E2E, each with location and what it covers), and test coverage goals (current → target, critical-path 100%).
- **Rollback strategy** — Immediate (< 5 min), Data (forward + backward migrations + how tested), Feature flags (name, toggle command, monitoring), Rollback decision tree.
- **Risk mitigation** — High-risk areas (probability / impact / mitigation / contingency), Unknowns.

## Optional sections (include only with substance)

Deployment sequencing (when order matters across services) · Communication plan (when stakeholders or oncall must be in the loop) · Open technical questions (only if you proceeded with user-approved residual uncertainty).

**Rule:** if a section has no substance, delete it — don't leave a placeholder.

## Important rules

1. **Safety first** — every phase needs a rollback plan.
2. **Incremental progress** — no "big bang" unless absolutely necessary.
3. **Measure everything** — if you can't measure it, you can't verify success.
4. **Plan for failure** — assume something will go wrong.
5. **Keep it realistic** — don't over-promise on timelines or scope.

## Output file

Write the final plan to `{refactor_name}_plan.md`, alongside the refactor description and audit. If no base name is discoverable, ask the user before writing. Confirm the consolidated plan with the user before writing, and ask whether it's OK to proceed to the next phase (the orchestrator's tasks phase, or end-of-command). (Workers return drafts and write nothing.)
