# ai-kit → Codex CLI adapter

Makes the **single canonical ai-kit source** consumable by **OpenAI Codex CLI**, alongside
Claude Code, from one source of truth — extending the existing `~/.claude` junction model.

> Design + recorded decision: `../../docs/codex-portability-assessment.md` (§3a Decision, §5,
> §8). Verified against **`codex-cli 0.130.0`, 2026-05-17**. Re-verify after a Codex update —
> Codex ships weekly; items tagged **[verify on installed binary]** below are version-sensitive.

## What this is (and is not)

- **Category-1, additive, Claude-untouched.** Nothing here edits the canonical
  `skills/*/SKILL.md` or `agents/*.md`. Claude is provably unaffected — the adapter only
  creates entries in Codex's skills root and generates Codex-only files there.
- **No kit-owned fan-out harness** (recorded decision: rely on the native harness, never an
  orchestration script in a skill). Strategy selection is *instruction*, in `AGENTS.md`.
- **`review-artifact` is frozen.** Run from the unchanged file in C-mode. The headless
  verdict-contract refactor is the separate, deferred cc-looper-class effort.

## How it works (verified v0.130.0)

| ai-kit primitive | Codex realization |
|---|---|
| `skills/<name>/` (34) | per-skill **directory junction** → `${CODEX_HOME:-~/.codex}/skills/<name>`. Codex enumerates `<root>/<name>/SKILL.md` and auto-discovers; the `SKILL.md` spec is identical, so **no body transform**. |
| `agents/<name>.md` (18) | Codex has **no `~/.codex/agents`** — a *skill is the unit of agent invocation*. Each agent is **generated** as a Codex skill at `${CODEX_HOME:-~/.codex}/skills/<name>/` (Codex-only; never written into the canonical tree) so every `@x-agent` reference resolves as `$x-agent`. Generated with `policy.allow_implicit_invocation: false` — workers, never user-triggered, so they don't bloat every session's context. |
| Claude `CLAUDE.md` conventions | `AGENTS.md` (this dir) — the Codex-side fan-out mapping (A/C selection), the `AskUserQuestion` plain-text degradation, model-pin note. Additive instruction; no canonical edit. |
| `commands/*` | **not ported.** Codex `~/.codex/prompts/` is deprecated + user-only; a Codex skill is directly invokable (`$name`/implicit), so the thin per-phase command shims have no job. Claude keeps `commands/` for its `/x` UX via the existing junction. |

**`openai.yaml` for the 34 canonical skills is intentionally deferred** (v1): it is
*recommended, not required* (verified) — bare `SKILL.md` skills are auto-discovered and trigger
off `description`. Injecting `openai.yaml` would either pollute the pristine canonical tree or
require privilege-fragile per-file symlinks on Windows. The *functionally* important case
(implicit-invocation off for the 18 worker agents) is handled, because those are generated.

## Usage

```powershell
# Windows (primary). Dry-run first:
pwsh adapters/codex/sync.ps1 -WhatIf
pwsh adapters/codex/sync.ps1
# macOS/Linux parity:
bash adapters/codex/sync.sh --dry-run
bash adapters/codex/sync.sh
```

Then place `AGENTS.md` where your Codex build reads instructions (see its header — global
location is **[verify on installed binary]**) and **restart Codex** to pick up new skills.

The sync is **idempotent** and safe: it never touches `.system`, never deletes a junction
target, never removes a non-kit entry, and **reports** (never auto-fixes) any
`quick_validate.py` failure — fixing a canonical `SKILL.md` would be Category-2 / out of
recorded near-term scope. `-Prune` is report-only unless `-Force`.

## Validation

`sync.ps1` runs **Codex's own** `quick_validate.py` (from `.system/skill-creator`) over every
exposed skill — **advisory, never gating**. It self-tests against a known-good `.system` skill
first; if the host Python is missing/broken or lacks PyYAML, validation **degrades to
"skipped"** (exit 0) rather than marking skills FAIL. Junction + generation is the deliverable;
validation is an optional report best run from Codex's own environment.

**Verified status (2026-05-17):** *statically* confirmed compliant — every canonical skill's
frontmatter uses only keys within `quick_validate.py`'s allowed set
(`name`/`description`/`license`/`allowed-tools`/`metadata`) and **no `description` contains
`<`/`>`** (the only content rule). The validator was **not run live on this machine** — the
host `C:\Python311` segfaults (`0xC0000005`) independent of the kit; run `sync` from a working
Python / Codex env to get the live report. Real validator failures (future skills) are
surfaced in the summary, never silently fixed (a canonical `SKILL.md` change is Category-2).

## Alternative: `skill-installer` (detached copy)

Codex ships `skill-installer` (`install-skill-from-github.py --repo <owner>/ai-kit --path
skills/<name>`). It **copies** (download / sparse-checkout), breaking the single-source
"edit once" property — hence junction is the chosen mechanism. Use the installer only if you
deliberately want a frozen, detached snapshot.

## Two-consumer test debt

The junction means "edit the canonical file once," but **verification is now 2×**: any change
to a canonical skill must be sanity-checked from *both* Claude Code and Codex.

## Open `[verify on installed binary]` items (re-check on Codex update)

- `AGENTS.md` **global** read-location (project cascade is standard; `~/.codex` global analog
  is build-dependent — `child_agents_md` was under-development at v0.130.0).
- `agents.max_depth` default and how it counts skill-invocation vs subagent-spawn.
- `project_doc_max_bytes`, `$ARGUMENTS`/`$1` arg-mapping, exact tool-surface absence of an
  `AskUserQuestion` analog.

## Commit vs. gitignore

ai-kit is a public repo. `adapters/codex/{sync.*,AGENTS.md,README.md}` are source — commit
them. Generated artifacts live in `~/.codex/skills` (outside the repo) — nothing generated is
written into the tree, so there is nothing to gitignore here.
