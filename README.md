# ai-kit

A skill-centric kit for AI-assisted engineering workflows across Claude Code, OpenAI Codex CLI, and Cursor CLI. It codifies a disciplined, evidence-based approach to analysis, design, implementation, verification, incident response, and documentation, plus a self-improving meta-layer that turns session friction into refined skills over time.

This is **v2** of the kit (2026-08 refactor). The v1 kit — five workflow-family orchestrator commands, 17 named agents, document templates — is **deprecated** and preserved under [`archive/v1/`](archive/v1/). What changed, in one line: **all the methodology moved into 31 flexible, mode-detecting skills; the command / agent / template scaffolding around it was retired.**

## What's in here

```
ai-kit/
├── skills/     31 skills — ALL the methodology lives here (one SKILL.md per folder)
├── docs/       Cross-cutting reference docs + repo rules (docs/rules/)
├── adapters/   Per-tool adapters (codex/, cursor/) — same canonical source on other CLIs
└── archive/    v1 kit (deprecated) + retired skills, kept restorable one by one
```

Skill-by-skill listing: [`INVENTORY.md`](INVENTORY.md).

## The core chain

Feature, refactor, and greenfield work all run the **same** chain — each skill detects the work type (integration / greenfield / refactor) and applies that lens, instead of forking into per-family variants:

```
analyze-work → techspec → tasks-breakdown → implement-task (× N tasks, verify-task gates inline)
        → review-implementation → qa-gates
```

Bugs and incidents enter through their own head and rejoin the chain (diagnosis is an incident lens inside `bug-investigation`; hotfix planning is `techspec` fix mode):

```
bug-investigation → review-artifact → techspec (fix mode) → implement-task (fix lens)
                  → qa-gates → post-mortem (incidents only)
```

Two helpers at the front: **`triage`** routes a free-text request to the right entry point (and detects mid-flight work first); **`lay-of-the-land`** is the optional Phase-0 recon of unfamiliar territory. Every pre-implementation artifact (`_analysis`, `_investigation`, `_techspec`, `_tasks`) can be adversarially reviewed in place by **`review-artifact`** before the next stage builds on it. Artifact filenames follow one contract: [`docs/output-filename-contract.md`](docs/output-filename-contract.md).

## Design principles (what v2 changed)

- **Skills only.** No named agents — skills fan out to *generic* subagents, so an archived persona can never silently break a live fan-out again. No command wrappers — a `commands/` shim adds a name, not methodology. No templates — output shapes live inline in the skills that produce them.
- **Mode detection over per-family forks.** One `analyze-work`, one `techspec`, one `tasks-breakdown` — each detects the work type and adapts, replacing ~5 near-duplicate per-family variants each.
- **Loose inputs.** Every skill accepts a loose target — a description, a path, a prefix, a number, a file with a draft — resolves it, and echoes back what it resolved. Never a rigid argument shape.
- **Suggestion-mode by default.** Skills that propose changes (`improve`, `triage`, the commit step in `close`) stage diffs or recommendations and ask before acting.
- **Review-then-commit.** No gate hard-requires a commit; committed-state is informational (`GO, conditional on commit`). The flow stays implement → verify → review → commit.
- **Evidence-based decisions.** Every gate failure records the specific check that failed; every observation has a date and a concrete trigger; `improve` consumes evidence, not impressions.
- **Archive-first evolution.** Nothing is deleted on retirement — it moves to `archive/`, and comes back individually only on felt need (that is how `triage`, `onboard-me`, `record-decision`, and `update-workflow-docs` returned).

## The self-improving loop

1. **In-session:** `verify-task` runs after each implemented task, recording pass/fail per gate.
2. **End of session:** the `close` skill retrospects — decisions, learnings, friction — and writes an observation file to `~/.claude/observations/`.
3. **Periodically:** the `improve` skill reads the accumulated observations, clusters friction patterns, audits which skills produced the friction, and stages proposed edits at `~/.claude/improvements/{date}/` — each diff tied to the observation that prompted it.
4. **You review and apply.** The applied edits flow back into the skills that run the next session.

This is ai-kit operating on itself: the skills here are the same skills that propose changes to themselves.

## Install and synchronize

The canonical `skills/` tree is the single source. The common engine manages per-skill links in
`~/.claude/skills/` and `~/.agents/skills/`, records ownership under
`~/.claude/ownership/ai-kit-skill-sync.json`, and leaves canonical targets unchanged. Preview
normal-home changes before applying them:

```bash
# macOS / Linux
python3 scripts/sync-skills.py --dry-run
python3 scripts/sync-skills.py --check
python3 scripts/sync-skills.py
```

On Windows, use `py -3` in place of `python3`. For an isolated home, add
`--home <isolated-home>` to each command. `--check` is read-only; `--uninstall` restores
the immutable first-managed baselines, and `--force` / `--prune` remain explicit opt-ins.
If a managed root already contains an externally owned entry with a canonical skill name, pass
`--preserve <claude|agents>/<skill-name>` once per entry to dry-run, apply, and check. The entry
must already exist as a directory or link containing a readable `SKILL.md`, is not recorded as
ai-kit ownership, and the preserve flag must be repeated for later checks; an unqualified
invocation refuses the exception.
The full policy is in [`docs/rules/skill-authoring.md`](docs/rules/skill-authoring.md).

Validate the repository surface with the locked Node checker:

```bash
npm ci
npm test
npm run check:portability
```

## Provider adapters

Provider-specific invocation and runtime mechanics live in thin, additive overlays:

- [Codex adapter mechanics](adapters/codex/README.md) — Codex instruction placement and wrapper details.
- [Cursor adapter mechanics](adapters/cursor/README.md) — Cursor instruction placement and wrapper details.

These guides refer back to the common engine; they do not define a second installation algorithm.

## v1 (deprecated)

The complete pre-refactor kit — READMEs, inventories, commands, agents, templates, retired skills — lives under [`archive/v1/`](archive/v1/), marked deprecated in place. A comparison of the two kits over real usage evidence drove the v2 absorptions; retired pieces return individually if genuinely missed.

## License

MIT. Everything here is intentionally hand-authored — adapt it to your own workflow.
