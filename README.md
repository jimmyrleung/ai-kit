# ai-kit

A skill-centric kit for AI-assisted engineering across Claude Code, OpenAI Codex CLI, and Cursor CLI. The live catalog covers discovery, requirements, design, implementation, review, QA, documentation, knowledge work, learning, walkthroughs, orchestration, and session improvement.

This is the current **v2** kit. Its source of truth is the 30 skills under [`skills/`](skills/); each skill owns its process and any bundled templates or references. The v1 command/agent/template kit is deprecated and preserved under [`archive/v1/`](archive/v1/).

## What's in here

```
ai-kit/
├── skills/     30 live skills — SKILL.md plus any bundled references or assets
├── docs/       Maintained shared-rule sources + repo rules (docs/rules/)
├── adapters/   Per-tool adapters (codex/, cursor/) — same canonical source on other CLIs
└── archive/    v1 kit (deprecated) + retired skills, kept restorable one by one
```

Skill-by-skill listing: [`INVENTORY.md`](INVENTORY.md).

## Main engineering workflow

For a defined feature, greenfield project, or refactor, the live end-to-end path is:

```text
lay-of-the-land (optional reconnaissance)
  → define-reqs
  → techspec
  → tasks-breakdown
  → implement-task (one task at a time)
  → review-implementation
  → qa-execution
  → qa-gates
```

`triage` can recommend the right entry point when it is unclear. Small, already-defined work can start later in the chain; the individual skill checks its own prerequisites.

Bugs and incidents start with evidence-based diagnosis, then join the same delivery path:

```text
bug-investigation
  → techspec (fix or hotfix mode)
  → implement-task
  → review-implementation
  → qa-execution
  → qa-gates
```

Documentation has its own related set: `docs-tasks-creator` inventories handlers, `document-workflow` traces one operation, and `update-workflow-docs` refreshes stale workflow docs. `document-terraform` documents Terraform estates, while `guides-and-sensors` proposes repository guidance and feedback mechanisms.

## Other live capabilities

- **Knowledge and learning:** `compile-kb`, `teach`, `breakout-session`, and `triage-learning-content`.
- **Guided understanding and decisions:** `onboard-me`, `walkthrough`, and `walkthrough-implementation`.
- **Orchestration and maintenance:** `orchestrate`, `close`, `improve`, `write-skills`, and `find-skills`.
- **Explicit architecture/grilling wrappers:** `grill-me`, `grill-with-docs`, and `improve-codebase-architecture`.

Four skills set `disable-model-invocation: true` and are intended for explicit invocation: `grill-me`, `grill-with-docs`, `improve-codebase-architecture`, and `teach`. See [`INVENTORY.md`](INVENTORY.md) for exact roles and dependency notes.

## Design principles

- **One skill, one job.** Each live folder has one `SKILL.md`; supporting templates and rules stay beside the skill that consumes them.
- **Loose inputs, explicit resolution.** Most workflows accept a description, path, task number, or existing artifact and resolve the concrete target before acting.
- **Evidence before confidence.** Source reads, executed checks, runtime observations, and external documentation support conclusions; a score never replaces evidence.
- **Separate stages.** Reconnaissance, requirements, design, implementation, review, live QA, and final release gates have different owners.
- **Bounded writes.** Documentation skills separate source roots from documentation roots; review and improvement workflows stage or request approval before broader changes.
- **Proportional orchestration.** Skills use focused subagents where independent coverage is valuable, while small scopes stay inline.
- **Archive-first evolution.** Retired material remains under `archive/` rather than being presented as live.

## The self-improving loop

1. `close` distills session state, durable learnings, open work, and workflow friction.
2. `improve` reviews recorded observations and unresolved proposals, then stages a backlog for owner review.
3. `write-skills` creates or refactors focused skills from approved needs.
4. Repository tests and portability checks validate the resulting skill population before distribution.

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

That manifest is internal link-manager state, not the feedback contract's ownership/decision
store; the preferred feedback profile keeps those records under `~/.agents/ownership/`.

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
