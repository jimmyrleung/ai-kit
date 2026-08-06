# ai-kit → Cursor CLI adapter (v2)

Makes the **single canonical ai-kit source** consumable by the **Cursor CLI**
(`cursor-agent`), alongside Claude Code and Codex, from one source of truth —
extending the existing `~/.claude` / `~/.codex` junction model.

> Design + decision record: `../../docs/cursor-portability-assessment.md`
> (written for the v1 kit; the symlink mechanism survived the 2026-08 v2
> refactor, the generated surfaces did not). Base mechanics verified against
> Cursor docs (`cursor.com/docs`) 2026-05-19 and probed live on `cursor-agent`.
> Cursor ships near-daily — re-verify items tagged **[verify on installed
> binary]** after an update.

## What this is (and is not)

- **Category-1, additive, Claude-untouched.** Nothing here edits the canonical
  `skills/*/SKILL.md`. The adapter only creates symlinks/junctions in Cursor's
  home (`~/.cursor/skills`).
- **No kit-owned fan-out harness** (recorded decision: rely on the native
  harness, never an orchestration script in a skill). Fan-out reading rules are
  *instruction*, in `AGENTS.md`.

## How it works (v2)

One mechanism left: every canonical `skills/<name>/` gets a per-skill
**symlink** (WSL/Linux) or **junction** (Windows) →
`${CURSOR_HOME:-~/.cursor}/skills/<name>` — Cursor's native user-level skills
root. The `SKILL.md` spec is identical, so **no body transform**. What Claude
invokes as `/name`, Cursor invokes as `/name` too — same key, same skill.
Junctioned skills auto-discover off their `description`, exactly as in Claude.

The v1 kit also **generated** Cursor-only artifacts: 8 orchestrator/executor
skills (from `commands/`, `disable-model-invocation: true`) and 17 native
subagents (from `agents/`, at `~/.cursor/agents/`). v2 retired those
populations entirely (archived under `archive/v1/`), so **nothing is generated
anymore** — the sync's generation paths are dormant and its allowlist is empty.
Run `--prune` once after upgrading from v1 to remove the leftovers (including
symlinks left dangling by the `archive/v1` move).

## Usage

```bash
# WSL / Linux (PRIMARY — cursor-agent is typically run under WSL because the
# Windows Cursor CLI hard-codes a PowerShell shell with cold-start hangs).
# Run from inside WSL so it targets the WSL ~/.cursor:
bash adapters/cursor/sync.sh --dry-run
bash adapters/cursor/sync.sh
bash adapters/cursor/sync.sh --prune            # report v1 leftovers
bash adapters/cursor/sync.sh --prune --force    # remove them
```

```powershell
# Windows-native parity (only if you run cursor-agent natively on Windows):
pwsh adapters/cursor/sync.ps1 -WhatIf
pwsh adapters/cursor/sync.ps1
```

Then **restart `cursor-agent`** to pick up new skills.

The sync is **idempotent** and safe: it never clobbers a non-kit entry, never
deletes a symlink/junction target, and `--prune` (`-Prune`) is report-only
unless `--force` (`-Force`).

> **WSL vs Windows `$HOME` — the original symptom.** `cursor-agent` resolves
> config against the invoking shell's home. Under WSL that is `/home/<you>`
> (a different `~/.cursor` than `C:\Users\<you>\.cursor`). The kit's skills
> were "invisible in `cursor-agent`" purely because they lived in the Windows
> home while `cursor-agent` ran under WSL — **not** a format incompatibility.
> Run `sync.sh` *inside* the WSL environment you launch `cursor-agent` from.

> **Line endings:** `sync.sh` must stay LF (`.gitattributes` enforces it) —
> a CRLF checkout breaks bash under WSL.

## Activating the instruction layer

`adapters/cursor/AGENTS.md` (the kit's Cursor-mechanics layer) must sit where
your Cursor build reads rules. Project-root `AGENTS.md`/`CLAUDE.md` is the
standard location; a global analog is **[verify on installed binary]**. If you
keep a private conventions AGENTS.md (see below), do **not** plain-copy over
it: paste the kit file's contents between its `<!-- kit-mechanics:begin/end -->`
markers and refresh that block after kit edits.

## The v1 subagent parity gap (#160426) — now moot for the kit

v1 generated 17 native subagents at `~/.cursor/agents/`, which the Cursor
**CLI** never loaded (user-level agents ignored — Cursor-staff-acknowledged
IDE↔CLI parity bug, forum **#160426**, ack 2026-05-13; the IDE reads them
fine). v2 archived the named-agent population, so the kit no longer installs
anything there and the bug no longer affects it. `--prune --force` removes the
v1-generated files. The bug reference only matters again if named agent files
ever return to the kit.

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
are source — commit them. Symlinks live in `~/.cursor/skills` (outside the
repo) — nothing is written into the tree, so there is nothing to gitignore
here.
