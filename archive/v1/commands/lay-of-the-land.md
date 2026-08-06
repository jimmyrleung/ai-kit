---
description: Pre-workflow reconnaissance — produce a sourced "lay of the land" of an unfamiliar area of the codebase before a requirement is written/refined or a workflow starts. Analysis only.
argument-hint: File with the requirement / discovery topics, or a brief description of the area to reconnoitre.
---

# Goal

Produce a sourced **lay-of-the-land** reconnaissance of an unfamiliar area — what exists today, with a concrete source and a confidence score for every finding — so the requirement can be written/refined or the right workflow started from facts, not guesses. Analysis only: no code, no design, no planning.

This command is a thin shim: the `lay-of-the-land` skill owns the methodology, the mandatory Understanding gate, the no-assumptions / sourced-findings contract, the parallel `Explore` fan-out, the confidence gate, and the output structure.

## Process

**MUST DO**: Execute Workflow 1.

### Workflow 1 — Reconnaissance (skill)

1. Create a todo list with all steps for this command.
2. Use the `lay-of-the-land` skill with:
   - the requirement / discovery doc (or brief description) in `$ARGUMENTS` as the input,
   - output file `{topic}_lay-of-the-land.md` (alongside the requirement doc).

   The skill handles reading the doc + every referenced file, the mandatory Understanding gate, mapping discovery items, the parallel `Explore` sweep, per-item adjudication (answered-with-source vs escalated open question), the coverage ledger, the ≥ 90% confidence gate, and writing the file. It produces reconnaissance — not a design or plan; the litmus test is in the skill.

There is no separate review workflow: recon's human checkpoint is the skill's Understanding gate plus its confidence gate. The produced doc feeds the recommended downstream workflow (`/triage` if unsure, `integration-analysis`, `refactor-audit`, or `bug-investigation`).

When the skill hands back, this command is complete.
