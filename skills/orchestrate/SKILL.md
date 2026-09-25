---
name: orchestrate
description: "Coordinates an ad-hoc parallel fan-out or swarm for analysis, research, review, extraction, or documentation outside a dedicated pipeline skill. Use when orchestrating multiple subagents or background agents, or when a prior fan-out lost results, duplicated work, or wasted budget. Pipeline-specific orchestration stays with its owning skill."
---

# orchestrate

Orchestrate an ad-hoc parallel fan-out of subagents with a verifiable contract and:

- Collect and persist their output as it arrives
- Consolidate **your own synthesis** to the same gates you impose on workers.

You do **not** re-derive what a worker already proved, respawn what you can resume, or hold deliverables only in conversation.

> **Litmus test:** if a run's evidence exists only in chat, if you're re-spawning a warm agent to ask a follow-up, or if your synthesis numbers were never re-derived from the workers' tables — you've left the lane.

## When to use

- **Ad-hoc:** "fan out agents", "spawn N subagents / research agents", parallel review/extraction/analysis/doc-gen that no pipeline skill owns.
- As the orchestration layer _inside_ a bespoke run (a spike review, a corpus sweep, a per-asset research pass).

## When NOT to use

- **Tasks-doc implementation loops** → the tasks-doc loop workflow.
- **KB compilation / vault doc refresh** → `compile-kb` / the vault's `kb-update` family (they embed their own orchestration).
- **A single subagent** → just launch it; this playbook's overhead needs N ≥ 2.

## Approach

**The approach should follow each subsection below sequentially.**

### Prepare

1. Gather context on the user's goal - what they want to accomplish and why they want a fan-out. If they proviced any inputs/references, read all of them e2e before proceeding.

2. Plan the fan-out - which agents you're going to dispatch and why.

- **Mandatory**: each subagent should provide a confidence score 0-100% with detailed uncertainty too.

3. Confirm plan with the user.

### Dispatch

Once the plan is confirmed, proceed with the dispatch.

### Collect

As the agents return, collect their outputs verbatim as it lands, and write them to disk with a meaningful name `collect_[slug].md`. Do not hold their entire output  in conversation context.

- **Mandatory check:** Confirm the output you collect has a confidence score with uncertainty details. Otherwise, go back to the agent and request it.

### Consolidate

Once they all complete, consolidate the fan-out and present a detailed summary of the results to the user. It should include:

- What each subagent was focused on
- What they accomplished
- Their collected result
- Summary of their confidence score

> Since this is a generic orchestrate skill, we don't have a structured template similar to other skills in this kit.

Ask the user if they want the consolidation persisted too. If yes, write `orchestration_[slug].md`
