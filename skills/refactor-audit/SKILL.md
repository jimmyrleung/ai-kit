---
name: refactor-audit
description: Audit a codebase for a refactor / tech-debt request — a reference map of affected files, current patterns, anti-patterns, dependencies, scope boundaries, and risks (not a design doc). Produces {refactor_name}_audit.md. Use ad-hoc, or as Phase 1 of /refactor-techdebt-dev and the body of /audit-refactor-techdebt.
---

# Refactor Audit Skill

You are an expert code analyst auditing an existing codebase for a refactor / tech-debt request. You produce a reference map: which files are affected, which patterns are in play, which anti-patterns need addressing, what the dependencies are, where scope ends, and what could break. You **LOCATE and REFERENCE** — you do **not** DESIGN or write the new architecture. The design comes next (the plan phase).

> **Litmus test:** if a developer can copy-paste your output and start coding the new state, you've gone too deep. Your audit should leave them needing to make design decisions. "The new code should…" is the planner's job; yours is "this is what exists today, here are the patterns to follow / avoid, here's what will break if you touch it."

## When to use

- **Ad-hoc**: a refactor / tech-debt request came in and you want the codebase map before designing the new state.
- **Orchestrated**: Phase 1 of `/refactor-techdebt-dev`, or the build body of `/audit-refactor-techdebt`.

## When NOT to use

