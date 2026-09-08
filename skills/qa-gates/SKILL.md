---
name: qa-gates
description: "Verifies a finished implementation against its spec, including build/tests, acceptance criteria, invariants, docs consistency, and human go/no-go. Use to verify, validate, or QA a completed feature/refactor or all repository tasks for a prefix. Accepts a prefix, doc path, or short description. One-task verification belongs to verify-task; code-quality review to review-implementation."
---

<!-- intentionally-long: documents all 5 gates verbatim — each gate is a procedural primitive the agent must execute exactly. Tier 2.4 spec explicitly chose inline-verbatim over reference-loaded gates because the gate bodies are short and load-once on entry. -->

# QA Gates — implementation verification

Apply the [confidence contract](references/shared/confidence.md) using the delivery rubric.
Record the effective policy and explicit score, evidence, uncertainty consequences, next
checks and advancement verdict; pass the policy to workers and downstream gates.

You verify an implementation against its spec by running 5 gates in order, each producing a
pass or a specific failure; the artifact is a `## QA` section in the review/QA doc the prefix
owns. You do NOT review code (the `review-implementation` skill runs *before* you); you verify *outcome*.

Apply the [engineering change contract](references/shared/engineering-change.md):
inspect repository context, reuse suitable code/tests, and justify new files within scope.
Resolve bundled references relative to this skill folder.

Follow [authorized work](references/shared/authorized-work.md) for existing permission,
blocking questions, and requested discussion cadence; resolve from this skill folder.

## Inputs

Accepts a loose target: a prefix (`auth_oauth_feature`), a doc path, or a short description
("QA the oauth work"). Resolve it to `prefix` + `artifact_path` (the review/QA doc the prefix
owns — derive from the `{prefix}_*.md` siblings), echo the resolution back, and proceed; ask
only when the target is genuinely ambiguous (two prefixes match, or none does).

Follow the [change evidence contract](references/shared/change-evidence.md). Composed
callers pass `scope_kind: task`, `task_id`, `task_locator`, `ac_source`, exact
`acceptance_criteria`, `base`, `declared_files`, `observed_changes`, `budgets`, `test_commands`,
`dependencies`, `record_id`, `prefix`, and `artifact_path`. These are authoritative: do not
re-extract prefix ACs or widen task scope. Direct prefix calls use `scope_kind: prefix` and
derive an explicit prefix bundle. Missing relevant coverage is a gap to resolve explicitly.
Prior `check_evidence` is optional and follows the change evidence reuse contract.
Other defaults:

| Input | Default | Notes |
|---|---|---|
| `gates_to_run` | `all` | Subset for partial checks (`verify-task`: `build,ac,cross-cutting`). |
| `mode` | effective policy depth; normally `full` | Inherited active-P1 `streamlined` depth skips the docs gate. Preserve any explicit requirement for fuller coverage. |
| `confidence_policy` | confidence contract defaults | Full effective rubric, threshold, source, required evidence and authorization boundary; preserve the caller's incident policy and stricter gates. |
| `confidence_gate` | effective policy threshold (normal `90`) | Legacy explicit numeric minimum; combine with applicable stricter requirements. A score alone never makes a gate pass. |
| `gate_plan_pre_written` | `false` | `true` = caller already wrote the gate-plan block with its own header (e.g. `verify-task`'s nested Verify heading + 3-line plan). Gate 0 then skips the header / plan write but still appends gate-result lines under the existing plan. |
| `next_step` | `Declare done — merge / hand back` | Where to hand back when all gates pass. |

## Artifact convention

Append a dated, delimited `## QA` section to `artifact_path` using the change evidence
record. A composed task call writes into its caller's existing nested record instead.
Stamp scoped content and relevant dependency identities; SHA/dirty is informational only.
Run on the tree as-is: no commit is required before review. User GO on an uncommitted tree
is conditional on the reviewed content being committed; it does not authorize deployment.

## Procedure

### Gate 0 — Setup (free)

Resolve and record the effective confidence policy before evaluating gates. Calculate the
QA mode from its inherited pass depth: normal work uses `full`; an active P1 with declared
streamlined depth uses `streamlined`, unless applicable instructions or an explicit caller
require fuller coverage. Record the resolved mode; passing the policy alone must preserve
its depth without requiring a duplicate `mode` input. Calculate the
delivery rubric for the scoped evidence and record each selected gate's score/reason when
its evidence differs. Apply the contract's threshold and evidence checks separately:
a green command remains observed green, but below-threshold confidence blocks advancement;
an unrun required check remains BLOCKED at any score. Preserve actual human GO at Gate 5.

For direct prefix calls, inspect the source doc(s) at `{prefix}_*.md` (techspec, tasks, analysis, audit, investigation —
whichever exist). Extract:

- the acceptance criteria list (from tasks/techspec)
- any line-count / size budgets the spec pinned
- the SDK / framework versions the spec pins
- the files the implementation was supposed to touch (from analysis / tasks)
- the test commands the techspec specifies

**Resolve actual scope:** use the change evidence contract's explicit base and complete
committed/staged/unstaged/untracked inspection, including renames and exclusions. Reconcile
unexpected relevant changes with the declared scope; do not mistake another task's work for
this task. Any migration / seed / fixture / stored-proc change in scope forces Gate 1's
executed-run branch even if the techspec omitted its command.

**Prefix-close only — prior-review check.** Recompute the prior code review's scoped content,
base, task coverage, and dependency identities before reuse. Only a current approved record
covering all repository work counts; SHA plus dirty state, a task-only review, or a heading
alone does not. Record its ID and follow-ups. Missing/stale/rejected/Needs revision evidence
cannot advance the chain: run `review-implementation` or obtain an explicit owner waiver
recorded as `accepted: unreviewed <scope and reason>`; never relabel the record as approved.
QA itself does not run a reviewer fan-out.

**Prefix-close only — lifecycle classification.** For manual / rehearsal / cutover /
deployment tasks that cannot be code-complete, classify each by lifecycle boundary
(`pre-merge` / `deploy` / `live`) from the tasks doc's labels (tasks-breakdown emits
them); ask the owner only when unstated. Repository gates judge repository scope;
`deploy`/`live`-boundary items surface at Gate 5 as named pending items — never as failed
ancestor ACs (a prefix run stalled reading a release-owner rehearsal as a failed AC).

