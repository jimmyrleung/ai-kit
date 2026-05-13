---
name: qa-gates
description: Verify an implementation against its spec — 5 pass/fail gates (build/test, AC checklist, cross-cutting invariants, docs consistency, human go/no-go). Each gate is a tool call with a recorded pass or a specific failure. Skipping a gate is visibly missing in the artifact, not hidden in chat. Invoked as `/qa-gates prefix=…` (back-compat alias: `/implementation-quality-assurance`) after every task for a prefix has been implemented; also invoked in-workflow at the end of the hotfix execution phase of `full-incident-response` (the only orchestrator with in-workflow execution). Per-task version: see `verify-task` (Tier 2.5; same gates, narrower inputs).
---

# QA Gates — implementation verification

You verify an implementation against its spec by running 5 gates in order, each producing a
pass or a specific failure. The artifact is a `## QA` section in the existing review/QA doc
the prefix already owns. You do NOT review the code (`@code-reviewer-agent` handles that
*before* you run, in the calling command's pre-work step); you verify the *outcome*.

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

## Procedure

### Gate 0 — Setup (free)

`Read` the source doc(s) at `{prefix}_*.md` (techspec, tasks, analysis, audit, investigation —
whichever exist). Extract:

- the acceptance criteria list (from tasks/techspec)
- any line-count / size budgets the spec pinned
- the SDK / framework versions the spec pins
- the files the implementation was supposed to touch (from analysis / tasks)
- the test commands the techspec specifies

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
non-zero exit.** Record:

```
- [x] Gate 1 — build/test: pass (commands: `…`)
```

or:

```
- [ ] Gate 1 — build/test: FAIL
  - command: `…`
  - output: <2-3 line digest of the failure>
  - resolution: <"address before re-running" / "accepted: <reason>">
```

If FAIL with `accepted`, require a `Why:` line; do not advance until the user states the reason.

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

The three checks the global `~/.claude/CLAUDE.md` "Verification before completion" names; each
is one structured tool call.

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

- **Yes** → record the go decision in the gate-line; hand back to `next_step`.
- **No** → ask what to address; loop the failed gate.

The LLM doesn't decide go; the user does, with the gate report in front of them.

## Observation write

For each gate (1-5), append one entry to the session-scoped observation buffer so `/close`
picks it up at session end (Tier 1.3 contract — written to
`~/.claude/observations/{YYYY-MM-DD}-{slug}.md`):

```
skill_or_workflow: qa-gates
phase/area: gate-{id} ({name})
outcome: pass | fail | accepted | skipped
friction_observed: <tag if fail/accepted> — e.g. line_budget_overrun, env_asymmetry, sdk_version_drift, doc_drift
would_have_helped: <if fail/accepted>
principle: <generalizable takeaway>
```

5 entries per full run; 4 in streamlined mode (Gate 4 = `skipped`).

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
- Doc reviews — that's `review-artifact`. `qa-gates` reviews an *implementation* against the doc;
  `review-artifact` reviews the *doc* itself before implementation.
- Code-quality review — that's `@code-reviewer-agent`, run by the calling command *before* gates.
  Gates verify outcomes against spec; the agent verifies code quality against itself.

## Composition

- **`verify-task` (Tier 2.5)** — same gates, narrower inputs (one task's ACs, one task's files,
  one task's budget). `gates_to_run: build,ac,cross-cutting`; skips docs + human go/no-go.
- **`/close`** — picks up the 5 observation entries per run; `/improve` clusters gate-fails by
  `gate-id` later (mechanical clustering, not inference from prose).
