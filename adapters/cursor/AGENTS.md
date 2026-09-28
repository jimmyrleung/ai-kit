# ai-kit — Cursor instruction layer (v3)

This file is the Cursor-side counterpart of the kit's Claude conventions. It is **additive
instruction only** — it changes nothing in the canonical ai-kit skills. Cursor reads
project-root `AGENTS.md` (and `CLAUDE.md`) as rules: paste this below the include point of
your private AGENTS.md, or copy/link it into the root of a project you run Cursor in (a
global read-location analog of `~/.claude/CLAUDE.md` is **[verify on installed binary]**).

> Originated in the v2 skill-centric refactor and refreshed for the **v3 kit**. Provider mechanics are
> checked against the [Cursor Agent Skills documentation](https://prod.cursor.com/docs/skills)
> and [Cursor subagent documentation](https://prod.cursor.com/docs/subagents), accessed 2026-09-01.
> Cursor is version-sensitive; re-verify after an update.

## The v3 surface (what Cursor sees)

The common engine enumerates every canonical skill once and manages per-skill links in
`~/.claude/skills/` and `~/.agents/skills/`; the adapter scripts only forward to that engine.
Cursor's current documentation lists `~/.agents/skills/` and `~/.cursor/skills/` plus
Claude/Codex compatibility roots. It can therefore surface duplicate entries. Require every
ai-kit occurrence to resolve to the same canonical `skills/<name>/` directory; make no
precedence claim and do not deduplicate provider roots here.
Cursor explicitly invokes skills with `/name` and may select them from `description`; the
shared `SKILL.md` body receives no provider transform.

Skill selection depends on the host catalog and active metadata policy. Work chains by invoking
the next skill, not by running an orchestrator: `/lay-of-the-land` (optional) → `/define-reqs`
→ `/techspec` → `/tasks-breakdown` → `/implement-task` → `/review-implementation` →
`/qa-execution` → `/qa-gates`. Bugs and incidents start with `/bug-investigation`, then
rejoin the same delivery path.

## Runtime capabilities and feedback

Resolve repository-relative references and commands from the ai-kit checkout, even when
this block is copied into a private instruction file. Locate that checkout through the
canonical target of a managed ai-kit skill (for example `define-reqs`), then verify its
`skills/` and `adapters/cursor/AGENTS.md` paths. Links below are relative to that
canonical adapter file, not the private copy or the user's current project. If the
checkout cannot be located, report the reference as unavailable; do not guess a home path.

Use the shared [provider capability reference](../../skills/document-workflow/references/shared/provider-capabilities.md)
for discovery, invocation, question tools, delegation, worker configuration, recurrence,
and recovery. Check the active host/mode rather than assuming capabilities from its name.
Use an exposed, permitted structured-question tool when available; otherwise ask in plain
text. Native workers require authorization and available tools; sequential passes must
record missing independence. Existing authorization also applies to local review/fix
iterations; only a real decision or an explicit owner gate requires another pause.

Feedback and memory are optional under [the public recorder contract](../../skills/document-workflow/references/shared/feedback.md).
Prefer the provider-neutral `~/.agents/feedback-store.json` profile across hosts. A legacy
`~/.claude` store is used only when explicitly configured; the adapter never migrates private
records. Each consuming skill owns its workflow artifact names and output location.

## Private instruction refresh

This file is a public mechanics layer, not a copy of private conventions. If it is copied
into a private project or user instruction file, manually refresh the copied
`kit-mechanics` block after adapter edits. No repository script or sync wrapper may overwrite
that private file. Compare only the delimited block with this public adapter; never print or
overwrite private text during the check.

## Common sync posture

The adapter remains additive: it never edits canonical `skills/*/SKILL.md`. Use the root
`sync-skills.py` entry point for deployment; the adapter scripts are compatibility
wrappers only. Run a dry-run first, then restart `cursor-agent` after a successful sync.

If an externally owned entry occupies a canonical skill name, use the common engine's explicit
`--preserve <claude|agents>/<skill-name>` policy (or PowerShell `-Preserve`) on dry-run, apply, and
check. It remains unowned and the flag must be repeated for qualified checks.
