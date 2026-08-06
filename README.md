# ai-kit

A skill-centric kit for [Claude Code](https://claude.com/claude-code) that codifies a disciplined, evidence-based approach to software engineering work — analysis, design, implementation, verification, incident response, documentation — plus a self-improving meta-layer that turns session friction into refined skills over time.

This is **v2** of the kit (2026-08 refactor). The v1 kit — five workflow-family orchestrator commands, 17 named agents, document templates — is **deprecated** and preserved under [`archive/v1/`](archive/v1/). What changed, in one line: **all the methodology moved into 29 flexible, mode-detecting skills; the command / agent / template scaffolding around it was retired.**

## What's in here

```
ai-kit/
├── skills/     29 skills — ALL the methodology lives here (one SKILL.md per folder)
├── docs/       Cross-cutting reference docs + repo rules (docs/rules/)
├── adapters/   Per-tool adapters (codex/, cursor/) — same canonical source on other CLIs
└── archive/    v1 kit (deprecated) + retired skills, kept restorable one by one
```

Skill-by-skill listing: [`INVENTORY.md`](INVENTORY.md).

## The core chain

Feature, refactor, and greenfield work all run the **same** chain — each skill detects the work type (integration / greenfield / refactor) and applies that lens, instead of forking into per-family variants:

```
/analyze → /techspec → /tasks-breakdown → /implement-task (× N tasks, verify-task gates inline)
        → /review-implementation → /qa-gates
```

Bugs and incidents enter through their own head and rejoin the chain (diagnosis is an incident lens inside `bug-investigation`; hotfix planning is `techspec` fix mode):

```
/bug-investigation → /review-artifact → /techspec (fix mode) → /implement-task (fix lens)
                  → /qa-gates → /post-mortem (incidents only)
```

Two helpers at the front: **`/triage`** routes a free-text request to the right entry point (and detects mid-flight work first); **`/lay-of-the-land`** is the optional Phase-0 recon of unfamiliar territory. Every pre-implementation artifact (`_analysis`, `_investigation`, `_techspec`, `_tasks`) can be adversarially reviewed in place by **`/review-artifact`** before the next stage builds on it. Artifact filenames follow one contract: [`docs/output-filename-contract.md`](docs/output-filename-contract.md).

## Design principles (what v2 changed)

- **Skills only.** No named agents — skills fan out to *generic* subagents, so an archived persona can never silently break a live fan-out again. No command wrappers — a `commands/` shim adds a name, not methodology. No templates — output shapes live inline in the skills that produce them.
- **Mode detection over per-family forks.** One `analyze`, one `techspec`, one `tasks-breakdown` — each detects the work type and adapts, replacing ~5 near-duplicate per-family variants each.
- **Loose inputs.** Every skill accepts a loose target — a description, a path, a prefix, a number, a file with a draft — resolves it, and echoes back what it resolved. Never a rigid argument shape.
- **Suggestion-mode by default.** Skills that propose changes (`improve`, `triage`, the commit step in `close`) stage diffs or recommendations and ask before acting.
- **Review-then-commit.** No gate hard-requires a commit; committed-state is informational (`GO, conditional on commit`). The flow stays implement → verify → review → commit.
- **Evidence-based decisions.** Every gate failure records the specific check that failed; every observation has a date and a concrete trigger; `/improve` consumes evidence, not impressions.
- **Archive-first evolution.** Nothing is deleted on retirement — it moves to `archive/`, and comes back individually only on felt need (that is how `triage`, `onboard-me`, `record-decision`, and `update-workflow-docs` returned).

## The self-improving loop

1. **In-session:** `verify-task` runs after each implemented task, recording pass/fail per gate.
2. **End of session:** `/close` retrospects — decisions, learnings, friction — and writes an observation file to `~/.claude/observations/`.
3. **Periodically:** `/improve` reads the accumulated observations, clusters friction patterns, audits which skills produced the friction, and stages proposed edits at `~/.claude/improvements/{date}/` — each diff tied to the observation that prompted it.
4. **You review and apply.** The applied edits flow back into the skills that run the next session.

This is ai-kit operating on itself: the skills here are the same skills that propose changes to themselves.

## Install (Claude Code)

Junction (or symlink) the skills into `~/.claude/` so Claude Code resolves them at runtime — edits in `ai-kit/` are then immediately live. v2 needs only the one junction (v1's `commands/` and `agents/` junctions are obsolete):

```powershell
# Windows
cmd /c mklink /J "$HOME\.claude\skills" "<path-to>\ai-kit\skills"
```

```bash
# macOS / Linux
ln -s /path/to/ai-kit/skills ~/.claude/skills
```

Or copy `skills/` into `~/.claude/` and re-copy after updates.

## Codex (OpenAI Codex CLI)

The kit runs on Codex from the same canonical source via a thin, additive adapter. Run it, then restart Codex:

```powershell
pwsh adapters/codex/sync.ps1 -WhatIf   # dry run
pwsh adapters/codex/sync.ps1           # bash adapters/codex/sync.sh on macOS/Linux
```

What it does in v2: junctions **every live skill 1:1** into `~/.codex/skills/` — nothing else. The v1-era generated twins (agent-skills, orchestrator-skills) are gone with the agents and commands that produced them; the sync prunes leftovers. The canonical tree is never modified.

> **Known-stale:** [`adapters/codex/AGENTS.md`](adapters/codex/AGENTS.md) (the Codex mechanics layer) and parts of [`adapters/codex/README.md`](adapters/codex/README.md) still describe the pre-refactor kit; their rewrite is a named pending bite. The sync itself is reconciled and verified against v2.

## Cursor (Cursor CLI)

> **Not yet reconciled with v2 — treat as v1-era.** [`adapters/cursor/`](adapters/cursor/) still expects the retired `commands/` and `agents/` populations (it generates orchestrator skills and native subagents from them) and its assessment predates the refactor. The per-skill symlink half would work, but run it only after a reconciliation pass like the one the Codex adapter got.

## v1 (deprecated)

The complete pre-refactor kit — READMEs, inventories, commands, agents, templates, retired skills — lives under [`archive/v1/`](archive/v1/), marked deprecated in place. A comparison of the two kits over real usage evidence drove the v2 absorptions; retired pieces return individually if genuinely missed.

## License

MIT. Everything here is intentionally hand-authored — adapt it to your own workflow.
