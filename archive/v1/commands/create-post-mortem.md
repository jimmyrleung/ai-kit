---
description: Write a blameless post-mortem after an incident — timeline + response metrics, root cause, what went well/wrong, action items with owners and deadlines.
argument-hint: (run from inside the incident directory, after the incident is fully resolved).
---

# Create Post-Mortem Command

This command is a thin shim: the `post-mortem` skill owns the methodology, the blameless discipline, and the output contract.

## Prerequisites

- You're in an incident directory.
- `incident_report.md`, `diagnosis.md` (reviewed — carries a `## Review` section), and `remediation_plan.md` all exist.
- **The incident is fully resolved** (not actively remediating). Best run 24–48 h after resolution — and ideally with execution notes (deviations, surprises, actual resolution time) appended to `remediation_plan.md`.

## Steps

1. Create a todo list with the steps for this command.
2. Use the `post-mortem` skill with:
   - `incident_dir`: the current directory (it reads `incident_report.md`, the reviewed `diagnosis.md`, and `remediation_plan.md`),
   - output file `postmortem.md` in the incident directory.

   The skill builds the timeline with response metrics, the root cause + contributing factors, what went well / what went wrong / where we got lucky, action items (owners, deadlines, success criteria, priority — bucketed immediate / short-term / long-term), prevention measures, the pattern check, and lessons & metrics — running on the main thread or delegating to one `@post-mortem-agent` worker for the Opus pin — then writes the file.

When the skill hands back, this command is complete. Next: create tracking tickets for the action items, distribute the post-mortem, and schedule the follow-up reviews.
