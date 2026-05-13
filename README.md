# ai-kit

A collection of skills, slash commands, agents, and templates for [Claude Code](https://claude.com/claude-code) that codify a disciplined, evidence-based approach to software engineering workflows — feature addition, bug fixing, refactoring, incident response, greenfield projects — plus a self-improving meta-layer that turns session friction into refined skills over time.

## What's in here

```
ai-kit/
├── skills/        25 skill bodies — methodology lives here
├── commands/      34 slash commands — thin shims that invoke skills with the right inputs
├── agents/        18 agent definitions — single-shot personas with pinned models
├── templates/     Per-family scaffolds (PRDs, techspecs, bug reports, post-mortems, …)
└── docs/          Methodology notes (model assignment rationale, …)
```

## Five workflow families

| Family                  | When to use                                          | Entry command                |
| ----------------------- | ---------------------------------------------------- | ---------------------------- |
| **greenfield-dev**      | New project from scratch                             | `/greenfield-dev`            |
| **feature-addition**    | Integrate a feature into an existing codebase        | `/integration-feature-dev`   |
| **bugfix**              | Investigate, fix, and verify a bug                   | `/full-bug-fix-workflow`     |
| **refactoring-tech-debt** | Audit-plan-tasks refactor of an existing area      | `/refactor-techdebt-dev`     |
| **incident-response**   | Diagnose, hotfix, post-mortem                        | `/full-incident-response`    |

Not sure which to run? `/triage` routes a free-text request to the right workflow or to "just do it directly."

## Cross-workflow skills

- **`triage`** — Routes engineering requests to the right workflow. Up to 2 clarifying questions; one-line recommendation. Suggestion-mode only.
- **`review-artifact`** — The standard "review the artifact" sub-phase. Launches 1–3 reviewer agents, consolidates, decides re-run vs. update vs. minor-edits by % affected.
- **`qa-gates`** — Five pass/fail gates verifying an implementation against its spec (build/test → AC checklist → cross-cutting invariants → docs consistency → human go/no-go). Each gate either passes with evidence or fails with a recorded reason. Run after every task for a prefix is implemented.
- **`verify-task`** — Per-task closeout. Runs the build/test + AC + cross-cutting gates inside the per-task implement command, before the task is marked Done.
- **`close`** — End-of-session retrospective. Distills decisions/learnings/friction into auto-memory + an observations log + a session log entry. Not a context dump.
- **`improve`** — Periodic self-improvement review. Reads accumulated observations, finds friction patterns, audits skill fitness, and produces a STAGED packet of proposed edits — never edits a live file without per-item approval.
- **`migrate-notion`** — Guide a Notion-to-Obsidian migration via the Notion MCP tool.

## Design principles

**Suggestion-mode by default.** Skills that propose changes (`improve`, the closeout commit step in `close`) stage diffs and ask before applying. The human stays in the loop.

**Anti-pattern guards.** Several skills are deliberately shaped to resist common AI failure modes — `greenfield-dev`'s anti-horizontal-scaffolding bias (build a vertical slice, not infrastructure for ten hypothetical features), the 3-way exploration pattern (minimal-changes / clean-architecture / pragmatic-balance, then commit) that forces tradeoff articulation, the % affected re-run heuristic in `review-artifact`.

**Composition over duplication.** `verify-task` composes `qa-gates` with per-task inputs; the 3-way explorers (`integration-techspec`, `refactor-plan`, …) have single-approach siblings (`pragmatic-techspec`, …) for cases where the 3-way comparison is overkill.

**Evidence-based decisions.** Every gate failure records the specific check that failed. Every observation has a date and a concrete trigger. `/improve` consumes evidence, not impressions.

**Composable closeout.** Per-task: `verify-task` runs 3 gates. Per-prefix: `/qa-gates` runs all 5. Per-session: `/close` writes a retrospective + observations. Per-week (or on demand): `/improve` mines patterns from those observations.

## Install

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

## Concrete example — the self-improving loop

1. **In-session:** `/verify-task` runs after each implemented task, recording pass/fail per gate.
2. **End of session:** `/close` retrospects — what was decided, what was learned, what was frustrating — writes an observation file to `~/.claude/observations/`.
3. **Periodically:** `/improve` reads accumulated observations, clusters friction patterns, audits which skills produced the friction, and stages proposed edits at `~/.claude/improvements/{date}/` — each diff tied to the observation that prompted it.
4. **You review and apply.** The applied edits flow back into the skills that run the next session. The loop closes.

This is `ai-kit` operating on itself: the skills here are the same skills that propose changes to themselves.

## License

MIT. Skills, commands, agents, and templates are intentionally hand-authored — feel free to adapt them to your own workflow.
