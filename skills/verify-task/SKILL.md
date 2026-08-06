---
name: verify-task
description: "Per-task implementation verification — composes the qa-gates skill with per-task inputs (one task's ACs, one task's files, one task's budgets) and runs gates 1 (build/test) + 2 (AC checklist) + 3 (cross-cutting invariants). Skips gates 4 (docs) and 5 (human go/no-go) — those are prefix-level concerns. Invoked at end-of-Workflow-1 inside the implement-task skill (tasks-doc tasks and fix-lens bug fixes alike), before the task is marked Done. Records a `## Verify — {date}` block in the task's section of the tasks-doc and logs 3 observations per run for /close → /improve. Per-prefix sibling: qa-gates (Tier 2.4)."
---

# Verify Task — per-task closeout

You verify that a single just-implemented task passes the per-task gates before the calling
implement command marks it Done. You do NOT review code quality (`/review-implementation`'s
batched per-prefix review handles that); you verify the *outcome of this task only*.

## Inputs the caller must provide (in the invoking message)

| Input            | Required | Example                                       | Notes                                                                          |
|------------------|----------|-----------------------------------------------|--------------------------------------------------------------------------------|
| `task_id`        | yes      | `Task 3` / `auth-oauth-impl-3`                | The task identifier as it appears in the tasks-doc.                            |
| `tasks_doc_path` | yes      | `specs/slices/auth/tasks.md`                  | The tasks-doc to read the task's section from.                                 |
| `prefix`         | no       | `auth_oauth_feature` / `specs/slices/auth`    | Derived from `tasks_doc_path` if not given; passed to `qa-gates`.              |
| `artifact_path`  | no       | (default = `tasks_doc_path`)                  | Where the `## Verify` block goes. Defaults to the task's section in tasks-doc. |

If `task_id` or `tasks_doc_path` is missing, ask the caller (or the user) for it before starting.

## Artifact convention

Append a `## Verify — {date}` block to `artifact_path` **inside the task's section** (not at
the bottom of the tasks-doc). One block per task per run; appended-only — never overwrite an
earlier run's block. Three checkboxes (one per gate), one line per AC sub-gate, one line per
cross-cutting sub-check. Same in-place marker discipline `review-artifact` (`## Review`) and
`qa-gates` (`## QA`) use, one scope tighter.

## Procedure

### Step 0 — Resolve per-task inputs and write the gate plan

1. `Read` `tasks_doc_path` and locate the task's section (matching `task_id` — usually a
   heading like `### Task 3: …` or a numbered checklist item).
2. **Extract per-task ACs.** From the task's section, collect any line that looks like an AC
   — bullets under an "Acceptance criteria" subsection (the post-2.2 tasks-doc template),
   checklist boxes (`- [ ]` style), lines containing `AC:` or matching `✅`/`☑`. If no ACs
   found in the task's section, fall back to the techspec's ACs filtered to mentions of this
   task (best-effort) and record a `warning: no per-task ACs in tasks-doc — used techspec
   fallback` line in the gate plan. Also extract the task's `Baseline:` completion-note line if
   present and record it in the gate plan — Gate 1's result is judged against it (a failure the
   baseline names is pre-existing; one it doesn't name is this task's).
3. **Extract per-task files-list.** Collect any file-path strings in the task's section
   ("Files: …", "Touches: …", visible paths). Also run `Bash` `git diff --name-only HEAD~3..HEAD`
   (widen the window if needed) to get the just-edited file set. **Union** the two lists;
   record both in the gate plan so a divergence is visible.
4. **Extract per-task line budgets.** `Read` the techspec at `{prefix}_techspec.md` (or
   `specs/slices/<slice>/techspec.md` for slice-style prefixes) and grep for any budget lines
   attached to files in the per-task files-list. Record budgets found; "no budget pinned
   (acceptable)" if none. Treat unlabeled `~`/approximate sizes as **forecasts**: record
   actual-vs-forecast as variance in the Verify block, never as a Gate 3 FAIL; only explicit
   hard caps fail the gate. For shared cumulative files, judge this task's **delta** against
   its stated share, and the total only against the final-slice ceiling. Where an AC demands
   source fidelity (a full-file port), fidelity governs — pair the size check with a
   content-level comparison (e.g. declaration count) before flagging.
5. **Behavior-pinning sweep.** For a task that *changes* behavior (not pure addition), grep
   the test tree for suites asserting the OLD behavior of the changed symbols/routes; add
   every hit to Gate 1's scope. Suites that only run in CI (integration fixtures needing new
   config keys, DI registrations, NOT NULL columns) are in scope: run them if runnable, else
   record Gate 1 `BLOCKED` naming the suite — never silently out of scope.
