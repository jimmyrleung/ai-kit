# ai-kit — Cursor instruction layer

This file is the Cursor-side counterpart of the kit's Claude conventions. It is
**additive instruction only** — it changes nothing in the canonical ai-kit
skills/agents. Cursor reads project-root `AGENTS.md` (and `CLAUDE.md`) as rules.

> Verified against Cursor docs (`cursor.com/docs`), 2026-05-19. The exact
> **global** read-location for `AGENTS.md` is **[verify on installed binary]** —
> project-root cascade is standard; a `~/.cursor/AGENTS.md` global analog
> (parallels `~/.claude/CLAUDE.md`) is build-dependent. Place this per project
> (or globally if your build reads it) — see `adapters/cursor/README.md`.

## How to read the kit's sub-agent fan-out idiom

Many ai-kit skill bodies say *"launch 1–3 `@{x}-agent` sub-agents for breadth,
then consolidate."* Cursor **has a native subagent primitive** (closer to Claude
than Codex), but apply this mapping — do **not** write or run any orchestration
script (the kit owns no fan-out harness, by decision):

- **Divergent + fixed roster** — the 3-way explorers (`integration-techspec`,
  `integration-tasks`, `refactor-plan`, `refactor-tasks`): run the
  approach/sizing passes by invoking the matching worker subagents **by name**
  (e.g. `integration-techspec-creator-agent`). They are installed as native
  Cursor subagents (`~/.cursor/agents/<name>.md`). The worker **count is
  conditional on the S/M/L/XL classifier the skill already computes** (S → 1
  pass; M → up to 3). Then do the skill's **existing one-shot consolidation**.

- **Convergent + stateful** — `review-artifact`, `bug-investigation` (M-path),
  `qa-loop`/`review-checkpoint`: run the **parallel independent passes** the
  same way (named subagents). The **multi-round re-run loop does NOT run
  autonomously.** `review-artifact`'s canonical file is **frozen for this
  initiative** — run it **unchanged**: independent reviewer passes → surface the
  verdict → **the human drives any re-run interactively** (this collapses into
  the skill's existing "confirm the change set / ask if OK to proceed" steps).
  Do not emit or consume a headless verdict-runner — that is the deferred,
  re-homed cc-looper-class effort, not this adapter.

- **Small / skip-checked** — `review-artifact` Step-0, small-bug paths:
  **single-thread**. The skill's own skip-checks already short-circuit these.

## Generated orchestrator / executor skills (how to read their bodies)

Cursor deprecated standalone slash-commands (folded into Skills). The kit's
**5 family orchestrators** (`/full-bug-fix-workflow`, `/integration-feature-dev`,
`/refactor-techdebt-dev`, `/full-incident-response`, `/greenfield-dev`) and
**3 per-task executors** (`/implement-task`, `/gf-implement-task`,
`/implement-bug-fix`) are installed as **generated Cursor skills with
`disable-model-invocation: true`** — they never auto-trigger; invoke them
explicitly by `/name` (exactly as you typed `/name` in Claude). The ~25 thin
per-phase shims are **not** generated — invoke their methodology skill directly.

Their bodies are the canonical command prose verbatim, written in Claude terms.
Read them with this mapping:

- **`use the X skill` / `the X skill`** → invoke the Cursor skill `X` (same
  name; skills are auto-discovered, or `/X` explicitly).
- **`/x` (a slash reference to another step)** → invoke the Cursor skill that
  owns that step's methodology. For thin per-phase shims the skill name
  **differs from the command name** — map by methodology, e.g.
  `/investigate-bug` → `bug-investigation`, `/review-investigation` →
  `review-artifact`, `/create-roadmap` → `roadmap-creation`,
  `/create-techspec` → `techspec-creation`, `/analyze-impact` →
  `impact-analysis`.
- **`@x-agent`** → the native Cursor subagent `x-agent` (apply the fan-out
  mapping above).
- **`create a todo list` / phase gates** → use Cursor's plan/todo facility;
  honor the gate as written (e.g. "confidence ≥ 90%" — surface it, do not
  silently pass).

This is *interpretation by instruction*, not a per-file transform — consistent
with the no-kit-harness decision.

## Subagents: Cursor CLI parity gap (empirically confirmed 2026-05-19)

The 17 agents are generated as native subagents at `~/.cursor/agents/<name>.md`.
**The Cursor CLI (`cursor-agent`, ≥ `2026.05.09`) does NOT load *user-level*
`~/.cursor/agents/`** — only *project-level* `.cursor/agents/`. This is a
Cursor-staff-acknowledged IDE↔CLI parity bug (forum #160426, ack 2026-05-13,
no fix date). Confirmed on this machine: the 17 do not appear in `cursor-agent`;
`/create-subagent` itself writes to the *project's* `.cursor/agents/`.

Consequence, by recorded decision (do not "fix" without revisiting):

- **Cursor IDE** reads user-level fine — the 17 work there now.
- **Cursor CLI** — the 17 are **not** available as subagents until #160426 is
  fixed (then `~/.cursor/agents/` starts working with zero rework — this is why
  the adapter still generates it: it is the self-healing path).
- **For CLI work now**, the kit's fan-out degrades to **invoking the worker's
  methodology skill by name** (skills are user-level and DO load in the CLI):
  e.g. instead of the `bug-investigation-agent` subagent, invoke the
  `bug-investigation` skill. The 3-way explorers likewise invoke their
  creator/analysis *skills* by name. This is the existing fan-out instruction —
  no behavioural change, just "skill, not subagent" as the CLI worker unit
  until the bug clears.

Do **not** generate agents-as-skills or add a per-project `.cursor/agents/`
bootstrap unless the user asks — the recorded decision is to wait for the
upstream fix and use the methodology-skill fallback for CLI fan-out meanwhile.

## Structured user questions (no Cursor `AskUserQuestion` analog)

The kit and the global Claude rule prefer a structured "ask the user" tool.
Cursor CLI has **no structured multiple-choice tool** [verify: tool surface].
When a skill — or the clarification rule — calls for it, **degrade to a numbered
plain-text list** and accept a free-text reply:

```
Pick one (reply with the number, or describe your own):
  1. <option> — <one-line implication>
  2. <option> — <one-line implication>
```

Keep the question batching/discipline the kit specifies; only the *rendering*
changes.

## Model pins

ai-kit `agents/*.md` carry Claude model pins (`model: opus|sonnet`). The adapter
**drops** them when generating Cursor subagents → Cursor uses `model: inherit`
(the parent conversation's model; only `composer-2.5-fast` is pinnable per the
CLI). The capability-tier abstraction (vendor-neutral tiers → per-tool model
map) is a **tracked, deferred follow-up** (Category-2 — edits canonical agent
files). No action needed in Cursor.

## Frozen / out of scope for the adapter

- **`review-artifact` is frozen.** It is the quality gate for 4 of 5 workflow
  families; a broken gate erodes quality silently rather than crashing. Run it
  from the unchanged file (above). Any verdict-contract refactor is the separate
  cc-looper-class effort.
- The adapter is **additive**: it never edits canonical `skills/*/SKILL.md` or
  `agents/*.md`.
