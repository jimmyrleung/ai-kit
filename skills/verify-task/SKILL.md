---
name: verify-task
description: "Verifies one just-implemented task or reviewed bug fix before it is marked Done: build/tests, its acceptance criteria, and cross-cutting invariants. Used by implement-task with a task ID and tasks-doc path, or bug ID and investigation path for a fix without tasks. Whole-prefix QA, docs consistency, and human go/no-go belong to qa-gates; code review to review-implementation."
---

# Verify Task — per-task closeout

Apply the [confidence contract](references/shared/confidence.md) using the delivery rubric.
Record the effective policy and explicit score, evidence, uncertainty consequences, next
checks and advancement verdict; pass the policy to workers and downstream gates.

You verify that a single just-implemented task passes the per-task gates before the calling
implement command marks it Done. You do NOT review code quality (the review-implementation skill's
batched per-prefix review handles that); you verify the *outcome of this task only*.

Apply the [engineering change contract](references/shared/engineering-change.md):
inspect repository context, reuse suitable code/tests, and justify new files within scope.
Resolve bundled references relative to this skill folder.

Follow [authorized work](references/shared/authorized-work.md) for existing permission,
blocking questions, and requested discussion cadence; resolve from this skill folder.

## Inputs the caller must provide (in the invoking message)

| Input            | Required | Example                                       | Notes                                                                          |
|------------------|----------|-----------------------------------------------|--------------------------------------------------------------------------------|
| `task_id`        | yes      | `Task 3` / `auth-oauth-impl-3` / `BUG-123`     | The task identifier, or the bug ID for a tasks-doc-less fix.                    |
| `tasks_doc_path` | yes      | `specs/slices/auth/tasks.md`                  | The tasks doc, or the reviewed investigation path for a tasks-doc-less fix.     |
| `prefix`         | no       | `auth_oauth_feature` / `specs/slices/auth`    | Derived from `tasks_doc_path` if not given; passed to `qa-gates`.              |
| `artifact_path`  | no       | (default = `tasks_doc_path`)                  | Where the nested Verify block goes. Defaults to the task's section in tasks-doc. |

Accept the caller's `confidence_policy` and assessment. If absent, resolve the confidence
contract defaults and applicable task/spec/investigation policy; do not depend on private
instructions. Reassess the delivery rubric against this task's actual evidence.

If `task_id` or `tasks_doc_path` is missing, ask the caller (or the user) for it before starting.

## Artifact convention

Follow the [change evidence contract](references/shared/change-evidence.md). Append a
uniquely identified, delimited Verify block inside the resolved task boundary; its heading
is one level below the task heading (for example `#### Verify` under `### Task`). Numbered
tasks use only the delimited block; fixes may use a top-level section. Preserve earlier runs.
Store authoritative input locators and content/dependency identity with every run.

## Procedure

### Step 0 — Resolve per-task inputs and write the gate plan

1. Inspect `tasks_doc_path`; resolve `task_id` and an exact `task_locator` under the change
   evidence contract, including its tasks-doc-less fix mapping when applicable.
2. **Extract the exact AC set** only from the designated Acceptance criteria section or
   resolved legacy AC range. For a tasks-doc-less fix, use the contract's expected-behavior
   and designated fix-AC mapping instead; deduplicate repeated obligations while retaining
   every source locator. Record `ac_source` and stable IDs/text; exclude prior Verify
   records, testing checkboxes, and neighboring tasks. Missing or ambiguous ACs require
   resolution, never a best-effort prefix fallback. Record any task Baseline with its
   evidence; a named baseline failure is context, not automatic acceptance of a failure.
3. **Resolve the change boundary.** Record explicit `base`, `declared_files` from the task's
   Files section, and `observed_changes` across all four layers. Record exclusions and
   resolve ownership of unexpected relevant changes; never use a fixed commit window.
4. **Extract per-task line budgets.** read the techspec at `{prefix}_techspec.md` (or
   `specs/slices/<slice>/the techspec file` for slice-style prefixes) and grep for any budget lines
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
   A running host that locks build outputs (a Web/worker process holding the old
   assembly) is the same failure: stop it, rebuild, restart before the suite — and
   prefer durable TRX/JUnit output so the stop/start cycle can't orphan the verdict.
7. **Browser preflight.** Before UI-heavy verification: check a browser backend is available
   and identify any AC whose probe is destructive (needs fresh human approval). Unavailable →
   record the affected ACs `BLOCKED` and halt Gate 2 per discipline (do NOT fall back to
   spawning a dev server ad hoc — a direct `next dev` fallback caused a worker-process runaway).
