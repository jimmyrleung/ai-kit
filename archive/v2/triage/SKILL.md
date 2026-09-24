---
name: triage
description: "Recommends where to start a non-trivial engineering request when the right skill or workflow is unclear. Use for “which skill?”, “where do I start?”, or “what should I run?”, including recurring or iterate-until-done work. Routes by current intent and valid related artifacts; recommendation-only unless execution is explicitly authorized. Skip when the next step is already clear or the task is trivial."
---

# Triage — pick the right entry skill (or skip the ceremony)

Route a free-text request to one of: the entry skill of a chain, a one-shot skill, a loop
primitive (recurring / iterate-until-done work), or "just do it directly". Default output is one recommendation. An explicit request to execute/continue may authorize
the selected next step after validating its prerequisites; recommendation-only always stops.

There are no workflow orchestrators to route to — each chain's entry skill detects the work type
itself (`analyze-work` detects integration / greenfield / refactor; `techspec` adds fix / hotfix;
`bug-investigation` carries the incident lens). Triage picks the *entry point*; the skill takes it
from there.

Two-question cap. Recommend at confidence ≥90% — otherwise recommend best-guess + state the
residual uncertainty.

---

Follow [authorized work](references/shared/authorized-work.md) for existing permission,
blocking questions, and requested discussion cadence; resolve from this skill folder.

## Phase 0 — Current intent and related state

Resolve the current request first: new work, continue named work, recommendation-only, or
explicit execution. Inspect Git status and related artifacts only to support that intent.
Recent unrelated files or an old chain cannot hijack a new request. If related identity is
ambiguous, ask which work item; do not routinely ask whether to abandon unrelated work.

For related in-flight work, inspect actual contents and validate review scope, verdict and
content/dependency identity under [change evidence](references/shared/change-evidence.md).
A heading, filename or timestamp alone never proves approval. Route by valid current state:

| Related artifact state | Next step |
|---|---|
| Analysis/investigation/techspec/tasks missing, stale or rejected review | `review-artifact` or its named corrective producer; never advance as approved |
| Valid approved analysis, no techspec | `techspec` |
| Valid approved techspec, no tasks | `tasks-breakdown` (or `implement-task` for a reviewed small fix) |
| Repository task open with dependencies met | `implement-task`; retain resource/readiness checks |
| Repository tasks Done, implementation review missing/stale | `review-implementation` |
| Valid reviewed implementation, repository QA incomplete | `qa-gates` |
| Repository GO, deploy/live tasks pending | Report repository completion and pending operations; execute operations only if specifically authorized |
| Resolved incident, no post-mortem | `post-mortem` |

Recommend that next step by default. If the current request explicitly authorizes continuing
it, follow it within scope after prerequisites are satisfied. A review failure needs correction,
not a generic fresh-chain restart; do not invent a waiver or completion from the request alone.

---

## Phase 1 — Classify (signals → route)

Inspect the request + the cwd `ls` + check `MEMORY.md` for project-level mode hints. Match against:

| Signal cluster | Route to | Notes |
|---|---|---|
| "bug / broken / fails / regression / wrong output / unexpected behaviour" — urgent or not | `bug-investigation` skill | Incident lens engages itself on production-incident signals (outage, P1, customers); then `review-artifact` → `techspec` (fix / hotfix) → `implement-task` (fix lens) → `qa-gates` → `post-mortem` if it was an incident |
| "add / integrate / new feature / endpoint / page / screen" + existing codebase | `analyze-work` skill | Integration mode; chain continues `techspec` → `tasks-breakdown` → `implement-task` → `review-implementation` → `qa-gates` |
| "refactor / restructure / extract / rename / consolidate / clean up / tech debt" + same-behaviour intent | `analyze-work` skill | Refactor mode (phased plan + rollback lives in `techspec`) |
| "new project / from scratch / greenfield / new module / slice" + empty-ish cwd | `analyze-work` skill | Greenfield mode (vertical-slice guarded) |
| Unfamiliar territory — "what's even here?", pre-refinement, no requirement written yet | `lay-of-the-land` skill | Phase-0 recon; feeds `analyze-work`, `bug-investigation`, or a refinement discussion |
| One-shot artefact production ("write me a techspec for X", "review this doc", "document this endpoint") | **Short-circuit → a single skill** (table below) | Skips the chain entirely |
| "every morning / every N hours / keep checking / watch this PR / poll / until the tests pass / until score ≥ X / re-run until" — recurring or iterate-until-condition intent | **Loop-primitive route** (table below) | The loop frame wraps whatever runs inside it — pick the frame first, then (if needed) triage the per-iteration work too |
| Trivial — typo, one-line edit, one grep, one-question | **"Just do it directly — no skill"** | Don't summon a chain for a 30-second task |
| Nothing fits cleanly | **"None of these fit — record the gap"** branch (Phase 3) | Do not force-fit |

Compute confidence using the loaded confidence-factor breakdown (API docs 30% / similar patterns 25% /
data flow 20% / complexity 15% / cross-system impact 10%).

### Short-circuit table (one-shot skill routes)

