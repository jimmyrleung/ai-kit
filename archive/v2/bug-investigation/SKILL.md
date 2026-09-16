---
name: bug-investigation
description: "Diagnoses a reported bug, error, crash, regression, or unexpected behavior from source and runtime evidence, with a minimal-fix proposal or next probe. Use to investigate, debug, or root-cause a failure, including a production incident or outage. Accepts a bug report, issue link, or inline reproduction; produces {bug_id}_investigation.md before fix implementation."
---

# Bug Investigation Skill

Apply the [confidence contract](references/shared/confidence.md) using the diagnosis rubric.
Record the effective policy and explicit score, evidence, uncertainty consequences, next
checks and advancement verdict; pass the policy to workers and downstream gates.

You are a specialized bug investigator. You take a bug report, trace through the code, identify the cause supported by the available evidence, or the precise next probe, and propose a **minimal** fix with specific `file:line` references. Separate source facts, runtime observations, and hypotheses; code alone does not establish that a branch caused a particular incident.

> **Litmus test:** if you're proposing a refactor or writing implementation pseudocode, you've gone too far. Your output diagnoses *why* it breaks and points at the minimal change — the implementation phase writes the code.

Apply the [engineering change contract](references/shared/engineering-change.md):
inspect repository context, reuse suitable code/tests, and justify new files within scope.
Resolve bundled references relative to this skill folder.

Follow [authorized work](references/shared/authorized-work.md) for existing permission,
blocking questions, and requested discussion cadence; resolve from this skill folder.

## When to use

- **Ad-hoc**: a bug came in and you want a thorough evidence-based diagnosis before touching code.
- **After recon**: the `lay-of-the-land` skill mapped an unfamiliar area and the failure is now scoped enough to trace.

## When NOT to use

- The bug is L/XL (system-wide / architectural) — expect to iterate; one pass won't be enough.
- You're being asked to *implement* the fix — that comes after the investigation (and its review) is approved.
- The work item is a feature / refactor, not a failure → `analyze-work`.

## Coordinator vs worker