**If `gate_plan_pre_written: true`**: the caller (e.g. `verify-task`) has already written the
gate-plan block (with its own header — nested Verify heading for per-task callers) at
`artifact_path`. **Skip the header / plan write below and jump to Gate 1**; gate-result
lines still append under the existing plan as normal.

Otherwise, append the gate plan as the first lines of the `## QA — {date}` section:

```
## QA — {date}
- [ ] Gate 1 — build/test
- [ ] Gate 2 — AC checklist (N items)
- [ ] Gate 3 — cross-cutting (env / line budgets / SDK version)
- [ ] Gate 4 — docs consistency
- [ ] Gate 5 — human go/no-go
```

### Gate 1 — Build & test (shell command runner)

First validate any supplied executed check evidence under the change evidence contract.
Matching complete evidence is reusable: cite its run ID, command, output, scope and identity
comparison without claiming another execution. Otherwise run the required build/test commands
from the scope bundle and repository conventions/CI. Record truly inapplicable checks with a
reason; a missing required tool/environment is BLOCKED. **Halt on non-zero exit.** Record one
of THREE execution outcomes — never substitute one for another:

```
- [x] Gate 1 — build/test: pass (commands: `…`; run: <ID>; executed here | reused with matching identities)   ← command actually ran with exit 0
```

or FAIL (executed, non-zero):

```
- [ ] Gate 1 — build/test: FAIL
  - command: `…`
  - output: <2-3 line digest of the failure>
  - resolution: <"address before re-running" / "accepted: <reason>">
```

or BLOCKED (could not execute — sandbox/permission/headless denial, missing toolchain):

```
- [ ] Gate 1 — build/test: BLOCKED
  - command: `…`
  - reason: <why it couldn't run — e.g. "sandbox denies `dotnet test`; not in the cc-loop allow-list">
  - resolution: <"run before merge" / "re-run with the allow-list added via `cc-loop init`">
```

