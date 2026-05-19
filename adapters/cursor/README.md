# ai-kit → Cursor CLI adapter

Makes the **single canonical ai-kit source** consumable by the **Cursor CLI**
(`cursor-agent`), alongside Claude Code and Codex, from one source of truth —
extending the existing `~/.claude` / `~/.codex` junction model.

> Design + decision record: `../../docs/cursor-portability-assessment.md`.
> Verified against **Cursor docs (`cursor.com/docs`), 2026-05-19** and probed
> live on the user's `cursor-agent` (skills discovered; commands+agents not).
> Re-verify after a Cursor update — Cursor ships near-daily; items tagged
> **[verify on installed binary]** below are version-sensitive.

## What this is (and is not)

- **Category-1, additive, Claude-untouched.** Nothing here edits the canonical
  `skills/*/SKILL.md`, `agents/*.md`, or `commands/*.md`. The adapter only
  creates entries in Cursor's home (`~/.cursor/skills`, `~/.cursor/agents`) and
  generates Cursor-only files there. Canonical `commands/` is *read from* but
  never modified — Claude is provably unaffected.
- **No kit-owned fan-out harness** (recorded decision: rely on the native
  harness, never an orchestration script in a skill). Strategy selection is
  *instruction*, in `AGENTS.md`.
- **`review-artifact` is frozen.** Run from the unchanged file. The headless
  verdict-contract refactor is the separate, deferred cc-looper-class effort.

## Why this adapter is smaller than the Codex one

Cursor natively consumes the **same `SKILL.md` spec** *and* has a **native
subagent primitive**, so — unlike Codex (no agent/command primitives, so
everything became skills + `openai.yaml` + a validator step) — Cursor needs
no `openai.yaml`, no validator, and agents map to a real subagent, not a
skill workaround.

| ai-kit primitive | Cursor realization |
|---|---|
| `skills/<name>/` (35) | per-skill **junction/symlink** → `${CURSOR_HOME:-~/.cursor}/skills/<name>`. Cursor's *native* user-level skills root (self-contained — does **not** depend on the `~/.claude` compat root). `SKILL.md` spec identical, **no body transform**. |
| `commands/*` (3 classes) | Cursor **deprecated standalone slash-commands** (folded into Skills; the built-in `/migrate-to-skills` converts them with `disable-model-invocation:true`). **~25 thin shims**: not generated — their skill is already junctioned, invoke its skill directly. **5 family orchestrators + 3 per-task executors**: **generated** as Cursor skills with `disable-model-invocation: true` (explicit-only `/name`, never auto-trigger). Canonical `commands/` untouched — Claude keeps the `/x` UX at zero context cost. |
| `agents/<name>.md` (17) | **generated** as native Cursor subagents at `${CURSOR_HOME:-~/.cursor}/agents/<name>.md` (`name`+`description`+body; `model`/`tools`/`color` dropped → `model: inherit`). Works in the Cursor **IDE**; **not in the CLI** until parity bug #160426 is fixed (see *Subagents: Cursor CLI parity gap* below). |
| Claude `CLAUDE.md` conventions | `AGENTS.md` (this dir) — fan-out A/C mapping, the `AskUserQuestion` plain-text degradation, model-pin note, the subagent caveat. Additive instruction; no canonical edit. |

## Usage

```bash
# WSL / Linux (PRIMARY — cursor-agent is typically run under WSL because the
# Windows Cursor CLI hard-codes a PowerShell shell with cold-start hangs).
# Run from inside WSL so it targets the WSL ~/.cursor:
bash adapters/cursor/sync.sh --dry-run
bash adapters/cursor/sync.sh
```

```powershell
# Windows-native parity (only if you run cursor-agent natively on Windows):
pwsh adapters/cursor/sync.ps1 -WhatIf
pwsh adapters/cursor/sync.ps1
```

Then place `AGENTS.md` where your Cursor build reads instructions (project-root
is standard; global is **[verify on installed binary]**) and **restart
`cursor-agent`** to pick up new skills/subagents.

The sync is **idempotent** and safe: it never clobbers a non-kit entry, never
deletes a junction/symlink target, and `--prune` (`-Prune`) is report-only
unless `--force` (`-Force`).

> **WSL vs Windows `$HOME` — the original symptom.** `cursor-agent` resolves
> config against the invoking shell's home. Under WSL that is `/home/<you>`
> (a different `~/.cursor` than `C:\Users\<you>\.cursor`). The kit's skills
> were "invisible in `cursor-agent`" purely because they lived in the Windows
> `~/.claude` junctions while `cursor-agent` ran under WSL with a different
> home — **not** a format incompatibility. Run `sync.sh` *inside* the WSL
> environment you launch `cursor-agent` from so it writes the WSL `~/.cursor`.

