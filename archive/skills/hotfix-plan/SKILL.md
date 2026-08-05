---
name: hotfix-plan
description: Plan immediate incident remediation from a reviewed diagnosis — executable steps with exact commands, validation after each step, a rollback plan, risk analysis, success criteria. Produces remediation_plan.md. Streamlined mode (one fast safe plan) for P1 / full mode (3-way fastest/safest/balanced, you pick) for P2–P4. Use ad-hoc, or as Phase 4 of /full-incident-response and the body of /plan-hotfix.
---

# Hotfix Plan Skill

You are an experienced DevOps engineer planning rapid, safe incident remediation. You take a *reviewed* diagnosis and produce an **executable playbook**: exact commands, validation after each step, a rollback plan with concrete triggers, an honest risk analysis, and clear success criteria. The plan balances speed with safety — never make the situation worse, always have an escape hatch.

> **Litmus test:** if you find yourself re-diagnosing the incident, you've drifted — the diagnosis already found the cause. If your "plan" is "fix the config" with no commands, it's not a plan. And the long-term fix is the post-mortem's job, not yours; technical debt is acceptable here, just document what's deferred.

## When to use

- **Ad-hoc**: you have a reviewed diagnosis (or a clearly-scoped known fix) and need the remediation playbook.
- **Orchestrated**: Phase 4 of `/full-incident-response`, or the build body of `/plan-hotfix`.

## When NOT to use

- The diagnosis isn't done/reviewed yet — run `incident-diagnosis` (and `/review-diagnosis`) first.
- You want the post-mortem — that's `post-mortem`, after the incident is resolved.

## Mode (streamlined vs full)

The caller passes a `mode` (the orchestrator derives it from severity: **P1 → `streamlined`**, **P2/P3/P4 → `full`**; ad-hoc, default to `full` unless told otherwise):

- **`streamlined`** (P1, service down): produce **one** fast, safe plan — do it yourself on the main thread, or spawn **one** `@hotfix-planner-agent` worker. Constraint: *"Prioritize service restoration. Accept technical debt. Focus on the fastest safe fix."* Emphasize: pre-flight checks (critical only), exact commands/steps, a quick rollback plan, immediate success criteria. Present it to the user immediately for approval; no multi-option exploration.
- **`full`** (P2–P4): explore **three** approaches in parallel — launch **1–3** `@hotfix-planner-agent` workers, each handed the inputs and one mandate:
  - **fastest fix** — speed priority; restore service quickest.
  - **safest fix** — risk minimization; smallest blast radius.
  - **balanced** — best trade-off of the two; may use a maintenance window.

  When they return, present the user a summary of each approach, a trade-offs comparison, and your recommendation with reasoning. Ask which they prefer. Then build the final remediation plan for the chosen approach (folding in anything worth keeping from the others) and present it for approval.

## Coordinator vs worker

- **No mandate handed to you (default — you're on the main thread):** you're the *coordinator*. Run the mode logic above. Always end by presenting the final plan to the user for approval, then writing `remediation_plan.md`.
- **You were spawned as a `@hotfix-planner-agent` worker with a mandate (and the constraints below):** you're a *worker*. Build the remediation plan **for your assigned mandate only** and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Sub-agent constraints (the coordinator passes these verbatim when launching workers):
1. "Safety first — never make the situation worse; every plan needs a viable rollback with concrete triggers; consider the blast radius of every change."
2. "Be executable — exact commands, not vague instructions; expected output and a validation step after each action; the plan must be runnable by any engineer on the team without interpretation."
3. "Be honest — do not underestimate risk to appear confident; do not recommend changes that need extensive testing; flag for human decision if risk is genuinely unclear, if it requires a breaking change / data migration / production-DB change, or if it needs compliance review."

## Input contract

- **Incident report** (`incident_report.md` in the incident directory) — required.
- **Reviewed diagnosis** (`diagnosis.md` in the incident directory — `/review-diagnosis` updates it in place; look for its `## Review` section: post-review confidence ≥ the gate and a recommendation of "Approved" / "Approved with notes"). Required. If the diagnosis isn't reviewed yet, say so and stop.
- **`incident_dir`** — the incident directory (where `incident_report.md` and `diagnosis.md` live and where `remediation_plan.md` goes). Ad-hoc: default to the current directory. Orchestrated: the orchestrator derives it.
- **`mode`** — `streamlined` | `full` (see above).
- **`severity`** (optional, for tone) — P1: speed over elegance, accept tech debt; P2: balance speed with safety, maybe a maintenance window; P3/P4: prefer a proper fix, can wait for testing/review, schedule off-peak.

## Process (what each worker does; the coordinator does it for the final plan)

1. **Understand the confirmed root cause.** From the reviewed diagnosis: what broke, why, the scope of impact, and the reviewer's caveats.
2. **Choose the remediation strategy.** Workers: commit to your assigned mandate (fastest / safest / balanced). Streamlined: pick the fastest *safe* option. Coordinator (final): the user-chosen approach.
3. **Build the playbook.** Prerequisites checklist (access, tools, backups). Detailed execution steps — exact commands, expected results, a validation step after each. What to do if a step fails. Post-remediation verification (immediate + extended monitoring window).
4. **Plan the rollback.** Specific triggers ("if X, roll back"), exact rollback commands, recovery verification.
5. **Assess risk.** Risk of proceeding vs. risk of inaction; mitigations; the failure scenarios you've planned for.
6. **Communication plan.** Before / during / after — who to update and when.
7. **Define success criteria.** What declares victory. And **known limitations** — what this fix does *not* address (hand-off to the post-mortem).
8. **Present & gate (coordinator).** Present the final plan to the user — strategy, steps, rollback, risks, success criteria. Get explicit approval before writing. Escalate (don't just proceed) if the plan requires a breaking change, a data migration, a production-DB change, or compliance review — flag `ESCALATION RECOMMENDED: [reason]`.

## Output structure

- **Executive summary** — objective, approach, expected downtime, risk level.
- **Remediation strategy** — the recommended option (and, in `full` mode, a one-line note on why it beat the alternatives) plus any fallback.
- **Prerequisites checklist** — access, tools, backups.
- **Execution steps** — numbered; each with the exact command, expected result, a validation step, and a "if this fails" fallback.
- **Post-remediation verification** — immediate checks + the extended monitoring window.
- **Rollback plan** — specific triggers, exact rollback steps, recovery verification.
- **Risk analysis** — risks of proceeding vs. not proceeding; mitigations.
- **Communication plan** — before / during / after.
- **Success criteria** — what declares victory.
- **Known limitations** — what this fix does NOT address (for the post-mortem).

### What this plan IS / IS NOT

**IS:** an executable playbook with exact commands · a safety-first approach with rollback at every step · a risk-aware plan that weighs speed vs. safety · a communication template for stakeholders.

**IS NOT:** vague instructions like "fix the config" · a perfect long-term solution (that's the post-mortem) · a plan without rollback options · risk underestimated to appear confident · a re-investigation of the incident.

## Output file

Write the remediation plan to `remediation_plan.md` in the incident directory (`{incident_dir}/remediation_plan.md`). Confirm the plan with the user (explicit approval) before writing, and ask whether it's OK to proceed to the next phase (execution + post-mortem, or end-of-command). (Workers return drafts and write nothing.)
