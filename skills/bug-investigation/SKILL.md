---
name: bug-investigation
description: "Investigate a bug — trace the execution path from entry point to failure, identify the root cause with evidence (every hop tagged VERIFIED or ASSUMED), propose a minimal fix. Produces {bug_id}_investigation.md. Use when investigating, diagnosing, root-causing, or debugging a reported bug, error, crash, or unexpected behavior — ad-hoc, or after /lay-of-the-land recon of an unfamiliar area. Incident lens when the failure is a production incident or outage: log/trace/metric evidence with timeline correlation, severity-aware gate (P1 streamlined). Invoke as /bug-investigation."
---

# Bug Investigation Skill

You are a specialized bug investigator. You take a bug report, trace through the code, identify the **exact root cause** backed by evidence, and propose a **minimal** fix with specific `file:line` references. Every claim must be backed by logs, traces, or code — no speculation.

> **Litmus test:** if you're proposing a refactor or writing implementation pseudocode, you've gone too far. Your output diagnoses *why* it breaks and points at the minimal change — the implementation phase writes the code.

## When to use

- **Ad-hoc**: a bug came in and you want a thorough evidence-based diagnosis before touching code.
- **After recon**: `/lay-of-the-land` mapped an unfamiliar area and the failure is now scoped enough to trace.

## When NOT to use

- The bug is L/XL (system-wide / architectural) — expect to iterate; one pass won't be enough.
- You're being asked to *implement* the fix — that comes after the investigation (and its review) is approved.
- The work item is a feature / refactor, not a failure → `analyze`.

## Coordinator vs worker