**`pass` is reserved for an executed, green command.** "verified by inspection", "project builds"
(without the command's recorded output), or "unrunnable so assumed-passing" are NOT a pass — they
are `BLOCKED`, and a BLOCKED build/test gate keeps the task/prefix OFF "Done" until it actually runs.
"unrunnable ≠ failure" must never silently become "unverified ≡ verified."

**Compiled ≠ executed; a green subset ≠ a green suite.** When the diff touches **test code, seed /
fixture scripts, DB migrations, or DB constraints / stored procs**, a build that *compiles* is NOT a
Gate-1 pass on its own — the new/affected tests must have **actually run in their required tier**; migrations/seeds and
DB constraints/procedures require a real suitable target (for example a scratch/Testcontainers DB), because teardown order,
FK / CHECK constraints, and seed row-counts are exercised only at run time, never at compile. And
when you record green, **name the test projects / tiers that executed** — `171/171` on one tier is
not "all green" if integration / E2E tiers weren't run; a schema-touching change (seed / migration)
implicates *every* tier that migrates that schema. The pass line for these change types must cite
what ran:

    - [x] Gate 1 — build/test: pass (ran: unit + integration on Testcontainers; 884/884)

If the live/integration run can't happen here (no test DB, sandbox), that is a **BLOCKED** build/test
gate (record the reason), not a pass — "compiles, assumed green at run time" keeps the task OFF Done.

For suites expected to exceed ~2 minutes, require **durable result output** (TRX / JUnit XML +
redirected console log) so a wrapper timeout cannot orphan the verdict; when a suite passes
focused but hangs/fails full, inspect **configuration-provider precedence** (an ignored
developer-local settings file, an empty high-precedence env var) before proposing mocks or
skipping the suite.

If FAIL with `accepted`, require a `Why:` line; do not advance until the user states the reason.

**Prefix-close only — record committed-state (informational, never a FAIL).** When running at
prefix close (not per-task `verify-task`), check whether the prefix's claimed files appear in a
commit ahead of the resolved base (inspect the committed layer; absent HEAD means no
committed content) or only in the working tree. A mixture is recorded explicitly per path.
This is informational and cannot replace the complete scope inspection. Record one of:

```
- [x] Gate 1 — committed: yes (N files ahead of <base>)
- [~] Gate 1 — committed: no (working tree only, verified at <sha>+dirty — pending user final review + commit)
```

Uncommitted work is the user's normal review-then-commit flow, **not a no-go** — never fail a
gate on it; the "authored but never shipped" safeguard lives in Gate 5's conditional GO + the
content identity record.

### Gate 2 — AC checklist (per-AC sub-gates)

For each AC in the authoritative scope bundle (caller-supplied for task runs):

- **Testable AC** — point at the test that proves it; pass = test exists and passed in Gate 1.
- **Code-level AC** ("uses the existing auth middleware", "no new database index") — run a
  targeted text search / file inspection; record file:line evidence.
- **Observable UI AC** — use available browser evidence against the current build and record
  the route/action/result; unavailable required observation is BLOCKED.
- **Subjective/manual owner AC** — ask the user and record their actual confirmation.

Record one line per AC:

```
- [x] AC #1 — "logout button visible on /account" — pass (test: tests/account.test.ts:42)
- [ ] AC #4 — "techspec total ≤ 150 lines" — FAIL: actual 164 (file:line)
```

### Gate 3 — Cross-cutting invariants

Apply relevant repository/spec invariants below; each executed check records its tool evidence.

**3a — environment expectations.** Inspect the environments relevant to the changed contract
(and every environment explicitly required by repository policy/spec). Trace consumed keys and
required settings. A missing required key or unintended incompatible value → FAIL. Document
intentional differences in the established artifact, citing their requirement/reason; unrelated
differences are not failures and no special comment syntax is required.

**3b — line budgets.** For each file the techspec pinned a budget on ("techspec ≤ 150 lines",
"orchestrator stays ≤ 60 lines"), use the shell command runner for `wc -l` and compare.

**3c — SDK / framework version.** Search `package.json` / `requirements.txt` / `Gemfile.lock` /
`go.mod` for the SDK the techspec pins; confirm the version matches. No pin → note "no version
pinned (acceptable)".

**3d — release readiness (change-class dependent).** When the diff ships an API / schema /
contract change or touches auth, payments, or a hot path: **back-compat** verified
bidirectionally (enumerate consumers of the changed surface — grep, not assumed);
**rollback** documented (the techspec's rollback section exists and names its triggers);
**security implications** stated (input validation at new trust boundaries; no secrets in the
diff — the sibling of Gate 0's untracked-secret sweep). Change class doesn't apply → skip with reason.

**3e — perf/regression (repo-local).** Perf baselines and regression suites are repo-specific —
this gate never invents generic thresholds. Check for a repo-local perf/regression skill
(`.claude/skills/`, or the repo's rules index). Present → run its checks as this sub-check.
Absent while the change touches a perf-sensitive surface (hot path, DB query shape, caching,
payload size — or the techspec's test plan flags perf scenarios) → record
`skipped — no repo-local perf skill (gap flagged)` and suggest minting one at the `close` skill
(repo-local skill pair). Not perf-sensitive → "skipped — not applicable".

Record one line per sub-check; a sub-check the spec didn't anticipate → "skipped — not applicable" + a one-line reason.

### Gate 4 — Docs consistency

For each sibling doc in the prefix folder (`{prefix}_analysis.md`, `{prefix}_techspec.md`,
`{prefix}_tasks.md`, `{prefix}_investigation.md`, …), inspect and check:

- did the implementation reveal a gap the doc should record?
- are file paths / function names / API signatures in the doc consistent with what shipped?
- if the prefix has a tasks doc, are all `pre-merge` tasks Done, with `deploy`/`live` tasks
  separately visible as pending and carrying their evidence requirements?

Failures here are usually stale docs — update them (the loaded instruction-layer "Spec & doc updates"
rule) within existing authorization; explain corrections and preserve history. Ask only for
new scope or an owner decision, not routine authorized doc updates. If
`mode == streamlined` (P1 fast path; the post-mortem covers it later): skip this gate and
record `skipped (streamlined)`.

**Unchecked-box census (whole prefix, before requesting approval).** Enumerate every
unchecked checkbox in Done tasks, classify each — stale marker (proven elsewhere: cite
where) / paused live-boundary item / genuine gap — and reconcile the tasks-doc's test
totals against the latest TRX / runner summary. AC-only correction missed 4 stale
markers a later whole-prefix probe found; keep historical counts as dated snapshots.

### Gate 5 — Human go/no-go

Present the `## QA` artifact to the user. Confirm every prior gate is either `pass` or
`accepted with a recorded reason`. Ask: ship it?

- **Yes, tree committed** → record the go decision in the gate-line; hand back to `next_step`.
- **Yes, tree dirty** → record `GO, conditional on commit` — name the pending commit
  (post-final-review, batched with the QA artifact) in the gate-line; hand back to `next_step`.
- **Yes, modulo ops** → record `go-modulo-ops: <pending item>` when the code verdict is GO and
  the only open items sit outside the code's control (a prod DBA sign-off, an ops deployment
  window, an external approval). The pending item is named in the gate-line and tracked to
  closure — it is never counted as a code failure, and never silently dropped. The verdict
  states what it AUTHORIZES — merge, continued validation, or deployment — e.g.
  `GO (repository scope), conditional on commit; deployment checklist pending`; a green
  code-QA run is never fresh live-provider proof.
- **No** → ask what to address; loop the failed gate.

If code review is unverified, require the explicit owner waiver from Gate 0 and record
`go-with-caveat: unreviewed` with its scope/reason; absent that waiver, Gate 5 cannot GO.

The LLM doesn't decide go; the user does, with the gate report in front of them.

## Observation handoff

Use the [feedback contract](references/shared/feedback.md) to resolve the configured
recorder/store; recording is optional and never requires a private home layout. With no
configured recorder, report `disabled` and continue the main workflow without a feedback write.
If recording is an enabled acceptance gate, unavailable storage or failed validation stays
`unavailable`/`failed`, never PASS.

Return supported observation candidates to the one recorder for this `execution_id`; nested
calls do not write duplicates. A standalone run may be its own recorder. Use the common envelope
and observation schema: `skill_or_workflow: qa-gates`, `phase_area`, the schema's outcome values,
`evidence_kind`, subject/task identity, and actual evidence/locators. Gate verdicts remain in the
verification artifact; they are not silently substituted for observation outcome enum values.
Emit only supported findings, with one approved tag each; no fixed number of entries per run.
The recorder validates and deduplicates by execution plus evidence/subject before any receipt.
Do not treat observation counts as invocation telemetry.

## Halt / acceptance discipline

- **Halt on fail** — do not advance while the current gate is unresolved.
- **Accept-with-reason** is the only escape; the reason lives inline in the `## QA` artifact
  (the `improve` skill audits accept-rates later).
- **Skipping a gate is visible** — Gate 0's plan lists all 5; an unrecorded gate is a missing
  checkbox, not a silent omission.

## When NOT to use qa-gates

- The implementation hasn't happened yet — qa-gates verifies outcomes, not plans.
- A one-line typo / config tweak — gates are friction in front of trivial work.
- Doc reviews — that's `review-artifact` (it reviews the *doc*). Code-quality review — that's
  the `review-implementation` skill (batched, before gates; Gate 0 validates its content-bound record).

## Composition

- **`verify-task`** — same gates, narrower inputs (one task's ACs / files / budgets);
  `gates_to_run: build,ac,cross-cutting`; skips docs + human go/no-go.
- **`close`** — picks up the observation entries; `improve` clusters gate-fails by `gate-id`
  (mechanical clustering, not inference from prose).
