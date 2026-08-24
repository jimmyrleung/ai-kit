# Skill authoring — repo rules

## Validate frontmatter with a strict YAML parser (node + js-yaml)

Before shipping any SKILL.md / command / agent frontmatter change, parse it with node + js-yaml —
Claude Code is lenient, but Codex / claude.ai / the API are strict (an unquoted `: ` inside a
`description` is the classic failure). This repo ships no `node_modules`, and js-yaml is not in the
global npm root either (verified 2026-08-06): the reliable pattern is `npm init -y` **then**
`npm install js-yaml` in the session scratchpad and run node from there — without a `package.json`,
`npm install --no-save` walks UP the tree and installs into an ancestor (silent no-op locally;
verified 2026-08-06, comparison session). `cd` into the scratchpad is required; `require()` fails
with MODULE_NOT_FOUND from the repo root, from a bare `NODE_PATH=$(npm root -g)`, and even with
NODE_PATH pointed inline at the scratchpad's own node_modules (verified 2026-08-06, step-9 session).

**Why:** strict parsers silently drop mis-parsed skills at load time (5 skills broke at once on
2026-06-04), and the no-local-node_modules gotcha kept recurring because it lived only in archived
session-log narrative.
*(added 2026-07-23 — /close repo-memory bootstrap; sources: 2026-06-04 strict-YAML sweep, 2026-07-07 and 2026-07-23 audit runs; scratchpad-install refinement 2026-08-06 — step-8 session, global-root probe failed)*

## External junctions in skills/ — enumerate with readdir, never Glob; mind what you commit

Three skill dirs (`grill-me`, `grill-with-docs`, `improve-codebase-architecture`) are Windows
junctions to `~/.agents/skills/<name>` — an external open-standard store; they are shims for a
partially installed pack (improvements backlog 38 tracks their fate). They show as untracked
(`??`) **with content** in `git status` — **never `git add skills/` wholesale**: this repo is
public and a wholesale add would vendor the external content in. Stage new skills by explicit
path. (The v1-era cc-looper symlinks and `commands/tasks-loop.md` are gone since v2, and
`skills/find-skills` + `skills/teach` are real dirs now — this rule covers the three junctions
above and any future junctioned entry.)

- **Detection:** `Get-Item <path> -Force | Select-Object FullName, LinkType, Target` — `ls -la`
  does not mark them on Windows.
- **Editing:** the Edit tool cannot write through a link path (its atomic tmp-rename fails with
  ENOENT). Read + Edit the **canonical** `~/.agents/skills/` path.
