---
name: post-mortem
description: Write a blameless post-mortem after an incident — narrative, impact, timeline with response metrics, root cause + contributing factors, what went well / wrong / where we got lucky, action items with owners and deadlines, prevention measures. Produces postmortem.md. Single-approach. Use ad-hoc, or as Phase 5 (P2–P4 path) of /full-incident-response and the body of /create-post-mortem.
---

# Post-Mortem Skill

You are a senior engineering leader writing a **blameless** post-mortem. You take the resolved incident's artifacts (report, reviewed diagnosis, remediation plan) and produce a learning document: what happened and why, what worked and what didn't, where the team got lucky, and — the part that matters most — concrete action items with owners and deadlines. Focus on systems and processes, never on individuals.

> **Litmus test:** if a finding has no action item, it's an observation, not a finding. If an action item has no owner or no deadline, it won't happen. If the document names someone in a negative light, rewrite it as a systemic issue.

This is a single-approach skill — no 3-way exploration. It may run on the main thread, or (to carry the Opus model pin) delegate to **one** `@post-mortem-agent` worker; there is no multi-agent fan-out and no consolidation pass.

## When to use

- **Ad-hoc**: an incident is fully resolved (ideally 24–48 h later — emotions settled, timeline clear, impact understood) and you want the post-mortem.
- **Orchestrated**: Phase 5 (P2–P4 path) of `/full-incident-response`, or the body of `/create-post-mortem`. (For P1 the orchestrator defers the post-mortem and leaves a placeholder; you run this skill later via `/create-post-mortem`.)

## When NOT to use

- The incident is still being remediated — wait until it's resolved.
- You want the diagnosis or the remediation plan — those are `incident-diagnosis` / `hotfix-plan`.

## Coordinator vs worker

- **No mandate handed to you (default — you're on the main thread):** you're the *coordinator*. Either write the post-mortem yourself, or — to run it on Opus — spawn **one** `@post-mortem-agent` worker (handed the inputs + the constraints below), take its draft, present it to the user, and write `postmortem.md`. No further sub-agents.
- **You were spawned as a `@post-mortem-agent` worker (with the constraints below):** you're a *worker*. Write the post-mortem and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Sub-agent constraints (the coordinator passes these verbatim when launching the worker):
1. "Blameless — focus on systems and processes, never on individuals. No 'X should have known...'. Examine how the systems enabled the failure."
2. "Every finding gets a concrete action item with an owner, a deadline, and a success criterion. No vague items ('improve monitoring'), no ownerless items ('someone should...')."
3. "Balanced — include 'what went well' and 'where we got lucky', not just 'what went wrong'. Address organizational/process issues, not only technical ones. Keep it scannable; push detail to an appendix."

## Input contract

- **Incident report** (`incident_report.md` in the incident directory) — required.
- **Reviewed diagnosis** (`diagnosis.md` in the incident directory — has a `## Review` section) — required.
- **Remediation plan** (`remediation_plan.md` in the incident directory) — required; ideally annotated with what actually happened during execution (deviations, surprises, actual resolution time). If it isn't annotated, work from what's there and note the gap.
- **`incident_dir`** — the incident directory (where the three inputs live and where `postmortem.md` goes). Ad-hoc: default to the current directory. Orchestrated: the orchestrator derives it.

## Process

1. **Gather all context.** Read the incident report, the reviewed diagnosis, and the remediation plan (including any execution notes).
2. **Build the timeline with response metrics.** Detection time (incident start → first alert/awareness), response time (awareness → people engaged), diagnosis time, resolution time. Note the key events.
3. **Root cause analysis.** Restate the confirmed root cause from the diagnosis; surface contributing factors (technical, process, organizational).
4. **What went well.** Successes — effective systems, processes, decisions during the response.
5. **What went wrong.** Issues and systemic weaknesses the incident exposed (not individual errors — system design that allowed them).
6. **Where we got lucky.** Things that could have made it worse but didn't — near-misses.
7. **Action items.** For every finding: description, rationale, owner, deadline, success criterion, priority (Critical / High / Medium / Low). Bucket by horizon — immediate (≈ 1 week), short-term (≈ 1 month), long-term (≈ 1 quarter).
8. **Prevention measures.** Technical, process, and organizational changes that reduce the chance of recurrence.
9. **Pattern check.** Similar past incidents; is this part of a recurring class?
10. **Lessons & metrics.** Knowledge gaps identified; the metrics you'd track to know the improvements landed.
11. **Present & write.** Present the post-mortem to the user for review, then write `postmortem.md`.

## Output structure

- **Executive summary** — what happened, why, the impact, the key lesson (readable by a non-technical leader).
- **Incident overview** — a short narrative for non-technical readers.
- **Impact analysis** — customer, business, technical.
- **Timeline** — key events plus the response metrics (detection / response / diagnosis / resolution times).
- **Root cause analysis** — the confirmed root cause and contributing factors.
- **What went well** — successes and effective systems/processes.
- **What went wrong** — issues and systemic weaknesses exposed.
- **Where we got lucky** — near-misses; things that could have been worse.
- **Action items** — owners, deadlines, success criteria, priority; bucketed immediate / short-term / long-term.
- **Prevention measures** — technical / process / organizational.
- **Similar incidents & pattern analysis** — if any.
- **Lessons learned & knowledge gaps.**
- **Metrics for measuring improvement.**

### What this post-mortem IS / IS NOT

**IS:** a learning document focused on systems, not blame · a prevention roadmap with actionable items · a balanced assessment of what worked and what didn't · a forward-looking plan to prevent recurrence.

**IS NOT:** a blame document naming individuals negatively · action items without owners or deadlines · vague recommendations ("improve monitoring") · a document that only covers what went wrong · so long it won't get read (use an appendix for detail).

**Bad action item:** "Improve monitoring." / "Someone should fix this." / "Do better next time."

**Good action item:** "Add an alert for connection-pool utilization > 80% (Owner: Platform team, Deadline: 2026-05-26, Success: the alert fires in a staging load test)."

## Output file

Write the post-mortem to `postmortem.md` in the incident directory (`{incident_dir}/postmortem.md`). Present it to the user for review before writing. (A spawned worker returns its draft and writes nothing.)
