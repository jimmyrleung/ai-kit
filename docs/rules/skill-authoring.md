# Skill authoring — repo rules

## Validate frontmatter with the repository portability checker

Before shipping any `SKILL.md` frontmatter change, run the repository-owned strict checker from
the repo root:

```bash
npm ci
npm test
npm run check:portability
```

The checker parses every frontmatter block with `js-yaml`, enforces the Agent Skills standard
profile, and validates only the reviewed provider overlays. It catches the classic strict-YAML
failure: an unquoted `: ` inside a plain `description` scalar. Use a quoted description whenever
it contains YAML-special syntax. The final checker is fail-closed for coupling and documentation
drift; transitional mode remains an isolated fixture/test mode, not the shipping gate.

**Why:** strict parsers silently drop mis-parsed skills at load time, and one repository command
keeps validation reproducible across the supported CLIs.
*(updated 2026-08-31 — common Python/Node portability implementation)*

## External links in skills/ — enumerate entries explicitly; mind what you commit

The canonical `skills/` tree may contain symlinked or junctioned entries owned by an external
open-standard store. They are deployment shims, not automatically publishable source. They show
as untracked entries **with content** in `git status` — **never stage `skills/` wholesale**: this
repo is public and a wholesale add could vendor externally owned content. Stage new skills by
explicit path, and edit the link target when the external store owns the canonical file.

- **Detection:** inspect directory-entry metadata and link targets with a platform-appropriate
  filesystem API; a plain directory listing may not identify every link kind.
- **Editing:** do not write through an externally owned link when the editor uses an atomic
  temporary-file rename. Read and edit the canonical target instead.
- **Scanning:** use an explicit directory enumeration such as Node `fs.readdirSync` and account
  for supported link entries. A glob-only population scan can silently under-count the corpus.

**Why:** links keep one physical file per entry while another store owns the canonical content;
scans that ignore link entries under-count the population, and staging linked content can duplicate
external ownership in a public repo.
*(updated 2026-08-31 — cross-platform link handling)*

## Deployment topology: one source, two managed roots, provider overlays

`skills/` is the canonical source. The common sync engine at `scripts/sync-skills.py` manages
per-skill links under `<home>/.claude/skills/` and `<home>/.agents/skills/`, with ownership and
rollback state in `<home>/.claude/ownership/ai-kit-skill-sync.json`. The Codex and Cursor shell
and PowerShell adapters are thin argument translators; they must not enumerate skills or mutate
the roots independently.

Use an isolated home for previews and tests. The common commands are:

```bash
python3 scripts/sync-skills.py --dry-run --home <isolated-home>
python3 scripts/sync-skills.py --check --home <isolated-home>
python3 scripts/sync-skills.py --uninstall --dry-run --home <isolated-home>
```

The adapters expose equivalent provider syntax (`--dry-run` on POSIX, `-WhatIf` on PowerShell)
and forward to the same engine. A normal apply or uninstall is state-changing; preview it first.
The engine preserves adopted links and restores recorded baselines, while `--force` and `--prune`
remain explicit opt-ins for stale owned state and orphan cleanup.

If a managed root has an externally owned directory or link whose name matches a canonical skill,
preserve it explicitly with `--preserve <claude|agents>/<skill-name>` on dry-run, apply, and check.
The entry must already exist as a directory or link with a readable `SKILL.md` and remains outside
the ownership manifest. Repeat the flag for every qualified check; an unqualified invocation fails
closed instead of silently accepting a partial population. Preserve policy is not valid with
`--uninstall` or `--prune`.

The live canonical population count is currently 31 and is derived by `scripts/check-skill-portability.mjs`, not maintained
by the sync adapters. Enumerate it with `fs.readdirSync` (or an equivalent directory enumeration)
that follows supported link entries; do not use a glob that silently omits junctioned directories.

Provider-specific behavior belongs in a documented overlay: reviewed Cursor fields stay in
frontmatter only where their behavior is justified, and Codex policy stays in a skill-local
`agents/openai.yaml`. The canonical body remains capability-oriented and does not assume one
provider's tool names, model names, convention file, or checkout path.

**Why:** one engine gives all providers the same conflict, ownership, and recovery semantics while
overlays keep genuinely provider-specific metadata explicit.
*(updated 2026-08-31 — common sync engine and standard/overlay profile)*

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
**Renames add three more legs:** (1) the renamed skill's own description — a mechanical
find-replace mangles the trigger sentence ("Use when asked to analyze-implementation") and loses
the trigger verb; rewrite it by hand and re-run the tier-1 trigger sim. (2) Sibling description
budgets — every in-description reference grows by the name-length delta (+5 chars per ref pushed
triage's desc over the 800 band in the analyze-work rename); re-measure the edited descs against
audit Check 2. (3) Non-skill surfaces: `adapters/*/AGENTS.md` chain diagrams, root README chain
diagram, INVENTORY row, `docs/output-filename-contract.md` family column — plus the per-machine
`~/.codex` / `~/.cursor` junctions, which keep the old name until the sync scripts re-run.

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

## Diff a manual skill rewrite against HEAD before shipping it

When a skill body is rewritten by hand (editor reformat, reflow, restructure), compare the result
against `git show HEAD:<path>` before committing — specifically for: words joined at former line
breaks (reflow drops spaces: "aprovider", "byfilename"), internal references to structure that no
longer exists ("see Process 2" after de-numbering), and load-bearing content silently dropped
(a `{token}` derivation rule still referenced elsewhere in the doc; a cross-skill contract line).
A reformat that only *moves* text still changes what survives.

**Why:** the analyze-work rewrite (2026-08-26) shipped all three defect classes in one pass —
5 corrupted words, a dead internal ref, and a dropped `{work_name}` rule — none of which any
runtime error would ever surface; they were caught only by an explicit old-vs-new comparison.
*(added 2026-08-26 — analyze-work rename/rewrite session)*

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
