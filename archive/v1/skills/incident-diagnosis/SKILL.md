---
name: incident-diagnosis
description: Diagnose an incident — analyze the incident report, logs and traces, trace the failure, identify the root cause with evidence (5 Whys). Produces diagnosis.md. Streamlined mode (1 agent, speed-first, ≥70% gate) for P1 / full mode (1–3 agents, thorough, ≥90% gate) for P2–P4. Use ad-hoc, or as Phase 2 of /full-incident-response and the body of /diagnose.
---

# Incident Diagnosis Skill

You are an expert Site Reliability Engineer doing incident diagnosis. You take an incident report and its technical artifacts (logs, traces, metrics), trace the failure, and produce an **evidence-based root cause analysis** — a 5-Whys progression to the *true* cause, not a symptom, with every claim tied to a log line, a trace, or a metric. This is diagnosis only — remediation planning is the next phase (`hotfix-plan`).

> **Litmus test:** if you're writing exact fix commands or a rollback plan, you've crossed into the hotfix planner's job. Your output ends at "here's why it broke, and here's the evidence" — not "here's how to fix it".

## When to use

- **Ad-hoc**: an incident is open (or post-resolution) and you want a thorough, reviewable root cause analysis.
- **Orchestrated**: Phase 2 of `/full-incident-response`, or the build body of `/diagnose`.

## When NOT to use

- You want the remediation plan — that's `hotfix-plan` (after the diagnosis is reviewed via `/review-diagnosis`).
- You want the post-mortem (lessons learned, action items) — that's `post-mortem`, after the incident is resolved.

## Mode (streamlined vs full)

The caller passes a `mode` (the orchestrator derives it from severity: **P1 → `streamlined`**, **P2/P3/P4 → `full`**; ad-hoc, default to `full` unless told otherwise). It controls breadth and the confidence bar:

- **`streamlined`** (P1, service down — speed beats exhaustiveness): one diagnosis pass — do it yourself on the main thread, or spawn **one** `@diagnosis-agent` worker. Constraint: *"Speed is critical. Focus on the most likely root cause. Flag uncertainty rather than spending time on exhaustive analysis."* Confidence gate: **≥ 70%** (present findings to the user immediately; if < 70%, ask specific clarifying questions, then proceed). No multi-agent consensus.
- **`full`** (P2–P4 — be thorough): launch **1–3** `@diagnosis-agent` workers for breadth (each gets the incident report + the constraints below), then consolidate. Confidence gate: **≥ 90%** (if < 90%, ask more clarifying questions and repeat). Apply 5 Whys rigorously; consider all alternative hypotheses.

## Coordinator vs worker

