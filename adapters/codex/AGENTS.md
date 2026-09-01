# ai-kit — Codex instruction layer (v2)

This file is the Codex-side counterpart of the kit's Claude conventions. It is **additive
instruction only** — it changes nothing in the canonical ai-kit skills. Codex consumes it
when it sits at an instruction-cascade location: paste it below the include point of your
private `~/.codex/AGENTS.md`, or copy it to the root of a project you run Codex in
(`AGENTS.override.md` in the home dir takes precedence; combined cap
`project_doc_max_bytes` = 32 KiB).

> Rewritten 2026-08-06 for the **v2 kit** (skill-centric refactor). Current skill mechanics are
> checked against the [Codex Agent Skills documentation](https://learn.chatgpt.com/docs/build-skills)
> and local `codex-cli 0.151.0` (`codex --version`, 2026-09-01). Re-verify after updates.

## The v2 surface (what Codex sees)

The common engine enumerates every canonical skill once and manages per-skill links in
`~/.claude/skills/` and `~/.agents/skills/`; the adapter scripts only forward to that engine.
Codex's documented user discovery root is `~/.agents/skills/`, and Codex follows symlinked
skill folders. The `SKILL.md` body is therefore shared without a provider transform. Codex
explicitly invokes a skill with `$skill` and may also select one from its `description`; see
the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills).

Skills auto-discover exactly as in Claude. Work chains by invoking the next skill, not by
running an orchestrator: `$analyze-work` → `$techspec` → `$tasks-breakdown` → `$implement-task`
(verify-task gates inline) → `$review-implementation` → `$qa-gates`; bugs/incidents enter
via `$bug-investigation` and rejoin the chain. `$triage` routes a free-text request.

## How to read the kit's fan-out idiom

Current Codex releases support subagent workflows in the CLI. Skills provide the work
contract; they do not provide a fan-out implementation. In Codex:

- **Native fan-out** → ask the active Codex session to delegate independent passes when its
  subagent facility is available; inspect/switch active threads with the build's documented
  interface. Keep the skill's consolidation step in the parent session.
- **Fallback** → if the installed build does not expose the needed spawn capability, run the
  same passes as independent sequential passes (fresh perspective, no shared scratch state).
  Never add a kit-owned orchestration script to compensate.
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

## Worker model and explicit overrides

Use the parent/session model by default. Codex's `--model` option selects the main-session
model; an explicit worker-model override is allowed only when the active subagent facility
supports it and the task requires it. Record that choice with the verification evidence.
Do not import historical model names or provider branches from `docs/model-assignments.md`
into canonical skill instructions.

## Goals and recurring work

Codex has no guaranteed provider-native `/goal`, `/loop`, or `/schedule` contract here.
Express the verifiable completion criterion in the active plan and use the available plan/todo
facility for phase gates. Treat recurrence as manual unless the installed runner documents a
compatible primitive; provider-native runner wiring stays in `docs/loop-recipes.md`. A context
reset in Codex is a new session — the SESSION_LOG handoff discipline still applies.

## Anchored feedback loop

`$close` / `$improve` / `$audit-skills` write to the fixed `~/.claude/…` paths
(observations, improvements, `last-audit.txt`) **even when run from Codex** — recorded
decision (§3a of the portability assessment): the self-improvement loop stays Claude-side
and works unchanged when driven from Codex. Artifact filenames follow
`docs/output-filename-contract.md` regardless of harness.

## Private instruction refresh

This file is a public mechanics layer, not a copy of private conventions. If it is copied
into `~/.codex/AGENTS.md` or a project instruction file, manually refresh the copied
`kit-mechanics` block after adapter edits. No repository script or sync wrapper may overwrite
that private file.

## Common sync posture

The adapter remains additive: it never edits canonical `skills/*/SKILL.md`. Use the root
`scripts/sync-skills.py` entry point for deployment; the adapter scripts are compatibility
wrappers only. Run a dry-run first, then restart Codex after a successful sync.

If an externally owned entry occupies a canonical skill name, use the common engine's explicit
`--preserve <claude|agents>/<skill-name>` policy (or PowerShell `-Preserve`) on dry-run, apply, and
check. It remains unowned and the flag must be repeated for qualified checks.
