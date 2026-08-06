# ai-kit — Cursor instruction layer (v2)

This file is the Cursor-side counterpart of the kit's Claude conventions. It is **additive
instruction only** — it changes nothing in the canonical ai-kit skills. Cursor reads
project-root `AGENTS.md` (and `CLAUDE.md`) as rules: paste this below the include point of
your private AGENTS.md, or copy/link it into the root of a project you run Cursor in (a
global read-location analog of `~/.claude/CLAUDE.md` is **[verify on installed binary]**).

> Rewritten 2026-08-06 for the **v2 kit** (skill-centric refactor). Base mechanics verified
> vs Cursor docs (`cursor.com/docs`) 2026-05-19 + live probe on `cursor-agent`. Cursor ships
> near-daily — re-verify tagged items after an update.

## The v2 surface (what Cursor sees)

`adapters/cursor/sync.sh` (WSL — operative) / `sync.ps1` (Windows parity) links **every
canonical skill 1:1** into `~/.cursor/skills/` — nothing else. There are **no generated
twins**: v1's orchestrator-skills and native-subagent files are gone with the commands and
named agents that produced them (all archived under `archive/v1/`). One primitive, one name:
what Claude invokes as `/name`, Cursor invokes as `/name` too — same key, same skill.

Skills auto-discover off their `description` exactly as in Claude. Work chains by invoking
the next skill, not by running an orchestrator: `/analyze` → `/techspec` →
`/tasks-breakdown` → `/implement-task` (verify-task gates inline) →
`/review-implementation` → `/qa-gates`; bugs/incidents enter via `/bug-investigation` and
rejoin the chain. `/triage` routes a free-text request.

## How to read the kit's fan-out idiom

v2 skill bodies say things like *"fan out 1–3 generic reviewer subagents in parallel, then
consolidate"* — generic workers, no named agent personas. In Cursor:

- **Parallel generic fan-out** → use Cursor's **native subagent facility** where your build
  exposes it for ad-hoc spawns; otherwise run the same passes as **independent sequential
  passes** (fresh perspective each pass, no shared scratch state), then do the skill's own
  consolidation step. Do **not** write or run an orchestration script for it (the kit owns
  no fan-out harness, by decision).
- **Multi-round re-run loops** (e.g. `/review-artifact` re-review after corrections) do
  **not** run autonomously — surface the verdict and let the human drive any re-run. This
  collapses into the skill's existing "confirm with the user" steps.
- **Worker constraints ride in the skill prose** (reviewer count, confidence filters,
  re-grounding rules) — honor them as written; only the spawning mechanism degrades.
- **`create a todo list` / phase gates** → use Cursor's plan/todo facility; honor gates as
  written (e.g. "confidence ≥ 90%" — surface it, do not silently pass).

The v1-era CLI parity gap (forum **#160426**: `cursor-agent` ignores user-level
`~/.cursor/agents/`) no longer affects the kit — v2 installs nothing there. It only matters
again if named agent files ever return.

## Structured user questions (no Cursor `AskUserQuestion` analog)

The kit prefers a structured "ask the user" tool. The Cursor CLI has none **[verify: tool
surface]** — when a skill calls for it, **degrade to a numbered plain-text list** and accept
a free-text reply:

```
Pick one (reply with the number, or describe your own):
  1. <option> — <one-line implication>
  2. <option> — <one-line implication>
```

Keep the question batching/discipline the kit specifies; only the *rendering* changes.

## Model references

Claude model names in skill bodies (Opus workers in `/orchestrate`, tier notes) are
**advisory** — follow `/orchestrate`'s own provider-aware worker table when fanning out;
otherwise use the session's configured model (Cursor subagents default to `model: inherit`).
`docs/model-assignments.md` is historical (v1 agent pins; the agents are archived).

## Claude-only primitives

`/goal`, `/loop`, `/schedule`, `/compact`, plan mode, and the cc-looper loop skills are
Claude Code / runner facilities with **no Cursor analog**. Where `/triage` routes to a loop
primitive, treat it as a manual recurrence in Cursor (run the underlying skill each
iteration). A context reset in Cursor is a new session — the SESSION_LOG handoff discipline
still applies.

## Anchored feedback loop

`/close` / `/improve` / `/audit-skills` write to the fixed `~/.claude/…` paths
(observations, improvements, `last-audit.txt`) **even when run from Cursor** — recorded
decision: the self-improvement loop stays Claude-side and works unchanged when driven from
another harness. Artifact filenames follow `docs/output-filename-contract.md` regardless of
harness. **WSL caveat:** `~` resolves to the *WSL* home under `cursor-agent`-in-WSL — if
your Claude feedback store lives in the Windows home, link the WSL `~/.claude` to it (e.g.
`ln -s /mnt/c/Users/<you>/.claude ~/.claude`) so observations land in one store, not two.

## Adapter posture

The adapter is **additive**: it never edits canonical `skills/*/SKILL.md`. Sync is
idempotent; re-run `sync.sh` (dry-run with `--dry-run` first) after the skill population
changes, then restart `cursor-agent`.
