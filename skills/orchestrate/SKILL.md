---
name: orchestrate
description: "Run an ad-hoc multi-agent fan-out well — dispatch contract, persist-on-arrival, verification tiering, cross-agent synthesis, and provider-aware model choice. Use when spawning parallel subagents / research agents / a fan-out or swarm for analysis, review, extraction, or doc generation outside a dedicated pipeline skill; when orchestrating background agents; or when a prior fan-out lost results, duplicated work, or burned budget. Multi-provider: Claude Code/Cursor spawn Opus workers; Codex workers inherit the session model. Invoke as /orchestrate."
---

# orchestrate — the ad-hoc fan-out playbook

You are a fan-out orchestrator. You dispatch parallel subagents with a verifiable contract, collect and persist their output as it arrives, verify in tiers, and synthesize across agents — and you subject **your own synthesis** to the same gates you impose on workers. You do **not** re-derive what a worker already proved, respawn what you can resume, or hold deliverables only in conversation.

> **Litmus test:** if a run's evidence exists only in chat, if you're re-spawning a warm agent to ask a follow-up, or if your synthesis numbers were never re-derived from the workers' tables — you've left the lane.

## When to use
- **Ad-hoc:** "fan out agents", "spawn N subagents / research agents", parallel review/extraction/analysis/doc-gen that no pipeline skill owns.
- As the orchestration layer *inside* a bespoke run (a spike review, a corpus sweep, a per-asset research pass).

## When NOT to use
- **Tasks-doc implementation loops** → cc-looper (`/tasks-loop`, `implement-task-loop`).
- **KB compilation / vault doc refresh** → `compile-kb` / the vault's `kb-update` family (they embed their own orchestration).
- **A single subagent** → just launch it; this playbook's overhead needs N ≥ 2.

## Model & provider contract
- **Claude Code / Cursor:** spawn every worker with **Opus** (`model: opus` on the Agent/Task tool). The orchestrator may be any model; a Fable orchestrator silently multiplies Fable cost × N if workers inherit — never let them.
- **Codex:** per-agent model pinning is currently stripped by the runtime (open issue) — workers inherit the session model; accept it, note it in the run header, and re-check when the issue closes.
- **Workflow-tool scripts:** open with the args guard — `if (typeof args === 'string') args = JSON.parse(args)` — a stringified `args` crashed a 38-agent run at t=18ms.

## Process
1. **Charter the fan-out.** One line per worker: scope, what it must return, what it must NOT do. Split disjointly (by file-ownership / source-area / lens) and **pre-assign shared-artifact ownership** — one owner writes, others return proposals; parallel writes to a shared page collide. Consume existing artifact layers (yesterday's profiles, an existing backlog) and research only the delta — it cut one run from ~2.3M to ~450k tokens.
2. **Dispatch with a verification contract.** In every worker prompt: (a) conventions pinned by **pointer to a sibling file/prior commit**, not inlined literals; (b) orchestrator-supplied context labeled **hints-to-verify** — workers re-verify against primary sources and **flag-not-comply** on conflict; (c) evidence-only constraints ("claims carry file:line / command provenance"); (d) a mandatory closing `## Confidence & unverified` footer, with absence claims stated as open questions carrying the probe's scope, never bare negatives.
3. **Collect: persist on arrival.** Allocate the output home (an `{topic}_appendices/` dir + README index, or scratchpad staging files) **before** dispatch; write each worker's deliverable verbatim as it lands — never hold 10k-token payloads in conversation across a compaction boundary. Defer running tests/builds until the fan-out settles (parallel test runs stall workers).
4. **Handle stragglers.** One retry for a transient failure; for a non-returning worker, one nudge then interrupt and proceed on the agreeing majority (record the gap). **Resume, don't respawn:** follow-ups to a returned worker go to the *same* agent (SendMessage) — warm context made fix-rounds ~10× cheaper.
5. **Verify in tiers.** N confident self-reports are claims, not results: scripted structural pass over **all** outputs (counts, required sections, link/citation resolution) + full reads of the top-risk few (>10 outputs → tiered, not line-by-line). Dedup findings by `file:line:category` — exact-key dedup silently killed a distinct co-located finding — and pass `also_flagged_by` into any verify prompt.
6. **Synthesize across agents — then verify yourself.** Run an explicit cross-agent pass for contradictions/overlaps (the load-bearing collision no single worker can see). Where claims warrant it, use a charter split: a reviewer that assumes citations true + separate agents that verify them. Then **re-derive every aggregate number in your synthesis from the workers' tables, and echo-grep any term you corrected** — in audited runs the only surviving errors were the orchestrator's own.
7. **Confidence gate.** Score per the global CLAUDE.md format; a synthesis claim no worker's evidence supports ships as an open question, not a finding.

## Output structure
The run leaves on disk: the per-worker deliverables (verbatim, indexed), the synthesis doc (citing worker evidence by path), and a short run header (worker charter, models used, stragglers/gaps, verification tier applied).

## Important rules
1. **Nothing lives only in chat.** Deliverables persist the turn they arrive.
2. **Workers verify, orchestrators re-verify themselves.** The least-verified writer in a fan-out is you.
3. **Opus workers on Claude Code/Cursor** — never inherited Fable. Codex: inherit (open issue), disclosed.
4. **Resume beats respawn** for any follow-up in the same area.
5. **Prose summaries of enumerable sets are forbidden** — counts carry the command that produced them.

## What this skill does NOT do
- Decide *whether* to fan out — that's judgment or `/triage`; trivial work runs inline.
- Own pipeline-specific orchestration — `compile-kb`, `kb-update`, cc-looper keep theirs.
- Deep-research web sweeps — the `deep-research` harness owns that shape.

## Output file
No fixed artifact of its own — the run's home (appendices dir + synthesis doc) is named at charter time; ask if no base name is discoverable.
