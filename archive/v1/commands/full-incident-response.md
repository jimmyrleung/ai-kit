---
description: Start the full incident response workflow with severity-based routing (P1 streamlined for speed, P2+ full process).
argument-hint: Severity level (P1/P2/P3/P4) followed by incident report file path.
---

# Goal

- Diagnose the incident root cause quickly and accurately.
- Review the diagnosis for confidence before remediation.
- Create an actionable hotfix plan to restore service.
- Generate a post-mortem with action items to prevent recurrence.

This command is a thin orchestrator: each phase invokes a skill that owns the methodology, output contract, and confidence gate. The orchestrator owns only the glue — the **severity routing** (which mode each phase runs in), the **per-severity confidence gates**, the **per-severity Phase-5 split**, the review hand-off, the phase wiring, the output manifest, and the escalation points.

## Input format

`$ARGUMENTS` should contain: `{severity} {incident_report_file}` — e.g. `P1 incidents/inc_2026-05-12_api_outage/incident_report.md`.

Derive `{incident_dir}` = the directory containing `{incident_report_file}` (where `diagnosis.md`, `remediation_plan.md`, `postmortem.md` will be written).

## Severity routing

| Severity | Mode | Diagnosis (Phase 2) | Review (Phase 3) | Hotfix (Phase 4) | Confidence gates | Post-mortem (Phase 5) |
| --- | --- | --- | --- | --- | --- | --- |
| **P1** (critical, service down) | **streamlined** — speed beats exhaustiveness | `incident-diagnosis` `mode: streamlined` (1 agent / main thread) | `review-artifact` `mode: abbreviated` | `hotfix-plan` `mode: streamlined` (one fast safe plan) | Phase 2→3: **≥ 70%** · Phase 3→4: quick validation pass | **deferred** — placeholder; run `/create-post-mortem` after resolution |
| **P2 / P3 / P4** (high / medium / low) | **full** — thorough | `incident-diagnosis` `mode: full` (1–3 agents + consensus) | `review-artifact` `mode: full` | `hotfix-plan` `mode: full` (3-way fastest/safest/balanced, user picks) | Phase 2→3: **≥ 90%** · Phase 3→4: **≥ 90%** (review-artifact) | **now** — `post-mortem` skill |

Phase 4→5 (both): user approval of the plan. Phase 5→Done: P1 — service restored; P2–4 — post-mortem complete.

## Process

Create a todo list with all phases, then go through them in order.

### Phase 1 — Validate the incident report

1. Parse `$ARGUMENTS` → `{severity}`, `{incident_report_file}`; derive `{incident_dir}`.
2. Read the incident report and confirm it has: incident summary (severity, affected systems, customer impact), timeline of events, technical details (symptoms, errors, logs/traces), an initial hypothesis if available.
3. If it's incomplete, ask the user to fill the missing sections before proceeding.
4. Confirm the severity with the user, then proceed in the matching mode (see the table).

### Phase 2 — Diagnosis

Use the `incident-diagnosis` skill with:

- `incident_dir`: `{incident_dir}` (it reads `incident_report.md` and the referenced logs/traces there)
- `mode`: `streamlined` if `{severity}` is P1, otherwise `full`
- `next_step`: `Phase 3 — Review Diagnosis`

The skill handles evidence analysis, the 5-Whys root-cause trace, the consolidation (consensus / disagreement / confidence-weighted findings — launching 1–3 `diagnosis-agent` workers in `full` mode), the mode-dependent confidence gate (≥ 70% streamlined / ≥ 90% full), and writing `{incident_dir}/diagnosis.md`.

When the skill hands back, proceed to [Phase 3].

### Phase 3 — Review Diagnosis

Use the `review-artifact` skill with:

- `artifact_path`: `{incident_dir}/diagnosis.md`
- `artifact_label`: `diagnosis`
- `reviewer_agent`: `diagnosis-reviewer-agent`
- `creator_agent`: `diagnosis-agent`
- `support_docs`: `{incident_dir}/incident_report.md`
- `mode`: `abbreviated` if `{severity}` is P1, otherwise `full`
- `next_step`: `Phase 4 — Hotfix Planning`

