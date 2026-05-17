# ai-kit — Codex instruction layer

This file is the Codex-side counterpart of the kit's Claude conventions. It is **additive
instruction only** — it changes nothing in the canonical ai-kit skills/agents. It is consumed
by Codex CLI when present at Codex's instruction-cascade location.

> Verified against `codex-cli 0.130.0` (2026-05-17). The exact **global** read-location for
> `AGENTS.md` is **[verify on installed binary]** — project-root cascade is standard; a
> `~/.codex/AGENTS.md` global analog (parallels `~/.claude/CLAUDE.md`) is build-dependent.
> Place this per project (or globally if your build reads it) — see `adapters/codex/README.md`.

## How to read the kit's sub-agent fan-out idiom (Codex-side A/C selection)

Many ai-kit skill bodies are written in Claude terms: *"launch 1–3 `@{x}-agent` sub-agents for
breadth, then consolidate."* **Codex does not autonomously spawn sub-agents** (`multi_agent` is
on, but workers are invoked **explicitly by name**, never model-spawned; `agents.max_depth`
default counting is **[verify]**). Apply this mapping instead — do **not** write or run any
orchestration script for it (the kit owns no fan-out harness, by decision):

- **Divergent + fixed roster** — the 3-way explorers (`integration-techspec`,
  `integration-tasks`, `refactor-plan`, `refactor-tasks`): run the approach/sizing passes by
  **invoking the matching worker skills by name** (e.g. `$integration-techspec-creator-agent`).
  The kit's 18 agents are installed as explicit-only skills (`$name`, implicit-invocation
  off). The worker **count is conditional on the S/M/L/XL classifier the skill already
  computes** (S → 1 pass; M → up to 3) — static definitions, model-chosen invocation. Then do
  the skill's **existing one-shot consolidation** step. *(Strategy C — no behavioural loss.)*

- **Convergent + stateful** — `review-artifact`, `bug-investigation` (M-path),
  `qa-loop`/`review-checkpoint`: run the **parallel independent passes** the same way (named
  workers, strategy C). The **multi-round re-run loop does NOT run autonomously in Codex.**
  `review-artifact`'s canonical file is **frozen for this initiative** — run it **unchanged**:
  independent reviewer passes → surface the verdict → **the human drives any re-run
  interactively** (this collapses into the skill's existing "confirm the change set with the
  user / ask if OK to proceed" steps). Do not emit or consume a headless verdict-runner here —
  that is the deferred, re-homed cc-looper-class effort, not this adapter.

- **Small / skip-checked** — `review-artifact` Step-0, small-bug paths: **single-thread**
  (strategy A). The skill's own skip-checks already short-circuit these; no fan-out needed.

## Structured user questions (no Codex `AskUserQuestion` analog)

The kit and the global Claude rule prefer a structured "ask the user" tool. **Codex has no
structured multiple-choice tool** [verify: tool surface]. When a skill — or the clarification
rule — calls for it, **degrade to a numbered plain-text list** and accept a free-text reply:

```
Pick one (reply with the number, or describe your own):
  1. <option> — <one-line implication>
  2. <option> — <one-line implication>
```

Keep the question batching/discipline the kit specifies; only the *rendering* changes.

## Model pins

ai-kit `agents/*.md` carry Claude model pins (`model: opus|sonnet`). **Codex ignores them**
and uses its configured `model` / `model_reasoning_effort`. The capability-tier abstraction
(vendor-neutral tiers → per-tool model map) is a **tracked, deferred follow-up** — it edits
canonical agent files (Category-2) and is out of near-term scope. No action needed in Codex.

## Frozen / out of scope for the adapter

- **`review-artifact` is frozen.** It is the quality gate for 4 of 5 workflow families; a
  broken gate erodes quality silently rather than crashing. Run it from the unchanged file in
  C-mode (above). Any verdict-contract refactor is the separate cc-looper-class effort.
- The adapter is **additive**: it never edits canonical `skills/*/SKILL.md` or `agents/*.md`.
