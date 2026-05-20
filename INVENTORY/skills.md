# Skills Inventory

Skills are the methodology — each is one `SKILL.md` (some carry a `templates/` subdir). Skills run ad-hoc, or as phases inside an orchestrator command. Grouped by workflow family.

## Discovery (pre-workflow)

| Skill             | Role                                                                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lay-of-the-land` | Pre-workflow recon: sourced current-state map; no-assumptions, every finding cited. Phase 0 feeding integration-analysis / refactor-audit / bug-investigation. |

## Greenfield / new project

| Skill               | Role                                                                                                              |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `roadmap-creation`  | Master roadmap + slice list (Part I product spec, Part II slices). Anti-horizontal-scaffolding. Has `templates/`. |
| `prd-creation`      | Per-slice PRD, just-in-time at slice pickup                                                                       |
| `techspec-creation` | Slice-scoped techspec, lightweight by default. Has `templates/`.                                                  |
| `tasks-creation`    | Decompose techspec into vertically-ordered tasks. Has `templates/`.                                               |
| `triage`            | Free-text request → routes to the right workflow / one-shot phase / "just do it"                                  |

## Feature integration

| Skill                     | Role                                                                                                              |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `integration-analysis`    | Reference map of how a feature integrates (entry points, patterns, risks). Phase 1 of `/integration-feature-dev`. |
| `integration-techspec`    | 3-way techspec exploration (minimal-changes / clean / pragmatic)                                                  |
| `pragmatic-techspec`      | Single-approach pragmatic techspec (skip the 3-way)                                                               |
| `integration-tasks`       | 3-way task-sizing exploration (granular / balanced / pragmatic)                                                   |
| `balanced-tasks-creation` | Single-approach balanced tasks (skip the 3-way)                                                                   |

## Bug fix

| Skill                  | Role                                                                    |
| ---------------------- | ----------------------------------------------------------------------- |
| `bug-investigation`    | Trace path from entry point to failure, evidence-based root cause       |
| `impact-analysis`      | Blast radius, risk level, coverage gaps, rollback strategy              |
| `regression-test-plan` | Bug-fix verification + related-functionality + integration + perf tests |

## Refactor / tech-debt

| Skill            | Role                                                                      |
| ---------------- | ------------------------------------------------------------------------- |
| `refactor-audit` | Reference map of files, patterns, anti-patterns, scope, risks             |
| `refactor-plan`  | 3-way phased plan (minimal-risk / clean / pragmatic) with rollback points |
| `refactor-tasks` | 3-way sizing exploration for refactor tasks                               |

## Incident response

| Skill                | Role                                                         |
| -------------------- | ------------------------------------------------------------ |
| `incident-diagnosis` | Root cause via 5-Whys + evidence. P1 streamlined / P2+ full. |
| `hotfix-plan`        | Executable remediation steps + rollback + risk               |
| `post-mortem`        | Blameless post-mortem with action items (P2+ only)           |

## Quality assurance

| Skill             | Role                                                                                                  |
| ----------------- | ----------------------------------------------------------------------------------------------------- |
| `qa-gates`        | 5 pass/fail gates: build/test, AC checklist, cross-cutting, docs, human go/no-go. Prefix-level.       |
| `verify-task`     | Per-task version: gates 1+2+3 only. Runs at end of each per-task implement command.                   |
| `review-artifact` | Generic "review the artifact" sub-phase — launches 1–3 reviewer agents, gates at confidence threshold |

## Engineering ownership (retention)

Personal-practice rituals — keep staff-level judgment sharp while using AI heavily: generate-before-consume, then test-after. Deliberately friction-adding (that's the point), invoked by hand, writing durable artifacts to `~/.claude/ownership/{topic}/`. `predict-first` ↔ `challenge-me` are a matched pair (the saved prediction is the answer key).

| Skill           | Role                                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `predict-first` | Before AI: predict (touches/invariant/edge/shape/unknowns); re-run after to reconcile vs. reality and tag misses. Answer key for `challenge-me`. |
| `debug-first`   | Before AI on a NON-incident bug: form hypotheses yourself (Observed/Hypotheses/Tried/Question); AI then engages each with evidence.              |
| `adr-first`     | Critique-only ADR: you write the rationale, AI challenges (steelman the rejected option) first, polishes a distant second.                       |
| `challenge-me`  | Feature code-complete: ~5 judgment questions (failure modes/alternatives/invariants/blast radius); won't answer until you try; grades vs. code + your prediction. |
| `onboard-me`    | Cold-read walkthrough of UNFAMILIAR code by a "staff engineer" — one step at a time, Socratic, lists assumptions every message.                  |

## Meta / session lifecycle

| Skill            | Role                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| `close`          | End-of-session retrospect → persist to auto-memory + observations + SESSION_LOG.md + propose commit             |
| `improve`        | Periodic self-improvement review of observations; produces staged review packet under `~/.claude/improvements/` |
| `migrate-notion` | Guide a Notion-to-Obsidian migration (Notion MCP)                                                               |
