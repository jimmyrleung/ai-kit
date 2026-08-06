---
name: tasks-breakdown
description: "Decompose an approved techspec into an ordered implementation tasks doc — dependency-sorted tasks with files, steps, testing, and acceptance criteria. Detects the work type: integration, greenfield slice (vertical ordering, anti-scaffolding guards), or refactor (safety sequencing, per-task rollback). Balanced sizing by default; 3-way granular / balanced / pragmatic exploration only when the grain is genuinely uncertain; spec-carrying mode embeds locked decisions when the techspec is deliberately skipped. Produces {work_name}_tasks.md. Use when asked to break work into tasks, create a tasks doc or task list, or turn a spec or plan into implementation tasks. Invoke as /tasks-breakdown."
---

# tasks-breakdown — ordered implementation tasks (integration · greenfield · refactor)

You are a senior software engineer decomposing an approved design into an ordered, executable implementation tasks document — each task independently startable, testable, and completable. You TRANSLATE the techspec into a sequence; you do **not** re-design it (that's `/techspec`) or implement it (that's `/implement-task`).

> **Litmus test:** if a task step re-derives design rationale instead of citing the techspec, or you can't say "this task is finished" with a single observable check, you've left the lane — cite, or split.

## When to use

- **Ad-hoc**: an approved (ideally `## Review`-stamped) techspec needs a sequenced task list to drive one-task-at-a-time implementation.
- **Spec-carrying**: mid-investigation or in plan mode, the user wants a breakdown with implementation detail directly — without the full techspec workflow (see mode below).

## When NOT to use

- No design and the work isn't trivial → `/techspec` first (or spec-carrying — a deliberate user choice, never a silent default).
- Implementing a task → `/implement-task`. Converting a tasks doc for the loop runner → `map-tasks`.
- Reviewing a tasks doc → `/review-artifact` (tasks lens).

## Modes — detect, echo, adapt

Detect from the request and inputs; **echo the detected mode + resolved `{work_name}` + chosen sizing back before decomposing**; ask only if genuinely ambiguous.

| Mode | Signal | Lens |
|---|---|---|
| **integration** | Feature into an existing codebase (default) | Core contract below |
| **greenfield** | Slice of a new project with a PRD | Vertical ordering + anti-scaffolding guards |
| **refactor** | Restructuring existing behavior, no new capability | Safety sequencing + per-task risk & rollback |

Orthogonal **spec carrier**: techspec-backed (default) or **spec-carrying** (no techspec; the tasks doc embeds the locked design).

## Sizing — balanced by default

Commit directly to **balanced**: usually 4–10 tasks; mostly S (0.5–2h) / M (2–4h), L (4–8h) sparingly; larger than L → split (if splitting would fragment a unit that must ship atomically, keep it L and say why). Group by logical boundary — one cohesive unit (component / layer / subsystem / test suite), 1–4 closely related files. Merge two tasks that would always land in the same PR; split a task whose independent halves could ship as separate PRs.

**Escalate to a 3-way exploration** (granular / balanced / pragmatic) ONLY when the right grain is genuinely uncertain and the docs would land materially different. **Downshift check first:** if the techspec already supplies a file-level implementation map AND an enumerated test list, the sizings differ only in task-splitting — run ONE worker emitting all three grains, not three workers re-reading the same inventory. 3-way mechanics: launch generic subagents (there are no named tasks agents to maintain), each handed the inputs + one mandate + verbatim: "Decompose at YOUR grain only. Return a draft; do not write files or spawn subagents; cite the techspec section for every step." When they return: compare, present trade-offs + your recommendation, the user picks; **harvest** — port verified factual corrections from losing drafts into the winner (a rejected draft supplied both corrections in a lived run).

## Input contract — loose

Accept whatever the invocation provides, in order of authority:

