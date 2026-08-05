---
name: qa-gates
description: "Verify an implementation against its spec — 5 pass/fail gates (build/test, AC checklist, cross-cutting invariants, docs consistency, human go/no-go). Each gate is a tool call with a recorded pass or a specific failure; skipping a gate is visibly missing in the artifact, not hidden in chat. Use to verify, validate, or QA a finished implementation. Invoked as `/qa-gates prefix=…` (back-compat alias: `/implementation-quality-assurance`) after every task for a prefix has been implemented. Per-task version: `verify-task` (same gates, narrower inputs)."
---

<!-- intentionally-long: documents all 5 gates verbatim — each gate is a procedural primitive the agent must execute exactly. Tier 2.4 spec explicitly chose inline-verbatim over reference-loaded gates because the gate bodies are short and load-once on entry. -->

# QA Gates — implementation verification

You verify an implementation against its spec by running 5 gates in order, each producing a
pass or a specific failure. The artifact is a `## QA` section in the existing review/QA doc
the prefix already owns. You do NOT review the code (`/review-implementation`'s batched
reviewer fan-out handles that *before* you run); you verify the *outcome*.

## Inputs the caller must provide (in the invoking message)

| Input | Required | Example | Notes |
|---|---|---|---|
| `prefix` | yes | `auth_oauth_feature` | The feature/bugfix/refactor identifier. Source docs at `{prefix}_*.md`. |
| `gates_to_run` | no (default `all`) | `build,ac,cross-cutting` | Subset for partial checks (used by `verify-task`). |
| `mode` | no (default `full`) | `streamlined` | `streamlined` skips the docs gate (P1-incident fast path). |
| `confidence_gate` | no (default `90`) | `70` (P1) | Per-gate min confidence to count as pass without review. |
| `artifact_path` | no (default = derive) | `auth_oauth_feature_techspec.md` | Doc to append the `## QA` section to. Derive from prefix if not given. |
| `gate_plan_pre_written` | no (default `false`) | `true` | `true` = caller already wrote the gate-plan block (e.g. `verify-task` writes its own `## Verify — {date}` header + 3-line plan in its Step 0). Gate 0 then skips the header / plan write but still appends gate-result lines under the existing plan. |
| `next_step` | yes | `Declare done — merge / hand back to orchestrator` | Where to hand back when all gates pass. |

If a required input wasn't supplied, ask the caller (or the user) for it before starting.

## Artifact convention

Append a `## QA` section to `artifact_path` (in place — no new file). Same `review-artifact`
"`## Review`" convention. One date-stamped block per run. Each gate is one line.

Stamp the `## QA — {date}` header with the commit/tree it verified: `(verified at: <short-sha>[ +dirty])`.
A gate result without the hash can silently outlive the tree it tested (a later stash/rework broke
the build while the QA block still asserted green). **Commit lifecycle (prefix-close):** gates run
on the tree as-is — a commit is NOT required first (the user reviews before committing; the
`+dirty` stamp protects a QA block from outliving its tree). Gate 1 records committed-state
informationally; a dirty tree at Gate 5 yields `GO, conditional on commit`, with the QA-artifact
commit batched alongside the implementation commit after the user's final review.

## Procedure

### Gate 0 — Setup (free)

