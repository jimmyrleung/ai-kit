---
name: integration-tasks
description: Break a techspec into an ordered list of implementation tasks by exploring three sizings in parallel — granular / balanced / pragmatic — then committing to one with the user. Produces {feature}_tasks.md. Used ad-hoc, or as Phase 5 (M-size path) of /integration-feature-dev and the body of /integration-create-tasks. For small features where a 3-way comparison is overkill, use `balanced-tasks-creation` instead.
---

# Integration Tasks Skill (3-way exploration)

You break a technical specification into a clear, sequenced list of tasks a developer can execute one at a time — each independently testable and completable. This skill explores three sizings side by side and then commits to one. Use it when the right granularity is genuinely uncertain; when it isn't, `balanced-tasks-creation` skips straight to the committed answer.

## When to use

- **Ad-hoc**: a feature where "lots of tiny tasks" vs "a few chunky ones" would land very differently and you want to see both before deciding.
- **Orchestrated**: Phase 5 (M-size path) of `/integration-feature-dev`, or the build body of `/integration-create-tasks`.

## When NOT to use

- Small features, or features where balanced sizing is obviously right — use `balanced-tasks-creation`.
- Greenfield work — use the greenfield `tasks-creation` skill.
- No techspec yet — produce the techspec first (`integration-techspec` or `pragmatic-techspec`). Tasks without a techspec drift into re-designing the feature.

## Coordinator vs worker