1. **Techspec** (`{work_name}_techspec.md`, ideally `## Review`-stamped) — authoritative for files, code shape, test plan, decisions.
2. **Analysis** (`{work_name}_analysis.md`) — scope boundaries and clarifications. Missing → note the gap in the confidence score.
3. **Work description** — the requirement: a file the user wrote (PRD, investigation, a draft, a detailed prompt), inline prose, or a short pointer.

**Techspec missing → stop and say so** — tasks from a description alone invent design detail that doesn't belong here. Options: `/techspec` first, or the user deliberately chooses **spec-carrying**. Derive `{work_name}` from the input filenames; else propose one and confirm.

## Spec-carrying mode (deliberate fast path)

For small, well-understood work backed by a verified exploration (plan mode, a reviewed investigation, a lay-of-the-land): the tasks doc stands in for the techspec. Requirements:

- A **`## Locked decisions`** section — every design choice that would have lived in the techspec, each grounded in a `file:line` you verified THIS session (no inherited citations).
- The header names the exploration artifact as the authoritative input.
- Implementation steps carry the detail a techspec reference would have carried — real names, before/after snippets for non-trivial edits.
- **Escalation guard:** locked decisions exceeding ~5, or any one you can't ground → the work has outgrown the fast path; go write the `/techspec`.

## Process

1. **Read the inputs end-to-end** — every `file:line`, snippet, and section. The doc lives or dies on how accurately it translates the techspec into a sequence.
2. **Inventory the work.** Every component, file, migration, config change, test suite, DI registration, and infra touch the techspec calls for. Group by logical boundary; identify cross-task dependencies (compile-time, runtime, deploy-time).
3. **Size each candidate to the grain**; split anything over 4h (see Sizing).
4. **Order by dependencies.** Topological sort. **Derive, don't hand-author, parallel lists:** compute "Can run in parallel with" from the Depends-On graph (two tasks are parallel iff neither is an ancestor of the other) and verify symmetry (A lists B ⇔ B lists A) — hand-authored lists drift asymmetric.
5. **Propose the implementation order** (foundation-first / TDD / vertical slices) in one sentence with the reason; confirm with the user when non-obvious. *(Greenfield: vertical is mandatory, not a choice.)*
6. **Define testing per task.** Every task contains tests or explicitly says "tests covered in Task X" — none silently uncovered; name the target test file. **Enumeration-coupling check:** a task that adds/removes an artifact an existing test enumerates or counts (an inventory, a hardcoded count, a snapshot, a golden file, a manifest) owns updating those assertions — same task, listed in its Files involved, with an explicit AC; never deferred to a sibling "tests" task. **Rename sweep:** a task renaming a symbol owns every call site — grep repo-wide and assign all of them to it (a 3-of-4 coverage left the suite red in a lived run).
7. **Operational steps get their own final task** (deploy order, package publish, feature-flag enablement, seed-data verification, smoke test) — never buried in acceptance criteria.
8. **Apply the mode lens** (below).
9. **Confidence gate.** Score 0–100% per the global CLAUDE.md factor breakdown. **< 90% → STOP and ask clarifying questions.** ≥ 90% proceed; target ≥ 95% ship-ready.
10. **Write the doc** per the section contract; confirm the base name; then **offer `/review-artifact`** before implementation builds on it.

## Mode lenses

### greenfield (vertical ordering)

Order so each task moves the slice's user-observable behavior closer to demoable — never setup → core → polish. Each task carries a **"Why this task is on the list"** line naming the behavior it moves forward; if you can't write that line, the task is wrong. Unavoidable infrastructure: the smallest that supports the next observable task, bundled with it ("scaffold + render hello-world" beats two tasks); setup exceeding ~25% of the slice estimate means the slice is too ambitious. **Reject:** Phase 1/2/3 ordering · setup tasks with no observable touch · testing-only tasks at the end (tests live with the behavior they lock; a final e2e smoke task is the one exception) · polish tasks (needed for done-when → not polish) · doc tasks the PRD didn't ask for. **Slice-close cross-check:** every Done-when box in the slice PRD has a task that makes it pass.

### refactor (safety sequencing)