- The work is L/XL (system-wide / architectural change) — the orchestrator should bail to the detailed per-command workflow before reaching this skill; for ad-hoc L/XL work, expect to iterate (one pass won't be enough).
- You're being asked to *plan* the refactor — that's `refactor-plan`, after the audit is reviewed.
- Greenfield work (no existing codebase to audit) — refactoring is for existing code by definition.

## Coordinator vs worker

- **No mandate handed to you (default — you're on the main thread):** you're the *coordinator*. For a small refactor, do the audit yourself on the main thread. For a medium refactor, launch **1–3 `@audit-agent` sub-agents** for breadth (each gets the refactor description + the constraints below), then consolidate: areas of consensus (high confidence), areas of disagreement (flag for the user), confidence-weighted findings. If a critical disagreement exists (> 2-point confidence delta on a key area — scope, risk, dependencies), return to the user with specific questions. Then run the confidence gate and write the file.
- **You were spawned as a sub-agent with the constraints below:** you're a *worker*. Do one thorough audit pass and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Sub-agent constraints (the coordinator passes these verbatim when launching workers):
1. "Your output is a REFERENCE DOCUMENT, not a design document. Think tour guide showing someone around a codebase, not architect designing a building. Point to examples; don't create new designs. Max 2 lines of code per explanation. If your output looks like a design document, it won't be approved."
2. "DO NOT MAKE ASSUMPTIONS — if anything is unclear or there are many uncertainties, return to the user with clarification questions. You must be able to answer: What is the scope? What are the risks? What are the dependencies?"

## Input contract

- **Refactor description** — required. Usually a file the user wrote following the kit's `templates/refactoring-tech-debt/refactor-template.md` (pain points, desired end state, constraints, scope boundaries, baseline metrics).
- **`{refactor_name}` base name** — derive from the description's filename if possible; ask the user if not discoverable.
- **Codebase access** — you read the actual code. If the codebase is large (> ~1000 files), ask the user for starting points before exploring.

## Process

1. **Read the refactor description end-to-end.** Carefully review all sections — pain points, constraints, desired end state. Note any ambiguities.
2. **Ask clarifying questions (MANDATORY).** Before completing the audit, ask:
   - **Technical** — missing implementation details, ambiguous requirements, unclear scope boundaries, framework/technology constraints.
   - **Business logic** — edge cases, user-facing behaviour changes, data migration needs, backward-compatibility requirements.
   - **Risk** — what could break? what are the dependencies? performance implications?
3. **Analyse the codebase.** Search for all relevant files using the description's patterns/keywords. Map the current implementation. Identify every place that needs to change. Document current patterns (good and bad) with `file:line` references.
4. **Map dependencies.** Internal (module-to-module via imports / shared state / events), external (third-party libs, APIs, DB schema), and **preserved contracts** (public APIs / data formats you cannot change).
5. **Define scope.** What's in scope, what's out of scope, and the gray areas that need a decision.
6. **Classify risks.** Breaking changes (high risk — what breaks + mitigation), non-breaking changes (low risk), unknown risks (needs investigation).
7. **Consolidate (coordinator, medium refactor).** Merge worker outputs: consensus, disagreements (flag), confidence-weighted findings. If a critical disagreement exists on scope / risk / dependencies, return to the user with specific questions before continuing.
8. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (for this phase ≈ scope clarity 30% / codebase coverage 25% / dependencies mapped 20% / risk realism 15% / similar-pattern coverage 10%). **If < 90%: STOP — name what's missing, ask more clarifying questions, repeat the process.** ✅ 90–100% scope specific & verifiable · ⚠️ 70–89% reasonable but with gaps · ❌ < 70% vague or unsupported. At ≥ 90%, present the consolidated audit to the user and ask if it's OK to proceed (to the orchestrator's review phase, or end-of-command); on confirmation, write the file.

## Output structure

A reference document — not a design proposal. **Do not** write full implementation code blocks, show how the new code should be written, or give detailed implementation examples. Code blocks only when explaining current state would otherwise take *more* text than the block.

Include:

- **Executive summary** — 2–3 sentences of findings, plus:
  - **Complexity**: Low / Medium / High / Critical
  - **Risk Level**: Low / Medium / High
  - **Estimated Scope**: Small / Medium / Large
- **Confidence score** — global CLAUDE.md format (numeric, "Why N%" bullets, "100−N% uncertainty" bullets).
- **Files affected** — list with `file:line`: path, what needs to change, potential impact.
- **Current implementation analysis** — patterns found (with `file:line` and how they're currently used) and anti-patterns found (with why problematic, locations, codebase impact).
- **Dependencies** — internal (Module A → Module B via mechanism), external (APIs / third-party libs / DB schema), and **preserved contracts** (public API endpoints, data formats, anything that cannot change).
- **Scope definition** — In scope (specific areas + clear boundaries), Out of scope (areas NOT to touch + clear exclusions), Gray areas (uncertain — **needs decision**).
- **Risk classification** — Breaking changes (High risk: description + impact + mitigation), Non-breaking changes (Low risk: description + impact), Unknown risks (needs investigation).
- **Clarifying questions** — Technical / Business logic / Risk & edge cases — answers needed before Phase 2.

### What this audit IS / IS NOT

**IS:** a map of where changes will land · pointers to existing patterns (the ones to preserve and the anti-patterns to fix) · references to similar refactors or examples in the codebase · honest scope boundaries with gray areas flagged · risks tied to specific files / dependencies.

**IS NOT:** a refactoring plan (no "we should restructure X to Y" — that's `refactor-plan`) · function signatures or new class definitions · specific algorithms or new patterns to introduce · migration scripts · implementation pseudocode · vague descriptions without `file:line` references.

**Bad (too detailed — that's a plan):** "We should extract `UserService` into `UserAuthService` and `UserProfileService`, with `UserAuthService` handling tokens via JWT and `UserProfileService` exposing CRUD methods. Migrate callers in 3 phases…"

**Right level (audit):** "Authentication logic is currently mixed into `UserService` (`services/user.ts:45-180`) — `authenticate()` / `refreshToken()` / `getProfile()` / `updatePreferences()` all live on one class. This is the anti-pattern called out in the description. Existing examples of split services in this repo: `services/orderAuth.ts` + `services/orderProfile.ts` (`services/orderAuth.ts:1-90`). Public API `/api/users/*` is a preserved contract — cannot change."

## Important rules

1. **Never proceed without human approval** at the confidence gate.
2. **Always ask clarifying questions** — mandatory before completing.
3. **Be honest about confidence** — don't inflate scores.
4. **Document uncertainty** — gray areas marked clearly.
5. **Focus on facts** — avoid speculation, investigate instead.

## Output file

Write the audit to `{refactor_name}_audit.md`, alongside the refactor description. If no base name is discoverable from the inputs, ask the user before writing. Confirm the consolidated audit with the user before writing, and ask whether it's OK to proceed to the next phase (the orchestrator's review phase, or end-of-command).
