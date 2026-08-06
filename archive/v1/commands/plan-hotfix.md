---
description: Plan immediate incident remediation from a reviewed diagnosis — executable steps, validation, rollback plan, risk analysis.
argument-hint: (run from inside the incident directory) optional severity hint — P1 → streamlined (one fast safe plan), P2–P4 → full (3-way).
---

# Plan Hotfix Command

This command is a thin shim: the `hotfix-plan` skill owns the methodology, the rollback/risk discipline, and the output contract.

## Prerequisites

- You're in an incident directory.
- `incident_report.md` exists.
- `diagnosis.md` exists **and has been reviewed** via `/review-diagnosis` — it carries a `## Review` section with post-review confidence ≥ the gate and a recommendation of "Approved" / "Approved with notes". You've read and accepted it.

## Steps

1. Create a todo list with the steps for this command.
2. Use the `hotfix-plan` skill with:
   - `incident_dir`: the current directory,
   - `mode`: `streamlined` if `$ARGUMENTS` indicates P1, otherwise `full` (default `full` ad-hoc),
   - `severity`: from `$ARGUMENTS` if given (tone — P1 accepts technical debt; P2 may need a maintenance window; P3/P4 prefer a proper fix),
   - output file `remediation_plan.md` in the incident directory.

   The skill handles the remediation strategy (one fast safe plan in `streamlined`; 3-way fastest/safest/balanced + trade-offs comparison in `full`, launching 1–3 `hotfix-planner-agent` workers), the prerequisites/execution/validation steps, the rollback plan with concrete triggers, the risk analysis, the user-approval gate, and writing the file.

When the skill hands back, this command is complete — execute the remediation, then run `/create-post-mortem` once the incident is resolved.