6. **Evidence-source freshness.** Live/browser/DB evidence counts only if the serving process
   provably runs the current build: restart it or prove watch-reload picked the change up (a
   stale `next start` and a stale non-watch server both produced convincing wrong evidence).
   Probe from the *calling* side (the host, not inside the container) — a probe on the wrong
   side of the boundary "verified" a DB 36/50 tests couldn't reach.
7. **Browser preflight.** Before UI-heavy verification: check a browser backend is available
   and identify any AC whose probe is destructive (needs fresh human approval). Unavailable →
   record the affected ACs `BLOCKED` and halt Gate 2 per discipline (do NOT fall back to
   spawning a dev server ad hoc — a direct `next dev` fallback caused a worker-process runaway).
8. **Write the `## Verify — {date}` block** to `artifact_path` inside the task's section:

   ```
   ## Verify — {date}
   - [ ] Gate 1 — build/test
   - [ ] Gate 2 — AC checklist (N items)
   - [ ] Gate 3 — cross-cutting (line budgets + SDK version for this task's files)
   ```

   This skill — not `qa-gates` — owns the `## Verify` header. The header stays `## Verify`;
   `qa-gates` will never write its own `## QA` header for this call (see Step 1's
   `gate_plan_pre_written: true` input).

### Step 1 — Invoke `qa-gates` with per-task scope

Use the `qa-gates` skill with:

- `prefix`: $prefix
- `gates_to_run`: `build,ac,cross-cutting`
- `mode`: `full`
- `confidence_gate`: `90`
- `artifact_path`: $artifact_path  ← (the task's section in `tasks_doc_path`)
- `gate_plan_pre_written`: `true`  ← (tells `qa-gates`' Gate 0 to skip the header / plan
  write but still append gate-result lines under the existing `## Verify — {date}` plan)
- `next_step`: `continue to Workflow 3 — Post implementation in the calling implement command`

`qa-gates` runs gates 1 + 2 + 3 against the per-task ACs / files / budgets listed in the
`## Verify — {date}` block this skill wrote in Step 0, and appends one gate-result line under
each checkbox.

### Step 2 — Halt / acceptance discipline (inherited from `qa-gates`)

- **Halt on fail.** Do not advance to the next gate while the current one is unresolved.
  The calling implement command must NOT mark the task Done while any gate is failing.
- **Accept-with-reason** is the only escape. The `## Verify` block must carry the reason
  inline (`accepted: <reason>`); `/improve` audits per-task accept-rates later.
- **Skipping a gate is visible.** The 3-checkbox plan from Step 0 makes any unrecorded gate
  a missing checkbox, not a silent omission.
- **Numbers are verbatim, filled after the run.** Suite results are recorded as
  `ProjectName N/N` copied from the runner's summary line — never a positional count, never a
  number inherited from the tasks-doc or typed before the command ran (a pre-filled "13x
  green" met a file with 10 tests; a positional "54" matched the wrong project).

## Observation write

For each of the 3 gates ran, append one entry to the session-scoped observation buffer so
`/close` picks it up (Tier 1.3 contract):

```
skill_or_workflow: verify-task
phase/area: gate-{id} ({name})
task_id: $task_id          ← (added on top of qa-gates' contract)
prefix: $prefix
outcome: pass | fail | accepted
friction_observed: <tag if fail/accepted> — e.g. line_budget_overrun, sdk_version_drift, ac_drift, env_asymmetry
would_have_helped: <if fail/accepted>
principle: <generalizable takeaway>
```

3 entries per run. The `task_id` field is the per-task-clustering hook for `/improve`.

## When NOT to use verify-task

- The task is a one-line config tweak / typo / formatting-only edit — gates are friction in
  front of trivial work.
- The task is a doc-only edit (no code touched) — there's no build/test gate to run; the
  prefix-level `qa-gates` Gate 4 (docs consistency) covers doc work.
- The task is itself a verification / QA task (running `verify-task` on a verify-step is silly).

In all three cases, the calling implement command can skip the skill call and continue to
Workflow 3 — Post implementation directly.

## Composition

- **`qa-gates` (Tier 2.4)** — the gate-body provider. `verify-task` is a thin wrapper that
  resolves per-task inputs, writes the `## Verify` plan, and calls `qa-gates` with
  `gates_to_run: build,ac,cross-cutting` and `gate_plan_pre_written: true`.
- **`/close`** — picks up the 3 per-task observation entries per run; `/improve` clusters
  per-task gate-fails by `gate-id` AND `task_id` (mechanical clustering).
- **The `implement-task` skill** — the sole caller (its fix lens covers bug fixes; the
  loop variant reviews at checkpoints instead); it invokes `verify-task` at
  end-of-Workflow-1 before continuing to Workflow 3 — Post implementation. The post-2.4 last-task `/qa-gates` suggest
  hint at end-of-Workflow-3 is unrelated and untouched — the two skills compose.