## Invocation: `/x` (Claude) vs `/x` (Cursor) — muscle-memory notes

- **Orchestrators/executors keep the `/name` slash** (Claude `/full-bug-fix-workflow`
  → Cursor `/full-bug-fix-workflow`) — they are explicit-only skills, so the
  UX is the *same key*, unlike Codex's `$name`.
- **A thin shim has no Cursor form** — invoke the skill it wrapped
  (`/investigate-bug` → the `bug-investigation` skill). The command→skill name
  often differs (see `AGENTS.md` → *Generated orchestrator / executor skills*).
- **Junctioned methodology skills auto-discover** off their `description`
  (implicit-capable, like Claude). The 8 generated orchestrators do **not**
  (`disable-model-invocation: true`).
- **Agents are native subagents** — work in the Cursor **IDE**; **not** in the
  CLI yet (parity bug #160426 — see below).

## Subagents: Cursor CLI parity gap (empirically confirmed 2026-05-19)

The 17 agents are generated as native subagents at `~/.cursor/agents/<name>.md`.
The Cursor **CLI** (`cursor-agent`, ≥ `2026.05.09`) does **not** load
*user-level* `~/.cursor/agents/` — only *project-level* `.cursor/agents/`. This
is a Cursor-staff-acknowledged IDE↔CLI parity bug (forum **#160426**, ack
2026-05-13, no fix date), confirmed on-machine: the 17 do not appear in
`cursor-agent`, and `/create-subagent` itself writes to the *project's*
`.cursor/agents/`.

**Recorded decision: wait for the upstream fix.** The adapter still generates
`~/.cursor/agents/` deliberately — it works in the IDE now and **self-heals the
day #160426 lands** (zero rework). For CLI fan-out meanwhile, invoke the
worker's **methodology skill by name** (skills are user-level and *do* load in
the CLI) — see `AGENTS.md` → *Subagents: Cursor CLI parity gap*. Do **not**
pivot agents→skills or add a per-project `.cursor/agents/` bootstrap unless
asked; the user runs `cursor-agent` from arbitrary repos, so a per-repo install
is a maintenance chore, and the skill fallback already covers CLI fan-out.

## Your personal conventions do not transfer (read this)

`adapters/cursor/AGENTS.md` is the kit's **Cursor-mechanics** layer only (the
fan-out A/C mapping, the `AskUserQuestion` plain-text degradation, the
orchestrator-body reading rules, the model-pin note, the subagent caveat). It is
**not** a replica of your `~/.claude/CLAUDE.md`.

The Cursor CLI does not read `~/.claude/CLAUDE.md` as a global rule (it reads a
**project-root** `CLAUDE.md`/`AGENTS.md`). So your personal working agreement —
**confidence scoring, ask-before-assuming, scope discipline, read-before-edit,
verification-before-completion, risky-command (`rm`/`del`/`reset`) confirmation,
session open/close offers** — **does not reach the Cursor CLI globally**, and
several kit skills implicitly assume it. Mirror `~/.claude/CLAUDE.md` into a
**private** `AGENTS.md` and place it where your Cursor build reads instructions.
**Keep it out of this public repo** — exactly as your `~/.claude/CLAUDE.md`
lives outside it today. `sync` does **not** do this for you; it prints a
reminder instead.

## Open `[verify on installed binary]` items (re-check on Cursor update)

- `AGENTS.md` **global** read-location (project-root cascade is standard; a
  `~/.cursor/AGENTS.md` global analog is build-dependent).
- **Bug #160426** (Cursor CLI does not load user-level `~/.cursor/agents/`) —
  re-check on each Cursor update; when fixed, the 17 subagents start working in
  `cursor-agent` with no adapter change.
- Precedence ordering among the four native skills dirs (`~/.cursor/skills`,
  `~/.agents/skills`, project `.cursor/skills`, `.agents/skills`) — docs silent.
- Absence of an `AskUserQuestion`-analog in the CLI tool surface.
- Whether the legacy `.cursor/commands/` runtime still executes (undocumented;
  the adapter does **not** rely on it — Skills is the forward path).

## Two-/three-consumer test debt

The junction means "edit the canonical file once," but **verification is now
3×**: any change to a canonical skill must be sanity-checked from Claude Code,
Codex, *and* the Cursor CLI.

## Commit vs. gitignore

ai-kit is a public repo. `adapters/cursor/{sync.sh,sync.ps1,AGENTS.md,README.md}`
are source — commit them. Generated artifacts live in `~/.cursor/{skills,agents}`
(outside the repo) — nothing generated is written into the tree, so there is
nothing to gitignore here.