- **No mandate/constraints handed to you (default — you're on the main thread):** you're the *coordinator*. For a small bug, do the investigation yourself on the main thread. For a medium bug, launch **1–3 generic subagents** (generic exploration / general-purpose — there are no named investigation agents to maintain) for breadth (each gets the bug report + the constraints below), then consolidate supported causal findings, competing hypotheses, and unresolved evidence gaps. Resolve critical disagreements by inspecting the conflicting evidence and running a discriminating probe; ask the user only for missing load-bearing facts. Worker agreement and numeric score differences do not prove causality. Then run the confidence gate and write the file.
- **You were spawned as a sub-agent with the constraints below:** you're a *worker*. Do one thorough investigation pass and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Pass the complete effective confidence and causal-evidence policy in every worker brief.
Workers calculate the diagnosis rubric for their assigned scope, with evidence, uncertainty
consequences and next checks; below-threshold or causally unproven claims remain candidates.

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
- **5-Whys depth:** "the pool was exhausted" is the symptom — keep asking why until you reach the change or design that caused it, tagging each why SOURCE / OBSERVED / INFERRED like any other hop.
- **One effective policy:** record severity, active/resolved incident state, pass depth,
  confidence threshold, causal evidence required, and authorized action boundary once.
  Active P1 → one streamlined pass, threshold 70; other work → normal depth, threshold 90.
  Pass this policy unchanged to `review-artifact` and fix design; no later default overrides
  it. User-required stricter gates still apply. Lower threshold never turns a plausible
  branch into a confirmed cause or grants remediation/deployment permission.
- **Hand-off:** the fix design is the `techspec` skill in fix mode (hotfix variant for live remediation); after resolution, offer the `post-mortem` skill.

## Process

1. **Inspect the bug report.** Extract: what's broken, how to reproduce, expected vs actual behavior, affected components. Note any suspected files the reporter named.
2. **Locate the relevant code.** Search the codebase for: entry points (API endpoints, UI handlers, jobs), the core business logic related to the bug, data-access layers, error-handling code.
3. **Trace the execution path.** Record each hop and variable state with evidence type:
   **SOURCE** = inspected code/config proves a possible mechanism; **OBSERVED** = executed
   reproduction, logs, debugger, trace or DB probe shows behavior with inputs, build/config,
   time/environment and result; **INFERRED** = causal hypothesis, with its next confirming
   probe and falsifier. Separate these within a hop when necessary. Do not call a source-read
   configuration/race branch the incident cause without evidence that it executed and explains
   the symptom in that incident. A deterministic reproduction can establish a reproducible
   defect; claiming it explains a production incident still needs incident linkage.
4. **Analyze the root cause.** Determine *why* it fails and categorize: Logic Error (wrong condition / bad calculation) · State Management (race condition / stale data) · Data Validation (missing check / wrong type) · Integration (API change / dependency problem) · Configuration (environment-specific). Check git history if relevant (when was the buggy code introduced?). If you find multiple plausible causes, investigate the most likely first.
   **Absence-claim protocol** — before asserting "no event / no error / not used / nobody sets this":
   - **Positive control first:** prove the probe can see data of the target class at all (query a known-to-exist event in-window) before interpreting an empty result as absence.
   - **Right channel / full enumeration:** enumerate which log channels/stores are actually enabled (platform operational channels, not just the default) and paginate to completion — page 1 of a filtered read is not the population.
   - **Sample the identifier format:** pull one known instance of the target class and copy its exact identifier encoding before sweeping (a GUID sweep missed base64-encoded protobuf ids).
   - **History before blame:** search the repo's SESSION_LOG / ADR / techspec artifacts for the suspect symbol before root-causing it as a mistake — a recorded decision was called a copy-paste error at 95% confidence. For authz bugs, enumerate scheme → handler → claims issued before reasoning from an endpoint's policy attribute.
5. **Propose a minimal solution only with causal evidence.** A deterministic reproduction
   that isolates the mechanism, or correlated runtime evidence that rules out competing
   explanations, can support a minimal fix. Cite expected/actual result, causal link,
   falsifier, and exact `file:line`; describe the change without implementation code.
   When causal evidence is missing, deliver the candidate hypothesis and precise next probe
   (what/where/inputs/result that would confirm or refute it), not confirmed remediation.
   During an incident, an authorized reversible mitigation may proceed separately: label it
   mitigation, with rollback, risk, monitoring, and unconfirmed cause; success is not proof
   of the diagnosis and does not replace later causal validation.
6. **Consolidate (coordinator, medium bug).** Re-ground supported causal findings, competing
   hypotheses and unresolved evidence gaps; do not average scores or weight causality by
   agreement. Resolve critical disagreements with a discriminating probe; ask the user only
   for a missing load-bearing fact or decision and continue independent investigation.
7. **Effective gate.** Use the single recorded policy (normal threshold 90; active P1 70,
   unless applicable instructions require a stricter gate); calculate the diagnosis rubric
   and report the confidence contract assessment, unresolved evidence and next checks.
   Below its threshold or without the required causal evidence, return the next probe and
   uncertainty rather than an approved fix. Above it, present the bounded diagnosis; write
   the requested investigation within existing authorization. Missing evidence, not worker
   agreement or a numeric score, controls whether the cause is confirmed.

## Output structure

The investigation must give a review pass everything it needs to validate your findings. Include:

- **Executive summary** — 1–2 sentences: what's broken, why, how to fix.
- **Effective policy** — severity/state, depth, threshold, causal requirements, action boundary.
- **Confidence score** — the confidence contract format: factor calculation, effective policy, "Why N%" evidence, "100−N% uncertainty" with consequences and next probes, and advancement verdict.
- **Bug understanding** — reported issue, expected vs actual behavior, reproduction steps.
- **Entry point** — with `file:line`.
- **Execution path trace** — the call chain from entry to failure, with the variable state at each step, each hop distinguishing `SOURCE`, `OBSERVED`, and `INFERRED`, with provenance, causal limits, and next probes.
- **Root cause** — with category (Logic Error / State Management / Data Validation / Integration / Configuration), plus a **Falsifier** line: the concrete observation that would disprove this diagnosis.
- **Evidence** — logs, code references, variable states that support the diagnosis.
- **Proposed solution or next probe** — confirmed remediation, reversible mitigation, or unconfirmed candidate clearly distinguished; specific `file:line` references, the minimal change described (not coded), why it fixes the root cause.
- **Alternative approaches considered** — if any.
- **Impact assessment preview** — files affected, tests needed, potential side effects.
- **Incident additions** (incident lens only): **Incident timeline** — the correlated event sequence with timestamps (error onset vs deploys, config changes, traffic shifts — the correlation evidence the lens gathered, laid out for the `post-mortem` skill to build on) · **Scope of impact** — affected users / services / data and duration, derived from the evidence, not estimated · **Hypotheses ruled out** — each with the evidence that ruled it out (this list is what stops a war room re-litigating dead ends).

### What this investigation IS / IS NOT

**IS:** an evidence-based diagnosis with specific code references · a traceable execution path from entry to failure · a minimal-fix proposal addressing the root cause · an honest confidence assessment that flags uncertainties.

**IS NOT:** speculative analysis without evidence · a large refactoring proposal · detailed implementation pseudocode (save it for the implementation phase) · vague descriptions without `file:line` references.

**Bad (too vague — no evidence):** "The bug is probably in the save function somewhere. It might be a validation issue or maybe a database problem."

**Right level (evidence-based):** "Root cause: missing null check in `DataLayer.save()` (`data.ts:89`). When `user.preferences` is undefined, line 92 throws TypeError. Evidence: error log shows `Cannot read property 'theme' of undefined` at `data.ts:92`. Proposed fix: add a null check before accessing `preferences` (lines 89–91) — keeps the change to one function, addresses the cause not the symptom."

## Output file

Write the investigation to `{bug_id}_investigation.md`, alongside the bug report. Use a clear topic-derived base name if none is supplied; ask only when the destination is ambiguous. After writing, **offer the `review-artifact` skill** over the investigation before any fix is implemented on top of it (a risky fix then gets the `techspec` skill in fix mode for the design + blast radius).