7b. **Config-readiness assertion.** After scripted config/connection setup and before
    the suite, run one non-secret readiness assertion (value present / non-empty) — a
    non-terminating setup failure left an empty connection string and masked 56 test
    failures as app HTTP 500s. A `bash -n`/script failure showing `$'…\r'` is a
    line-ending (CRLF) problem — classify that before debugging logic.
8. **Write the delimited Verify plan** inside the resolved task boundary, with the
   appropriate nested heading and `record_id`. Include the explicit input bundle, then
   checkboxes for Gate 1 build/test, Gate 2 AC checklist (count from the exact AC set), and
   Gate 3 cross-cutting. This skill owns the block; QA appends only within that record.

### Step 1 — Invoke `qa-gates` with per-task scope

Use the `qa-gates` skill with:

- `scope_kind`: `task`
- `task_id`, `task_locator`, `ac_source`, `acceptance_criteria`: the resolved task and exact source AC set
- `base`, `declared_files`, `observed_changes`, `budgets`, `test_commands`, `dependencies`: the resolved scope bundle
- `record_id`: this run's delimited evidence block
- `check_evidence`: any prior executed checks; validate identities/scope per change evidence before reuse
- `prefix`: $prefix
- `gates_to_run`: `build,ac,cross-cutting`
- `mode`: `full`
- `confidence_policy`: complete effective policy, assessment and unresolved consequences
- `confidence_gate`: effective numeric threshold, preserving stricter user-required gates
- `artifact_path`: $artifact_path  ← (the task's section in `tasks_doc_path`)
- `gate_plan_pre_written`: `true`  ← (tells `qa-gates`' Gate 0 to skip the header / plan
  write but still append gate-result lines under the existing delimited Verify plan)
- `next_step`: `continue to Workflow 3 — Post implementation in the calling implement command`

`qa-gates` runs gates 1 + 2 + 3 against the per-task ACs / files / budgets listed in the
delimited Verify block this skill wrote in Step 0, and appends one gate-result line under
each checkbox.

### Step 2 — Halt / acceptance discipline (inherited from `qa-gates`)

- **Halt on fail.** Do not advance to the next gate while the current one is unresolved.
  The calling implement command must NOT mark the task Done while any gate is failing.
- **Accept-with-reason** is the only escape. The delimited Verify block must carry the reason
  inline (`accepted: <reason>`); the improve skill audits per-task accept-rates later.
- **Skipping a gate is visible.** The 3-checkbox plan from Step 0 makes any unrecorded gate
  a missing checkbox, not a silent omission.
- **Numbers are verbatim, filled after the run.** Suite results are recorded as
  `ProjectName N/N` copied from the runner's summary line — never a positional count, never a
  number inherited from the tasks-doc or typed before the command ran (a pre-filled "13x
  green" met a file with 10 tests; a positional "54" matched the wrong project).

## Observation handoff

Use the [feedback contract](references/shared/feedback.md) to resolve the configured
recorder/store; recording is optional and never requires a private home layout. With no
configured recorder, report `disabled` and continue the main workflow without a feedback write.
If recording is an enabled acceptance gate, unavailable storage or failed validation stays
`unavailable`/`failed`, never PASS.

Return supported observation candidates to the one recorder for this `execution_id`; nested
calls do not write duplicates. A standalone run may be its own recorder. Use the common envelope
and observation schema: `skill_or_workflow: verify-task`, `phase_area`, the schema's outcome values,
`evidence_kind`, subject/task identity, and actual evidence/locators. Gate verdicts remain in the
verification artifact; they are not silently substituted for observation outcome enum values.
Emit only supported findings, with one approved tag each; no fixed number of entries per run.
The recorder validates and deduplicates by execution plus evidence/subject before any receipt.
Do not treat observation counts as invocation telemetry.

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
  resolves per-task inputs, writes the nested Verify plan, and calls `qa-gates` with
  `gates_to_run: build,ac,cross-cutting` and `gate_plan_pre_written: true`.
- **The configured recorder / close skill** — persists validated, deduplicated observation
  candidates using execution, evidence and task identity; observation counts are not invocations.
- **The `implement-task` skill** — the sole caller (its fix lens covers bug fixes; the
  loop variant reviews at checkpoints instead); it invokes `verify-task` at
  end-of-Workflow-1 before continuing to Workflow 3 — Post implementation. The post-2.4 last-task qa-gates suggest
  hint at end-of-Workflow-3 is unrelated and untouched — the two skills compose.
