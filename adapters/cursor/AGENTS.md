# ai-kit — Cursor instruction layer (v2)

This file is the Cursor-side counterpart of the kit's Claude conventions. It is **additive
instruction only** — it changes nothing in the canonical ai-kit skills. Cursor reads
project-root `AGENTS.md` (and `CLAUDE.md`) as rules: paste this below the include point of
your private AGENTS.md, or copy/link it into the root of a project you run Cursor in (a
global read-location analog of `~/.claude/CLAUDE.md` is **[verify on installed binary]**).

> Rewritten 2026-08-06 for the **v2 kit** (skill-centric refactor). Current mechanics are
> checked against the [Cursor Agent Skills documentation](https://prod.cursor.com/docs/skills)
> and [Cursor subagent documentation](https://prod.cursor.com/docs/subagents), accessed 2026-09-01.
> Cursor is version-sensitive; re-verify after an update.

## The v2 surface (what Cursor sees)

The common engine enumerates every canonical skill once and manages per-skill links in
`~/.claude/skills/` and `~/.agents/skills/`; the adapter scripts only forward to that engine.
Cursor's current documentation lists `~/.agents/skills/` and `~/.cursor/skills/` plus
Claude/Codex compatibility roots. It can therefore surface duplicate entries. Require every
ai-kit occurrence to resolve to the same canonical `skills/<name>/` directory; make no
precedence claim and do not deduplicate provider roots here.
Cursor explicitly invokes skills with `/name` and may select them from `description`; the
shared `SKILL.md` body receives no provider transform.

Skills auto-discover off their `description` exactly as in Claude. Work chains by invoking
the next skill, not by running an orchestrator: `/analyze-work` → `/techspec` →
`/tasks-breakdown` → `/implement-task` (verify-task gates inline) →
`/review-implementation` → `/qa-gates`; bugs/incidents enter via `/bug-investigation` and
rejoin the chain. `/triage` routes a free-text request.

## How to read the kit's fan-out idiom

Current Cursor documentation supports subagents in the CLI, including foreground and
background/parallel work. Skills provide the work contract; they do not provide a fan-out
implementation. In Cursor:

- **Native fan-out** → use Cursor's subagent facility for independent passes when the installed
  CLI exposes it; use foreground work when the parent needs an immediate result and background
  work for long-running or parallel passes. Keep the skill's consolidation step in the parent.
- **Fallback** → if the needed facility is unavailable or blocked by the current mode, run the
  same passes independently and sequentially (fresh perspective, no shared scratch state).
  Never add a kit-owned orchestration script to compensate.
- **Multi-round re-run loops** (e.g. `/review-artifact` re-review after corrections) do
  **not** run autonomously — surface the verdict and let the human drive any re-run. This
  collapses into the skill's existing "confirm with the user" steps.
- **Worker constraints ride in the skill prose** (reviewer count, confidence filters,
  re-grounding rules) — honor them as written; only the spawning mechanism degrades.
- **`create a todo list` / phase gates** → use Cursor's plan/todo facility; honor gates as
  written (e.g. "confidence ≥ 90%" — surface it, do not silently pass).


## Structured user questions

The public Cursor docs do not establish a structured question tool for every CLI build. If
the installed surface does not expose one, **degrade to a numbered plain-text list** and accept
a free-text reply:

```
Pick one (reply with the number, or describe your own):
  1. <option> — <one-line implication>
  2. <option> — <one-line implication>
```

Keep the question batching/discipline the kit specifies; only the *rendering* changes.

## Worker model and explicit overrides

Use the parent/session model by default. Current Cursor subagent documentation uses
`model: inherit` as the default; an explicit worker-model override is appropriate only when
the active facility supports it and the task requires it. Team, plan, or mode restrictions may
still select a compatible fallback. Record the effective choice with the verification evidence.
Do not import historical model pins or provider branches from `docs/model-assignments.md`
into canonical skill instructions.

## Loop and goal mechanics

Current Cursor documentation exposes `/loop` to run a prompt or skill repeatedly at an interval.
Use it only after checking the installed CLI's current syntax; `/goal` and `/schedule` are not
assumed here. Skills remain the source of verifiable completion criteria. If the native loop is
unavailable or blocked, treat recurrence as manual and keep provider wiring in
`docs/loop-recipes.md`. A context reset in Cursor is a new session — the SESSION_LOG handoff
discipline still applies. See the [Cursor Agent Skills documentation](https://prod.cursor.com/docs/skills).

## Anchored feedback loop

`/close` / `/improve` / `/audit-skills` write to the fixed `~/.claude/…` paths
(observations, improvements, `last-audit.txt`) **even when run from Cursor** — recorded
decision: the self-improvement loop stays Claude-side and works unchanged when driven from
another harness. Artifact filenames follow `docs/output-filename-contract.md` regardless of
harness. **WSL caveat:** `~` resolves to the *WSL* home under `cursor-agent`-in-WSL — if
your Claude feedback store lives in the Windows home, link the WSL `~/.claude` to it (e.g.
`ln -s /mnt/c/Users/<you>/.claude ~/.claude`) so observations land in one store, not two.

## Private instruction refresh

This file is a public mechanics layer, not a copy of private conventions. If it is copied
into a private project or user instruction file, manually refresh the copied
`kit-mechanics` block after adapter edits. No repository script or sync wrapper may overwrite
that private file.

## Common sync posture

The adapter remains additive: it never edits canonical `skills/*/SKILL.md`. Use the root
`scripts/sync-skills.py` entry point for deployment; the adapter scripts are compatibility
wrappers only. Run a dry-run first, then restart `cursor-agent` after a successful sync.

If an externally owned entry occupies a canonical skill name, use the common engine's explicit
`--preserve <claude|agents>/<skill-name>` policy (or PowerShell `-Preserve`) on dry-run, apply, and
check. It remains unowned and the flag must be repeated for qualified checks.
