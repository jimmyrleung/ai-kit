---
name: qa-gates
description: "Verify an implementation against its spec — 5 pass/fail gates (build/test, AC checklist, cross-cutting invariants, docs consistency, human go/no-go). Each gate is a tool call with a recorded pass or a specific failure; skipping a gate is visibly missing in the artifact, not hidden in chat. Use to verify, validate, or QA a finished implementation, after every task for a prefix is implemented. Accepts a loose target: a prefix, a doc path, or a short description — it resolves the rest. Per-task version: verify-task (same gates, narrower inputs)."
---

<!-- intentionally-long: documents all 5 gates verbatim — each gate is a procedural primitive the agent must execute exactly. Tier 2.4 spec explicitly chose inline-verbatim over reference-loaded gates because the gate bodies are short and load-once on entry. -->

# QA Gates — implementation verification

You verify an implementation against its spec by running 5 gates in order, each producing a
pass or a specific failure; the artifact is a `## QA` section in the review/QA doc the prefix
owns. You do NOT review code (the `review-implementation` skill runs *before* you); you verify *outcome*.

## Inputs

Accepts a loose target: a prefix (`auth_oauth_feature`), a doc path, or a short description
("QA the oauth work"). Resolve it to `prefix` + `artifact_path` (the review/QA doc the prefix
owns — derive from the `{prefix}_*.md` siblings), echo the resolution back, and proceed; ask
only when the target is genuinely ambiguous (two prefixes match, or none does).

Composed callers (e.g. `verify-task`) pass explicit `prefix` / `artifact_path` and override these defaults:

| Input | Default | Notes |
|---|---|---|
| `gates_to_run` | `all` | Subset for partial checks (`verify-task`: `build,ac,cross-cutting`). |
| `mode` | `full` | `streamlined` skips the docs gate (P1-incident fast path). |
| `confidence_gate` | `90` | Per-gate min confidence to count as pass without review. |
| `gate_plan_pre_written` | `false` | `true` = caller already wrote the gate-plan block with its own header (e.g. `verify-task`'s `## Verify — {date}` + 3-line plan). Gate 0 then skips the header / plan write but still appends gate-result lines under the existing plan. |
| `next_step` | `Declare done — merge / hand back` | Where to hand back when all gates pass. |

## Artifact convention

Append a `## QA` section to `artifact_path` (in place — no new file; same `review-artifact`
`## Review` convention). One date-stamped block per run; each gate is one line. Stamp the
`## QA — {date}` header with the tree it verified: `(verified at: <short-sha>[ +dirty])` — an
unhashed gate result can silently outlive the tree it tested (a later stash/rework broke the
build while the QA block still asserted green). **Commit lifecycle (prefix-close):** gates run
on the tree as-is — a commit is NOT required first (the user reviews before committing; the
`+dirty` stamp protects the block). Gate 1 records committed-state informationally; a dirty
tree at Gate 5 yields `GO, conditional on commit`, with the QA-artifact commit batched
alongside the implementation commit after the user's final review.

## Procedure

### Gate 0 — Setup (free)

Inspect the source doc(s) at `{prefix}_*.md` (techspec, tasks, analysis, audit, investigation —
whichever exist). Extract:

- the acceptance criteria list (from tasks/techspec)
- any line-count / size budgets the spec pinned
- the SDK / framework versions the spec pins
- the files the implementation was supposed to touch (from analysis / tasks)
- the test commands the techspec specifies

**Then derive gate scope from the working tree, not only the spec:** run `git status --short` +
`git diff --stat <base>..HEAD` (and `git status` for untracked files) and diff the file list against
the docs' claims. Anything in the tree the tasks doc never named (an untracked secret, a stray
config) becomes a Gate 3 line-item; any **migration / seed / fixture / stored-proc file in the
diff** forces Gate 1's executed-run branch **even if the techspec's test commands don't mention
it** — the 2026-07-16 seed failure shipped prod-wrong values precisely because gate scope came
from the techspec alone.

**Prefix-close only — prior-review check.** Look for a `## Review — {date}` block (from
the `review-implementation` skill) whose `(reviewed at: <sha>[ +dirty])` stamp covers the current tree
(same sha; a dirty delta consisting only of doc/QA bookkeeping still counts). Covered → record
the pointer (`Pre-work — code review: covered by ## Review — {date} (reviewed at <sha>)`) and
let its open `follow-up` findings surface at Gate 5. Not covered → suggest running
the `review-implementation` skill first; if the user proceeds anyway, Gate 5 records `go-with-caveat:
unreviewed`. Never run a reviewer fan-out here — review is the `review-implementation` skill's job.

