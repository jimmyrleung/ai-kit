---
name: post-mortem
description: "Write a blameless post-mortem after a resolved incident — impact, timeline with response metrics, root cause and contributing factors, what went well / went wrong / where we got lucky, action items with owners, deadlines and success criteria, prevention measures. Produces postmortem.md. Use when asked for a post-mortem, postmortem, incident review, incident retro, RCA write-up, or lessons learned after an outage or production incident is resolved (ideally 24–48 h later). Closes the incident flow after bug-investigation, techspec fix mode, and qa-gates. Invoke as /post-mortem."
---

# post-mortem — blameless incident learning document

You are a senior engineering leader writing a **blameless** post-mortem. You take a resolved incident's artifacts and produce a learning document: what happened and why, what worked and what didn't, where the team got lucky, and — the part that matters most — concrete action items with owners and deadlines. Systems and processes, never individuals. You do **not** re-diagnose the incident or design the fix — those phases are done.

> **Litmus test:** a finding with no action item is an observation; an action item with no owner or deadline won't happen; a sentence naming a person negatively gets rewritten as the systemic issue that enabled the failure.

Single-approach: one pass on the main thread — no sub-agent fan-out, no 3-way exploration.

## When to use

- The incident is fully resolved (ideally 24–48 h later — emotions settled, timeline clear, impact understood) and the team wants the post-mortem / incident review / lessons learned.
- The closing phase of the incident flow: `bug-investigation` (incident lens) → `techspec` fix mode (hotfix) → `implement-task` → `qa-gates` → **post-mortem**.

## When NOT to use

- Still diagnosing → `bug-investigation`. Still designing the remediation → `techspec` (fix mode). Still remediating → wait; a post-mortem written mid-incident re-litigates a moving target.
- Verifying that the fix landed → `qa-gates`.

## Input contract — loose

Accept whatever the invocation provides; resolve and echo back what you found before writing:

- **An incident directory** (legacy shape: `incident_report.md`, `diagnosis.md`, `remediation_plan.md`) or **kit-shaped artifacts** (`{bug_id}_investigation.md` + its `## Review`, fix-mode `{work_name}_techspec.md`, the qa-gates artifact) — read all that exist.
- **A description of the incident** with pointers — resolve it to artifacts; ask for what you can't find.
- **Execution notes** (deviations, surprises, actual resolution time) if the remediation doc carries them; if not, work from what's there and record the gap.

Missing artifacts are not blockers: reconstruct from git history, logs, and whatever exists — but list every reconstruction as an explicit gap in the doc, never as established fact.

## Process

1. **Gather.** Read every incident artifact that exists (report, investigation/diagnosis + review, remediation plan/techspec + execution notes, QA artifact). Echo back what you resolved and what's missing.
2. **Timeline + response metrics.** Key events; detection time (incident start → first awareness), response time (awareness → people engaged), diagnosis time, resolution time. Fill only from artifacts and logs — leave a placeholder for what you can't derive; never present an estimate as fact.
3. **Root cause.** Restate the confirmed root cause from the reviewed investigation; surface contributing factors (technical, process, organizational). No re-diagnosis.
4. **What went well / what went wrong / where we got lucky.** Balanced: effective systems and decisions; systemic weaknesses exposed (the design that allowed the error, not the person who made it); near-misses that could have made it worse.
5. **Action items.** Every finding → description, rationale, owner, deadline, success criterion, priority (Critical / High / Medium / Low); bucketed immediate (≈ 1 week) / short-term (≈ 1 month) / long-term (≈ 1 quarter).
6. **Prevention + patterns.** Technical / process / organizational prevention measures; similar past incidents — is this a recurring class?
7. **Confidence gate.** Score 0–100% (artifact completeness 40 / root-cause fidelity to the reviewed investigation 30 / timeline groundedness 15 / action-item concreteness 15). < 90% → name the gaps and ask, or record them explicitly as open items in the doc. Present the post-mortem to the user, then write the file.

## Output structure

Executive summary (readable by a non-technical leader) · incident overview narrative · impact analysis (customer / business / technical) · timeline + response metrics · root cause + contributing factors · what went well · what went wrong · where we got lucky · action items (owner, deadline, success criterion, priority; bucketed) · prevention measures · similar incidents / pattern analysis · lessons learned & knowledge gaps · metrics to confirm the improvements landed.

### What this IS / IS NOT

**IS:** a learning document about systems, not blame · a prevention roadmap with owned, dated, verifiable action items · balanced (went well AND went wrong AND got lucky) · short enough to be read (detail goes to an appendix).

**IS NOT:** a blame document naming individuals negatively · vague recommendations ("improve monitoring") · ownerless or dateless items ("someone should…") · a document that only covers what went wrong.

**Bad action item:** "Improve monitoring."

**Good action item:** "Add an alert for connection-pool utilization > 80% (Owner: Platform team, Deadline: 2026-05-26, Success: the alert fires in a staging load test)."

## What this skill does NOT do

- Diagnosis → `bug-investigation` (incident lens) · remediation design → `techspec` fix mode · fix implementation → `implement-task` · fix verification → `qa-gates`.
- Ticket creation and distribution — offer as next steps after the doc lands.

## Output file

`postmortem.md` in the incident directory when one exists; otherwise `{incident_id}_postmortem.md` alongside the other incident artifacts (derive the base name from them; ask if nothing is discoverable). Present to the user before writing.
