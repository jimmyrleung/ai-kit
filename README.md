# ai-kit

A collection of skills, slash commands, agents, and templates for [Claude Code](https://claude.com/claude-code) that codify a disciplined, evidence-based approach to software engineering workflows — feature addition, bug fixing, refactoring, incident response, greenfield projects — plus a self-improving meta-layer that turns session friction into refined skills over time, and an engineering-ownership layer that keeps your own judgment sharp while you lean on AI.

## What's in here

```
ai-kit/
├── skills/        Skill bodies — methodology lives here
├── commands/      Slash commands — mostly thin shims onto skills; a handful are
│                  multi-phase family orchestrators and per-task executors
├── agents/        Agent definitions — single-shot personas with pinned models
├── templates/     Per-family scaffolds (PRDs, techspecs, bug reports, post-mortems, …)
├── adapters/      Per-tool adapters (codex/, cursor/ — make the canonical source
│                  Codex- and Cursor-CLI-consumable from one source)
└── docs/          Methodology notes (model assignment rationale, Codex portability, …)
```

> **Primarily a Claude Code kit.** It also runs on **OpenAI Codex CLI** and the
> **Cursor CLI** via thin, additive adapters (`adapters/codex/`, `adapters/cursor/`)
> — see [Codex](#codex-openai-codex-cli) and [Cursor](#cursor-cursor-cli) below.

## Five workflow families

| Family                    | When to use                                   | Entry command              |
| ------------------------- | --------------------------------------------- | -------------------------- |
| **greenfield-dev**        | New project from scratch                      | `/greenfield-dev`          |
| **feature-addition**      | Integrate a feature into an existing codebase | `/integration-feature-dev` |
| **bugfix**                | Investigate, fix, and verify a bug            | `/full-bug-fix-workflow`   |
| **refactoring-tech-debt** | Audit-plan-tasks refactor of an existing area | `/refactor-techdebt-dev`   |
| **incident-response**     | Diagnose, hotfix, post-mortem                 | `/full-incident-response`  |

Not sure which to run? `/triage` routes a free-text request to the right workflow or to "just do it directly."

## Cross-workflow skills

- **`triage`** — Routes engineering requests to the right workflow. Up to 2 clarifying questions; one-line recommendation. Suggestion-mode only.
- **`review-artifact`** — The standard "review the artifact" sub-phase. Launches 1–3 reviewer agents, consolidates, decides re-run vs. update vs. minor-edits by % affected.
- **`qa-gates`** — Five pass/fail gates verifying an implementation against its spec (build/test → AC checklist → cross-cutting invariants → docs consistency → human go/no-go). Each gate either passes with evidence or fails with a recorded reason. Run after every task for a prefix is implemented.
- **`verify-task`** — Per-task closeout. Runs the build/test + AC + cross-cutting gates inside the per-task implement command, before the task is marked Done.
- **`close`** — End-of-session retrospective. Distills decisions/learnings/friction into auto-memory + an observations log + a session log entry. Not a context dump.
- **`improve`** — Periodic self-improvement review. Reads accumulated observations, finds friction patterns, audits skill fitness, and produces a STAGED packet of proposed edits — never edits a live file without per-item approval.

## Engineering ownership (retention)

A layer orthogonal to the workflow families: the families multiply _execution_; this layer protects _understanding_ — so you can still explain the design and trade-offs of code you shipped, without the chat history. Slimmed to its two low-friction members in the 2026-08 kit refactor; the friction-heavy rituals (`predict-first`, `debug-first`, `adr-first`, `challenge-me`) are preserved under `archive/skills/` and can return individually if genuinely missed.

| Skill             | When                                            | What it does                                                                                                                                                                             |
| ----------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `record-decision` | A decision surfaces mid-work, no time for an ADR | Snapshots it as a full ADR-template record — facts from the session, rationale AI-drafted and hard-flagged `UNREVIEWED` so it never passes as owned; you own the Rationale at review (in-session, or swept later by `/close`). |
| `onboard-me`      | **Unfamiliar** code you must understand         | A staff-engineer cold-read walkthrough — one step at a time, Socratic, lists its assumptions every message. (Not for code you just wrote.)                                                 |

**Durable artifacts.** Both skills write to `~/.claude/ownership/{topic}/` (private — your claude-home, **not** this public repo); ADR-shaped records prefer the repo's own decision dir (`docs/adr/`, `docs/decisions/`, …) when one exists. `{topic}` resolves identically across the skills (arg → git branch → doc basename → ask), so records about one area live together.

```
~/.claude/ownership/{topic}/
  onboarding.md      adr-NNNN-{slug}.md
```

These are invoked **deliberately** (`/record-decision`, `/onboard-me`) — they don't auto-trigger mid-work.

## Design principles

**Suggestion-mode by default.** Skills that propose changes (`improve`, the closeout commit step in `close`) stage diffs and ask before applying. The human stays in the loop.

**Anti-pattern guards.** Several skills are deliberately shaped to resist common AI failure modes — `greenfield-dev`'s anti-horizontal-scaffolding bias (build a vertical slice, not infrastructure for ten hypothetical features), the 3-way exploration pattern (minimal-changes / clean-architecture / pragmatic-balance, then commit) that forces tradeoff articulation, the % affected re-run heuristic in `review-artifact`.

**Composition over duplication.** `verify-task` composes `qa-gates` with per-task inputs; the 3-way explorers (`integration-techspec`, `refactor-plan`, …) have single-approach siblings (`pragmatic-techspec`, …) for cases where the 3-way comparison is overkill.

**Evidence-based decisions.** Every gate failure records the specific check that failed. Every observation has a date and a concrete trigger. `/improve` consumes evidence, not impressions.

**Composable closeout.** Per-task: `verify-task` runs 3 gates. Per-prefix: `/qa-gates` runs all 5. Per-session: `/close` writes a retrospective + observations. Per-week (or on demand): `/improve` mines patterns from those observations.

## Install (Claude Code)

> For Codex CLI, skip this section — see [Codex](#codex-openai-codex-cli) below (it has its
> own sync, not these junctions).

### Option A — Directory junction (one disk location, two filesystem names)

If `ai-kit` is your source-of-truth, junction the relevant subdirs into `~/.claude/` so Claude Code resolves them at runtime. On Windows:

```powershell
cmd /c mklink /J "$HOME\.claude\skills"   "C:\ai-kit\skills"
cmd /c mklink /J "$HOME\.claude\commands" "C:\ai-kit\commands"
cmd /c mklink /J "$HOME\.claude\agents"   "C:\ai-kit\agents"
```

On macOS/Linux, symlinks work the same way:

```bash
ln -s /path/to/ai-kit/skills   ~/.claude/skills
ln -s /path/to/ai-kit/commands ~/.claude/commands
ln -s /path/to/ai-kit/agents   ~/.claude/agents
```

Pros: edits in `ai-kit/` are immediately live in Claude Code; no mirror discipline.

### Option B — Copy

Copy the three subdirs into `~/.claude/`. Pros: no junction surface area. Cons: you have to re-copy after every update.

## Codex (OpenAI Codex CLI)

The kit is Claude-first but runs on Codex from the **same canonical source** via a thin,
additive adapter. Run it, then restart Codex:

```powershell
pwsh adapters/codex/sync.ps1 -WhatIf   # dry run
pwsh adapters/codex/sync.ps1           # bash adapters/codex/sync.sh on macOS/Linux
```

What it does: junctions the skills into Codex's skills root, and **generates Codex-only
skills** for the 17 agents and the 8 multi-phase orchestrators/executors (Codex has no
command primitive). The canonical tree is never modified — Claude is provably unaffected.
Design + recorded decision: [`docs/codex-portability-assessment.md`](docs/codex-portability-assessment.md).

**End state in Codex — one primitive.** `~/.codex/skills/` holds **41 junctioned canonical
skills** (auto-discovered, implicit-capable, exactly as in Claude) + **17 agent-skills** +
**8 orchestrator/executor skills**. The 25 generated ones are **explicit-only `$name`** —
they never auto-trigger. The ~28 thin shims are intentionally _not_ generated (their
methodology skill is already among the 41). Contrast Claude: three separate primitives
(skills + commands + agents), where commands carry orchestration at **zero always-on
context cost** — which is _why_ the kit keeps `commands/` on the Claude side rather than
collapsing it into skills.

**Gotchas (read before relying on it):**

- **Invocation differs:** `/full-bug-fix-workflow` (Claude command) → `$full-bug-fix-workflow`
  (Codex generated skill). Thin per-phase shims have no Codex form — invoke the skill they
  wrapped (`/investigate-bug` → `$bug-investigation`).
- **Your `~/.claude/CLAUDE.md` conventions do not transfer** — Codex never reads `~/.claude`.
  The kit ships only a Codex-_mechanics_ `AGENTS.md`; you must mirror your personal
  conventions into a private `AGENTS.md` yourself. See
  [`adapters/codex/README.md`](adapters/codex/README.md) → _Your personal conventions do not transfer_.
- **`review-artifact` is frozen** for the Codex initiative (it's the quality gate for 4 of 5
  families); it runs from the unchanged file. Full rationale + the `[verify on installed
binary]` list are in the adapter README.

## Cursor (Cursor CLI)

The kit also runs on the **Cursor CLI** (`cursor-agent`) from the same canonical
source. Run it, then restart `cursor-agent`:

```bash
bash adapters/cursor/sync.sh --dry-run   # WSL/Linux — the PRIMARY path
bash adapters/cursor/sync.sh             # pwsh adapters/cursor/sync.ps1 on native Windows
```

What it does: per-skill **symlinks** the skills into Cursor's _native_ skills
root (`~/.cursor/skills`), **generates** the 8 multi-phase orchestrators/executors
as explicit-only skills (`disable-model-invocation: true`), and **generates** the
17 agents as **native Cursor subagents** (`~/.cursor/agents/`). The canonical tree
is never modified — Claude is provably unaffected. Design + recorded decision:
[`docs/cursor-portability-assessment.md`](docs/cursor-portability-assessment.md).

**Why smaller than the Codex adapter.** Cursor natively consumes the same
`SKILL.md` spec _and_ has a native subagent primitive _and_ treats explicit
commands as skills — so there is no `openai.yaml`, no validator step, and no
agent-as-skill workaround. Skills auto-discover exactly as in Claude.

**Gotchas (read before relying on it):**

- **The original symptom was an environment gap, not a format one.**
  `cursor-agent` resolves config against the invoking shell's home; run under
  **WSL** it uses `/home/<you>/.cursor`, not the Windows `~/.claude` junctions.
  Run `sync.sh` _inside_ the WSL environment you launch `cursor-agent` from.
- **Invocation keeps the slash:** `/full-bug-fix-workflow` (Claude) →
  `/full-bug-fix-workflow` (Cursor explicit-only skill) — same key, unlike
  Codex's `$name`. Thin shims have no Cursor form — invoke their skill
  (`/investigate-bug` → the `bug-investigation` skill).
- **Cursor has no explicit-only flag for subagents** — the 17 agents _may_
  auto-delegate (governed by `description`). Documented caveat, not suppressed
  (forcing it would edit canonical agent files = Category-2).
- **Your `~/.claude/CLAUDE.md` conventions do not transfer** — the Cursor CLI
  reads a _project-root_ `CLAUDE.md`/`AGENTS.md`, not `~/.claude` globally.
  Mirror them into a private `AGENTS.md` yourself. See
  [`adapters/cursor/README.md`](adapters/cursor/README.md).
- **`review-artifact` is frozen** (same rationale as the Codex initiative).

## Concrete example — the self-improving loop

1. **In-session:** `/verify-task` runs after each implemented task, recording pass/fail per gate.
2. **End of session:** `/close` retrospects — what was decided, what was learned, what was frustrating — writes an observation file to `~/.claude/observations/`.
3. **Periodically:** `/improve` reads accumulated observations, clusters friction patterns, audits which skills produced the friction, and stages proposed edits at `~/.claude/improvements/{date}/` — each diff tied to the observation that prompted it.
4. **You review and apply.** The applied edits flow back into the skills that run the next session. The loop closes.

This is `ai-kit` operating on itself: the skills here are the same skills that propose changes to themselves.

> **From Codex:** the same loop runs as `$verify-task` / `$close` / `$improve`, and the
> artifacts still write to `~/.claude/…` — the feedback loop is **Anchored** to Claude by
> design (it works unchanged when driven from Codex; this is the recorded §3a decision, not
> a limitation).

## License

MIT. Skills, commands, agents, and templates are intentionally hand-authored — feel free to adapt them to your own workflow.
