# Skills Inventory

Skills are the methodology — each is one `SKILL.md` (some carry a `templates/` subdir). Skills run ad-hoc, or as phases inside an orchestrator command. Grouped by workflow family.

## Discovery (pre-workflow)

| Skill             | Role                                                                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lay-of-the-land` | Pre-workflow recon: sourced current-state map; no-assumptions, every finding cited. Phase 0 feeding `analyze` / `bug-investigation`. |
| `triage`          | Route a free-text request to the right entry skill / chain / loop primitive, or "just do it directly". Mid-flight detection first; ≤2 questions; one-line recommendation, never auto-executes. Restored + adapted to the skill-centric kit 2026-08-06. |

## Pre-implementation analysis & design (skill-centric, 2026-08-05)

One flexible analysis skill and one flexible design skill replace the per-family phases
(greenfield PRD pipeline, integration analysis/techspec, refactor audit/plan, impact analysis —
bodies preserved under `archive/`).

| Skill             | Role                                                                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `analyze`         | Unified reference map of upcoming work; detects mode (integration / greenfield / refactor) and applies its lens. Produces `{work_name}_analysis.md`. |
| `bug-investigation` | Trace path from entry point to failure, evidence-based root cause (VERIFIED/ASSUMED hops), minimal-fix proposal. Produces `{bug_id}_investigation.md`. |
| `techspec`        | Unified committed design blueprint; detects mode (integration / greenfield / refactor / fix + orthogonal risk lens), single-approach pragmatic by default with 3-way escalation. Produces `{work_name}_techspec.md`. |
| `tasks-breakdown` | Unified implementation-tasks decomposition; detects mode (integration / greenfield / refactor), balanced sizing by default with 3-way escalation, spec-carrying mode when the techspec is deliberately skipped. Produces `{work_name}_tasks.md`. |
| `review-artifact` | Adversarial review of an analysis / investigation / techspec / tasks doc — generic reviewer fan-out, re-grounding, doc-type lens (altitude vs section contract vs decomposition), in-place `## Review` block. (was `review-analysis`) |

## Implementation

| Skill            | Role                                                                                                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `implement-task` | Implement one task end-to-end (loose target: prefix / tasks-doc path / description); runs `verify-task` gates; review batched via `review-implementation` |

## Quality assurance

| Skill             | Role                                                                                                  |
| ----------------- | ----------------------------------------------------------------------------------------------------- |
| `qa-gates`        | 5 pass/fail gates: build/test, AC checklist, cross-cutting, docs, human go/no-go. Prefix-level.       |
| `verify-task`     | Per-task version: gates 1+2+3 only. Runs at end of each per-task implement command.                   |

## Incident response

Diagnosis rides inside `bug-investigation` (incident lens); hotfix planning inside fix-mode `techspec`. Only the closeout is a dedicated skill.

| Skill         | Role                                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| `post-mortem` | Blameless post-mortem after a resolved incident — impact, timeline, root cause, action items. Produces `postmortem.md` / `{incident_id}_postmortem.md`. |

## Engineering ownership (retention)

Personal-practice rituals invoked by hand, writing durable artifacts to `~/.claude/ownership/{topic}/`. Slimmed to its two low-friction members in the kit refactor (2026-08-06): the friction-heavy rituals (`predict-first`, `debug-first`, `adr-first`, `challenge-me`) stay under `archive/skills/` and can be restored individually if genuinely missed.

| Skill           | Role                                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `record-decision` | Cheap mid-work decision capture: full ADR-template record with AI-drafted rationale hard-flagged `UNREVIEWED`; the human owns the Rationale at review — in-session, or swept later by `/close`. |
| `onboard-me`    | Cold-read walkthrough of UNFAMILIAR code by a "staff engineer" — one step at a time, Socratic, lists assumptions every message.                  |

## Meta / session lifecycle

| Skill            | Role                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| `close`          | End-of-session retrospect → persist to auto-memory + observations + SESSION_LOG.md + propose commit             |
| `improve`        | Periodic self-improvement review of observations; produces staged review packet under `~/.claude/improvements/` |
