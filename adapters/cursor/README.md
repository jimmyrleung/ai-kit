# ai-kit → Cursor CLI adapter (v2)

Makes the **single canonical ai-kit source** consumable by the **Cursor CLI**
(`cursor-agent`). The common deployment engine is `../../scripts/sync-skills.py`; this
adapter supplies only Cursor compatibility and runtime guidance.

> Design + decision record: `../../docs/cursor-portability-assessment.md`
> (historical; the v2 implementation uses the common engine). Current skill and subagent
> mechanics are checked against the [Cursor Agent Skills documentation](https://prod.cursor.com/docs/skills)
> and [Cursor subagent documentation](https://prod.cursor.com/docs/subagents), accessed 2026-09-01.
> Cursor is version-sensitive; re-verify claims against the installed CLI.

## What this is (and is not)

- **Category-1, additive, Claude-untouched.** Nothing here edits the canonical
  `skills/*/SKILL.md`.
- **Compatibility only.** `sync.sh` and `sync.ps1` forward to the common engine; they contain
  no canonical enumeration, link classification, mutation, or rollback implementation.
- **No kit-owned fan-out harness.** Use Cursor's native facility when available; the
  capability fallback and reading rules are documented in `AGENTS.md`.

## How it works (v2)

The common engine enumerates every canonical `skills/<name>/` directory once and manages
per-skill links in exactly `~/.claude/skills/` and `~/.agents/skills/`. Cursor's current
documentation also lists `~/.cursor/skills/` and the Claude/Codex compatibility roots,
but the common engine does not create or modify those provider-private roots. The
`SKILL.md` body is shared without a provider transform; see the [Cursor skill directories
and format](https://prod.cursor.com/docs/skills).

The adapter does not generate provider-specific skill copies, command/agent twins, or
subagent files. Historical v1 generation details remain in the superseded assessment;
the common engine's explicit `--prune` behavior applies only to its managed roots.

## Duplicate discovery: source equivalence, no precedence

Cursor can discover the same ai-kit skill from more than one root. The source-equivalence
rule is: every ai-kit occurrence must resolve to the same canonical `skills/<name>/` directory.
This adapter makes **no precedence claim** and does not attempt provider-root deduplication.

## Deployment
The root [`README.md`](../../README.md) is the canonical installation guide. Run the common
engine from the repository root, previewing the normal home before applying:

```bash
python3 scripts/sync-skills.py --dry-run
python3 scripts/sync-skills.py --check
```

The adapter paths remain compatibility entry points and forward the common switches unchanged:

```bash
bash adapters/cursor/sync.sh --dry-run --home <isolated-home>
```

```powershell
pwsh adapters/cursor/sync.ps1 -WhatIf -UserHome <isolated-home>
```

When a managed root contains an externally owned canonical-name entry, pass
`--preserve agents/<skill-name>` (or `-Preserve agents/<skill-name>` through PowerShell) once per
entry on dry-run, apply, and check. Preserved entries stay outside ai-kit ownership and the flag
must be repeated for qualified checks; the wrappers only translate and forward this policy.

They reject `CURSOR_HOME` / `-CursorHome` for sync-root selection; use `--home` / `-UserHome`
only for an isolated common user base. Restart `cursor-agent` after a sync.

The common engine is **idempotent** and safety-gated: it never changes a non-kit entry or
link target, and it records ownership/baselines before mutation. The wrappers do not write
private instruction files; `--check` is read-only.

> **Same-home rule.** Cursor reads user-level skills on the machine where the agent runs.
> Run the common sync in the same OS/user-home context as `cursor-agent`: a WSL run writes
> the WSL `~/.agents`/`~/.claude` roots, while a native Windows run writes that Windows
> user's roots. This is a home mismatch issue, not a skill-format incompatibility.

> **Line endings:** `sync.sh` must stay LF (`.gitattributes` enforces it) —
> a CRLF checkout breaks bash under WSL.

## Activating the instruction layer

`adapters/cursor/AGENTS.md` (the kit's Cursor-mechanics layer) must sit where
your Cursor build reads rules. Project-root `AGENTS.md`/`CLAUDE.md` is the
standard location; a global analog is **[verify on installed binary]**. If you
keep a private conventions AGENTS.md (see below), do **not** plain-copy over
it: paste the kit file's contents between its `<!-- kit-mechanics:begin/end -->`
markers and refresh that block after kit edits.

Refresh the copied block manually after adapter edits; no repository script or sync wrapper
may overwrite a private conventions file.


## Your personal conventions do not transfer (read this)

`adapters/cursor/AGENTS.md` is the kit's **Cursor-mechanics** layer only (the
v2 surface, fan-out reading rules, the structured-question plain-text
degradation, model notes, the anchored `~/.claude` paths). It is **not** a
replica of your `~/.claude/CLAUDE.md`.

The Cursor CLI does not read `~/.claude/CLAUDE.md`. So your personal working
agreement — confidence scoring, ask-before-assuming, scope discipline,
read-before-edit, verification-before-completion, risky-command confirmation,
session open/close offers — **does not reach Cursor**, and several kit skills
implicitly assume it. The fix mirrors how Claude already layers it:

- **Kit layer** (public, in-repo, this dir): `AGENTS.md`.
- **User layer** (private, **you own this**): mirror `~/.claude/CLAUDE.md` into
  a private AGENTS.md placed where your Cursor build reads rules, with an
  include point where the kit block is pasted. **Keep it out of this public
  repo.** `sync` never writes it; it prints a reminder instead.

## Open `[verify on installed binary]` items (re-check on Cursor update)

- `AGENTS.md` **global** read-location (project-root cascade is standard; a
  `~/.cursor/AGENTS.md` global analog is build-dependent).
- Precedence ordering among the native skills dirs (`~/.cursor/skills`,
  `~/.agents/skills`, project `.cursor/skills`, `.agents/skills`) — docs
  silent.
- Absence of an `AskUserQuestion`-analog in the CLI tool surface.
- Whether your build exposes native ad-hoc subagent spawns to the CLI (affects
  the fan-out degradation in `AGENTS.md`).

## Two-/three-consumer test debt

The junction means "edit the canonical file once," but **verification is now
3×**: any change to a canonical skill must be sanity-checked from Claude Code,
Codex, *and* the Cursor CLI.

## Commit vs. gitignore

ai-kit is a public repo. `adapters/cursor/{sync.sh,sync.ps1,AGENTS.md,README.md}`
are source — commit them. Managed links live in `~/.claude/skills` and
`~/.agents/skills` outside the repo — nothing is written into the tree, so there is
nothing to gitignore here.
