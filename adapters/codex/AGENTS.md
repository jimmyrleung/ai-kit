# ai-kit — Codex instruction layer (v2)

This file is the Codex-side counterpart of the kit's Claude conventions. It is **additive
instruction only** — it changes nothing in the canonical ai-kit skills. Codex consumes it
when it sits at an instruction-cascade location: paste it below the include point of your
private `~/.codex/AGENTS.md`, or copy it to the root of a project you run Codex in
(`AGENTS.override.md` in the home dir takes precedence; combined cap
`project_doc_max_bytes` = 32 KiB).

> Rewritten 2026-08-06 for the **v2 kit** (skill-centric refactor). Current skill mechanics are
> checked against the [Codex Agent Skills documentation](https://learn.chatgpt.com/docs/build-skills)
> and local `codex-cli 0.151.0` (`codex --version`, 2026-09-01). Re-verify after updates.

## The v2 surface (what Codex sees)

The common engine enumerates every canonical skill once and manages per-skill links in
`~/.claude/skills/` and `~/.agents/skills/`; the adapter scripts only forward to that engine.
Codex's documented user discovery root is `~/.agents/skills/`, and Codex follows symlinked
skill folders. The `SKILL.md` body is therefore shared without a provider transform. Codex
explicitly invokes a skill with `$skill` and may also select one from its `description`; see
the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills).

Skill selection depends on the host catalog and active metadata policy. Work chains by invoking the next skill, not by
running an orchestrator: `$analyze-work` → `$techspec` → `$tasks-breakdown` → `$implement-task`
(verify-task gates inline) → `$review-implementation` → `$qa-gates`; bugs/incidents enter
via `$bug-investigation` and rejoin the chain. `$triage` routes a free-text request.

## Runtime capabilities and feedback

Resolve repository-relative references and commands from the ai-kit checkout, even when
this block is copied into a private instruction file. Locate that checkout through the
canonical target of a managed ai-kit skill (for example `triage`), then verify its
`skills/`, `docs/`, and `adapters/codex/AGENTS.md` paths. Links below are relative to that
canonical adapter file, not the private copy or the user's current project. If the
checkout cannot be located, report the reference as unavailable; do not guess a home path.

Use the shared [provider capability reference](../../docs/provider-capabilities.md)
for discovery, invocation, question tools, delegation, worker configuration, recurrence,
and recovery. Check the active host/mode rather than assuming capabilities from its name.
Use an exposed, permitted structured-question tool when available; otherwise ask in plain
text. Native workers require authorization and available tools; sequential passes must
record missing independence. Existing authorization also applies to local review/fix
iterations; only a real decision or an explicit owner gate requires another pause.

Feedback and memory are optional under [the public recorder contract](../../docs/contracts/feedback.md).
Prefer the provider-neutral `~/.agents/feedback-store.json` profile across hosts. A legacy
`~/.claude` store is used only when explicitly configured; the adapter never migrates private
records. Follow `docs/output-filename-contract.md` for workflow artifacts.

## Private instruction refresh

This file is a public mechanics layer, not a copy of private conventions. If it is copied
into `~/.codex/AGENTS.md` or a project instruction file, manually refresh the copied
`kit-mechanics` block after adapter edits. No repository script or sync wrapper may overwrite
that private file. Check drift without writes using the shared reference’s
`check-mechanics-mirror.py` command.

## Common sync posture

The adapter remains additive: it never edits canonical `skills/*/SKILL.md`. Use the root
`scripts/sync-skills.py` entry point for deployment; the adapter scripts are compatibility
wrappers only. Run a dry-run first, then restart Codex after a successful sync.

If an externally owned entry occupies a canonical skill name, use the common engine's explicit
`--preserve <claude|agents>/<skill-name>` policy (or PowerShell `-Preserve`) on dry-run, apply, and
check. It remains unowned and the flag must be repeated for qualified checks.
