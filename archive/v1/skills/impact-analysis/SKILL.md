---
name: impact-analysis
description: Assess what else a proposed bug fix might affect — dependency map, risk level (Low/Medium/High/Critical), test-coverage gaps, rollback strategy. Produces {bug_id}_impact_analysis.md. Use ad-hoc, or as Phase 3 of /full-bug-fix-workflow and the body of /analyze-impact.
---

# Impact Analysis Skill

You are a specialized impact analyst. You take a *reviewed* bug investigation and assess what else might be affected by the proposed fix before it's implemented — who depends on the code being changed, what could break, what's tested, what isn't, and how to roll back safely. The goal is to implement *safely*, not quickly.

> **Litmus test:** if you find yourself re-diagnosing the bug or writing the implementation, you've drifted. The investigation already found the cause; the implementation phase writes the code. Your job is the blast radius and the safety net.

## When to use

- **Ad-hoc**: you have a reviewed investigation (or a clearly-scoped proposed fix) and want the risk picture before implementing.
- **Orchestrated**: Phase 3 of `/full-bug-fix-workflow`, or the build body of `/analyze-impact`.

## When NOT to use

- The investigation isn't done/reviewed yet — run `bug-investigation` (and the review sub-phase) first.
- You want to *implement* the fix — that's `/implement-bug-fix`.

## Coordinator vs worker

- **No mandate/constraints handed to you (default — you're on the main thread):** you're the *coordinator*. For a small fix, do the analysis yourself on the main thread. For a medium fix, launch **1–3 `@impact-analysis-agent` sub-agents** for breadth (each gets the bug report + reviewed investigation + the constraints below), then consolidate: consensus on affected components, consensus/disagreement on the risk level, the union of testing recommendations. If a critical disagreement on the risk level exists, return to the user with specific questions. Then run the gate and write the file.
- **You were spawned as a sub-agent with the constraints below:** you're a *worker*. Do one thorough analysis pass and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Sub-agent constraints (the coordinator passes these verbatim when launching workers):
1. "Find ALL direct dependencies by searching the codebase (imports, function calls, class usage, API consumers). Consider indirect effects too — shared state, side effects, events, configuration. Verify dependencies; don't assume them."
2. "Assess risk objectively — do not underestimate risk to speed implementation. Include a viable rollback strategy and specific test recommendations. This is not a re-investigation of the bug and not an implementation plan."

## Input contract

- **Bug report** (`{bug_id}.md`) and **reviewed investigation** (`{bug_id}_investigation.md` — `/review-investigation` updates it in place) — required. From these, extract: which files will be modified, which functions/methods change, what behavior changes.
- **`{bug_id}` base name** — derive from the input filenames.
- **Codebase access** — you search for dependencies and read test files.

## Process

1. **Understand the proposed change.** From the reviewed investigation: files to modify, functions/methods that change, behavior that changes.
2. **Find direct dependencies.** Search the codebase: who imports the changed code? where is the changed function/method called? where are changed classes instantiated? what calls the affected endpoints?
3. **Find indirect dependencies.** Shared state (does the change affect shared variables/state?), side effects (DB, cache, files), events (does it trigger events others listen to?), configuration (does it depend on config used elsewhere?).
4. **Analyze test coverage.** Existing tests for the changed code, integration tests exercising related workflows, E2E scenarios involving the feature, and — explicitly — the gaps.
5. **Assess the risk level.** Weigh: change scope (one function vs many files), code criticality (core vs edge case), test coverage (well-tested vs none), usage frequency (common path vs rare), data impact (DB changes vs logic only). Land on **LOW** (single file, well-tested, no external deps, easy rollback) / **MEDIUM** (multiple files, moderate coverage, some external deps) / **HIGH** (many files, limited coverage, critical deps, hard rollback) / **CRITICAL** (core system changes, production data at risk, no rollback — escalate before proceeding).
6. **Plan the rollback.** Code rollback, data rollback (if any), and whether a feature flag is warranted.
7. **Consolidate (coordinator, medium fix).** Merge worker outputs: consensus on affected components, the risk level (flag disagreement → ask the user), union of test recommendations.
8. **Present & gate.** Present to the user: affected-components summary, risk level, rollback strategy, testing recommendations, and a recommendation — **SAFE TO IMPLEMENT** / **IMPLEMENT WITH CAUTION** / **REQUIRES ADDITIONAL REVIEW**. Ask if it's OK to proceed (to implementation, or end-of-command). On confirmation, write the file.

## Output structure

- **Executive summary** — risk level (LOW / MEDIUM / HIGH / CRITICAL) and the SAFE-TO-IMPLEMENT / WITH-CAUTION / REQUIRES-ADDITIONAL-REVIEW recommendation.
- **Change scope analysis** — files to modify, functions affected, behavior changes.
- **Dependency analysis** — direct callers, indirect dependencies, shared state, external systems — each with `file:line` where it matters.
- **Related features** that might be affected.
- **Test coverage assessment** — existing tests (with paths), gaps identified.
- **Risk assessment** — specific risks, each with probability, impact, and mitigation.
- **Rollback strategy** — code rollback, data rollback, feature-flag recommendation.
- **Testing recommendations** — pre-deployment, post-deployment, edge cases.
- **Implementation recommendations** — development, deployment, monitoring phases.

### What this analysis IS / IS NOT

**IS:** a risk assessment of the proposed fix · a dependency map of affected code and systems · a testing guide for validation · a rollback plan for safe deployment.

**IS NOT:** a re-investigation of the bug (that's done) · a detailed implementation plan (that's the implementation phase) · a code review (that comes after implementation) · speculation about hypothetical scenarios (focus on likely impacts).

## Output file

Write the impact analysis to `{bug_id}_impact_analysis.md`, alongside the bug report and investigation. Confirm the consolidated analysis with the user before writing, and ask whether it's OK to proceed to the next phase (implementation, or end-of-command).
