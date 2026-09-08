# ai-kit

A skill-centric kit for AI-assisted engineering workflows across Claude Code, OpenAI Codex CLI, and Cursor CLI. It codifies a disciplined, evidence-based approach to analysis, design, implementation, verification, incident response, and documentation, plus a self-improving meta-layer that turns session friction into refined skills over time.

This is **v2** of the kit (2026-08 refactor). The v1 kit — five workflow-family orchestrator commands, 17 named agents, document templates — is **deprecated** and preserved under [`archive/v1/`](archive/v1/). What changed, in one line: **all the methodology moved into 31 flexible, mode-detecting skills; the command / agent / template scaffolding around it was retired.**

## What's in here

```
ai-kit/
├── skills/     31 skills — self-contained folders (SKILL.md + supporting files)
├── docs/       Maintained shared-rule sources + repo rules (docs/rules/)
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

Two helpers at the front: **`triage`** routes the current request using relevant, valid artifact state; **`lay-of-the-land`** is the optional Phase-0 recon of unfamiliar territory. Every pre-implementation artifact (`_analysis`, `_investigation`, `_techspec`, `_tasks`) can be adversarially reviewed in place by **`review-artifact`** before the next stage builds on it. Artifact filenames follow one contract: [`docs/output-filename-contract.md`](docs/output-filename-contract.md).

## Design principles (what v2 changed)

- **Skills only.** No named agents — skills fan out to *generic* subagents, so an archived persona can never silently break a live fan-out again. No command wrappers — a `commands/` shim adds a name, not methodology. No templates — output shapes live inline in the skills that produce them.
- **Mode detection over per-family forks.** One `analyze-work`, one `techspec`, one `tasks-breakdown` — each detects the work type and adapts, replacing ~5 near-duplicate per-family variants each.
- **Loose inputs.** Every skill accepts a loose target — a description, a path, a prefix, a number, a file with a draft — resolves it, and echoes back what it resolved. Never a rigid argument shape.
- **Respect existing authorization.** `improve` stages proposals; `triage` recommends by default and can continue when execution is explicitly authorized. Commits and publishing retain their own authorization boundaries.
- **Review-then-commit.** No gate hard-requires a commit; committed-state is informational (`GO, conditional on commit`). The flow stays implement → verify → review → commit.
- **Evidence-based decisions.** Every gate failure records the specific check that failed; every observation has a date and a concrete trigger; `improve` consumes evidence, not impressions.
- **Archive-first evolution.** Nothing is deleted on retirement — it moves to `archive/`, and comes back individually only on felt need (that is how `triage`, `onboard-me`, `record-decision`, and `update-workflow-docs` returned).

## The self-improving loop

1. **In-session:** `verify-task` runs after each implemented task, recording pass/fail per gate.
2. **End of session:** the `close` skill records decisions, learnings, and supported friction through an optional configured recorder/store. The established `~/.claude` layout remains supported.
3. **Periodically:** the `improve` skill reads new observations and unresolved work, clusters supported friction, and stages proposed edits in the configured improvements store — each diff tied to evidence. Observation coverage is distinct from invocation telemetry.
4. **You review and apply.** The applied edits flow back into the skills that run the next session.

This is ai-kit operating on itself: the skills here are the same skills that propose changes to themselves.

## Install and synchronize

Prerequisites: Git, Python 3.12 or newer, Node 24 with npm, and a supported agent host.
Clone or download the whole repository into a stable path and run commands from its
root. Validate with the locked commands below before applying a sync. Provider
installation, authentication, and account access are separate from the link setup.
No private instruction, taxonomy, memory, or feedback files are required.

To rehearse without changing your real home, create an empty temporary directory and
pass its absolute path as `--home` to dry-run, apply, then check. The check follows
apply on a fresh home. Restart or refresh the host's catalog, inspect the discovered
canonical skill path, then try a bounded request such as “recommend only: document one
workflow in this disposable repository.” Record unavailable host execution explicitly;
a successful link check alone does not prove discovery or task execution.

The link-based installation needs its checkout to remain in place. To install a detached
skill, copy its complete `skills/<name>/` folder, including references, scripts, and provider
metadata. Shared supporting documents are already bundled under `references/shared/`;
their links resolve within that skill folder. No manual copy from `docs/` is needed.
Other skills explicitly invoked by a workflow and external tools remain separate prerequisites;
self-contained supporting files do not bundle an entire workflow chain or agent host.
See [provider capabilities and probes](docs/provider-capabilities.md) and the
[optional feedback contract](docs/contracts/feedback.md).

The canonical `skills/` tree is the single source. The common engine manages per-skill links in
`~/.claude/skills/` and `~/.agents/skills/`, records ownership under
`~/.claude/ownership/ai-kit-skill-sync.json`, and leaves canonical targets unchanged. Preview
normal-home changes before applying them:

```bash
# macOS / Linux
python3 scripts/sync-skills.py --dry-run
python3 scripts/sync-skills.py
python3 scripts/sync-skills.py --check
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

## Updating skills and shared rules

Symlink/junction installs expose edits to the checkout immediately on disk, including
uncommitted edits. They do not fetch repository updates; pull updates explicitly. Refresh
or restart the host to avoid relying on previously loaded instructions. Rerun sync after
adding or renaming skill directories. A detached copy updates only when you replace it
with a newer complete skill folder; preserve any local customizations first.

Maintainers edit shared rules in `docs/contracts/` and the shared provider/filename references
in `docs/`, then run:

```bash
npm run build:skill-references
npm run check:portability
```

Generation updates the required copies and their transitive document dependencies for each
skill. Generated headers identify the maintained source; edit that source instead of the copy.
Generation leaves unchanged output untouched and retires only unused generated files.
Include generated copies with source changes when distributing the skills. The normal final
portability check fails on missing, stale, or unowned generated content and performs no writes.
The generator is a maintenance step; detached users do not need it to read the bundled rules.

## Provider adapters

Provider-specific invocation and runtime mechanics live in thin, additive overlays:

- [Codex adapter mechanics](adapters/codex/README.md) — Codex instruction placement and wrapper details.
- [Cursor adapter mechanics](adapters/cursor/README.md) — Cursor instruction placement and wrapper details.

These guides refer back to the common engine; they do not define a second installation algorithm.

## v1 (deprecated)

The complete pre-refactor kit — READMEs, inventories, commands, agents, templates, retired skills — lives under [`archive/v1/`](archive/v1/), marked deprecated in place. A comparison of the two kits over real usage evidence drove the v2 absorptions; retired pieces return individually if genuinely missed.

## License

[MIT](LICENSE). Copyright (c) 2026 Jimmy Leung. Preserve third-party attribution when adapting bundled material.