- **No mandate handed to you (default — you're on the main thread):** you're the *coordinator*.
  1. Read the inputs (techspec — authoritative — plus integration analysis and feature description) carefully, every `file:line` and snippet.
  > **Downshift check (before launching workers).** If the techspec already supplies a **file-level implementation map AND an enumerated test list**, the three sizings will differ only in task-splitting, not content — run **one sizing worker that emits all three grains (granular / balanced / pragmatic)** rather than three workers re-reading the same inventory. Reserve the full 3-way parade for when the right grain is genuinely uncertain.
  2. Launch **3 `@integration-tasks-creator-agent` sub-agents in parallel**, each handed the inputs and one mandate:
     - **granular** — small tasks, higher quantity; maximum checkpointing.
     - **balanced** — mid-size tasks, "okay" quantity (usually 4–10); each big enough to be its own checkpoint, small enough to finish without fatigue.
     - **pragmatic** — bigger tasks, lower quantity; minimum overhead.
  3. When they return, compare. Form your opinion on which fits *this* feature, considering: small fix vs large feature, urgency, complexity, team context — and that the tasks will be executed one at a time.
  4. Present to the user: a brief summary of each sizing, a trade-offs comparison, your recommendation with reasoning.
  5. Ask the user which sizing they prefer.
  6. Build the final tasks document at the chosen sizing, run the confidence gate, and write the file.
- **You were spawned as a sub-agent with a mandate:** you're a *worker*. Decompose the techspec **at your assigned sizing only** and return your draft tasks list to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

## Input contract

Expect, in order of authority:
1. **Techspec** (`*_techspec.md`) — authoritative for files, code shape, test plan, decisions. **If missing, stop and tell the user** — don't generate tasks from a feature description alone (you'll invent implementation detail that doesn't belong here). Options: produce the techspec first, or explicitly accept speculative tasks at < 90% confidence.
2. **Integration analysis** (`*_integration.md`) — authoritative for scope boundaries and PO/team clarifications. If missing but the techspec is present, proceed and note the gap in the confidence score.
3. **Feature description** — the requirement. Derive the `{feature}` base name from the inputs; ask if not discoverable.

## Process (per sizing — what each worker does, and what the coordinator does for the final)

1. **Review previous phases' outputs.** Feature description, integration analysis + review notes, then the techspec **carefully** — every reference, every snippet, every section. The tasks doc lives or dies on how accurately it translates the techspec into a sequence.
2. **Inventory the work.** Every component, file, migration, config change, test suite, DI registration, infra touch the techspec calls for. Group by logical boundary (cohesive unit — one component / layer / subsystem / test suite). Identify cross-task dependencies (compile-time, runtime, deploy-time).
3. **Size each candidate task** to your mandate's grain:
   - **S** (0.5–2h): single-file edit, small component, one DTO field, a test class stub, a DI registration change.
   - **M** (2–4h): new service with DI, API endpoint + validation, component with state, a focused integration suite, a mid-size refactor.
   - **L** (4–8h): complex component with many interactions, DB migration + backfill, an E2E suite, a complex generator.
   - **Larger than L → split it.** If splitting would fragment a unit that must ship atomically, keep it L and say why. (Granular pushes toward S; pragmatic tolerates more L; balanced sits in the middle and stays in the 4–10 range.)
4. **Order by dependencies.** Topological sort. Mark parallelizable tasks ("Can run in parallel with: Task X, Y"). A small ASCII dependency graph only when the linear list doesn't make the order obvious.
5. **Propose an implementation order** and confirm with the user when it's non-obvious: foundation-first (DB → backend → frontend → tests), TDD (test → code → test → code per scenario), or vertical slices (smallest end-to-end slice first). State the choice in one sentence with the reason.
6. **Define testing per task.** Every task either contains tests or explicitly says "tests covered in Task X" — no task silently has zero coverage. Specify unit vs integration vs manual; name the target test file.
7. **Call out critical operational steps** (deploy order, package publish, feature-flag enablement, seed-data verification, smoke test) as their own final task — don't bury them in acceptance criteria.
8. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (API docs 30% / similar patterns 25% / data flow 20% / complexity 15% / cross-system impact 10%). **If < 90%: STOP and ask clarifying questions** — don't write the doc yet. At ≥ 90%, proceed. Target ≥ 95% ship-ready.
9. **Write the tasks document** (coordinator only) following the section contract below.

## Required sections

1. **Header / companion docs** — names the feature, links the companion docs (feature description, integration analysis, techspec — *"authoritative for all technical detail"*), and states the chosen approach + task count: `**Approach:** Balanced (N tasks, mid-size grouping)` (or Granular / Pragmatic).
2. **Tasks overview** — a progress table: `| Task | Title | Complexity | Est. Time | Depends On | Status |`. Then `**Overall Progress**: 0/N tasks completed (0%)`, `**Last Updated**: {YYYY-MM-DD}`, and one parallelism line if relevant.
3. **Implementation order** — only when non-obvious (a short ASCII graph or numbered ordering); otherwise delete the section.
4. **Detailed tasks** — per task: Description (1–3 sentences, why it's its own task) · Complexity / Estimated time / Depends on / Can run in parallel with · **Files involved** (`path` + modify/create/delete) · **Implementation steps** (specific; reference the techspec — "Add X per techspec §4.3" — not re-derive it; small snippets only, real names not placeholders) · **Testing requirements** (specific scenarios; or "Tests covered in Task X") · **Acceptance criteria** (observable outcomes, not restatements of steps; + "Tests pass", "project builds") · **Reference** (techspec §, precedent `file:line`) · **Status**: Not Started.
5. **Notes & decisions** — a running log; seed it with the approach choice and any non-obvious sequencing call; expect the developer to append during execution.
6. **Confidence score** — global CLAUDE.md format: `Confidence score: N% — <one-line why>`, then **Why N%** (3–5 bullets: techspec sections mapped 1:1, file paths verified, deps understood, patterns reused) and **100−N% uncertainty** (2–4 bullets, each with an impact note: blocks starting which task?).

## Optional sections (include only with substance — never a placeholder)

Dependency graph (when the "Depends on" columns don't convey the shape — e.g. two parallel tracks converging) · Deployment sequencing (multi-repo/service deploy order) · Rollback plan (effects not safe to revert via a single PR revert) · Definition of Done (multi-repo features or a ship checklist beyond per-task criteria) · Risks (task-level risks the acceptance criteria don't cover).

## Do not include

Generic "Task Complexity Guidelines" recap (the Complexity column is enough) · generic "Common Task Categories" recap (use Setup/Backend/Frontend/Testing/Docs/Polish mentally; don't echo them) · an "Architecture Decisions" table copied from the techspec (link to it) · per-task empty `Started:`/`Completed:` timestamp placeholders (the Status line is enough; dates go in Notes & Decisions) · "TBD" test scenarios (if you can't name one, either it doesn't exist — say so — or your confidence is too low to be writing the doc) · standalone "Documentation Needs" checklists (make doc updates their own task if real, else skip).

**Rule:** if a section has no substance, delete it — don't leave a placeholder.

## Output guidance

Map 1:1 to the techspec — every step traceable to a techspec section or a verified code ref; anything the techspec doesn't cover goes in Notes & Decisions with a reason. Be specific (real paths, real names, real `file:line`). Size consistently within the chosen grain. Write for execution one task at a time — each task startable in isolation given its declared dependencies. Preserve PR discipline — say in Notes which tasks should land as separate PRs and which should land together. Delete, don't placeholder.

## Output file

Write the final tasks document to `{feature_name}_tasks.md`, alongside the feature description, integration analysis, and techspec. If no base name is discoverable, ask the user before writing. (Workers return drafts and write nothing.)
