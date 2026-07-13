# ai-kit — Codex instruction layer

This file is the Codex-side counterpart of the kit's Claude conventions. It is **additive
instruction only** — it changes nothing in the canonical ai-kit skills/agents. It is consumed
by Codex CLI when present at Codex's instruction-cascade location.

> Verified against `codex-cli 0.130.0` (2026-05-17); re-verified on `0.144.1` (2026-07-10).
> Global read-location **confirmed**: **`~/.codex/AGENTS.md`** (parallels
> `~/.claude/CLAUDE.md`; `AGENTS.override.md` in the home dir takes precedence when present),
> plus the standard project-root→cwd cascade (combined cap `project_doc_max_bytes` = 32 KiB).
> Place this file there (or per project) — see `adapters/codex/README.md`.

## How to read the kit's sub-agent fan-out idiom (Codex-side A/C selection)

Many ai-kit skill bodies are written in Claude terms: *"launch 1–3 `@{x}-agent` sub-agents for
breadth, then consolidate."* **Codex does not autonomously spawn sub-agents** (`multi_agent` is
on, but workers are invoked **explicitly by name**, never model-spawned; `agents.max_depth`
default counting is **[verify]**). Apply this mapping instead — do **not** write or run any
orchestration script for it (the kit owns no fan-out harness, by decision):

- **Divergent + fixed roster** — the 3-way explorers (`integration-techspec`,
  `integration-tasks`, `refactor-plan`, `refactor-tasks`): run the approach/sizing passes by
  **invoking the matching worker skills by name** (e.g. `$integration-techspec-creator-agent`).
  The kit's 17 agents are installed as explicit-only skills (`$name`, implicit-invocation
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

## Generated command skills (how to read their bodies)

Codex has no command primitive. Any command whose capability **no junctioned skill owns** is
installed as a **generated Codex skill** — 10 today: the kit's **5 family orchestrators**
(`$full-bug-fix-workflow`, `$integration-feature-dev`, `$refactor-techdebt-dev`,
`$full-incident-response`, `$greenfield-dev`), **3 per-task executors**
(`$implement-task`, `$gf-implement-task`, `$implement-bug-fix`), and **2 standalone
doc-generation commands** (`$document-workflow` — only a stripped `$document-workflow-loop`
fork exists as a junctioned skill; `$update-workflow-docs` — no skill at all). All are
implicit-invocation **off** — they never auto-trigger; you invoke them explicitly by
`$name`, exactly as you typed `/name` in Claude. The ~25 thin per-phase shims are **not**
generated — invoke their methodology skill directly.

Their bodies are the canonical command prose verbatim, written in Claude terms. Read them
with this mapping:

- **`use the X skill` / `the X skill`** → invoke the Codex skill `$X` (same name).
- **`/x` (a slash reference to another step)** → invoke the Codex skill that owns that
  step's methodology. For thin per-phase shims the skill name **differs from the command
  name** — map by methodology, e.g. `/investigate-bug` → `$bug-investigation`,
  `/review-investigation` → `$review-artifact`, `/create-roadmap` → `$roadmap-creation`,
  `/create-techspec` → `$techspec-creation`, `/analyze-impact` → `$impact-analysis`.
- **`@x-agent`** → `$x-agent` (the 17 agents are generated explicit-only skills); apply
  the fan-out A/C mapping above.
- **`create a todo list` / phase gates** → use `update_plan`; honor the gate as written
  (e.g. "confidence ≥ 90%" — surface it, do not silently pass).

This is *interpretation by instruction*, not a per-file transform — consistent with the
no-kit-harness decision. The command→skill name divergence for shims is a known v1 rough
edge (the orchestrators themselves increasingly reference skills by skill-name already).

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
