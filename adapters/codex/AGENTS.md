# ai-kit — Codex instruction layer (v2)

This file is the Codex-side counterpart of the kit's Claude conventions. It is **additive
instruction only** — it changes nothing in the canonical ai-kit skills. Codex consumes it
when it sits at an instruction-cascade location: paste it below the include point of your
private `~/.codex/AGENTS.md`, or copy it to the root of a project you run Codex in
(`AGENTS.override.md` in the home dir takes precedence; combined cap
`project_doc_max_bytes` = 32 KiB).

> Rewritten 2026-08-06 for the **v2 kit** (skill-centric refactor). Mechanics last verified
> live on `codex-cli 0.144.1`; repo-level skill discovery verified on `0.146.0`. Re-verify
> after any Codex update.

## The v2 surface (what Codex sees)

`adapters/codex/sync.ps1` junctions **every canonical skill 1:1** into `~/.codex/skills/`
— nothing else. There are **no generated twins**: v1's agent-skills and orchestrator/command
skills are gone with the named agents, commands, and templates that produced them (all
archived under `archive/v1/`). One primitive, one name: what Claude invokes as `/name`,
Codex invokes as `$name` — the v1 command→skill name divergence no longer exists.

Skills auto-discover exactly as in Claude. Work chains by invoking the next skill, not by
running an orchestrator: `$analyze-work` → `$techspec` → `$tasks-breakdown` → `$implement-task`
(verify-task gates inline) → `$review-implementation` → `$qa-gates`; bugs/incidents enter
via `$bug-investigation` and rejoin the chain. `$triage` routes a free-text request.

## How to read the kit's fan-out idiom

v2 skill bodies say things like *"fan out 1–3 generic reviewer subagents in parallel, then
consolidate"* (Claude's Agent tool with generic Explore / general-purpose workers — there
are no named agent personas anymore). In Codex:

- **Parallel generic fan-out** → run the same passes as **independent sequential passes**
  (fresh perspective each pass, no shared scratch state), then do the skill's own
  consolidation step. If your Codex build exposes native multi-agent workers, use them;
  do **not** write or run an orchestration script for it (the kit owns no fan-out harness,
  by decision).
- **Multi-round re-run loops** (e.g. `$review-artifact` re-review after corrections) do
  **not** run autonomously — surface the verdict and let the human drive any re-run. This
  collapses into the skill's existing "confirm with the user" steps.
- **Worker constraints ride in the skill prose** (reviewer count, confidence filters,
  re-grounding rules) — honor them as written; only the spawning mechanism degrades.
- **`create a todo list` / phase gates** → use `update_plan`; honor gates as written
  (e.g. "confidence ≥ 90%" — surface it, do not silently pass).

## Structured user questions (no Codex `AskUserQuestion` analog)

The kit prefers a structured "ask the user" tool. Codex has none — when a skill calls for
it, **degrade to a numbered plain-text list** and accept a free-text reply:

```
Pick one (reply with the number, or describe your own):
  1. <option> — <one-line implication>
  2. <option> — <one-line implication>
```

Keep the question batching/discipline the kit specifies; only the *rendering* changes.

## Model references

Claude model names in skill bodies (Opus workers in `$orchestrate`, tier notes) are
**advisory for Claude harnesses** — Codex ignores them and uses its configured
`model` / `model_reasoning_effort`. `$orchestrate` is already provider-aware: Codex
workers inherit the session model. `docs/model-assignments.md` is historical (v1 agent
pins; the agents are archived).

## Claude-only primitives

`/goal`, `/loop`, `/schedule`, `/compact`, plan mode, and the cc-looper loop skills are
Claude Code / runner facilities with **no Codex analog**. Where `$triage` routes to a loop
primitive, treat it as a manual recurrence in Codex (run the underlying skill each
iteration). A context reset in Codex is a new session — the SESSION_LOG handoff discipline
still applies.

## Anchored feedback loop

`$close` / `$improve` / `$audit-skills` write to the fixed `~/.claude/…` paths
(observations, improvements, `last-audit.txt`) **even when run from Codex** — recorded
decision (§3a of the portability assessment): the self-improvement loop stays Claude-side
and works unchanged when driven from Codex. Artifact filenames follow
`docs/output-filename-contract.md` regardless of harness.

## Adapter posture

The adapter is **additive**: it never edits canonical `skills/*/SKILL.md`. Sync is
idempotent; re-run `sync.ps1` (dry-run with `-WhatIf` first) after the skill population
changes, then restart Codex.
