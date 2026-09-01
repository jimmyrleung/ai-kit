# ai-kit → Codex CLI adapter (v2)

Makes the **single canonical ai-kit source** consumable by **OpenAI Codex CLI**. The common
deployment engine is `../../scripts/sync-skills.py`; this adapter supplies only Codex
compatibility and invocation guidance.

> Design + recorded decision: `../../docs/codex-portability-assessment.md` (§3a Decision, §5,
> §8 — historical; the v2 implementation uses the common engine). Current skill mechanics are
> checked against the [Codex Agent Skills documentation](https://learn.chatgpt.com/docs/build-skills)
> and local `codex-cli 0.151.0` (`codex --version`, 2026-09-01). Re-verify after updates.

## What this is (and is not)

- **Category-1, additive, Claude-untouched.** Nothing here edits the canonical
  `skills/*/SKILL.md`.
- **Compatibility only.** `sync.sh` and `sync.ps1` forward to the common engine; they contain
  no canonical enumeration, link classification, mutation, or rollback implementation.
- **No kit-owned fan-out harness.** Use the native Codex facility when available; the
  capability fallback and reading rules are documented in `AGENTS.md`.

## How it works (v2)

The common engine enumerates canonical `skills/<name>/` directories once and manages per-skill
links in exactly `~/.claude/skills/` and `~/.agents/skills/`. On POSIX it creates symlinks; on
Windows it creates directory junctions. Codex's documented user discovery root is
`~/.agents/skills/`, and Codex follows symlinked skill folders, so the `SKILL.md` body needs
no transform. See the [Codex skill locations and format](https://learn.chatgpt.com/docs/build-skills).

No provider-specific skill copies, generated command/agent twins, or secondary sync
implementation are current v2 surfaces. Optional `agents/openai.yaml` metadata is a skill-local
Codex overlay; it does not create another copy of the skill. Historical v1 details remain in
the superseded assessment.

## Deployment
The root [`README.md`](../../README.md) is the canonical installation guide. Run the common
engine from the repository root, previewing the normal home before applying:

```bash
python3 scripts/sync-skills.py --dry-run
python3 scripts/sync-skills.py --check
```

The adapter paths remain compatibility entry points and forward the common switches unchanged:

```bash
bash adapters/codex/sync.sh --dry-run --home <isolated-home>
```

```powershell
pwsh adapters/codex/sync.ps1 -WhatIf -UserHome <isolated-home>
```

When a managed root contains an externally owned canonical-name entry, pass
`--preserve agents/<skill-name>` (or `-Preserve agents/<skill-name>` through PowerShell) once per
entry on dry-run, apply, and check. Preserved entries stay outside ai-kit ownership and the flag
must be repeated for qualified checks; the wrappers only translate and forward this policy.

They reject `CODEX_HOME` / `-CodexHome` for sync-root selection; use `--home` / `-UserHome`
only for an isolated common user base. Restart Codex after a sync so it re-reads the skill list.

**Activating the instruction layer:** `adapters/codex/AGENTS.md` (the kit's Codex-mechanics
layer) must sit at an instruction-cascade location to be read. The verified global location
is `~/.codex/AGENTS.md` — but that file is typically your **private conventions layer**
(see below), so do **not** plain-copy over it: paste the kit file's contents at your private
file's include point (between its `kit-mechanics` markers). Refresh that copied block manually after
adapter edits; no repository script or sync wrapper writes private conventions. Per-project placement
(copy into the repo you run Codex from) also works. Combined
cap `project_doc_max_bytes` = 32 KiB; `AGENTS.override.md` in the home dir takes precedence.

**Non-interactive invocation:** `codex exec` accepts a prompt argument or reads stdin. If a
prompt argument is supplied while stdin is piped, Codex appends stdin as a `<stdin>` block;
close stdin for automation (`codex exec … </dev/null` on POSIX or `< NUL` on Windows) unless
that appended input is intentional. Confirm the installed build's help before scripting.

The common engine is **idempotent** and safety-gated: it never changes a non-kit entry or
link target, and it records ownership/baselines before mutation. The wrappers do not write
private instruction files. Use `--check` for a read-only completeness and ownership check.

## Your personal conventions do not transfer (read this)

`adapters/codex/AGENTS.md` is the kit's **Codex-mechanics** layer only (the v2 surface,
fan-out reading rules, the structured-question plain-text degradation, model notes, the
Anchored `~/.claude` paths). It is **not** a replica of your `~/.claude/CLAUDE.md`.

Codex never reads `~/.claude`. So your personal working agreement — confidence scoring,
ask-before-assuming, scope discipline, read-before-edit, verification-before-completion,
risky-command confirmation, session open/close offers — **does not reach Codex**, and
several kit skills implicitly assume it. The fix mirrors how Claude already layers it:

- **Kit layer** (public, in-repo, this dir): `AGENTS.md`.
- **User layer** (private, **you own this**): mirror `~/.claude/CLAUDE.md` into
  `~/.codex/AGENTS.md` (or the loaded project instruction file), with an include
  point where the kit block is pasted. **Keep it out of this public repo.** Sync never writes
  private instructions (it would either publish personal preferences or mutate `$HOME` silently);
  it prints a reminder instead.

## Validation

The repository's `npm test` and `npm run check:portability` are the authoritative common
validation commands. Codex's optional validator, when present in the installed environment,
is advisory only; an unavailable or provider-specific validator does not change the common
checker result. A validator failure is reported for investigation, never fixed by the wrapper.

## Alternative: `skill-installer` (detached copy)

Codex ships `skill-installer` (`install-skill-from-github.py --repo <owner>/ai-kit --path
skills/<name>`). It **copies** (download / sparse-checkout), breaking the single-source
"edit once" property — hence junction is the chosen mechanism. Use the installer only if you
deliberately want a frozen, detached snapshot.

## Two-consumer test debt

The junction means "edit the canonical file once," but **verification is now 2×**: any change
to a canonical skill must be sanity-checked from *both* Claude Code and Codex.

## Commit vs. gitignore

ai-kit is a public repo. `adapters/codex/{sync.*,AGENTS.md,README.md}` are source — commit
them. Managed user-root links live outside the repo — nothing is written into the
tree, so there is nothing to gitignore here.