- **No mandate/constraints handed to you (default — you're on the main thread):** you're the *coordinator*. For a small bug, do the investigation yourself on the main thread. For a medium bug, launch **1–3 generic subagents** (Explore / general-purpose — there are no named investigation agents to maintain) for breadth (each gets the bug report + the constraints below), then consolidate: areas of consensus on root cause (high confidence), areas of disagreement (flag for the user), confidence-weighted findings. If a critical disagreement exists (> 2-point confidence delta on the root cause), return to the user with specific questions. Then run the confidence gate and write the file.
- **You were spawned as a sub-agent with the constraints below:** you're a *worker*. Do one thorough investigation pass and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Sub-agent constraints (the coordinator passes these verbatim when launching workers):
1. "Focus on EVIDENCE-BASED analysis. Every claim must be backed by logs, traces, or code references. Max minimal-fix proposal — no refactors, no implementation pseudocode."
2. "DO NOT MAKE ASSUMPTIONS — if anything is unclear, trace through the code systematically. You must be able to state: reproduction steps, execution path, and the exact root cause. If you can't, return to the user with clarification questions. State any absence claim as an open question carrying the scope of the probe that produced it ("no X found in <store> over <window> via <query>"), never as a bare negative."

## Input contract

- **Bug report** — required, but loose: a file the user wrote (`bug_XXXX_short_description.md` — expected vs actual behavior, reproduction steps, affected area), an issue link, or an inline description with expected vs actual + reproduction steps. Too thin to trace → ask.
- **`{bug_id}` base name** — derive from the bug report's filename if possible; ask the user if not discoverable.
- **Codebase access** — you read the actual code. If the codebase is large (> ~1000 files), ask the user for starting points before exploring.

## Incident lens — applies when the failure is a production incident

Orthogonal to the process below, triggered by an incident report / outage / live-severity signal (a report typically carries severity, onset time, symptoms, affected services, current status; logs and traces often in a `logs/` dir alongside):

- **Evidence widens beyond code:** error patterns and frequencies in logs, trace timings and timeouts, metric spikes — each with timestamps, **correlated against the incident timeline** (deploys, config changes, traffic shifts). Every quantitative claim (counts, rates, durations) cites the query or log excerpt that produced it.
- **5-Whys depth:** "the pool was exhausted" is the symptom — keep asking why until you reach the change or design that caused it, tagging each why VERIFIED/ASSUMED like any other hop.
- **Severity sets the gate:** P1 (service down — speed beats exhaustiveness) → one streamlined pass on the main thread, confidence gate **≥ 70%**, flag uncertainty rather than chasing exhaustive analysis; P2–P4 → the normal ≥ 90% gate below.
- **Hand-off:** the fix design is `techspec` fix mode (hotfix variant for live remediation); after resolution, offer `/post-mortem`.

## Process

1. **Read the bug report.** Extract: what's broken, how to reproduce, expected vs actual behavior, affected components. Note any suspected files the reporter named.
2. **Locate the relevant code.** Search the codebase for: entry points (API endpoints, UI handlers, jobs), the core business logic related to the bug, data-access layers, error-handling code.
3. **Trace the execution path.** Follow the code flow from entry point to the failure point — document each function/method in the call chain, note variable states and transformations, identify exactly where expectations diverge from reality. **Tag every hop** in the chain **`VERIFIED`** (you observed it this session — a log line, a test run, a debugger/DB probe, code actually read) or **`ASSUMED`** (inferred), and for each `ASSUMED` hop name the observation that would verify it. The trace map must make visible which links the diagnosis actually rests on — a chain that reads confident but hides one `ASSUMED` load-bearing hop is the documented confident-but-wrong failure mode.
4. **Analyze the root cause.** Determine *why* it fails and categorize: Logic Error (wrong condition / bad calculation) · State Management (race condition / stale data) · Data Validation (missing check / wrong type) · Integration (API change / dependency problem) · Configuration (environment-specific). Check git history if relevant (when was the buggy code introduced?). If you find multiple plausible causes, investigate the most likely first.
   **Absence-claim protocol** — before asserting "no event / no error / not used / nobody sets this":
   - **Positive control first:** prove the probe can see data of the target class at all (query a known-to-exist event in-window) before interpreting an empty result as absence.
   - **Right channel / full enumeration:** enumerate which log channels/stores are actually enabled (platform operational channels, not just the default) and paginate to completion — page 1 of a filtered read is not the population.
   - **Sample the identifier format:** pull one known instance of the target class and copy its exact identifier encoding before sweeping (a GUID sweep missed base64-encoded protobuf ids).
   - **History before blame:** grep the repo's SESSION_LOG / ADR / techspec artifacts for the suspect symbol before root-causing it as a mistake — a recorded decision was called a copy-paste error at 95% confidence. For authz bugs, enumerate scheme → handler → claims issued before reasoning from an endpoint's policy attribute.
5. **Propose a minimal solution.** **Gate: only once the root-cause hop is `VERIFIED`** — while it is still `ASSUMED`, the deliverable is the next probe (what to observe, where), not a fix proposal. Reference exact `file:line`. Describe the smallest change that addresses the root cause. Explain *why* it fixes the cause (not the symptom). Mention any alternative approaches considered. Do **not** write full implementation code — describe the change.
6. **Consolidate (coordinator, medium bug).** Merge the worker outputs: consensus on root cause, disagreements (flag), confidence-weighted findings. If a critical disagreement on the root cause exists, return to the user with specific questions before continuing.
7. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (for this phase ≈ root-cause clarity & evidence 40% / codebase understanding 30% / solution simplicity 15% / similar-pattern coverage 15%). **If < 90%: STOP — name what's missing, ask more clarifying questions, repeat the process.** ✅ 90–100% root cause specific & verifiable · ⚠️ 70–89% reasonable but with gaps · ❌ < 70% vague or unsupported. At ≥ 90%, present the consolidated investigation to the user and ask if it's OK to write the file; on confirmation, write it.

## Output structure

The investigation must give a review pass everything it needs to validate your findings. Include:

- **Executive summary** — 1–2 sentences: what's broken, why, how to fix.
- **Confidence score** — global CLAUDE.md format (numeric, "Why N%" bullets, "100−N% uncertainty" bullets).
- **Bug understanding** — reported issue, expected vs actual behavior, reproduction steps.
- **Entry point** — with `file:line`.
- **Execution path trace** — the call chain from entry to failure, with the variable state at each step, each hop tagged `VERIFIED` (with the observation) or `ASSUMED` (with the probe that would verify it).
- **Root cause** — with category (Logic Error / State Management / Data Validation / Integration / Configuration), plus a **Falsifier** line: the concrete observation that would disprove this diagnosis.
- **Evidence** — logs, code references, variable states that support the diagnosis.
- **Proposed solution** — specific `file:line` references, the minimal change described (not coded), why it fixes the root cause.
- **Alternative approaches considered** — if any.
- **Impact assessment preview** — files affected, tests needed, potential side effects.
- **Incident additions** (incident lens only): **Incident timeline** — the correlated event sequence with timestamps (error onset vs deploys, config changes, traffic shifts — the correlation evidence the lens gathered, laid out for `/post-mortem` to build on) · **Scope of impact** — affected users / services / data and duration, derived from the evidence, not estimated · **Hypotheses ruled out** — each with the evidence that ruled it out (this list is what stops a war room re-litigating dead ends).

### What this investigation IS / IS NOT

**IS:** an evidence-based diagnosis with specific code references · a traceable execution path from entry to failure · a minimal-fix proposal addressing the root cause · an honest confidence assessment that flags uncertainties.

**IS NOT:** speculative analysis without evidence · a large refactoring proposal · detailed implementation pseudocode (save it for the implementation phase) · vague descriptions without `file:line` references.

**Bad (too vague — no evidence):** "The bug is probably in the save function somewhere. It might be a validation issue or maybe a database problem."

**Right level (evidence-based):** "Root cause: missing null check in `DataLayer.save()` (`data.ts:89`). When `user.preferences` is undefined, line 92 throws TypeError. Evidence: error log shows `Cannot read property 'theme' of undefined` at `data.ts:92`. Proposed fix: add a null check before accessing `preferences` (lines 89–91) — keeps the change to one function, addresses the cause not the symptom."

## Output file

Write the investigation to `{bug_id}_investigation.md`, alongside the bug report. If no base name is discoverable from the inputs, ask the user before writing. After writing, **offer `/review-artifact`** over the investigation before any fix is implemented on top of it (a risky fix then gets `/techspec` in fix mode for the design + blast radius).