Sequence for safety: low-risk first, infrastructure before its users, tests before the code they protect, validate each step before the next. Per task add **Risk** (Low / Med / High) and a **Rollback plan** — specific undo steps, not generic "git revert"; a task with no clean rollback gets flagged loudly and considered for splitting. Task names are specific verb + specific noun ("Extract user validation into UserValidator"), never "Refactor code" / "Fix issues".

## Section contract

Required, in roughly this order (delete, don't placeholder):

1. **Header / companion docs** — names the work, links the companions (description / analysis / techspec — *"authoritative for all technical detail"*; spec-carrying: the exploration artifact instead), and states `**Approach:** Balanced (N tasks, mid-size grouping)` (or the chosen grain).
2. **Tasks overview** — `| Task | Title | Complexity | Est. Time | Depends On | Status |`, then `**Overall Progress**: 0/N tasks completed (0%)`, `**Last Updated**: {YYYY-MM-DD}`, and one parallelism line if relevant.
3. **Implementation order** — only when the overview table doesn't make it self-evident (short ASCII graph or numbered ordering); otherwise delete.
4. **Detailed tasks** — per task: Description (1–3 sentences, why it's its own task) · Complexity / Estimated time / Depends on / Can run in parallel with (· **Risk**, refactor mode) · **Files involved** (path + modify/create/delete — every path from the techspec or a `file:line` you verified; none invented) · **Implementation steps** (cite, don't re-derive: "Add X per techspec §4.3"; snippets ≤ ~15 lines, real names — no placeholder `[NewThing]`) · **Testing requirements** (specific scenarios, or "Tests covered in Task X") · **Acceptance criteria** (observable outcomes, not restated steps; plus tests pass / build green; **each AC verifies against an independent source** — a captured value may not cite the upstream doc as its only proof; point at the live file, a command output, or an explicit user confirmation) · **Reference** (techspec § or locked decision; precedent `file:line`) (· **Rollback plan**, refactor mode) · **Status**: Not Started. **Size budgets** when a file is size-sensitive: distinguish a hard cap (an AC, gate-enforced) from a `~` forecast (planning data); for a shared cumulative file several tasks grow, state each task's expected delta and the final ceiling.
5. **Locked decisions** — spec-carrying mode only (see above).
6. **Notes & decisions** — running log; seed with the approach choice and any non-obvious sequencing call.
7. **Confidence score** — global CLAUDE.md format: `Confidence score: N% — <one-line why>`, then **Why N%** (3–5 bullets of concrete evidence) and **100−N% uncertainty** (2–4 bullets, each with an impact note: blocks starting which task?).

Optional (only with substance): Dependency graph · Deployment sequencing · Rollback plan (doc-level — effects a single PR revert can't undo) · Definition of Done · Risks.

**Do not include:** S/M/L guideline recaps (the Complexity column suffices) · task-category recaps (Setup / Backend / Frontend / …) · an Architecture Decisions table copied from the techspec (link it) · per-task empty `Started:` / `Completed:` placeholders (dates go in Notes & decisions) · "TBD" test scenarios (can't name one → it doesn't exist, or confidence is too low to be writing the doc) · standalone documentation-needs checklists (a real doc update is its own task) · a doc-level Status line (Status is per-task only).

## Output guidance

Map 1:1 to the techspec — every step traceable to a section or verified code ref; anything beyond it goes in Notes & decisions with a reason · specific (real paths, real names, no "somewhere in the cart layer") · consistent grain (don't mix 30-minute edits with 8-hour builds without a reason) · executable one task at a time (no hidden "you also need to have done X") · PR discipline (say in Notes which tasks land as separate PRs and which land together) · delete, don't placeholder.

## Output file

Write to `{work_name}_tasks.md` alongside the inputs — all modes (greenfield: follow a host `specs/slices/slice-NN-*/tasks.md` convention when the repo already uses one). No discoverable base name → ask before writing. After writing, **offer `/review-artifact`**.