| Request shape | Skill |
|---|---|
| "Write me a techspec / design doc / impact analysis for X" | `techspec` |
| "Break this spec into tasks" | `tasks-breakdown` |
| "Just investigate this bug — no need for the full chain" | `bug-investigation` |
| "Review this {analysis / investigation / techspec / tasks} doc" | `review-artifact` |
| "Review the implemented code for prefix X" | `review-implementation` |
| "Verify / QA the finished implementation" | `qa-gates` |
| "Write the post-mortem" | `post-mortem` |
| "Document this workflow / endpoint / handler / job" | `document-workflow` |
| "Document this Terraform codebase" | `document-terraform` |
| "Walk me through this unfamiliar code" / "walk me through what we built" | `onboard-me` / `walkthrough-implementation` |
| "Record this decision" | `record-decision` |

### Loop-primitive table (recurring / iterate-until-condition routes)

Full recipes, constraints, and local-vs-cloud rules live in the loop-recipes document
(`docs/` + `loop-recipes.md`).

| Request shape | Recommend |
|---|---|
| Iterate until a **verifiable** condition, with a cap ("until all tests pass, max 5 tries") | bounded loop frame — deterministic done-check + explicit turn cap |
| Recurring on an interval, touches local files / private repos ("summarize X every morning") | local recurrence frame — stops when the machine is off |
| Recurring with no local-FS dependency, must survive the machine | cloud recurrence frame |
| Watching an external system for change (PR reviews, CI, a queue) | local watch frame with the interval matched to how fast the watched thing actually changes |
| A tasks-doc stream (implement / document each task in a doc) | tasks-doc stream workflow — checkpoints, ledgers, and resume; native loop frames do not replace it |

Two rules carried from the recipes doc:

- Pick the loop frame *before* the inner work — a loop wraps invocations; it doesn't change
  what runs inside each one. If the per-iteration work itself needs routing, recommend both
  ("wrap the `bug-investigation` skill in a bounded loop frame …").
- Loop-frame availability varies by active runner — verify the selected frame before recommending it;
  if unavailable, fall back to a plain turn-based prompt with explicit "stop after N tries" criteria.

---

## Phase 2 — Ask up to 2 clarifying questions if confidence <90%

Use the available structured-question capability (fallback: plain-text "I need to clarify: …" if it isn't available).
High-leverage questions to pick from:

- **"Is the change supposed to alter behaviour, or preserve it?"** — feature vs refactor.
- **"Is this customer-impacting right now, or can it wait?"** — incident lens vs plain bug.
- **"Is there an existing codebase, or are we starting fresh?"** — integration vs greenfield.
- **"Do you want the full chain, or just one artefact (e.g. just the techspec)?"** — chain entry vs short-circuit.
- **"Is this a one-off, or should it recur / keep iterating until a condition is met?"** — skill route vs loop-primitive route.

**Cap: 2 questions.** If still <90% after, recommend best-guess + state residual uncertainty. Do
not ask a third — the cost of one extra question on every triage outweighs the cost of an occasional
re-route after one bad guess.

---

## Phase 3 — Recommend, or continue when explicitly authorized

Output exactly:

> **Recommend:** `{skill}` `{short-arg-hint}` — confidence X% — because Y.
> (Run it when ready; redirect if this is wrong.)

For the "none fits" branch:

> No existing skill fits cleanly. Noted the gap in this session (Phase 4). Consider whether this is recurring
> — the `improve` skill will surface a "propose new skill" suggestion if you see it again.

For the "just do it" branch:

> This is a one-shot task — just do it directly, no skill needed.

Recommendation-only/default triage stops here. If the user explicitly requested execution or
continuation, state the selected route and invoke it within existing authorization after
checking prerequisites. Do not add a second generic permission question.

---

## Phase 4 — Observation note (one short line for the `close` skill to pick up)

Leave a single candidate line in the current session context. The optional recorder resolves
through [the feedback contract](references/shared/feedback.md), from this skill's canonical
directory; no configured recorder means `disabled`, with no private store write:

> Triage note — `route_picked: {skill}` · `confidence: X%` · `questions_asked: N` · `signals: {keywords}`

If the route later changes, include `route_actually_used` and the observed reason. A new user
intent is not automatically a routing defect. Emit a supported observation only through the
one execution recorder, using the contract's envelope, approved outcome enum and exact tag;
keep the route transition in its evidence, never `outcome: switched`. The recorder validates
and deduplicates before persistence. A session note is not a persisted receipt or invocation
telemetry. Supported routing friction can inform `improve` without manufacturing a finding.

---

## When NOT to use triage

- The user named the skill explicitly ("run `analyze-work`") — just go.
- The related next step is already explicit and valid; continue it within the request's authorization.
- The task is trivial (typo, one-line edit, one grep). Triage adds friction in front of trivial work.
- The user is asking a *question*, not requesting *work* ("how does X work?", "what does Y do?"). Don't triage Q&A.

## What triage is NOT

- Not a planner — it picks the entry skill; that skill's own mode detection and process plan the work.
- Not a size/severity classifier — each skill's own detection does that (e.g. `bug-investigation`'s severity-aware gate).
- No inferred execution permission: recommendation-only by default; explicit continuation is bounded by valid prerequisites and scope.
- Not a memory write — Phase 4 leaves *one line for the `close` skill*, it does not edit
  `MEMORY.md` or any other live file.
