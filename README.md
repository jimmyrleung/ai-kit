# ai-kit

A skill-centric kit for AI-assisted engineering across Claude Code, OpenAI Codex CLI, and
Cursor CLI. The live catalog covers discovery, requirements, design, implementation, review,
QA, documentation, learning, walkthroughs, orchestration, and session improvement.

This is the current **v3** skill set. Its source of truth is the 26 tracked skills under
[`skills/`](skills/); each skill owns its process and any bundled templates or references.
The complete v1 kit and material retired during the v3 review remain under
[`archive/`](archive/).

## What's in here

```
ai-kit/
├── skills/          26 live skills, each rooted at skills/<name>/SKILL.md
├── root/            Global agent instructions (AGENTS.md) symlinked into the user home
├── adapters/        Codex and Cursor compatibility guidance and sync wrappers
├── loops/           Small reusable goal prompts
├── sync-skills.py   Common skill-link synchronization engine
└── archive/         The deprecated v1 kit and material retired from v2
```

See [`INVENTORY.md`](INVENTORY.md) for every live skill, its invocation mode, current role,
and external dependencies.

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

Small, already-defined work can enter later in the chain. Each skill resolves its own target
and prerequisites. `create-implementation-tasks` can replace the `techspec` → `tasks-breakdown`
pair with one pass that writes the techspec and the task files together.

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

- **Learning:** `breakout-session` and `triage-learning-content`.
- **Guided decisions:** `walkthrough` and `walkthrough-implementation`. Both run in chat by default and offer a `render-view` page when a round or change set is large.
- **Review views:** `render-view` turns a spec folder, a walkthrough decision round or an implementation tour into a generated, local HTML page (standard-library Python, no network requests). The reader answers on the page and pastes a Respond block back; the owning skill writes it into the markdown, which stays the source of truth.
- **Orchestration and maintenance:** `orchestrate`, `close`, `consolidate-sessions`, `improve`, `write-skills`, and `find-skills`.

Third-party skills installed locally—including `grill-me`, `grill-with-docs`,
`improve-codebase-architecture`, and `teach` from
[Matt Pocock's skills repository](https://github.com/mattpocock/skills)—are not part of ai-kit
and do not count as live skills. Local links under `skills/` are ignored by synchronization and
portability checks. See [`INVENTORY.md`](INVENTORY.md) for remaining external handoffs.

## Design principles

- **One skill, one job.** Each live folder has one `SKILL.md`; supporting templates and rules stay beside the skill that consumes them.
- **Loose inputs, explicit resolution.** Most workflows accept a description, path, task number, or existing artifact and resolve the concrete target before acting.
- **Evidence before confidence.** Source reads, executed checks, runtime observations, and external documentation support conclusions; a score never replaces evidence.
- **Separate stages.** Reconnaissance, requirements, design, implementation, review, live QA, and final release gates have different owners.
- **Bounded writes.** Documentation skills separate source roots from documentation roots; review and improvement workflows stage or request approval before broader changes.
- **Proportional orchestration.** Skills use focused subagents where independent coverage is valuable, while small scopes stay inline.
- **Markdown is the source; views are build output.** Generated pages are rebuilt from the docs, git-ignored, and never edited or committed.
- **Archive-first evolution.** Retired material remains under `archive/` rather than being presented as live.

## The self-improving loop

1. `close` distills session state, durable learnings, open work, and workflow friction.
2. `improve` reviews recorded observations and unresolved proposals, then stages a backlog for owner review.
3. `write-skills` creates or refactors focused skills from approved needs.
4. The portability workflow validates the reviewed skill population before distribution.

## Install and synchronize

Prerequisites: Git, Python 3.12 or newer, and a supported agent host. Clone or download the
repository into a stable path and run commands from its root.

The common engine manages links for repository-owned, real skill directories in
`~/.claude/skills/` and `~/.agents/skills/`. It ignores linked directories inside the source
tree. On Windows it creates directory junctions; on macOS and Linux it creates symbolic links.
Preview normal-home changes before applying them:

```bash
# macOS / Linux
python3 sync-skills.py --dry-run
python3 sync-skills.py
python3 sync-skills.py --check
```

On Windows, use `py -3` in place of `python3`. To rehearse against an isolated home, add
`--home <isolated-home>` to each command. `--check` is read-only. Other recovery or exception
switches are documented by `python3 sync-skills.py --help` and require deliberate use.

The same run symlinks [`root/AGENTS.md`](root/AGENTS.md), the owner's global agent
instructions, to `~/.agents/AGENTS.md` and `~/.claude/CLAUDE.md`, so an edit or a pull in the
checkout takes effect at once. If you fork the kit, replace that file with your own first.
Sync replaces an existing file at either path only when its bytes match `root/AGENTS.md`;
any other file is a conflict to merge by hand. `--uninstall` turns the links into plain copies.
Windows needs Developer Mode (Settings > System > For developers) to create file symlinks.

The link-based installation needs the checkout to remain in place. For a detached install,
copy the complete `skills/<name>/` folder, including its references, scripts, assets, and
provider metadata. No separate top-level `docs/` copy is required; required live support files
are bundled with their consuming skills.

After a sync, restart or refresh the host's skill catalog. A successful link check proves the
installation shape, not skill discovery or task execution; validate those separately in the
target host.

## Portability check

The GitHub Actions workflow validates the live skill names and frontmatter, local Markdown
links, Python and adapter syntax, and synchronization dry runs on Linux, macOS, and Windows.
It uses only Python's standard library and does not define or run skill evaluations.

## Provider adapters

Provider-specific invocation and runtime mechanics live in thin overlays:

- [Codex adapter mechanics](adapters/codex/README.md)
- [Cursor adapter mechanics](adapters/cursor/README.md)

Both adapters use the common synchronization engine. Their provider-specific operating notes
remain separate from the live skill inventory.

## Archive

- [`archive/v1/`](archive/v1/) contains the complete pre-refactor command, agent, template,
  and skill kit.
- [`archive/v2/`](archive/v2/) contains retired v2 skills and the former top-level shared
  documentation sources.

Archived material and locally linked third-party skills are not part of the 26 live skills.

## License

[MIT](LICENSE). Copyright (c) 2026 Jimmy Leung. Preserve third-party attribution when adapting bundled material.