- **Scanning:** Glob and Grep do NOT traverse directory junctions — a Glob-based population scan
  silently excludes all three (it bit audit run 11's Phase 1). Enumerate `skills/` via
  `Get-ChildItem` / Node `fs.readdirSync`.

**Why:** junctions keep one physical file per entry while external tools own the canonicals;
scans that trust Glob under-count the population and its description budget, and committing
junction content here would duplicate external ownership into a public repo.
*(added 2026-07-23 as the cc-looper symlink rule; rewritten 2026-08-24 — v2 dropped the cc-looper
links, and audit run 11 found the new `~/.agents` junctions the old text didn't cover)*

## Deployment topology: skills are junction-live; commands were copies; Codex twins block conversion

Three deploy surfaces, three sync semantics. `~/.claude/skills` is a single **wholesale junction**
to this repo's `skills/` — a new skill dir is discoverable immediately, no sync step.
`~/.claude/commands/*.md` were **real file copies** — an edit or removal had to be mirrored there
by hand. `~/.codex/skills/` holds per-skill junctions plus kit-GENERATED twins (`.ai-kit-generated`
marker) for commands/agents; when a command is converted to a skill, `sync.ps1`'s skill pass skips
any existing real dir, so the generated twin must be removed (and the `$GenCmds` entry dropped)
before the junction can be created — always `-WhatIf` first. Run `sync.ps1` **in-process under
pwsh 7** (`& C:\ai-kit\adapters\codex\sync.ps1 -WhatIf`) — invoking it via `powershell -File`
(Windows PowerShell 5.1) misparses the script's UTF-8 em-dashes into bogus syntax errors that look
like file corruption. Its dry-run flag is `-WhatIf`, not `-DryRun`. And don't pipe its output
through `Select-Object`/`Get-Item` in the same call — the Format-Table stream collides and exits 1
despite a successful sync; verify effects in a separate call.

**Why:** assuming one model (all junctions or all copies) leaves stale twins shadowing new skills,
or edits that never deploy — the twin-blocks-junction case surfaced during the first command→skill
conversion of the kit-refactor.
*(added 2026-08-05 — implement-task command→skill conversion session; pwsh-7/-WhatIf/format-stream
invocation refinements 2026-08-06 — step-8 session, all three hit in one sync run)*

## Grep live consumers before archiving or retiring an entity class

Before moving skills, commands, or agents to `archive/` (or renaming them), grep every live
surface for their names — skill bodies AND descriptions, the cc-looper canonical tree
(`~/projects/cc-looper/claude-config/`, which Grep won't reach through the symlinks), adapter
scripts (`sync.ps1` allowlists), and INVENTORY/docs. Derive the name list from the directory
being archived, not from memory. When sweeping *retrospectively* (an audit over the existing
`archive/`), **subtract names that are also live first** — `archive/` keeps pre-refactor copies
of skills later restored under the same name, and those self-match (359 of 360 hits in the
2026-08-05 run-2 sweep were self-matches until the live set was subtracted). References resolved
at spawn/run time (`@x-agent` subagent types, dynamic paths) produce **zero errors at archive
time** and fail only when someone runs the consumer. The sweep is **bidirectional**: also grep
what the surviving siblings *claim about* the retired/changed entity's structure — existence
checks catch dangling pointers, not stale descriptions of a shape that changed (verify-task
kept instructing "continue to Workflow 2 — Review" for two weeks after implement-task's
Workflow 2 was retired; three audit runs missed it because its own references all resolved).
The sweep also covers **conventions, not just entities**: when a *pattern* is retired (e.g. the
command-wraps-skill pairing), grep live bodies for it cited as doctrine or example — such
mentions can consist entirely of live names, so the name sweep never hits them (audit-skills
Check 10 kept teaching the retired pairing as "the intended pattern" via `/qa-gates → qa-gates`
— both names live; caught by judgment in audit run 5, third finding of this class).

**Why:** the 2026-08 agent archive silently broke review-implementation and all three cc-looper
loop review skills (`@code-reviewer-agent` fan-outs) — discovered 5 days later by /audit-skills,
not by any error. A hand-recalled sweep pattern also missed two of the refs; the archive dir
listing is the authoritative enumeration.
*(added 2026-08-05 — non-technical-paths consolidation + full audit session; archive-minus-live
refinement added same day — techspec-consolidation audit run 2; bidirectional refinement added
same day — implementation-family consolidation, step 5; doctrine/convention refinement added
same day — QA-family consolidation, step 6)*

## Population changes sync the self-description surfaces in the same step

When a step adds, restores, or archives a skill, update the kit's self-description
surfaces — the root `INVENTORY.md` and the affected `README.md` sections — in that
same step, or record an explicit deferral to a named reconciliation bite. "Done" for a population
change includes the listings, exactly like the Codex sync.

**Why:** nothing consumes these listings at runtime, so a stale row never throws — steps 8
(post-mortem added, no row) and 10 (triage restored, no row; archived migrate-notion still listed)
both drifted silently and were caught one and two steps late by /audit-skills run 9, which also
found README still shipping the retired five-workflow table and pre-refactor Codex numbers
(backlog 33). The consumer-grep rule above catches dangling *references*; it never catches a
*listing* that simply omits or over-includes.
*(added 2026-08-06 — step-10 close; audit run 9 INVENTORY delta-sync + backlog 33 enumeration)*

## Check new names against built-in CLI commands before choosing them

Before naming a new skill or command, check it doesn't collide with a Claude Code built-in
(`/code-review`, `/review`, `/security-review`, `/init`, `/run`, `/loop`, `/schedule`, `/config`,
`/compact`, `/clear`, …) or another provider's native command. Prefer a corpus-consistent
alternative (e.g. the family pattern: `review-artifact` / `review-checkpoint` /
`review-implementation`).

**Why:** a colliding name makes the invocation ambiguous or unreachable — the built-in wins or the
user can't tell which ran — and the collision only surfaces after the skill ships. Caught at design
time 2026-07-23: the batched-review skill was almost named `code-review`.
*(added 2026-07-23 — review-implementation authoring session)*

## Templates concept is retired — shapes live inline in skill bodies

The kit-root `templates/` dir was deleted 2026-08-06 (user call, "kill the templates concept").
Never reference `templates/<family>/...` from a live skill — describe the expected input/output
shape inline in one line instead ("a report typically carries severity, onset time, symptoms, …").
Historical copies remain byte-identical under `archive/templates/`. Skill-LOCAL template subdirs
(`skills/<name>/templates/`, `references/`) are unaffected — this rule is about the retired
kit-root scaffolds only.

**Why:** the dir sat 5/8 orphaned for months while skills silently pointed at it; loose input
contracts made per-family scaffolds dead weight, and dangling `templates/` refs shipped in the
same session that wired them (caught at close by git status).
*(added 2026-08-06 — archive-comparison close session)*