`Read` the source doc(s) at `{prefix}_*.md` (techspec, tasks, analysis, audit, investigation —
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

### Gate 1 — Build & test (`Bash`)

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

Uncommitted work is the user's normal review-then-commit flow, **not a no-go** — never fail or
block a gate on it. The safeguard against "authored but never shipped" (uncommitted edits
masquerading as merged work) lives in Gate 5's conditional GO + the `+dirty` stamp.

### Gate 2 — AC checklist (per-AC sub-gates)

For each AC line extracted in Gate 0:

- **Testable AC** (a verifiable behaviour the build/test gate already covers) — point at the
  test that proves it. Pass = test exists and passed in Gate 1.
- **Code-level AC** ("uses the existing auth middleware", "no new database index") — run a
  targeted `Grep` / `Read` and record file:line evidence.
- **Manual AC** (UI behaviour, copy, animation) — ask the user; record their confirm.

Record one line per AC:

```
- [x] AC #1 — "logout button visible on /account" — pass (test: tests/account.test.ts:42)
- [ ] AC #4 — "techspec total ≤ 150 lines" — FAIL: actual 164 (file:line)
```

### Gate 3 — Cross-cutting invariants

The three global CLAUDE.md "Verification before completion" checks; each is one structured tool call.

**3a — env asymmetry.** For repos with multiple environments (Terraform `dev/test/staging/prod`,
`.env.{env}` files), `Read` all env files in parallel; diff structurally. Any key present in
one without a `# deliberate-asymmetry: <reason>` comment in the others → FAIL.

**3b — line budgets.** For each file the techspec pinned a budget on ("techspec ≤ 150 lines",
"orchestrator stays ≤ 60 lines"), `Bash` `wc -l` and compare.

**3c — SDK / framework version.** `Grep` `package.json` / `requirements.txt` / `Gemfile.lock` /
`go.mod` for the SDK the techspec pins; confirm version matches. If the techspec doesn't pin
one, note "no version pinned (acceptable)".

Record one line per sub-check. If any sub-check is project-specific in a way the spec didn't
anticipate, note "skipped — not applicable" with a one-line reason.

### Gate 4 — Docs consistency

For each sibling doc in the prefix folder (`{prefix}_analysis.md`, `{prefix}_techspec.md`,
`{prefix}_tasks.md`, `{prefix}_investigation.md`, …), `Read` and check:

- did the implementation reveal a gap the doc should record?
- are file paths / function names / API signatures in the doc consistent with what shipped?
- if the prefix has a `tasks.md`, are all tasks marked Done?

Failures here are usually "the docs are stale relative to the implementation" — resolution is
to update the docs (the global CLAUDE.md "Spec & doc updates" rule). **Propose the diff and
let the user approve** — do not silently rewrite the docs.

Skip this gate if `mode == streamlined` (P1-incident fast path; the post-mortem covers it later).
Record as `skipped (streamlined)`.

### Gate 5 — Human go/no-go

Present the `## QA` artifact to the user. Confirm every prior gate is either `pass` or
`accepted with a recorded reason`. Ask: ship it?

- **Yes, tree committed** → record the go decision in the gate-line; hand back to `next_step`.
- **Yes, tree dirty** → record `GO, conditional on commit` — the pending commit (post-final-review,
  batched with the QA artifact) is named in the gate-line for `/improve` to audit. Hand back to `next_step`.
- **No** → ask what to address; loop the failed gate.

If no `## Review` block (review-implementation) covers the verified tree, record **go-with-caveat:
unreviewed** naming the missing review — a gates-green tree later grew two HIGH-severity review findings.

The LLM doesn't decide go; the user does, with the gate report in front of them.

## Observation write

For each gate (1-5), append one entry to the session-scoped observation buffer so `/close`
picks it up at session end (Tier 1.3 contract — written to
`~/.claude/observations/{YYYY-MM-DD}-{slug}.md`):

Use the canonical schema from `~/.claude/observations/README.md` — numbered `### Observation N:`
headings with the standard fields (project, skill_or_workflow: qa-gates, phase/area: gate-{id},
outcome, friction_observed + tag, would_have_helped, improvement_suggestion, principle). Do NOT
emit bare key-value blocks — a run that did produced a file carrying two schemas. Batch the 5
gates into as few observations as their content warrants (a clean run can be one observation
listing the gate outcomes; each fail/accepted gate gets its own).

## Halt / acceptance discipline

- **Halt on fail** — do not advance to the next gate while the current one is unresolved.
- **Accept-with-reason** is the only escape. The `## QA` artifact must carry the reason inline;
  `/improve` audits accept-rates later.
- **Skipping a gate is visible** — the gate-plan in Gate 0 lists all 5; an unrecorded gate at
  end-of-run is a missing checkbox, not a silent omission.

## When NOT to use qa-gates

- The implementation hasn't happened yet — `qa-gates` verifies outcomes; if there's nothing to
  verify, you're in the wrong phase.
- A one-line typo / config tweak — gates are friction in front of trivial work.
- Doc reviews — that's `review-artifact` (it reviews the *doc*; qa-gates verifies the *implementation*).
- Code-quality review — that's `/review-implementation` (batched, before gates) or the calling command's pre-work fan-out.

## Composition

- **`verify-task` (Tier 2.5)** — same gates, narrower inputs (one task's ACs, one task's files,
  one task's budget). `gates_to_run: build,ac,cross-cutting`; skips docs + human go/no-go.
- **`/close`** — picks up the 5 observation entries per run; `/improve` clusters gate-fails by
  `gate-id` later (mechanical clustering, not inference from prose).
