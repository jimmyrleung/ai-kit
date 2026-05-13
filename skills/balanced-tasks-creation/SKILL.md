---
name: balanced-tasks-creation
description: Produce a balanced implementation tasks document (mid-size tasks, "okay" quantity) for integrating a feature into an existing codebase. Use ad-hoc for small features, or as the build/review body in an orchestrated command. Skips the 3-way granular/balanced/pragmatic exploration and commits directly to balanced.
---

# Balanced Tasks Creation Skill

You are a senior software engineer breaking a technical specification into an ordered list of executable implementation tasks. You commit to a single sizing strategy — **balanced** — and produce a complete, actionable tasks document that a developer can execute one task at a time.

## When to use

- **Ad-hoc**: a small-to-medium feature where the full parallel exploration (`/integration-create-tasks` with granular / balanced / pragmatic agents) would be overkill, but a standardized tasks-for-the-record is still wanted.
- **Orchestrated**: invoked from a command that wants a single-agent build-and-review loop (no 3-way exploration).

## When NOT to use

- The feature has genuine uncertainty about the right granularity and you'd benefit from comparing granular vs balanced vs pragmatic side by side. Use `/integration-create-tasks` instead.
- The work is greenfield (no existing codebase to integrate with). Use the greenfield `tasks-creation` skill instead.
- You don't have a techspec yet. Produce the techspec first (`@pragmatic-techspec` or `/integration-create-techspec`); tasks without a techspec drift into re-designing the feature.

## What "balanced" means

Mid-size tasks, "okay" quantity. Concretely:

- **Task count**: usually **4–10** for a small-to-medium feature. If you land at 2–3, you're too coarse; if you land at 15+, you're too granular.
- **Task size**: most tasks are **S (0.5–2h)** or **M (2–4h)**. Use **L (4–8h)** sparingly. **If a task is larger than L, break it down further.**
- **Grouping rule**: group by logical boundary — a cohesive unit of work (one component, one layer, one subsystem, one test suite). One task may touch 1–4 closely related files; don't split a single file across tasks unless the edits are genuinely independent.
- **Tests stance**: tests live in their own task(s) positioned right after the implementation they cover, OR as an explicit subsection of the implementation task. Do not scatter tests as line items inside multiple implementation tasks — consolidate them so the test task is runnable end-to-end.
- **Granularity check**: if two adjacent tasks would always be worked together and reviewed in the same PR, merge them. If one task has two independent halves that could ship as separate PRs, split them.

Balanced is not "maximum safety" (that's granular) and not "minimum overhead" (that's pragmatic). It's the shape where each task is big enough to be worth its own checkpoint and small enough to be completable and reviewable without fatigue.

## Input contract

Expect, in order of authority:

1. **Techspec** (`*_techspec.md`) — authoritative for files, code shape, test plan, and decisions.
2. **Integration analysis** (`*_integration.md`) — authoritative for scope boundaries and PO/team clarifications.
3. **Feature description** — the requirement itself.

If the **techspec is missing**, stop and tell the user. Do not generate tasks from a feature description alone — you'll invent implementation detail that doesn't belong in the tasks doc. The user's options are: (a) run `/integration-pragmatic-techspec` first, or (b) explicitly accept speculative tasks at < 90% confidence.

If the **integration analysis is missing** but the techspec is present, proceed and call out the gap in the confidence score.

## Process

