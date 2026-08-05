# Skills Inventory

Skills are the methodology — each is one `SKILL.md` (some carry a `templates/` subdir). Skills run ad-hoc, or as phases inside an orchestrator command. Grouped by workflow family.

## Discovery (pre-workflow)

| Skill             | Role                                                                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lay-of-the-land` | Pre-workflow recon: sourced current-state map; no-assumptions, every finding cited. Phase 0 feeding `analyze` / `bug-investigation`. |

## Pre-implementation analysis & design (skill-centric, 2026-08-05)

One flexible analysis skill and one flexible design skill replace the per-family phases
(greenfield PRD pipeline, integration analysis/techspec, refactor audit/plan, impact analysis —
bodies preserved under `archive/`).

| Skill             | Role                                                                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `analyze`         | Unified reference map of upcoming work; detects mode (integration / greenfield / refactor) and applies its lens. Produces `{work_name}_analysis.md`. |
| `bug-investigation` | Trace path from entry point to failure, evidence-based root cause (VERIFIED/ASSUMED hops), minimal-fix proposal. Produces `{bug_id}_investigation.md`. |
| `techspec`        | Unified committed design blueprint; detects mode (integration / greenfield / refactor / fix + orthogonal risk lens), single-approach pragmatic by default with 3-way escalation. Produces `{work_name}_techspec.md`. |
| `review-artifact` | Adversarial review of an analysis / investigation / techspec doc — generic reviewer fan-out, re-grounding, doc-type lens (altitude vs section contract), in-place `## Review` block. (was `review-analysis`) |

## Implementation

| Skill            | Role                                                                                                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `implement-task` | Implement one task end-to-end (loose target: prefix / tasks-doc path / description); runs `verify-task` gates; review batched via `review-implementation` |

## Quality assurance

| Skill             | Role                                                                                                  |
| ----------------- | ----------------------------------------------------------------------------------------------------- |
| `qa-gates`        | 5 pass/fail gates: build/test, AC checklist, cross-cutting, docs, human go/no-go. Prefix-level.       |
| `verify-task`     | Per-task version: gates 1+2+3 only. Runs at end of each per-task implement command.                   |

## Engineering ownership (retention)

Personal-practice rituals — keep staff-level judgment sharp while using AI heavily: generate-before-consume, then test-after. Deliberately friction-adding (that's the point), invoked by hand, writing durable artifacts to `~/.claude/ownership/{topic}/`. `predict-first` ↔ `challenge-me` are a matched pair (the saved prediction is the answer key); `record-decision` → `adr-first` are a capture→author pipeline (cheap AI capture now, owned-and-challenged later) — `record-decision` is the one friction-*removing* member, included here because it shares the decision store, numbering, and ADR gate.

| Skill           | Role                                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `predict-first` | Before AI: predict (touches/invariant/edge/shape/unknowns); re-run after to reconcile vs. reality and tag misses. Answer key for `challenge-me`. |
| `debug-first`   | Before AI on a NON-incident bug: form hypotheses yourself (Observed/Hypotheses/Tried/Question); AI then engages each with evidence.              |
| `adr-first`     | Critique-only ADR: you write the rationale, AI challenges (steelman the rejected option) first, polishes a distant second.                       |
| `record-decision` | Cheap mid-work decision capture: full ADR-template record with AI-drafted rationale flagged `UNREVIEWED`, reusing adr-first's store/numbering; `/close` sweeps unreviewed records to own + challenge via `adr-first`. The low-friction front-end to `adr-first`. |
| `challenge-me`  | Feature code-complete: ~5 judgment questions (failure modes/alternatives/invariants/blast radius); won't answer until you try; grades vs. code + your prediction. |
| `onboard-me`    | Cold-read walkthrough of UNFAMILIAR code by a "staff engineer" — one step at a time, Socratic, lists assumptions every message.                  |

## Meta / session lifecycle

| Skill            | Role                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| `close`          | End-of-session retrospect → persist to auto-memory + observations + SESSION_LOG.md + propose commit             |
| `improve`        | Periodic self-improvement review of observations; produces staged review packet under `~/.claude/improvements/` |
| `migrate-notion` | Guide a Notion-to-Obsidian migration (Notion MCP)                                                               |
