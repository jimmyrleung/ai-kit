# ai-kit → Codex CLI adapter (v2)

Makes the **single canonical ai-kit source** consumable by **OpenAI Codex CLI**, alongside
Claude Code, from one source of truth — extending the existing `~/.claude` junction model.

> Design + recorded decision: `../../docs/codex-portability-assessment.md` (§3a Decision, §5,
> §8 — written for the v1 kit; the mechanism survived the 2026-08 v2 refactor, the generated
> surfaces did not). Mechanics verified on **`0.144.1`** (2026-07-10); repo-level skill
> discovery verified on **`0.146.0`**. Re-verify after a Codex update — Codex ships weekly.

## What this is (and is not)

- **Category-1, additive, Claude-untouched.** Nothing here edits the canonical
  `skills/*/SKILL.md`. The adapter only creates junctions in Codex's skills root.
- **No kit-owned fan-out harness** (recorded decision: rely on the native harness, never an
  orchestration script in a skill). Fan-out reading rules are *instruction*, in `AGENTS.md`.

## How it works (v2)

One mechanism left: every canonical `skills/<name>/` gets a per-skill **directory junction**
→ `${CODEX_HOME:-~/.codex}/skills/<name>`. Codex enumerates `<root>/<name>/SKILL.md` and
auto-discovers; the `SKILL.md` spec is identical, so **no body transform**. What Claude
invokes as `/name`, Codex invokes as `$name` — same name, no divergence.

The v1 kit also **generated** Codex-only skills for its 17 named agents and 10
orchestrator/executor commands. v2 retired those populations entirely (archived under
`archive/v1/`), so **nothing is generated anymore** — the sync's generation paths are
dormant and its command allowlist is empty. `openai.yaml` remains intentionally absent for
junctioned skills: it is *recommended, not required* (verified) — bare `SKILL.md` skills
auto-discover and trigger off `description`.

## Usage

```powershell
# Windows (primary). Dry-run first:
pwsh adapters/codex/sync.ps1 -WhatIf
pwsh adapters/codex/sync.ps1
# macOS/Linux parity:
bash adapters/codex/sync.sh --dry-run
bash adapters/codex/sync.sh
```

Then **restart Codex** to pick up new skills.

**Activating the instruction layer:** `adapters/codex/AGENTS.md` (the kit's Codex-mechanics
layer) must sit at an instruction-cascade location to be read. The verified global location
is `~/.codex/AGENTS.md` — but that file is typically your **private conventions layer**
(see below), so do **not** plain-copy over it: paste the kit file's contents at your private
file's include point (between its `kit-mechanics` markers) and refresh that block after kit
edits. Per-project placement (copy into the repo you run Codex from) also works. Combined
cap `project_doc_max_bytes` = 32 KiB; `AGENTS.override.md` in the home dir takes precedence.

**Scripting caveat (verified 0.144.1):** `codex exec` appends piped stdin to the prompt and
blocks until EOF — in a non-TTY/background pipe it hangs forever. Close stdin in any
scripted call: `cmd /c "codex exec … < NUL"` (Windows) / `codex exec … </dev/null` (POSIX).

The sync is **idempotent** and safe: it never touches `.system`, never deletes a junction
target, never removes a non-kit entry, and **reports** (never auto-fixes) any validator
failure. `-Prune` is report-only unless `-Force`.

## Your personal conventions do not transfer (read this)

`adapters/codex/AGENTS.md` is the kit's **Codex-mechanics** layer only (the v2 surface,
fan-out reading rules, the structured-question plain-text degradation, model notes, the
Anchored `~/.claude` paths). It is **not** a replica of your `~/.claude/CLAUDE.md`.

Codex never reads `~/.claude`. So your personal working agreement — confidence scoring,
ask-before-assuming, scope discipline, read-before-edit, verification-before-completion,
risky-command confirmation, session open/close offers — **does not reach Codex**, and
several kit skills implicitly assume it. The fix mirrors how Claude already layers it:

- **Kit layer** (public, in-repo, this dir): `AGENTS.md`.
- **User layer** (private, **you own this**): mirror `~/.claude/CLAUDE.md` into a private
  `~/.codex/AGENTS.md`, with an include point where the kit block is pasted. **Keep it out
  of this public repo.** `sync` never writes it (it would either publish your personal
  prefs or mutate `$HOME` silently); it prints a reminder instead.

## Validation

`sync.ps1` runs **Codex's own** `quick_validate.py` (from `.system/skill-creator`) over every
exposed skill — **advisory, never gating**. It self-tests against a known-good `.system`
skill first; if the host Python is missing/broken it **degrades to "skipped"** (exit 0)
rather than marking skills FAIL. Junctions are the deliverable; validation is an optional
report best run from Codex's own environment. Real validator failures are surfaced in the
summary, never silently fixed (a canonical `SKILL.md` change is out of adapter scope).

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
them. Junctions live in `~/.codex/skills` (outside the repo) — nothing is written into the
tree, so there is nothing to gitignore here.