1. **Review previous phases' outputs.**
   - Read the feature description end to end.
   - Read the integration analysis (or the lighter plan, if that's what exists) and any review notes.
   - Read the techspec **carefully** — every `file:line` reference, every snippet, every section. The tasks doc lives or dies on how accurately it translates the techspec into a sequence.

2. **Inventory the work.**
   - List every component, file, migration, config change, test suite, DI registration, and infra touch the techspec calls for.
   - Group the inventory by logical boundary (see "What balanced means"). The groups become candidate tasks.
   - Identify cross-task dependencies (compile-time, runtime, deploy-time).

3. **Size each candidate task.**
   - **S**: 0.5–2h. Single-file edit, small component, one DTO field, one xUnit test class stub, a DI registration change.
   - **M**: 2–4h. New service with DI, API endpoint + validation, component with state, a focused integration test suite, a mid-size refactor.
   - **L**: 4–8h. Complex component with many interactions, a DB migration + backfill, an E2E suite, a complex generator (e.g. QuestPDF).
   - If a candidate exceeds 4h, **split it**. If splitting would fragment a unit of work that must ship atomically, keep it as L and note why.

4. **Order by dependencies.**
   - Topological sort: a task that depends on another comes after it.
   - Mark parallelizable tasks with "Can run in parallel with: Task X, Y".
   - Draw a small ASCII dependency graph only when the order isn't obvious from the linear task list.

5. **Propose an implementation order and confirm with the user.**
   - Pick one of: foundation-first (DB → backend → frontend → tests), TDD (test → code → test → code per scenario), or vertical slices (deliver smallest end-to-end slice first).
   - State your choice in one sentence with the reason. Confirm with the user before finalizing the doc if the order is non-obvious.

6. **Define testing per task.**
   - Every task either contains tests or explicitly says "tests covered in Task X". No task silently has zero test coverage.
   - Specify unit vs. integration vs. manual, and name the target test file.

7. **Call out critical operational steps**, where applicable (deploy order, NuGet publish, feature flag enablement, seed data verification, smoke test). Give these their own final task rather than burying them in acceptance criteria.

8. **Confidence gate.**
   - Compute the confidence score using the factor breakdown in the user's global CLAUDE.md (API docs 30%, similar patterns 25%, data flow 20%, complexity 15%, cross-system impact 10%).
   - **If < 90%, STOP and ask clarifying questions.** Do not write the tasks doc yet.
   - At ≥ 90%, proceed.

9. **Write the tasks document** following the section contract below.

## Required sections

Every tasks document produced by this skill includes all of the following, in roughly this order:

### 1. Header / companion documents

A short block at the top naming the feature and linking the companion docs:

```markdown
# Implementation Tasks — {feature_name}

> **Companion documents:**
> - Feature description: `{feature}_description.md`
> - Integration analysis: `{feature}_integration.md`
> - Techspec: `{feature}_techspec.md` (authoritative for all technical detail)
>
> **Approach:** Balanced (N tasks, mid-size grouping)
```

### 2. Tasks overview

A progress-tracking table:

| Task | Title | Complexity | Est. Time | Depends On | Status |
|------|-------|------------|-----------|------------|--------|
| 1 | ... | S | 30 min | — | Not Started |
| 2 | ... | M | 2h | 1 | Not Started |

Followed by:

- `**Overall Progress**: 0/N tasks completed (0%)`
- `**Last Updated**: {YYYY-MM-DD}`
- One line on parallelism if relevant: `**Parallelizable**: Tasks 2 and 3 after Task 1.`

### 3. Implementation order (only when non-obvious)

Include a short ASCII dependency graph or numbered ordering only if the overview table doesn't make the order self-evident. Otherwise delete this section.

### 4. Detailed tasks

For every task, follow this template exactly:

```markdown
### Task N — {Title}

**Description**: {Clear, 1–3 sentence description of what needs to be done and why it's its own task.}

**Complexity**: S / M / L
**Estimated time**: {X h / X min}
**Depends on**: None / Task X, Y
**Can run in parallel with**: Task X, Y / None

#### Files involved

- `path/to/file1.ext` (modify / create / delete)
- `path/to/file2.ext` (modify)

#### Implementation steps

1. Step 1 — specific, with `file:line` refs where relevant.
2. Step 2 — include short code snippets for non-trivial edits; no placeholder `[NewThing]` — use the actual names from the techspec.
3. ...

#### Testing requirements

- [ ] Unit test: {specific name / assertion}
- [ ] Integration test: {specific name / assertion}
- [ ] Manual verification: {what to check}

(If this task is pure tests, this section lists the test scenarios. If tests live in a later task, write "Tests covered in Task X" and skip the checkboxes.)

#### Acceptance criteria

- [ ] {Criterion 1 — observable outcome, not a restatement of the step}
- [ ] {Criterion 2}
- [ ] Tests pass
- [ ] File(s) compile / project builds

#### Reference

- Techspec §X.Y
- Precedents: `path/to/similar.ext:line`

**Status**: Not Started
```

Rules for the task body:

- **Steps reference the techspec**, they do not re-derive it. "Add `X` per techspec §4.3" is correct; re-explaining *why* X is the right design is not.
- **Code snippets stay small.** One-liner changes — show the line before and the line after. Larger snippets — keep to ~15 lines and only when the step is genuinely non-obvious from prose + techspec ref.
- **Acceptance criteria are outcomes**, not restatements of steps. Bad: "Add property X." Good: "Property X is set by the mapper when the source field is non-null."
- **No invented files.** Every `path/to/file` must come from the techspec or from a `file:line` you have actually verified.

### 5. Notes & decisions

A running log. Keep at least one seed bullet explaining the approach choice; expect the developer to append during execution:

```markdown
## Notes & decisions

- {YYYY-MM-DD}: Tasks document created — balanced approach (N tasks).
- {YYYY-MM-DD}: {Seed note explaining any non-obvious sequencing choice, e.g. "Tests split across Task 4 (unit) and Task 5 (integration) so unit feedback lands before the DB-dependent suite."}
```

### 6. Confidence score

Follow the user's global CLAUDE.md format exactly:

```
Confidence score: <N>% — <one-line summary of why N>
```

Followed by:

- **Why <N>%:** 3–5 bullets naming concrete evidence (techspec sections mapped 1:1, file paths verified, dependencies understood, patterns reused).
- **<100-N>% uncertainty:** 2–4 bullets naming specific unknowns, each with an impact note (does it block starting any task? which task does it affect?).

Target ≥ 95% for ship-ready; ≥ 90% to proceed at all.

## Optional sections

Include each only when it adds substance. Do not include an empty or placeholder version — delete the heading if there is nothing to say.

- **Dependency graph** — include when the prose "Depends on" columns don't convey the shape at a glance (e.g. two parallel tracks converging on a shared integration task). A small ASCII graph is enough.
- **Deployment sequencing** — include when deploy order matters across repos / services (migration before code, NuGet publish before consumer deploy, feature flag enable after code lands, two-repo rollout, etc.).
- **Rollback plan** — include when tasks produce effects that aren't safe to revert via a single PR revert (DB migration with data, message published to a queue, external state change).
- **Definition of Done** — include for features that touch multiple repos or have a specific "ship checklist" beyond per-task acceptance criteria.
- **Risks** — include for specific task-level risks the acceptance criteria don't already cover (e.g. "Task 6: EF Core `GroupBy + Count(predicate)` may not translate to SQL — fallback is `FromSqlRaw`").

## Do not include

These sections appear in generic tasks templates but are absent from tasks docs that have shipped. Omit unless you have real substance:

- Generic "Task Complexity Guidelines" recap — the overview table's Complexity column is enough; do not duplicate the S/M/L definitions in every doc.
- Generic "Common Task Categories" recap (Setup / Backend / Frontend / Testing / Documentation / Polish) — use these categories mentally while you decompose, but don't echo them into the output doc.
- "Architecture Decisions" table copying the techspec. Link to the techspec instead.
- Per-task `**Started**:` / `**Completed**:` empty timestamp placeholders in every task — the Status line is enough; developers fill dates in the Notes & Decisions log.
- Placeholder "TBD" scenarios in the testing section — if you can't name a scenario, either it doesn't exist (say so) or your confidence is too low and you should not be writing the doc yet.
- Separate "Documentation Needs" checklists — surface doc updates as their own task if real; otherwise skip.

**Rule:** if a section has no substance, delete it — don't leave a placeholder.

## Output guidance

- **Map 1:1 to the techspec.** Every implementation step should be traceable to a techspec section or a verified code reference. If you add something the techspec doesn't cover, call it out in Notes & Decisions and explain why.
- **Be specific.** Actual file paths, actual function names, actual `file:line` refs. No "somewhere in the cart layer."
- **Size consistently.** Don't mix 30-minute line-edit tasks with 8-hour infra builds in the same doc without a reason. If the feature genuinely needs that range, group the tiny ones together.
- **Write for execution one task at a time.** Each task must be startable in isolation given its declared dependencies — no hidden "you also need to have done X" assumptions buried in the implementation steps.
- **Preserve PR discipline.** If two tasks should land as separate PRs for bisectability or revertability, say so in the Notes section. If multiple tasks should land together, say that too.
- **Delete, don't placeholder.** If a section in the required list truly doesn't apply (e.g. a tasks doc with no cross-task dependencies genuinely has nothing to put in "Implementation order"), write one sentence explaining why that section is empty rather than leaving TODO-style filler.

## Output file

Write the tasks document to a new file alongside the feature description, integration analysis, and techspec, using the same base name: `{feature_name}_tasks.md`. If no base name is discoverable from the inputs, ask the user for one before writing.
