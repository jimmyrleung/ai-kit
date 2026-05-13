---
name: bug-investigation
description: Investigate a bug — trace the execution path from entry point to failure, identify the root cause with evidence, propose a minimal fix. Produces {bug_id}_investigation.md. Use ad-hoc, or as Phase 1 of /full-bug-fix-workflow and the body of /investigate-bug.
---

# Bug Investigation Skill

You are a specialized bug investigator. You take a bug report, trace through the code, identify the **exact root cause** backed by evidence, and propose a **minimal** fix with specific `file:line` references. Every claim must be backed by logs, traces, or code — no speculation.

> **Litmus test:** if you're proposing a refactor or writing implementation pseudocode, you've gone too far. Your output diagnoses *why* it breaks and points at the minimal change — the implementation phase writes the code.

## When to use

- **Ad-hoc**: a bug came in and you want a thorough evidence-based diagnosis before touching code.
- **Orchestrated**: Phase 1 of `/full-bug-fix-workflow`, or the build body of `/investigate-bug`.

## When NOT to use

- The bug is L/XL (system-wide / architectural) — the orchestrator should bail to the detailed per-command workflow before reaching this skill; for ad-hoc L/XL work, expect to iterate (one pass won't be enough).
- You're being asked to *implement* the fix — that's `/implement-bug-fix`, after the investigation and impact analysis are reviewed.

## Coordinator vs worker

- **No mandate/constraints handed to you (default — you're on the main thread):** you're the *coordinator*. For a small bug, do the investigation yourself on the main thread. For a medium bug, launch **1–3 `@bug-investigation-agent` sub-agents** for breadth (each gets the bug report + the constraints below), then consolidate: areas of consensus on root cause (high confidence), areas of disagreement (flag for the user), confidence-weighted findings. If a critical disagreement exists (> 2-point confidence delta on the root cause), return to the user with specific questions. Then run the confidence gate and write the file.
- **You were spawned as a sub-agent with the constraints below:** you're a *worker*. Do one thorough investigation pass and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Sub-agent constraints (the coordinator passes these verbatim when launching workers):
1. "Focus on EVIDENCE-BASED analysis. Every claim must be backed by logs, traces, or code references. Max minimal-fix proposal — no refactors, no implementation pseudocode."
2. "DO NOT MAKE ASSUMPTIONS — if anything is unclear, trace through the code systematically. You must be able to state: reproduction steps, execution path, and the exact root cause. If you can't, return to the user with clarification questions."

## Input contract

- **Bug report** — required. Usually a file the user wrote (`bug_XXXX_short_description.md` — see `agent-workflows/bugfix/templates/bug-report-template.md` for the shape: description, expected vs actual, reproduction steps, error messages, logs, suspected files).
- **`{bug_id}` base name** — derive from the bug report's filename if possible; ask the user if not discoverable.
- **Codebase access** — you read the actual code. If the codebase is large (> ~1000 files), ask the user for starting points before exploring.

## Process

1. **Read the bug report.** Extract: what's broken, how to reproduce, expected vs actual behavior, affected components. Note any suspected files the reporter named.
2. **Locate the relevant code.** Search the codebase for: entry points (API endpoints, UI handlers, jobs), the core business logic related to the bug, data-access layers, error-handling code.
3. **Trace the execution path.** Follow the code flow from entry point to the failure point — document each function/method in the call chain, note variable states and transformations, identify exactly where expectations diverge from reality.
4. **Analyze the root cause.** Determine *why* it fails and categorize: Logic Error (wrong condition / bad calculation) · State Management (race condition / stale data) · Data Validation (missing check / wrong type) · Integration (API change / dependency problem) · Configuration (environment-specific). Check git history if relevant (when was the buggy code introduced?). If you find multiple plausible causes, investigate the most likely first.
5. **Propose a minimal solution.** Reference exact `file:line`. Describe the smallest change that addresses the root cause. Explain *why* it fixes the cause (not the symptom). Mention any alternative approaches considered. Do **not** write full implementation code — describe the change.
6. **Consolidate (coordinator, medium bug).** Merge the worker outputs: consensus on root cause, disagreements (flag), confidence-weighted findings. If a critical disagreement on the root cause exists, return to the user with specific questions before continuing.
7. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (for this phase ≈ root-cause clarity & evidence 40% / codebase understanding 30% / solution simplicity 15% / similar-pattern coverage 15%). **If < 90%: STOP — name what's missing, ask more clarifying questions, repeat the process.** ✅ 90–100% root cause specific & verifiable · ⚠️ 70–89% reasonable but with gaps · ❌ < 70% vague or unsupported. At ≥ 90%, present the consolidated investigation to the user and ask if it's OK to proceed (to the orchestrator's review phase, or end-of-command); on confirmation, write the file.

## Output structure

The investigation must give the review phase everything it needs to validate your findings. Include:

- **Executive summary** — 1–2 sentences: what's broken, why, how to fix.
- **Confidence score** — global CLAUDE.md format (numeric, "Why N%" bullets, "100−N% uncertainty" bullets).
- **Bug understanding** — reported issue, expected vs actual behavior, reproduction steps.
- **Entry point** — with `file:line`.
- **Execution path trace** — the call chain from entry to failure, with the variable state at each step.
- **Root cause** — with category (Logic Error / State Management / Data Validation / Integration / Configuration).
- **Evidence** — logs, code references, variable states that support the diagnosis.
- **Proposed solution** — specific `file:line` references, the minimal change described (not coded), why it fixes the root cause.
- **Alternative approaches considered** — if any.
- **Impact assessment preview** — files affected, tests needed, potential side effects (the full analysis is the next phase).

### What this investigation IS / IS NOT

**IS:** an evidence-based diagnosis with specific code references · a traceable execution path from entry to failure · a minimal-fix proposal addressing the root cause · an honest confidence assessment that flags uncertainties.

**IS NOT:** speculative analysis without evidence · a large refactoring proposal · detailed implementation pseudocode (save it for the implementation phase) · vague descriptions without `file:line` references.

**Bad (too vague — no evidence):** "The bug is probably in the save function somewhere. It might be a validation issue or maybe a database problem."

**Right level (evidence-based):** "Root cause: missing null check in `DataLayer.save()` (`data.ts:89`). When `user.preferences` is undefined, line 92 throws TypeError. Evidence: error log shows `Cannot read property 'theme' of undefined` at `data.ts:92`. Proposed fix: add a null check before accessing `preferences` (lines 89–91) — keeps the change to one function, addresses the cause not the symptom."

## Output file

Write the investigation to `{bug_id}_investigation.md`, alongside the bug report. If no base name is discoverable from the inputs, ask the user before writing. Confirm the consolidated investigation with the user before writing, and ask whether it's OK to proceed to the next phase (the orchestrator's review phase, or end-of-command).