When the skill hands back, proceed to [Phase 4].

### Phase 4 — Hotfix Planning

Use the `hotfix-plan` skill with:

- `incident_dir`: `{incident_dir}` (it reads `incident_report.md` and the reviewed `diagnosis.md` there)
- `mode`: `streamlined` if `{severity}` is P1, otherwise `full`
- `severity`: `{severity}` (tone — P1 accepts technical debt; P2 may need a maintenance window; P3/P4 prefer a proper fix)
- `next_step`: `Phase 5 — Execution & Post-Mortem`

The skill handles the remediation strategy (one fast safe plan in `streamlined`; 3-way fastest/safest/balanced + trade-offs comparison in `full`, launching 1–3 `hotfix-planner-agent` workers), the rollback plan, risk analysis, the user-approval gate, and writing `{incident_dir}/remediation_plan.md`.

When the skill hands back, proceed to [Phase 5].

### Phase 5 — Execution & Post-Mortem

This phase is executed manually by the on-call engineers. Provide implementation guidance from `{incident_dir}/remediation_plan.md` (prerequisites, exact steps, validation, rollback triggers), then:

**IF `{severity}` is P1 (streamlined):**

1. Emphasize: pre-flight checks (critical only), the exact commands, the quick rollback plan, the immediate success criteria.
2. After the hotfix is applied and verified working in the affected environment, use the `qa-gates` skill with:
   - `prefix`: `{incident_dir}` (the source of truth — `incident_report.md`, `diagnosis.md`, `remediation_plan.md`)
   - `mode`: `streamlined` (skips the docs gate; the post-mortem covers doc drift later)
   - `confidence_gate`: `70` (matches the P1 streamlined gates already in earlier phases)
   - `next_step`: `Phase 5 — Post-mortem deferral`
3. After service is restored, defer the post-mortem 24–48 h: write a placeholder `{incident_dir}/postmortem_scheduled.md` ("Schedule the post-mortem for [date] once the team has recovered").
4. End the workflow: "Service restoration is the priority. Run `/create-post-mortem` when ready."

**IF `{severity}` is P2 / P3 / P4 (full):**

1. Ask the user to confirm when remediation is complete (ideally with execution notes — deviations, surprises, actual resolution time — appended to `remediation_plan.md`).
2. After the hotfix is applied and verified working, use the `qa-gates` skill with:
   - `prefix`: `{incident_dir}`
   - `mode`: `full` (all 5 gates including docs)
   - `confidence_gate`: `90` (matches the P2-4 full gates already in earlier phases)
   - `next_step`: `Phase 5 — Post-mortem`
3. Use the `post-mortem` skill with:
   - `incident_dir`: `{incident_dir}` (it reads `incident_report.md`, the reviewed `diagnosis.md`, and `remediation_plan.md`)
4. The skill produces the blameless post-mortem (timeline + response metrics, root cause, what went well / wrong / where we got lucky, action items with owners & deadlines, prevention measures) and writes `{incident_dir}/postmortem.md`. When it hands back, this command is complete.

## Output documents

Written into `{incident_dir}` (alongside `incident_report.md`):

**P1 (streamlined):**

1. `diagnosis.md` — quick root cause analysis (reviewed; carries a `## Review` section)
2. `remediation_plan.md` — fast-track fix plan
3. `postmortem_scheduled.md` — placeholder for the deferred post-mortem

**P2 / P3 / P4 (full):**

1. `diagnosis.md` — comprehensive root cause analysis (reviewed; carries a `## Review` section)
2. `remediation_plan.md` — detailed remediation plan
3. `postmortem.md` — full post-mortem with action items

## Escalation points

At any phase, escalate to a human expert if:

- a P1 incident still has an unclear root cause after ~30 minutes
- there are multiple plausible root causes with no clear winner
- remediation requires breaking changes or a data migration
- the team lacks expertise in the affected system
- there are regulatory/compliance implications

Flag it clearly: "ESCALATION RECOMMENDED: [reason]".