**Prefix-close only — lifecycle classification.** For manual / rehearsal / cutover /
deployment tasks that cannot be code-complete, classify each by lifecycle boundary
(`pre-merge` / `deploy` / `live`) from the tasks doc's labels (tasks-breakdown emits
them); ask the owner only when unstated. Repository gates judge repository scope;
`live`-boundary items surface at Gate 5 as named pending items — never as failed
ancestor ACs (a prefix run stalled reading a release-owner rehearsal as a failed AC).

**If `gate_plan_pre_written: true`**: the caller (e.g. `verify-task`) has already written the
gate-plan block (with its own header — `## Verify — {date}` for per-task callers) at
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

Run the build + test commands the techspec specifies (default: `npm run build && npm test`
or the repo equivalent — `pytest`, `terraform fmt && terraform validate`, …). **Halt on
non-zero exit.** Record one of THREE outcomes — never substitute one for another:

```
- [x] Gate 1 — build/test: pass (commands: `…`)   ← only when the command ACTUALLY RAN with exit 0
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
Gate-1 pass on its own — the new/affected tests (or the migration/seed) must have **actually run
against a real target** (a scratch/Testcontainers DB, a live integration), because teardown order,
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
commit *ahead of the base branch* (`git diff --stat <base>..HEAD` / `git log -S`) or only in the
working tree. Record one of:

```
- [x] Gate 1 — committed: yes (N files ahead of <base>)
- [~] Gate 1 — committed: no (working tree only, verified at <sha>+dirty — pending user final review + commit)
```

Uncommitted work is the user's normal review-then-commit flow, **not a no-go** — never fail a
gate on it; the "authored but never shipped" safeguard lives in Gate 5's conditional GO + the
`+dirty` stamp.

### Gate 2 — AC checklist (per-AC sub-gates)

For each AC line extracted in Gate 0:

- **Testable AC** — point at the test that proves it; pass = test exists and passed in Gate 1.
- **Code-level AC** ("uses the existing auth middleware", "no new database index") — run a
  targeted text search / file inspection; record file:line evidence.
- **Manual AC** (UI behaviour, copy, animation) — ask the user; record their confirm.

Record one line per AC:

```
- [x] AC #1 — "logout button visible on /account" — pass (test: tests/account.test.ts:42)
- [ ] AC #4 — "techspec total ≤ 150 lines" — FAIL: actual 164 (file:line)
```

### Gate 3 — Cross-cutting invariants

The three loaded instruction-layer "Verification before completion" checks; each is one structured tool call.

**3a — env asymmetry.** For repos with multiple environments (Terraform `dev/test/staging/prod`,
`.env.{env}` files), inspect all env files in parallel; diff structurally. Any key present in
one without a `# deliberate-asymmetry: <reason>` comment in the others → FAIL.

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
- if the prefix has a `tasks.md`, are all tasks marked Done?

Failures here are usually stale docs — update them (the loaded instruction-layer "Spec & doc updates"
rule); **propose the diff and let the user approve**, never silently rewrite. If
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

If no `## Review` block (review-implementation) covers the verified tree, record **go-with-caveat:
unreviewed** naming the missing review — a gates-green tree later grew two HIGH-severity review findings.

The LLM doesn't decide go; the user does, with the gate report in front of them.

## Observation write

Append gate observations to the session-scoped buffer so the `close` skill picks them up at session end
(Tier 1.3 contract, `~/.claude/observations/{YYYY-MM-DD}-{slug}.md`). Use the canonical schema
from `~/.claude/observations/README.md` — numbered `### Observation N:` headings with the
standard fields (project, skill_or_workflow: qa-gates, phase/area: gate-{id}, outcome,
friction_observed + tag, would_have_helped, improvement_suggestion, principle); never bare
key-value blocks (a run that did produced a two-schema file). Batch: a clean run can be one
observation listing the gate outcomes; each fail/accepted gate gets its own.

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
  the `review-implementation` skill (batched, before gates; Gate 0 checks for its stamp).

## Composition

- **`verify-task`** — same gates, narrower inputs (one task's ACs / files / budgets);
  `gates_to_run: build,ac,cross-cutting`; skips docs + human go/no-go.
- **`close`** — picks up the observation entries; `improve` clusters gate-fails by `gate-id`
  (mechanical clustering, not inference from prose).