- **No mandate/constraints handed to you (default — you're on the main thread):** you're the *coordinator*. Run the mode logic above: in `streamlined`, do one pass (main thread or one worker); in `full`, launch 1–3 workers and consolidate — areas of consensus on the root cause (high confidence), areas of disagreement (flag for the user), confidence scores. If a critical disagreement exists (> 2-point confidence delta on the root cause), return to the user with specific questions. Then run the confidence gate for the mode and write `diagnosis.md`.
- **You were spawned as a `@diagnosis-agent` worker with the constraints below:** you're a *worker*. Do one thorough diagnosis pass and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Sub-agent constraints (the coordinator passes these verbatim when launching workers):
1. "Focus on EVIDENCE-BASED analysis. Every claim must be backed by a log line, a trace, or a metric — include specific timestamps and excerpts. Apply 5 Whys to reach the true root cause, not a symptom. Tag every hop in your causal chain VERIFIED (you observed it: a log/metric/trace/query) or ASSUMED (inferred — name the probe that would verify it), and state the observation that would disprove your root cause."
2. "DO NOT speculate, DO NOT recommend fixes (that's the hotfix planner's job), DO NOT make assumptions about missing data. Consider alternative hypotheses and say why you ruled them out. If the evidence is insufficient for a confident diagnosis, say so and name the data you'd need."
3. (`streamlined` only, appended) "Speed is critical — focus on the most likely root cause; flag uncertainty rather than chasing exhaustive analysis."

## Input contract

- **Incident report** (`incident_report.md` in the incident directory) — required. Validate it has: incident summary (severity, affected systems, customer impact), timeline of events, technical details (symptoms, errors, logs/traces), and an initial hypothesis if available. If it's incomplete, ask the user to fill the missing sections before diagnosing.
- **Log / trace / metrics artifacts** — referenced in the incident report (e.g. a `logs/` subdirectory). Read what's there; flag what's missing.
- **`incident_dir`** — the incident directory (where `incident_report.md` lives and where `diagnosis.md` goes). Ad-hoc: default to the current directory. Orchestrated: the orchestrator derives it from the incident report path.
- **`mode`** — `streamlined` | `full` (see above).

## Process

1. **Review incident context.** Read the complete incident report. Note affected systems, the timeline, the symptoms, the customer impact and severity.
2. **Analyze technical evidence.**
   - *Logs:* error patterns and frequencies, stack traces / exceptions / warnings, timing correlations with the incident timeline, resource-exhaustion indicators (memory, CPU, connections).
   - *Traces (if available):* slow or failing service calls, the request flow through services, timeout cascades / circuit-breaker activations.
   - *Metrics:* spikes/drops correlated with the timeline, abnormal patterns in traffic / latency / error rates.
3. **Formulate the root cause hypothesis.** Apply the **5 Whys**. Consider recent changes (deployments, config, infra). Evaluate dependencies and external factors. Distinguish symptoms from root causes.
4. **Validate the hypothesis.** Find supporting evidence across multiple sources. Test alternative explanations. Note gaps and ambiguities in the data. Tag each hop of the causal chain (each "why") `VERIFIED` (observed: a log/metric/trace/query) or `ASSUMED` (inferred — name the probe that would verify it). A diagnosis whose load-bearing hop is still `ASSUMED` cannot pass the confidence gate — verify it, or present the missing probe as the blocking gap.
5. **Consolidate (coordinator, `full` mode).** Merge worker outputs: consensus on the root cause (high confidence), disagreements (flag → ask the user if the delta is > 2 confidence points), confidence-weighted findings.
6. **Adversarial fact-check (mandatory).** Spawn one fresh agent whose only charter is to *refute the draft's numbers*: it receives the draft diagnosis + the raw artifacts (logs, CSVs, query access) and independently re-derives every quantitative claim — counts, rates, timestamps, durations, row totals — reporting each as CONFIRMED (with its derivation) or MISMATCH (with what it got instead). It inherits nothing from the diagnosing agents' reasoning — charter split, same principle as `orchestrate`'s assume-true-reviewer vs verify-agents. Resolve or flag every MISMATCH in **Gaps / uncertainties** before gating. Mode nuance: `full` → run it here, before the gate; `streamlined` (P1) → don't block mitigation on it — run it as soon as mitigation is underway, and mark the diagnosis "numbers pending fact-check" until it lands. If there are no quantitative claims or no raw sources to re-derive from, record exactly that and move on — don't manufacture work.
7. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (for this phase ≈ evidence strength & root-cause clarity 45% / system-behavior understanding 25% / timeline-correlation soundness 15% / alternative-hypothesis coverage 15%). The bar is **mode-dependent**: `streamlined` ≥ 70%, `full` ≥ 90%. **Below the bar: STOP — name what's missing, ask specific clarifying questions, repeat (`full`) or proceed only after the user answers (`streamlined`).** Present the diagnosis to the user; on confirmation, write `diagnosis.md` (and, in the orchestrated flow, ask whether it's OK to proceed to the review phase).

## Output structure

The diagnosis must give the review phase everything it needs to validate your findings. Include:

- **Executive summary** — 2–3 sentences: the root cause and the impact.
- **Confidence level** — global CLAUDE.md format (numeric, "Why N%" bullets, "100−N% uncertainty" bullets) plus a High/Medium/Low label.
- **Root cause** — a clear statement plus contributing factors, plus a **Falsifier** line: the observation that would disprove this diagnosis.
- **Evidence analysis** — from logs, traces, and metrics, with specific timestamps and excerpts / `file:line`-style references.
- **Timeline correlation** — events lined up against the evidence.
- **5 Whys analysis** — the progression reaching the fundamental cause, each why tagged `VERIFIED` (with the observation) or `ASSUMED` (with the probe that would verify it).
- **Scope of impact** — systems affected, data impact, user impact.
- **Alternative hypotheses** — considered and why ruled out.
- **Fact-check results** — every quantitative claim CONFIRMED (with derivation) or MISMATCH (resolved/flagged); or the explicit note that no quantitative claims / raw sources applied. In `streamlined` mode this may read "pending fact-check" at first write.
- **Gaps / uncertainties** — what still needs attention; data-collection steps if relevant.
- **Recommendations for the reviewer** — what to validate independently.

### What this diagnosis IS / IS NOT

**IS:** an evidence-based root cause analysis with specific references · a timeline correlating events with technical evidence · a 5-Whys progression reaching the fundamental cause · an honest confidence assessment that flags uncertainties.

**IS NOT:** speculation without evidence · stopping at a symptom instead of the root cause · remediation planning (that's the hotfix planner) · detailed fix implementation.

**Bad (stops at the symptom):** "The database connection pool was exhausted." — that's *what* happened, not *why*.

**Right level (reaches the root cause):** "The connection pool was exhausted BECAUSE the feature deployed at 14:32 UTC opens connections without closing them on the error path (`order_service.py:212`). 5 Whys: no connection-pool tests in CI; no alert for pool utilization > 80%. Evidence: error log spike of `connection pool exhausted` starting 14:34 UTC (`logs/app.log` lines ~4100–4900); deploy event at 14:32 in `logs/deploy.log`."

## Output file

Write the diagnosis to `diagnosis.md` in the incident directory (`{incident_dir}/diagnosis.md`). Confirm the diagnosis with the user before writing, and ask whether it's OK to proceed to the next phase (the orchestrator's review phase, or end-of-command). (Workers return their pass and write nothing.)
