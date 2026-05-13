---
name: triage
description: Route a free-text engineering request to the right workflow (greenfield-dev | integration-feature-dev | full-bug-fix-workflow | refactor-techdebt-dev | full-incident-response), to a one-shot phase skill, or to "just do it directly". Asks up to 2 clarifying questions if signals are ambiguous. Stops mis-routes — running greenfield-dev on a bug, or feature-dev on a refactor, costs 30-60 min apiece. Invoke as /triage when starting non-trivial work and the right workflow isn't obvious. Output is a one-line recommendation; the user invokes the chosen command. Suggestion-mode only — never auto-executes the chosen workflow.
---

# Triage — pick the right workflow (or skip the workflow)

Route a free-text request to one of: a workflow orchestrator, a one-shot phase skill, or "just do
it directly". Output is a single one-line recommendation. **You do NOT auto-execute.**

Two-question cap. Recommend at confidence ≥90% — otherwise recommend best-guess + state the
residual uncertainty.

---

## Phase 0 — Mid-flight detection (do this first, it's free)

Before triaging, check whether the user is already mid-workflow in this cwd. Run:

- `git status --short` and `ls` of the cwd
- look for any of:
  - `*_techspec.md`, `*_tasks.md`, `*_investigation.md`, `*_audit.md` recently modified at the repo root or under a feature folder
  - an open `incidents/{id}/` dir with `diagnosis.md` / `remediation_plan.md` inside
  - `slices/{n}/` with PRD / techspec / tasks docs

**If mid-flight, STOP. State which workflow you detected and the next command** (`/gf-implement-task` /
`/integration-create-tasks` / `/implement-bug-fix` / `/diagnose` / `/plan-hotfix` /
`/create-post-mortem` / `/incident-status` / etc.). Ask "continue this work, or triage a different
task?" and let the user pick. Do not silently re-triage on top of in-progress work.

---

## Phase 1 — Classify (signals → route)

Read the request + the cwd `ls` + check `MEMORY.md` for project-level mode hints. Match against:

| Signal cluster | Route to | Notes |
|---|---|---|
| "production down / failing / urgent / customers / outage / P1-4 / hotfix" + existing codebase | `/full-incident-response` | The workflow's own Phase 1 severity-routes P1 (streamlined, ≥70% gate) vs P2-4 (full, ≥90% gate). |
| "bug / broken / fails / regression / wrong output / unexpected behaviour" + existing codebase, NOT urgent | `/full-bug-fix-workflow` | Workflow handles S/M/L/XL classify → skills / bail. |
| "add / integrate / new feature / endpoint / page / screen" + existing codebase | `/integration-feature-dev` | Workflow handles S (fast path → `pragmatic-techspec` / `balanced-tasks-creation`) / M (3-way) / L+XL (bail to per-command). |
| "refactor / restructure / extract / rename / consolidate / clean up / tech debt" + same-behaviour intent | `/refactor-techdebt-dev` | Workflow enforces risk gates, abort criteria, success-metrics-required gate, rollback decision tree. |
| "new project / from scratch / greenfield / new module / slice list / roadmap" + empty-ish cwd OR explicit greenfield mode in `MEMORY.md` | `/greenfield-dev` | Workflow drives roadmap → per-slice PRD → techspec → tasks → implement. |
| One-shot artefact production ("write me a techspec for X", "review this doc", "audit this corner") | **Short-circuit → a single phase skill** (table below) | Skips the orchestrator entirely. |
| Trivial — typo, one-line edit, one grep, one-question | **"Just do it directly — no workflow"** | Don't summon a full workflow for a 30-second task. |
| Nothing fits cleanly | **"None of these fit — record the gap"** branch (Phase 3) | Do not force-fit. |

Compute confidence using the global CLAUDE.md factor breakdown (API docs 30% / similar patterns 25% /
data flow 20% / complexity 15% / cross-system impact 10%).

### Short-circuit table (one-shot phase-skill routes)

| Request shape | Skill / command |
|---|---|
| "Write me a quick techspec for X" (existing codebase, small) | `/integration-pragmatic-techspec` |
| "Break this techspec into tasks (balanced)" | `/integration-balanced-tasks` |
| "Just investigate this bug — no need for the full loop" | `/investigate-bug` |
| "Just analyze the impact of this fix" | `/analyze-impact` |
| "Just audit this corner of the codebase" | `/audit-refactor-techdebt` |
| "Review this {investigation / techspec / audit / diagnosis} doc" | `/review-investigation` / `/review-techspec` / `/review-diagnosis` / (or `review-artifact` ad-hoc for the rest) |
| "Just diagnose this incident" / "just write the post-mortem" | `/diagnose` / `/create-post-mortem` |
| "Create a per-slice PRD" / "create the master roadmap" | `/create-prd` / `/create-roadmap` |
| "Generate QA scenarios for this slice" | `/create-qa-scenarios` |

---

## Phase 2 — Ask up to 2 clarifying questions if confidence <90%

Use the `AskUserQuestion` tool (fallback: plain-text "I need to clarify: …" if it isn't available).
High-leverage questions to pick from:

- **"Is the change supposed to alter behaviour, or preserve it?"** — feature vs refactor.
- **"Is this customer-impacting right now, or can it wait?"** — incident vs bug.
- **"Is there an existing codebase, or are we starting fresh?"** — integration vs greenfield.
- **"Do you want the full workflow, or just one artefact (e.g. just the techspec)?"** — orchestrator vs short-circuit.

**Cap: 2 questions.** If still <90% after, recommend best-guess + state residual uncertainty. Do
not ask a third — the cost of one extra question on every triage outweighs the cost of an occasional
re-route after one bad guess.

---

## Phase 3 — Recommend (one line, then stop)

Output exactly:

> **Recommend:** `/{workflow-or-skill}` `{short-arg-hint}` — confidence X% — because Y.
> (Run it when ready; redirect if this is wrong.)

For the "none fits" branch:

> No existing workflow fits cleanly. Recorded the gap (Phase 4). Consider whether this is recurring
> — `/improve` will surface a "propose new workflow" suggestion if you see it again.

For the "just do it" branch:

> This is a one-shot task — just do it directly, no workflow needed.

**Do NOT auto-invoke the recommended command.** Recommend and stop. The user invokes.

---

## Phase 4 — Observation note (one short line for `/close` to pick up)

Leave a single line in the current session context so `/close` writes it through to
`~/.claude/observations/{date}-{slug}.md` at session end:

> Triage note — `route_picked: {workflow-or-skill}` · `confidence: X%` · `questions_asked: N` · `signals: {keywords}`

If the session ends up using a *different* workflow than recommended (you mid-flight switched
because the user redirected), `/close` will pair `route_actually_used` against `route_picked` and
log `outcome: switched`. That's the friction signal `/improve` reads to propose tightening this
skill's Phase-1 signals table.

---

## When NOT to use triage

- The user named the workflow explicitly ("run `/integration-feature-dev`") — just go.
- You're mid-workflow (Phase 0 caught this — exit early).
- The task is trivial (typo, one-line edit, one grep). Triage adds friction in front of trivial work.
- The user is asking a *question*, not requesting *work* ("how does X work?", "what does Y do?"). Don't triage Q&A.

## What triage is NOT

- Not a planner — it picks the workflow; the workflow plans.
- Not a size/severity classifier inside a workflow — each workflow's own Phase 1 does that.
- Not auto-executing — recommendation only; the user invokes.
- Not a memory write — Phase 4 leaves *one line for `/close`*, it does not edit `MEMORY.md` or any other live file.
