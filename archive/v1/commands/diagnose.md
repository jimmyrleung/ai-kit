---
description: Diagnose an incident — analyze the report, logs and traces, trace the failure, identify the root cause with evidence.
argument-hint: (run from inside the incident directory) optional severity hint — P1 → streamlined, P2–P4 → full.
---

# Diagnose Command

This command is a thin shim: the `incident-diagnosis` skill owns the methodology, the 5-Whys trace, the confidence gate, and the output contract.

## Prerequisites

- You're in an incident directory (e.g. `incidents/inc_2026-05-12_orders_api_outage/`).
- `incident_report.md` exists and is filled out.
- Referenced log/trace files are available (e.g. in `logs/`).

## Steps

1. Create a todo list with the steps for this command.
2. Use the `incident-diagnosis` skill with:
   - `incident_dir`: the current directory,
   - `mode`: `streamlined` if `$ARGUMENTS` indicates P1, otherwise `full` (default `full` ad-hoc),
   - output file `diagnosis.md` in the incident directory.

   The skill handles validating the incident report, the evidence analysis (logs / traces / metrics with timestamps), the 5-Whys root-cause trace, the consolidation (consensus / disagreement / confidence-weighted findings — launching 1–3 `diagnosis-agent` workers in `full` mode), the mode-dependent confidence gate (≥ 70% streamlined / ≥ 90% full), and writing the file.

When the skill hands back, this command is complete — the diagnosis is ready for `/review-diagnosis`.
