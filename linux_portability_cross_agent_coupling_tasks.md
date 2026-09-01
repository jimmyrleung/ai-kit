# Linux portability and cross-agent coupling — implementation tasks

Date: 2026-08-31
Mode: refactor

Companion documents:

- [Lay of the land](linux_portability_cross_agent_coupling_lay-of-the-land.md)
- [Analysis](linux_portability_cross_agent_coupling_analysis.md)
- [Technical specification](linux_portability_cross_agent_coupling_techspec.md) — authoritative
  for all technical detail

## Review

- **Review date:** 2026-08-31
- **Post-review confidence:** 97%
- **Recommendation:** Approved with notes
- **Review scope:** one independent layer-scoped reviewer traced the decomposition from the common
  sync and ownership contract through executable policy, canonical batches, documentation closure,
  final CI enforcement, and live migration; the coordinator re-grounded every finding against the
  reviewed techspec and current tasks document.
- **Corrections applied:** moved the Codex `teach` policy into the checker task; assigned an explicit
  post-neutralization owner for fail-closed CI; serialized public and provider documentation
  closure; split the oversized twelve-file semantic batch; assigned the manual scenario 43
  rehearsal; recomputed task numbering, dependencies, and parallel declarations.
- **Notes:** time estimates and unavailable cross-OS/provider runtime behavior remain execution-time
  evidence. They do not leave a decomposition decision open.

**Approach:** Balanced (10 tasks, mid-size grouping). Nine tasks complete the repository refactor;
the tenth is an approval-gated live migration after review and QA.

## Tasks overview

| Task | Title | Complexity | Est. Time | Depends On | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Build the common sync engine and compatibility surface | L | 6–8h | — | Done |
| 2 | Build the strict portability checker | M | 3–4h | Task 1 | Done |
| 3 | Enforce provider profiles in policy and transitional CI | M | 3–4h | Task 2 | Done |
| 4 | Neutralize low-risk invocation and handoff wording | M | 3–4h | Task 3 | Done |
| 5 | Neutralize research and discovery workflows | M | 3–4h | Task 3 | Done |
| 6 | Neutralize review, design, and learning workflows | M | 3–4h | Task 3 | Done |
| 7 | Neutralize routing, orchestration, and maintenance workflows | M | 3–4h | Task 3 | Done |
| 8 | Reconcile public, policy, and historical documentation | M | 2–4h | Tasks 4, 5, 6, 7 | Done |
| 9 | Reconcile provider mechanics and enforce final portability | M | 2–4h | Task 8 | Done |
| 10 | Migrate and verify the Linux user-home roots | S | 1–2h | Task 9 + review/QA gates | Done |

**Overall Progress**: 10/10 implementation tasks completed (100%); hosted cross-OS CI remains a
publication-time external gate and is not represented as a local pass.

**Last Updated**: 2026-09-01

**Parallelism:** After Task 3, Tasks 4–7 can run in parallel. Tasks 8–10 are deliberately serial;
Task 10 is post-gate.

## Implementation order

Use foundation-first safety sequencing: establish and test filesystem ownership before changing
the corpus it deploys, make policy executable before broad edits, then close documentation before
touching normal user-home state.

```text
1 -> 2 -> 3 -> 4 ----\
               -> 5 -----\
               -> 6 ------+-> 8 -> 9 -> review-implementation -> qa-gates -> 10
               -> 7 -----/
```

## Detailed tasks

### Task 1 — Build the common sync engine and compatibility surface

**Description:** Implement the complete two-root filesystem contract and replace all four adapter
implementations with thin wrappers. The engine, wrappers, and their single named test harness stay
in one task because wrapper parity, transaction recovery, and baseline-safe rollback form one
atomic deployment contract.

- **Complexity:** L
- **Estimated time:** 6–8h
- **Depends on:** None
- **Can run in parallel with:** None
- **Risk:** High
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `scripts/sync-skills.py` — create
- `tests/test_sync_skills.py` — create; sole owner of the sync test artifact
- `adapters/codex/sync.sh` — modify
- `adapters/codex/sync.ps1` — modify
- `adapters/cursor/sync.sh` — modify
- `adapters/cursor/sync.ps1` — modify
- `.gitattributes` — modify

**Implementation steps:**

1. Implement the Python 3.12+ standard-library CLI, exact flag combinations, exit codes, sorted
   canonical enumeration, two managed roots, root-layout refusal, and normalized target
   classification from techspec Phase 1, **Common CLI contract**.
2. Implement schema-1 ownership state, immutable first-managed baselines, atomic prepared
   transactions, action-time revalidation, recovery, and finalization exactly as specified in
   techspec Phase 1, **Ownership state**.
3. Implement apply, read-only check, dry-run, report-only orphan discovery, guarded orphan action,
   and baseline-restoring uninstall without following or changing target directories.
4. Replace the two POSIX adapters with safe forwarding wrappers. Reject provider-private home
   environment variables and preserve common-engine arguments and exit codes.
5. Replace the two PowerShell adapters with exact translations for `WhatIf`, `Check`, `Uninstall`,
   `Force`, `Prune`, and `UserHome`; retain legacy home parameters only as exit-2 diagnostics.
6. Extend LF enforcement to the new Python and JavaScript executable sources.
7. Implement techspec scenarios 1–29 and the automated fixture portion of scenario 43 in
   `tests/test_sync_skills.py`, including interruption and before/after object-preservation hooks.
8. Rehearse scenario 43's manual whole-root migration procedure against an isolated root containing
   canonical and unrelated children; record its inventory, stop for explicit dispositions, and
   compare every child name and resolved target after the approved fixture migration.

**Testing requirements:**

- Run `tests/test_sync_skills.py` only against isolated temporary homes; never point the test
  harness at the normal home.
- Exercise clean apply, idempotence, dry-run, completeness check, invalid input, malformed state,
  collision protection, adoption, checkout moves, guarded correction, orphan behavior,
  interruption recovery, rollback, root-layout conflict, and wrapper parity.
- Run POSIX shell syntax checks locally. Run PowerShell wrapper and Windows junction cases through
  the three-OS matrix established in Task 3.
- Run the manual half of scenario 43 only against an isolated fixture. Prove that an unrelated child
  stops migration until disposition and that the approved preservation path uses an unmanaged link
  to the original resolved target rather than copying target data.
- Confirm the isolated end state contains the derived canonical population in both roots and that
  no target content changes.

**Acceptance criteria:**

- `python3 scripts/sync-skills.py --home <isolated-home>` followed by `--check` exits 0 and every
  managed entry resolves to its live `skills/<name>` directory.
- Every conflict fixture leaves both managed roots, unrelated entries, targets, and manifest state
  unchanged, proven by before/after fixture assertions.
- A mixed created/adopted/retargeted fixture returns each entry to its captured baseline and passes
  the retry tests at every specified interruption point.
- Both shell wrappers contain forwarding/argument code only; text search finds no link
  classification or mutation implementation outside `scripts/sync-skills.py`.
- The scenario 43 rehearsal records identical pre/post child-name and resolved-target inventories,
  leaves the old root target unchanged, and proves the stop-before-disposition branch.
- POSIX syntax checks and all locally applicable sync tests pass; cross-OS cases are explicitly
  pending Task 3 rather than claimed from Linux.

**Reference:** Techspec Phase 1; test-plan scenarios 1–29 and 43; analysis **Preserved contracts**
items 8–11.

**Rollback plan:** Restore the four wrappers and `.gitattributes` to their pre-task content and
return the two newly created repository files to an absent state. No normal-home state exists at
this stage. For an isolated fixture, finish any prepared transaction and exercise the fixture's
baseline-restoring uninstall before discarding the fixture.

## Verify — 2026-08-31

- [x] Gate 1 — build/test: pass (`python3 tests/test_sync_skills.py`; 29 tests, 1 platform-specific Windows test skipped; `python3 -m py_compile`; `bash -n` for both POSIX wrappers)
- [x] Gate 2 — AC #1: pass (isolated apply/check and 31 links per root: `tests/test_sync_skills.py:107`)
- [x] Gate 2 — AC #2: pass (conflict fixtures preserve roots, entries, targets, and manifest: `tests/test_sync_skills.py:243`, `259`, `376`, `394`)
- [x] Gate 2 — AC #3: pass (created/adopted/retargeted recovery and baseline rollback: `tests/test_sync_skills.py:220`, `281`, `413`, `424`)
- [x] Gate 2 — AC #4: pass (POSIX wrappers are forwarding-only; PowerShell wrappers are translators-only: `adapters/codex/sync.sh`, `adapters/cursor/sync.sh`, and `tests/test_sync_skills.py:472`)
- [x] Gate 2 — AC #5: pass for the isolated rehearsal (stop-before-disposition and unchanged child inventory: `tests/test_sync_skills.py:542`).
- [x] Gate 2 — AC #6: pass for locally applicable POSIX syntax and sync tests; the Windows junction case is implemented at `tests/test_sync_skills.py:519` and the macOS/Windows runtime evidence is covered by the Task 3 matrix and remains externally pending.
- [x] Gate 3 — cross-cutting: pass (no explicit line/SDK budget in Task 1; LF attributes cover `.sh`, `.py`, and `.mjs`; `git diff --check` passed; normal-home state untouched)

**Status:** Done

### Task 2 — Build the strict portability checker

**Description:** Add one locked Node-based checker and its fixture suite so metadata, population,
and coupling policy can be evaluated mechanically before canonical edits. Coupling checks begin in
the techspec's transitional warn-only mode.

- **Complexity:** M
- **Estimated time:** 3–4h
- **Depends on:** Task 1
- **Can run in parallel with:** None
- **Risk:** Medium
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `scripts/check-skill-portability.mjs` — create
- `tests/test_skill_portability.mjs` — create; sole owner of the portability test artifact
- `package.json` — create
- `package-lock.json` — create
- `skills/teach/agents/openai.yaml` — create
- `.gitignore` — modify

**Implementation steps:**

1. Pin Node 24 and `js-yaml@5.4.1`, add checker/test commands, lock the dependency, and ignore only
   `node_modules/` in addition to current exclusions.
2. Create the Codex explicit-only policy for `teach` while preserving its existing Cursor
   frontmatter behavior from techspec Phase 2.
3. Strictly parse each canonical frontmatter block and validate duplicate keys, directory/name
   equality, standard field shapes and bounds, provider overlays, and Codex metadata per techspec
   Phase 2, **Metadata profiles**.
4. Derive the live skill count and compare it with README, inventory, and rule claims; do not embed
   a second authoritative population list.
5. Implement classified checks for invocation suffixes, live Windows repo paths, convention-file
   tokens, explicit-only `teach` policy, and the unchanged `find-skills` neutral reference.
6. Add explicit structural-only, transitional warn-only, and final fail-closed coupling modes.
7. Implement techspec scenarios 30–32, 35–37, and the checker-owned portions of scenarios 33, 36,
   and 42 as isolated fixtures.

**Testing requirements:**

- Run `tests/test_skill_portability.mjs` against malformed YAML, duplicate keys, boundary lengths,
  unknown fields, justified and unjustified overlays, drifted counts, and each coupling class.
- Run the checker against the current pre-neutralization corpus with structural/profile gates
  enabled and coupling gates warn-only.
- Confirm fixture failures name the file, field or coupling class, and intended reason.

**Acceptance criteria:**

- `npm test` passes all checker fixtures and rejects each malformed or unknown-profile case for the
  expected reason.
- The structural/profile checker completes against every directory currently enumerated under
  `skills/`; coupling findings are warnings only in the declared transition mode.
- `teach` is explicit-only under both checked provider contracts before the CI/policy task starts.
- Changing any fixture count independently in README, inventory, or the rule makes the drift test
  fail until all sources agree with enumeration.
- `package-lock.json` resolves only the declared checker dependency tree, and no dependency output
  becomes tracked.

**Reference:** Techspec Phase 2, **Metadata profiles** and checker enforcement list; test-plan
scenarios 30–37 and 42.

**Rollback plan:** Return the five new checker/package/metadata files to an absent state and restore
the previous `.gitignore`. Task 1 remains usable because the common engine intentionally does not
parse YAML.

## Verify — 2026-08-31

- [x] Gate 1 — build/test: pass (`npm test`; all portability fixtures passed; `npm run check:portability:transition` completed with 0 errors and 410 transitional warnings)
- [x] Gate 2 — AC #1: pass (strict-YAML, duplicate-key, bounds, unknown-field, overlay, and coupling fixtures: `tests/test_skill_portability.mjs`)
- [x] Gate 2 — AC #2: pass (all 31 live directories enumerate and structural/profile mode exits 0; transitional mode reports coupling as warnings)
- [x] Gate 2 — AC #3: pass (`skills/teach/SKILL.md` retains Cursor explicit-only metadata and `skills/teach/agents/openai.yaml` sets Codex `allow_implicit_invocation: false`)
- [x] Gate 2 — AC #4: pass (independent README population drift fixture fails with `population-count-drift`)
- [x] Gate 2 — AC #5: pass (`package-lock.json` contains only `js-yaml@5.4.1` and its `argparse` dependency; `node_modules/` is ignored and untracked)
- [x] Gate 3 — cross-cutting: pass (Node `24.x` engine and `js-yaml@5.4.1` are pinned; no explicit line budget; `git diff --check` passed)

**Status:** Done

### Task 3 — Enforce provider profiles in policy and transitional CI

**Description:** Connect the checker to the authoring/audit workflows and establish the three-OS
release gate in its explicit transitional mode. This task also applies the Phase 3 surgical changes
for `audit-skills` and `write-skills`, so each file is edited once.

- **Complexity:** M
- **Estimated time:** 3–4h
- **Depends on:** Task 2
- **Can run in parallel with:** None
- **Risk:** Medium
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `.github/workflows/portability.yml` — create
- `docs/rules/skill-authoring.md` — modify
- `skills/audit-skills/SKILL.md` — modify
- `skills/write-skills/SKILL.md` — modify

**Implementation steps:**

1. Replace stale deployment topology and manual validation instructions in the repo rule with the
   common sync, strict checker, standard profile, and documented overlay policy.
2. Patch only the committed anchors in `audit-skills` and `write-skills`; preserve their checks,
   limits, thresholds, proposal destinations, approval flow, and authoring contract from techspec
   Phase 3, **Context-verified file map**.
3. Add the read-only GitHub Actions matrix using the pinned action majors, Python 3.12, Node 24,
   locked install, syntax checks, both test suites, checker, wrapper dry-runs, and isolated sync.
4. Invoke the checker in explicit transitional mode: structural/profile failures block CI while
   known coupling and documentation drift are reported without hiding new regressions.
5. Leave the workflow's final fail-closed promotion to Task 9 after every canonical and
   documentation batch is complete.

**Testing requirements:**

- Use the portability harness owned by Task 2 to validate strict YAML, overlay justification,
  `teach` explicit-only policy, unchanged named-input fields, and fixture-level rule/count drift;
  live documentation drift remains explicit transitional output until Tasks 8–9.
- Use the sync harness owned by Task 1 for wrapper and filesystem coverage in each matrix OS.
- Review the workflow source for `contents: read`, pinned runtimes, disabled unneeded caching, and
  the exact Linux/macOS/Windows matrix.
- Run the installed Codex validator when available and classify documented foreign-provider
  extensions as profile notes, never as repository-checker success or failure by inference.

**Acceptance criteria:**

- The three-OS workflow completes syntax, structural/profile checks, portability tests, sync tests,
  wrapper exercises, and explicit transitional coupling reporting on their intended hosts.
- All live frontmatters pass the declared repository profiles; unknown or unjustified fields fail.
- `teach` is explicit-only under both checked provider contracts, while `find-skills` remains
  byte-for-byte unchanged.
- The rule, authoring skill, and audit skill point to the same common commands and profile model;
  full-file reads and strict parsing show no dropped preserved contract.

**Reference:** Techspec Phase 2; Phase 3 rows for `audit-skills` and `write-skills`; test-plan
scenarios 33, 34, 36, 42, and 49.

**Rollback plan:** Restore the three modified policy files and return the workflow to an absent
state. Tasks 1–2 continue to run locally without making CI or the new profile policy mandatory.

## Verify — 2026-08-31

- [x] Gate 1 — build/test: pass for locally runnable checks (`npm test`; `node scripts/check-skill-portability.mjs --mode structural` with 0 errors; `npm run check:portability:transition` with 0 errors and 410 warnings; Python syntax/tests; POSIX shell syntax). The workflow's Windows/macOS runtime is not executable in this Linux session and remains a required remote matrix check.
- [x] Gate 2 — AC #1: pass (workflow has syntax, structural/profile, both test suites, transitional checker, isolated sync, and OS-specific wrapper dry-run steps: `.github/workflows/portability.yml`)
- [x] Gate 2 — AC #2: pass (structural/profile mode enumerates 31 live skills with 0 errors; fixture suite covers unknown and unjustified fields)
- [x] Gate 2 — AC #3: pass (`teach` retains Cursor explicit-only frontmatter, Codex policy sets `allow_implicit_invocation: false`, and the locked `find-skills` digest remains unchanged)
- [x] Gate 2 — AC #4: pass (rule, audit skill, and authoring skill use the common checker/sync profile; full target-file reads, strict parsing, workflow YAML parsing, and `git diff --check` passed)
- [x] Gate 3 — cross-cutting: pass (workflow grants only `contents: read`, pins action majors/runtime versions, omits package-manager caching, and uses isolated temporary homes; installed provider validator unavailable locally and no inference was made)

**Status:** Done

### Task 4 — Neutralize low-risk invocation and handoff wording

**Description:** Apply the lowest-risk surgical batch: slash-form invocation and cross-skill
handoff wording in workflows whose control flow does not depend on provider worker, routing, or
convention-file behavior.

- **Complexity:** M
- **Estimated time:** 3–4h
- **Depends on:** Task 3
- **Can run in parallel with:** Tasks 5, 6, 7
- **Risk:** Medium
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `skills/breakout-session/SKILL.md` — modify
- `skills/close-tasks/SKILL.md` — modify
- `skills/document-workflow/SKILL.md` — modify
- `skills/implement-task/SKILL.md` — modify
- `skills/post-mortem/SKILL.md` — modify
- `skills/record-decision/SKILL.md` — modify
- `skills/triage-learning-content/SKILL.md` — modify
- `skills/update-workflow-docs/SKILL.md` — modify
- `skills/verify-task/SKILL.md` — modify
- `skills/walkthrough/SKILL.md` — modify
- `skills/walkthrough-implementation/SKILL.md` — modify

**Implementation steps:**

1. Read each file end-to-end immediately before its edit and snapshot frontmatter, headings,
   artifact names, thresholds, approval gates, and ordered workflow steps.
2. Patch only the stable anchors and committed deltas for these eleven rows in techspec Phase 3,
   **Context-verified file map**.
3. Replace slash-form sibling references with unprefixed skill names or capability wording from
   techspec Phase 3, **Committed edit rules**; do not rename skills or change workflow order.
4. Run caller closure for each edited skill name and inspect every changed caller sentence.
5. Strict-parse the full corpus, search replaced terms for echoes, and compare the snapshots after
   the batch.

**Testing requirements:**

- Run the portability harness owned by Task 2 in transitional mode for scenarios 35, 37, 38, and
  40.
- Run focused trigger prompts for each changed description and its closest neighbors; verify
  `teach` remains explicit-only.
- Run any skill-local structural or workflow checks named by the edited file; no testing is
  silently deferred beyond the batch.

**Acceptance criteria:**

- Strict YAML parsing succeeds for every live skill, and the checker reports no new unknown field
  or coupling class.
- Snapshot comparison shows unchanged names, headings, artifact filenames, worker/order contracts,
  thresholds, named inputs, and approval gates.
- Repository-wide caller closure contains no missed slash-form call site assigned to this batch.
- Trigger probes select the same intended workflows before and after the wording changes.

**Reference:** Techspec Phase 3 rows for the eleven listed skills; **Committed edit rules**;
test-plan scenarios 35, 37, 38, and 40.

**Rollback plan:** Restore only this eleven-file wording batch. Re-run the strict checker and caller
closure to prove Tasks 1–3 remain valid and no partial wording assumption escaped into another
batch.

## Verify — 2026-08-31

- [x] Gate 1 — build/test: pass (`npm test`; transitional portability checker exits 0 with 300 warnings; Python syntax/tests; POSIX shell syntax; `git diff --check`)
- [x] Gate 2 — AC #1: pass (all 31 live frontmatters remain strict/profile-valid; no Task 4 target carries a new coupling finding)
- [x] Gate 2 — AC #2: pass (target headings, artifact contracts, thresholds, named inputs, and workflow order were preserved; changes are sentence-level wording edits only)
- [x] Gate 2 — AC #3: pass (repository-wide search found no remaining slash-form reference to a Task 4 skill in the edited target set; caller references in later semantic batches remain assigned to their owners)
- [x] Gate 2 — AC #4: pass by before/after description comparison: trigger phrases and routing distinctions are unchanged apart from removing provider-specific slash syntax and suffixes; `teach` remains explicit-only
- [x] Gate 3 — cross-cutting: pass (no explicit line/SDK budget; strict checker, fixture suite, and diff checks pass; no whole-file rewrites or new artifacts)

**Status:** Done

### Task 5 — Neutralize research and discovery workflows

**Description:** Replace provider-named file, worker, question, shell, and convention vocabulary in
the research, investigation, knowledge-compilation, handler-discovery, and Terraform-documentation
workflows while preserving their evidence and named-input contracts.

- **Complexity:** M
- **Estimated time:** 3–4h
- **Depends on:** Task 3
- **Can run in parallel with:** Tasks 4, 6, 7
- **Risk:** Medium
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `skills/analyze-work/SKILL.md` — modify
- `skills/bug-investigation/SKILL.md` — modify
- `skills/compile-kb/SKILL.md` — modify
- `skills/docs-tasks-creator/SKILL.md` — modify
- `skills/document-terraform/SKILL.md` — modify
- `skills/lay-of-the-land/SKILL.md` — modify

**Implementation steps:**

1. Read and snapshot each file using the same preservation ledger as Task 4.
2. Apply only these six committed file-map rows from techspec Phase 3, using capability terms for
   file access, shell execution, structured questions, generic research subagents, and loaded
   conventions.
3. Preserve all named `arguments` contracts, worker counts and ordering, evidence tags, topology
   rules, confidence thresholds, and output filenames.
4. Run repository-wide caller closure and inspect every changed cross-skill sentence.
5. Strict-parse all frontmatters, search every replaced token globally, and run focused semantic
   probes for evidence classification, named inputs, discovery precedence, and output selection.

**Testing requirements:**

- Run the Task 2 portability harness for scenarios 35, 37, 38, and 40 in transitional mode.
- Run focused behavior probes for analysis modes, investigation evidence tags, compilation guards,
  handler detection, Terraform topology, named arguments, confidence gates, and filenames.
- Confirm full-file diffs contain sentence/line patches only at the reviewed anchors and no heading
  restructure or whole-file rewrite.

**Acceptance criteria:**

- Provider-named tool and generic convention occurrences assigned to these six files are replaced
  or present on the checker's reviewed provider/historical allowlist.
- Snapshot and semantic probes show unchanged modes, evidence rules, worker counts, named inputs,
  thresholds, topology behavior, and outputs.
- Caller closure matches the reviewed analysis table for every changed workflow reference.
- Strict parsing, portability tests, and all focused probes pass for this batch.

**Reference:** Techspec Phase 3 rows for the six listed skills; **Committed edit rules** and
**Edit discipline**; test-plan scenarios 35, 37, 38, and 40.

**Rollback plan:** Restore only this six-file batch, then rerun strict parsing, caller closure, and
the affected behavior probes. The common deployment and executable policy remain intact.

## Verify — 2026-08-31

- [x] Gate 1 — build/test: pass (`npm test`; transitional portability checker exits 0 with 230 warnings; `git diff --check`)
- [x] Gate 2 — AC #1: pass (all provider/tool/convention findings assigned to the six files are closed; no Task 5 target carries a coupling finding)
- [x] Gate 2 — AC #2: pass (named arguments, modes, evidence tags, worker counts, thresholds, topology rules, and output contracts were preserved; target line counts and headings match `HEAD`)
- [x] Gate 2 — AC #3: pass (repository-wide caller search leaves only slash-form references in the later Task 6/7 owner batches; no Task 5 target retains one)
- [x] Gate 2 — AC #4: pass (strict checker and focused semantic probes for analysis modes, investigation evidence, compilation guards, handler detection, Terraform topology, named inputs, confidence gates, and filenames)
- [x] Gate 3 — cross-cutting: pass (frontmatter remains strict/profile-valid; changed files are sentence/line patches only; no new artifacts or whole-file rewrites)

**Status:** Done

### Task 6 — Neutralize review, design, and learning workflows

**Description:** Neutralize provider-specific worker, question, shell, and convention vocabulary in
the interactive learning, review, QA, task-decomposition, and design workflows while preserving
their review counts, modes, gates, sizing, and output contracts.

- **Complexity:** M
- **Estimated time:** 3–4h
- **Depends on:** Task 3
- **Can run in parallel with:** Tasks 4, 5, 7
- **Risk:** Medium
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `skills/onboard-me/SKILL.md` — modify
- `skills/qa-gates/SKILL.md` — modify
- `skills/review-artifact/SKILL.md` — modify
- `skills/review-implementation/SKILL.md` — modify
- `skills/tasks-breakdown/SKILL.md` — modify
- `skills/techspec/SKILL.md` — modify

**Implementation steps:**

1. Read and snapshot each file using the same preservation ledger as Task 4.
2. Apply only these six committed file-map rows from techspec Phase 3, using capability terms for
   structured questions, shells, generic reviewers, follow-up messaging, file access, and loaded
   conventions.
3. Preserve the Socratic cadence, reviewer counts and constraints, QA gate scope, sizing rules,
   mode/depth gates, confidence thresholds, approval points, and output filenames.
4. Run repository-wide caller closure and inspect every changed cross-skill sentence.
5. Strict-parse all frontmatters, search every replaced token globally, and run focused semantic
   probes for reviewer dispatch, task sizing, techspec depth, QA gates, and learning cadence.

**Testing requirements:**

- Run the Task 2 portability harness for scenarios 35, 37, 38, and 40 in transitional mode.
- Run focused behavior probes for exact reviewer counts, evidence disposition, task sizing,
  techspec depth, QA gates, output filenames, and one-step-per-turn learning behavior.
- Confirm full-file diffs contain sentence/line patches only at the reviewed anchors and no heading
  restructure or whole-file rewrite.

**Acceptance criteria:**

- Provider-named tool and generic convention occurrences assigned to these six files are replaced
  or present on the checker's reviewed provider/historical allowlist.
- Snapshot and semantic probes show unchanged modes, reviewer counts, task order, sizing, gates,
  approvals, learning cadence, and outputs.
- Caller closure matches the reviewed analysis table for every changed workflow reference.
- Strict parsing, portability tests, and all focused probes pass for this batch.

**Reference:** Techspec Phase 3 rows for the six listed skills; **Committed edit rules** and
**Edit discipline**; test-plan scenarios 35, 37, 38, and 40.

**Rollback plan:** Restore only this six-file batch, then rerun strict parsing, caller closure, and
the affected behavior probes. The common deployment and executable policy remain intact.

## Verify — 2026-09-01

- [x] Gate 1 — build/test: pass (`npm test`; transitional portability checker exits 0 with 126 warnings; `git diff --check`)
- [x] Gate 2 — AC #1: pass (all Task 6 target provider/tool/convention findings are closed; no target coupling finding)
- [x] Gate 2 — AC #2: pass (Socratic cadence, reviewer counts, modes, gates, sizing, thresholds, approvals, learning cadence, and outputs preserved; line counts equal `HEAD` and heading shape is unchanged apart from reviewed inline label wording)
- [x] Gate 2 — AC #3: pass (repository-wide caller search leaves only later Task 7 owner references; no Task 6 target retains a slash-form handoff)
- [x] Gate 2 — AC #4: pass (strict checker and focused semantic probes for reviewer dispatch, evidence disposition, task sizing, techspec depth, QA gates, output filenames, and one-step-per-turn learning behavior)
- [x] Gate 3 — cross-cutting: pass (strict/profile-valid frontmatter; sentence/line patches only; no new artifacts or whole-file rewrites)

**Status:** Done

### Task 7 — Neutralize routing, orchestration, and maintenance workflows

**Description:** Patch the four highest-risk behavior-bearing workflows: provider-native runner
routing, subagent/model selection, planning/question capabilities, and private convention-target
resolution. This remains separate because a wording error can change dispatch or maintenance
behavior even when structural tests pass.

- **Complexity:** M
- **Estimated time:** 3–4h
- **Depends on:** Task 3
- **Can run in parallel with:** Tasks 4, 5, 6
- **Risk:** High
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `skills/close/SKILL.md` — modify
- `skills/improve/SKILL.md` — modify
- `skills/orchestrate/SKILL.md` — modify
- `skills/triage/SKILL.md` — modify
- `tests/test_skill_portability.mjs` — modify; keep the live-corpus transition assertion future-proof and inject the invocation fixture into frontmatter

**Implementation steps:**

1. Read and snapshot all four skill files before editing, including anchored maintenance paths, approval
   gates, dispatch persistence, verification tiers, route order, and output contracts.
2. Apply the exact Phase 3 file-map deltas and capability-based orchestration rule; preserve the
   anchored `~/.claude` maintenance stores.
3. In `improve`, resolve repository conventions through `AGENTS.md` and active private conventions
   through the loaded harness instruction file; stage separate proposals rather than guessing when
   mirrored private files can diverge.
4. In `triage`, route recurrence to the runner category and `docs/loop-recipes.md` without embedding
   provider-native command spellings.
5. In `orchestrate`, default workers to the session model and use explicit overrides only when the
   active spawn facility supports them and the task requires them; preserve dispatch,
   persist-on-arrival, verification, and resume semantics.
6. Run caller closure, strict parsing, replaced-token searches, and the high-risk semantic probes
   before closing the batch.

**Testing requirements:**

- Run scenario 39 probes for triage routing, orchestration dispatch/persist/verify behavior, and
  improve's convention-target proposal behavior.
- Run Task 2 scenarios 35, 37, 38, and 40 in transitional mode; Task 9 owns the final fail-closed
  promotion after all four canonical batches and documentation tasks complete.
- Confirm no repository action writes a private convention file and every cross-target proposal
  remains user-approved.

**Acceptance criteria:**

- Triage preserves its classification order and confidence gate while emitting no provider-native
  runner syntax in canonical output.
- Orchestration preserves worker dispatch, result persistence, verification tiers, resume behavior,
  and quality floor under capability-based wording.
- Improve resolves each convention target without treating `~/.claude/CLAUDE.md` as universal;
  an unresolved active-harness target stops for user input.
- Close retains its anchored stores, offer/approval rules, and commit boundary.
- High-risk semantic probes, strict parsing, caller closure, and changed-file coupling checks pass
  for this batch without depending on Tasks 4–6.

**Reference:** Techspec Phase 3 rows for `close`, `improve`, `orchestrate`, and `triage`; specific
rules following **Committed edit rules**; test-plan scenarios 35, 37–40.

**Rollback plan:** Restore the four skill files and the test-harness maintenance as one high-risk
batch, rerun the semantic probes, and keep the checker in transitional mode until a corrected batch
is ready. Anchored maintenance data is never migrated or rewritten by this task.

## Verify — 2026-09-01

- [x] Gate 1 — build/test: pass (`npm test`; transitional portability checker exits 0 with 4 warnings; `git diff --check`)
- [x] Gate 2 — AC #1: pass (all Task 7 target skill coupling findings are closed; the test harness contains only fixture/transition maintenance)
- [x] Gate 2 — AC #2: pass (anchored stores, offer/approval and commit boundaries, convention-target routing, loop categories, classification order, confidence gate, and dispatch/persist/verify/resume behavior preserved)
- [x] Gate 2 — AC #3: pass (high-risk semantic probes confirm capability-based orchestration, runner-neutral triage output, and staged improve proposals with no private-file writes)
- [x] Gate 2 — AC #4: pass (strict/profile parsing, repository-wide caller search, replaced-token search, fixture coverage, and changed-file coupling checks pass)
- [x] Gate 3 — cross-cutting: pass (frontmatter remains strict/profile-valid; skill changes are sentence/line patches with no heading reorganization; test changes are limited to stale live-corpus assumptions)

**Status:** Done

### Task 8 — Reconcile public, policy, and historical documentation

**Description:** Make the public entry point, inventory, rule index, loop guidance, standing
research action, and historical records agree with the finished common surface. Preserve the
historical assessment bodies and change only their supersession banners/current cross-links.

- **Complexity:** M
- **Estimated time:** 2–4h
- **Depends on:** Tasks 4, 5, 6, 7
- **Can run in parallel with:** None
- **Risk:** Medium
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `README.md` — modify
- `INVENTORY.md` — modify
- `AGENTS.md` — modify
- `docs/loop-recipes.md` — modify
- `agentic_auto_scheduling_experimental_study_research_action_items.md` — modify
- `docs/codex-portability-assessment.md` — modify
- `docs/cursor-portability-assessment.md` — modify
- `tests/test_skill_portability.mjs` — modify; keep the population-drift fixture aligned with the derived count

**Implementation steps:**

1. Update the public identity, derived population statement, common sync/check commands, and
   provider-mechanics links per techspec Phase 4.
2. Align inventory status and the root rule-index description with the common topology and
   executable checker.
3. Keep provider-native recurring runners isolated in `docs/loop-recipes.md`; add equal-OS
   scheduling guidance and current capability caveats without putting those spellings back into
   canonical skills.
4. Replace only the standing Codex sync reference in the research action list with the common
   checker/sync path.
5. Add dated supersession banners and current cross-links to both portability assessments; preserve
   each historical body byte-for-byte.
6. Run population/document checks over this task's seven owned files and search those files for
   retired topology, stale counts, and old operational entry points. Task 9 owns repository-wide
   closure after the adapter documents are updated.

**Testing requirements:**

- Run Task 2's population/document drift checks against this task's seven owned files.
- Compare each assessment body before and after its new banner to prove byte preservation.
- Review public commands against the actual CLI and wrapper help output from Task 1.
- Verify the root `AGENTS.md` index still points to an existing repo-rule file and remains within
  its concise index contract.

**Acceptance criteria:**

- Enumeration, README, inventory, and the repo rule agree on the live population without a manually
  maintained second source of truth in the checker.
- None of this task's seven owned documents presents provider-private sync scripts, retired v1
  generation, or the old whole-root topology as the current common install path.
- The historical assessment bodies compare byte-for-byte with their pre-task bodies after removing
  only the new supersession banner/current links from the comparison.
- Public commands match executable help and pass the owned-file documentation checks; global
  documentation/config closure is explicitly covered by Task 9.

**Reference:** Techspec Phase 4 file table; test-plan scenarios 36, 42, 47, and 49; repository
preserve-history rule.

**Rollback plan:** Restore the seven documentation files and the synchronized population-drift
fixture together so counts, entry points, supersession status, and their test remain consistent.
Repository code and canonical skills remain functional.

## Verify — 2026-09-01

- [x] Gate 1 — build/test: pass (`npm test`; structural checker exits 0; transitional checker exits 0 with 3 warnings; `git diff --check`)
- [x] Gate 2 — AC #1: pass (derived 31 skills agrees with README, inventory rows, and the repo rule's population claim)
- [x] Gate 2 — AC #2: pass (owned current documentation uses the common sync/check path; provider-native loop wiring remains isolated to `docs/loop-recipes.md`)
- [x] Gate 2 — AC #3: pass (both historical assessment bodies are byte-identical after excluding only their new supersession banners/current links)
- [x] Gate 2 — AC #4: pass (common engine and both wrapper help outputs match the README commands; AGENTS index resolves; owned-document probes pass)
- [x] Gate 3 — cross-cutting: pass (documentation changes stay within the seven owned docs; the test change only updates the stale population fixture; no new runtime artifacts)

**Status:** Done

### Task 9 — Reconcile provider mechanics and enforce final portability

**Description:** Reduce both provider adapters to mechanics-only guidance, then switch the CI
workflow from transitional reporting to final fail-closed portability enforcement. This serial
closure task proves root and adapter documentation together before live migration.

- **Complexity:** M
- **Estimated time:** 2–4h
- **Depends on:** Task 8
- **Can run in parallel with:** None
- **Risk:** Medium
- **Lifecycle boundary:** pre-merge

**Files involved:**

- `.github/workflows/portability.yml` — modify; promote the checker invocation to final mode
- `scripts/sync-skills.py` — modify; enumerate canonical directory-link children without losing the source entry path
- `tests/test_sync_skills.py` — modify; cover deployment of a symlinked canonical skill directory
- `skills/audit-skills/SKILL.md` — modify; clear the final checker's remaining live Windows-path findings
- `docs/rules/skill-authoring.md` — modify; make the final checker the shipping validation command
- `agentic_auto_scheduling_experimental_study_research_action_items.md` — modify; align its validation command with final CI
- `adapters/codex/README.md` — modify
- `adapters/codex/AGENTS.md` — modify
- `adapters/cursor/README.md` — modify
- `adapters/cursor/AGENTS.md` — modify

**Implementation steps:**

1. Make each README mechanics-only, point deployment to the root common entry point, and document
   its wrapper as compatibility rather than an independent implementation.
2. Update Codex invocation, native subagent, model-override, and goals mechanics while retaining the
   managed private-instruction block and anchored-store contracts.
3. Update Cursor invocation, native subagent, and loop mechanics; state the source-equivalence rule
   for duplicate discovery without claiming precedence.
4. Surface the manual refresh requirement for copied private instruction blocks; no repository
   script may overwrite private conventions.
5. Compare every adapter claim with the committed common CLI and current provider evidence cited by
   the techspec.
6. Change the CI checker invocation from Task 3's transitional mode to final fail-closed mode after
   confirming every canonical and documentation batch is present.
7. Run repository-wide documentation/config closure across root, policy, historical, adapter,
   package, ignore, attribute, workflow, and canonical-skill surfaces.

**Testing requirements:**

- Run final fail-closed coupling and repository-wide documentation/config closure from the Task 2
  harness, plus wrapper parity from Task 1.
- Mechanically enumerate synthetic occurrences across shared, Claude, Codex, and Cursor roots and
  fail any divergent ai-kit target without making a precedence assertion.
- Review the managed include-block markers and confirm public instructions require manual refresh.
- Runtime presentation is deferred to Task 10 and must be classified as unavailable or ambiguous
  when it cannot be observed.

**Acceptance criteria:**

- Adapter documentation contains no independent deployment algorithm or stale provider-private
  root as the common path.
- The copied-block contract remains intact and no tracked script writes a private convention file.
- Cursor documentation states duplicate source equivalence and no precedence promise; a divergent
  synthetic target fails the check.
- Codex and Cursor mechanics match the current reviewed provider evidence and do not alter canonical
  workflow semantics.
- CI invokes the final checker mode, all prohibited coupling and documentation drift fail the
  workflow, and the complete three-OS matrix is green.
- Repository-wide documentation/config closure passes only after both Task 8 root docs and this
  task's adapter docs are present.

**Reference:** Techspec Phase 4 adapter rows; **Patterns reused** managed-block contract; test-plan
scenarios 41, 42, 45, and 48.

**Rollback plan:** Restore the canonical directory-link handling and its regression fixture along
with the audit residual, policy rule, research-action note, four adapter documents, and workflow;
then return the workflow invocation to Task 3's explicit transitional mode. Reapply only after the
mechanics claims, common-entry links, and final checker results are internally consistent. The thin
wrappers from Task 1 remain operational.

## Verify — 2026-09-01

- [x] Gate 1 — build/test: pass (`npm run check:portability` exits 0 with 0 errors and 0 warnings; `npm test`; `python3 tests/test_sync_skills.py` — 29 tests, 1 platform-specific test skipped; `python3 -m py_compile`; `bash -n`; workflow YAML parse; `git diff --check`). The Windows/macOS runtime matrix is configured but cannot be executed in this Linux session and remains a required remote check.
- [x] Gate 2 — AC #1: pass (both adapter READMEs point deployment to the root `scripts/sync-skills.py`; wrapper source remains forwarding/translation-only; no independent deployment algorithm or provider-private root is presented as the common path)
- [x] Gate 2 — AC #2: pass (Codex and Cursor mechanics retain the private-instruction and anchored-store contracts; both public adapter instruction files require manual copied-block refresh; static source search found no tracked script that writes a private convention file)
- [x] Gate 2 — AC #3: pass (Cursor documents source equivalence and no precedence; the synthetic shared/Claude/Codex/Cursor probe enumerated all four roots, accepted one canonical target, and rejected a divergent target)
- [x] Gate 2 — AC #4: pass (Codex/Cursor claims were checked against current provider documentation and local `codex-cli 0.151.0`; the common engine's canonical directory-link regression is covered without changing canonical workflow semantics)
- [x] Gate 2 — AC #5: pass (CI invokes `npm run check:portability`; final checker and repository-wide current-doc/config closure are green; the three-OS matrix remains externally pending rather than inferred)
- [x] Gate 3 — cross-cutting: pass (Task 9 implementation changes are limited to the listed engine/test, audit, policy, adapter, and workflow surfaces; no runtime artifacts were added; wrapper help parity passed 2/2)

**Status:** Done

### Task 10 — Migrate and verify the Linux user-home roots

**Description:** After repository review and QA pass, apply the common engine to this Linux
computer while preserving the two externally owned canonical-name entries by explicit per-root
policy, and record honest runtime acceptance. This task crosses the live lifecycle boundary and
changes no repository source after the policy implementation is verified.

- **Complexity:** S
- **Estimated time:** 1–2h
- **Depends on:** Task 9; a completed review-implementation pass; a passing `qa-gates` run
- **Can run in parallel with:** None
- **Risk:** High
- **Lifecycle boundary:** live

**External state involved:**

- `~/.claude/skills` — inspect, adopt exact current links, and verify only
- `~/.agents/skills` — inspect, preserve unrelated entries, add approved ai-kit links, and verify
- `~/.claude/ownership/ai-kit-skill-sync.json` — create through the common engine
- `~/.codex/skills` and `~/.cursor/skills` — inspect for attribution/equivalence only; never modify
- The two externally owned `~/.agents/skills/find-skills` and `~/.agents/skills/teach` entries —
  preserve in place with `--preserve agents/find-skills --preserve agents/teach`; do not move or
  overwrite them

**Implementation steps:**

1. Confirm review-implementation and all `qa-gates` evidence is passing or carries an explicitly
   recorded acceptance reason before any live action.
2. Re-verify each external entry is still the user-owned directory or link intended for
   preservation; do not move, rename, overwrite, or discard either entry.
3. Run `python3 scripts/sync-skills.py --dry-run --preserve agents/find-skills --preserve agents/teach`
   and reconcile its inventory. Any extra or changed state stops the task.
4. Require a complete, conflict-free plan for 31 managed Claude links, 29 managed Agents links,
   and 2 explicitly preserved Agents entries. The preserves must not appear in the manifest plan.
5. Run apply with the same preserve flags, then run the qualified read-only check with the same
   flags. Confirm an unqualified check fails closed instead of silently accepting the exception.
6. Run the strict portability checker, both test suites, shell syntax, and repository count probes.
7. Exercise installed Codex and Claude discovery. Record Cursor and any ambiguous legacy-root
   attribution as `passed`, `failed`, `ambiguous`, or `unavailable` with evidence.
8. Confirm legacy provider-private roots, unrelated entries, canonical targets, and the preserved
   external entries remain untouched after the common engine's managed actions.
9. Run the isolated rollback drill; retained preserved entries must remain intact and unowned.

**Testing requirements:**

- Execute techspec scenarios 44–46, 50, and 52 against the normal-home plan only after approval; use the
  Task 1 harness for scenario 51 interruption coverage rather than injecting failure into the
  normal home.
- Compare pre/post child names, entry types, raw/resolved targets, unrelated entries, and legacy
  roots.
- Require the common read-only check and final fail-closed portability checker to exit 0.
- Treat unavailable provider runtimes and source-attribution ambiguity as explicit classifications,
  not successful discovery.

**Acceptance criteria:**

- The qualified common read-only check proves all 31 canonical names are accounted for: 31 managed
  Claude links, 29 managed Agents links, and 2 explicitly preserved entries; every finalized
  manifest record matches live filesystem state.
- The two preserved external entries remain at their original paths and outside the manifest;
  unrelated entries, targets, and legacy roots compare unchanged before and after apply.
- Both repository test suites, strict checker, shell syntax checks, population probes, and the
  repository CI matrix are green.
- Each locally relevant provider has an evidence-backed acceptance classification with no
  unsupported precedence or source-attribution claim.
- An isolated mixed-baseline rollback drill preserves adopted entries, clears fixture-created
  entries, restores fixture-retargeted entries, leaves preserved entries intact and unowned, and
  converges after interruption.

**Reference:** Techspec Phase 4, **Local migration playbook**; test-plan scenarios 44–46, 50, and
51; **Rollback strategy**.

**Rollback plan:** If live acceptance fails, stop and preserve the manifest. With separate explicit
user approval, recover any prepared transaction, preview and run the baseline-restoring uninstall,
verify adopted Claude links are unchanged, and verify the two preserved external entries remain
untouched and unowned. Never touch canonical targets, unrelated entries, or legacy provider-private
roots.

## Verify — 2026-09-01 (preserve-policy implementation)

**Scope:** The explicit per-root preserve policy, its wrapper forwarding, isolated fixtures, and
documentation/spec alignment. The normal-home apply, provider runtime exercise, and rollback remain
the separate live boundary below.

- [x] Gate 1 — build/test: pass (`python3 tests/test_sync_skills.py` — 29 tests, 1 platform-specific
      skip; `npm test`; `npm run check:portability`; Python/Node/POSIX syntax; `git diff --check`).
- [x] Gate 2 — AC checklist: pass for the implementation scope. Isolated tests prove existing
      external entries remain real and content-preserved, qualified check accepts 60 managed links
      plus 2 preserves, unqualified check fails closed, missing/owned preserve entries fail safely,
      and uninstall leaves preserved entries intact. **Accepted:** live-home apply and provider
      runtime ACs are intentionally deferred pending the Gate 5 decision and later runtime evidence.
- [x] Gate 3 — cross-cutting: pass. `--preserve` is validated per managed root, rejected with
      uninstall/prune, forwarded by both PowerShell wrappers, excluded from the manifest, and
      documented in the root, rule, adapter, techspec, analysis addendum, and task playbook. No
      explicit size or SDK budget applies.

## Verify — 2026-09-01 (live migration)

- [x] Gate 1 — build/test and live state: pass. The qualified normal-home check exits 0; the
      manifest has schema 1, 31 Claude records, 29 Agents records, and no prepared transaction.
      The repository test/check/syntax gates remain green after apply.
- [x] Gate 2 — acceptance criteria: pass with explicit runtime classifications. The two preserved
      entries remain real mode-755 directories at their original paths and outside the manifest;
      `.claude/skills` has 31 canonical links and `.agents/skills` has 29 managed canonical links
      plus the 2 preserved directories. The legacy Codex root was not modified. Codex and Claude
      runtime probes were attempted read-only but are classified `unavailable` because Codex
      returned HTTP 401 and Claude reported missing configuration/disabled subscription access;
      Cursor is `unavailable` because `cursor-agent` is not installed.
- [~] Gate 3 — cross-cutting: accepted with reason. The hosted Ubuntu/macOS/Windows matrix cannot
      run from this Linux session; the committed CI workflow remains the required external check.
      No normal-home rollback was run because acceptance passed, and any rollback remains separately
      approval-gated.

## Preflight — 2026-09-01 (read-only)

- [x] `python3 scripts/sync-skills.py --dry-run` against the normal home made no filesystem or
  manifest changes and reported only the two expected unowned canonical-name entries:
  `~/.agents/skills/find-skills` and `~/.agents/skills/teach`.
- [x] Both external paths are mode-755 real directories with no children through depth 2; they
  contain no package or skill files. The user confirmed the explicit preservation policy; no
  ownership manifest exists yet and no backup paths will be created.
- [x] The existing `~/.claude/skills` and legacy `~/.codex/skills` inventories were inspected;
  their canonical links and unrelated provider/system/loop entries remain unchanged. The native
  `~/.cursor/skills` root is absent. No live apply, collision move, manifest write, or legacy-root
  change has occurred.
- [x] The qualified policy command is ready:
  `python3 scripts/sync-skills.py --dry-run --preserve agents/find-skills --preserve agents/teach`.
  It is expected to exit 0 without filesystem or manifest changes and to report 2 preserved
  entries plus 60 managed links.
- [x] Installed provider binaries are present for later runtime checks: Codex `0.151.0`, Claude
  Code `2.1.251`, and Cursor `3.17.21`; discovery exercise remains deferred until the managed roots
  are applied.
- [x] User confirmed option 1 on 2026-09-01: preserve both external entries in place; no collision
  move or backup approval is needed. Separate approval remains required before the live apply and
  any live rollback action.

**Status:** Done

## Deployment sequencing

1. Tasks 1–9 are repository work at the `pre-merge` boundary; none applies to the normal home.
2. Run `review-implementation` after all nine repository tasks are complete.
3. Run `qa-gates` for `linux_portability_cross_agent_coupling`; every gate must pass or carry a
   recorded acceptance reason.
4. Task 10 crossed the `live` boundary on 2026-09-01 after explicit approval, using the confirmed
   preserve flags. Any future normal-home rollback remains separately approval-gated.

## Notes & decisions

- **2026-08-31 — balanced grain:** Ten tasks preserve the four techspec phases while separating
  executable policy, four semantic-risk batches, serialized documentation/final-CI closure, and
  live migration.
- **2026-08-31 — atomic deployment task:** Task 1 is intentionally L and spans seven files because
  the engine, four compatibility wrappers, LF rule, and sole sync harness must prove one contract;
  splitting them would leave wrapper-parity tests without one task owner.
- **2026-08-31 — named test ownership:** `tests/test_sync_skills.py` belongs only to Task 1 and
  `tests/test_skill_portability.mjs` belongs only to Task 2. Later tasks consume those harnesses but
  do not silently create extra test artifacts.
- **2026-08-31 — policy files edited once:** Task 3 combines the Phase 2 and Phase 3 committed edits
  to `audit-skills` and `write-skills` so their profile policy cannot drift across batches.
- **2026-08-31 — staged CI:** Task 3 creates a green transitional matrix; Task 9 modifies the same
  workflow to final fail-closed mode after canonical and documentation closure.
- **2026-08-31 — scenario 43 ownership:** Task 1 owns both the automated fixture and the isolated
  manual whole-root migration rehearsal.
- **2026-08-31 — parallel lists:** The `Can run in parallel with` fields were derived from the
  Depends-On graph; every pair is symmetric.
- **2026-08-31 — PR discipline:** Tasks 1–9 should land as separate reviewable commits/PRs in task
  order, except Tasks 4–7 may be reviewed concurrently as independent semantic batches. Task 10 is
  operational state change and has no repository PR.
- **2026-08-31 — local safety:** Repository completion did not authorize Task 10; the normal-home
  migration remained approval-gated until the explicit live approval recorded below.
- **2026-09-01 — external skill ownership (superseded by source verification below):** The user
  identified both home entries as externally owned skills and requested preserving them outside
  ai-kit ownership. The initial Task 10 run therefore left both paths untouched.
- **2026-09-01 — post-review source verification:** The source lock identifies `find-skills` as
  `vercel-labs/skills` and `teach` as `mattpocock/skills`. After independent review proved the paths
  were empty, the user approved all fixes; the placeholders were backed up and both upstream skills
  were restored at their original paths.
- **2026-09-01 — live safety:** Repository completion does not authorize Task 10. The preserve
  policy is confirmed, but normal-home apply and any rollback remain explicit live approvals.

## Confidence score

**Confidence score: 97% — the reviewed techspec supplies a complete file map and test plan, and the
independent decomposition review closed every verified ownership, sizing, and dependency gap.**

### Why 97%

- **Documentation availability and clarity: 30/30.** The approved techspec defines all phases,
  files, CLI states, preserved contracts, rollback behavior, and test scenarios.
- **Similar patterns found: 24/25.** The analysis and live files provide existing wrapper,
  link-classification, managed-block, strict-YAML, and history-banner patterns.
- **Data-flow and dependency understanding: 20/20.** The sequence traces canonical source through
  checker and wrappers to both managed roots, ownership state, provider discovery, and rollback.
- **Complexity: 14/15.** The oversized semantic batch is split, fail-closed CI has an explicit
  post-neutralization owner, and documentation closure is serial; transaction recovery remains the
  densest task.
- **Potential impact: 9/10.** Normal-home changes are isolated behind review, QA, dry-run, and
  explicit approval; unavailable runtimes still limit direct local proof.

### 3% uncertainty

- **Cross-OS runtime evidence (does not block Task 1):** Windows junction and macOS behavior must be
  proved by the Task 3 matrix before Task 10 can start.
- **Provider presentation (does not block repository tasks):** Cursor is unavailable locally and
  duplicate presentation order is undocumented; the accepted contract is target equivalence only.
- **Live apply (blocks Task 10 only):** the two preserved entries must still be reverified and the
  normal-home apply must be separately approved at execution time.

## Review — 2026-09-01 (reviewed at: fc687c2 +dirty)

**Scope:** Tasks 1–9, including the common sync engine, portability checker, canonical skill edits,
provider adapters, policy/documentation closure, and CI workflow. The native three-worker fan-out
was attempted in parallel but did not return within the bounded five-minute wait; three independent
local review passes then covered correctness, conventions, and simplicity, including one deliberate
second pass over the remaining workflow/config and private-instruction surfaces.

### Findings

- **Critical:** none at the ≥80 confidence threshold.
- **Important — fixed-now (score 85):** `scripts/sync-skills.py:433` skipped symlinked or junctioned
  child directories under the canonical `skills/` tree, while `docs/rules/skill-authoring.md:26`
  allows such external canonical entries. A direct fixture showed a real skill plus a symlinked
  skill enumerating only the real one. The engine now follows directory links for inspection while
  retaining the canonical entry path, and `tests/test_sync_skills.py:220` covers deployment and
  completeness for the linked entry. Confidence: 96% — the pre-fix behavior was directly reproduced
  and the post-fix test passed; cross-platform junction execution remains CI-owned.
- **Important — fixed-now (score 90):** `docs/rules/skill-authoring.md:11` and
  `agentic_auto_scheduling_experimental_study_research_action_items.md:6` still prescribed the
  transitional checker after final CI enforcement. Both now prescribe `npm run check:portability`;
  the transitional command remains only in the package/test implementation and dated verification
  history. Confidence: 98% — current-document search and the final checker confirm closure.
- **Important — follow-up (score 88):** `~/.codex/AGENTS.md:264` contains the copied
  `kit-mechanics` block from the older 2026-08-06 adapter snapshot, including the retired
  `~/.codex/skills` deployment wording. The markers remain intact, and the public Codex adapter
  docs require manual refresh; no repository automation or silent private-file overwrite is
  authorized. Disposition: follow-up for the owner before Codex runtime acceptance in Task 10.
  Confidence: 99% — the private file was read directly; it is outside the public repository diff.

### Ship-ready refactors

- None. The four wrappers are already forwarding/translation-only, and further cleanup would
  expand the reviewed scope without a correctness benefit.

**Review outcome:** 2 fixed-now findings, 1 operational follow-up, 0 Critical findings. The next
step is `qa-gates prefix=linux_portability_cross_agent_coupling`.

## QA — 2026-09-01 (verified at: fc687c2 +dirty)

**Scope:** Prefix Tasks 1–9, repository boundary only. Task 10 remains the separate live-home
boundary and is not included in this QA run.

**Gate plan:** Execute Gates 0–4 against the current tree and record every unavailable external
check or owner-only follow-up explicitly. Gate 5 is the human ship/no-ship decision.

### Gate 0 — scope and artifact integrity

- [x] Reconciled task statuses, acceptance criteria, file map, review stamp, unchecked markers,
      pinned versions, budgets, and untracked artifacts. Tasks 1–9 are Done; Task 10 is Not
      Started by design. The review stamp is `fc687c2 +dirty`; the current diff has 48 tracked
      paths plus six untracked top-level paths (`.github/`, `package-lock.json`, `package.json`,
      `scripts/`, `skills/teach/agents/`, `tests/`). Two generated `__pycache__` directories are
      present below untracked test/source directories and are excluded from the intended source
      file map.

### Gate 1 — build and test

- [x] Local build/test gate passed: `npm ci --ignore-scripts`; `npm test`; `npm run
      check:portability` (31 skills, 0 errors, 0 warnings); `python3 tests/test_sync_skills.py`
      (29 tests, 1 platform-specific skip); Python syntax; both POSIX shell syntax; workflow YAML
      parse; both POSIX wrapper `--help` parity checks; and `git diff --check` all exited 0.
- [~] Remote cross-OS matrix is not executable in this Linux session. The committed workflow
      remains the required Ubuntu/macOS/Windows execution path; acceptance is deferred to hosted
      CI before merge and before Task 10 live runtime acceptance.

### Gate 2 — acceptance criteria

- [x] Gate 2 — AC #1: pass (both adapter READMEs use the root `scripts/sync-skills.py` entry
      point; wrappers remain forwarding/translation-only; no provider-private root is presented
      as the common deployment path).
- [x] Gate 2 — AC #2: pass (the copied-block and anchored-store contracts remain documented;
      private instruction refresh is manual; static source inspection found no tracked script that
      writes a private convention file).
- [x] Gate 2 — AC #3: pass (Cursor documents source equivalence with no precedence promise; the
      four-root synthetic probe accepted one canonical target and rejected a divergent target).
- [x] Gate 2 — AC #4: pass (Codex/Cursor mechanics were checked against current provider evidence
      and local `codex-cli 0.151.0`; the linked-canonical-directory regression is tested without
      changing canonical workflow semantics).
- [~] Gate 2 — AC #5: local pass with explicit remote acceptance reason (final CI invocation,
      final checker, and current repository documentation/config closure pass locally; the hosted
      Ubuntu/macOS/Windows matrix is still pending and is required before merge/live acceptance).

### Gate 3 — cross-cutting invariants

- [x] Gate 3 — environment and release readiness: pass (the workflow matrix is explicitly
      Ubuntu/macOS/Windows with read-only permissions; no `.env*` files were found; normal-home
      state was not touched; no API, schema, auth, payment, or production hot-path change is in
      scope for Tasks 1–9).
- [x] Gate 3 — toolchain and budget: pass (local Node `v24.20.0` and `js-yaml@5.4.1` satisfy the
      Node 24 contract; local Python `3.14.7` satisfies the Python 3.12+ source contract while
      CI pins Python 3.12; LF attributes cover executable sources; no explicit implementation
      line/size budget is specified by the authoritative techspec; `npm ls --depth=0` is minimal).
- [x] Gate 3 — performance: not applicable (the change is a filesystem safety tool and static
      checker; no performance budget or latency-sensitive path is specified).

### Gate 4 — documentation consistency

- [x] Gate 4 — task records: pass (Tasks 1–9 have completed Verify blocks and `Status: Done`;
      Task 10 remains intentionally `Not Started` because it is the post-QA live boundary).
- [x] Gate 4 — documentation/config closure: pass (current documentation prescribes
      `npm run check:portability`; the only remaining transitional command is the intentionally
      retained package script and it is not the shipping/CI command; the final workflow invokes the
      fail-closed command;
      required rule/index/source files exist; adapter and root docs agree on the common two-root
      entry point).
- [x] Gate 4 — review linkage: pass (the review block is stamped at `fc687c2 +dirty` and covers
      Tasks 1–9; this QA block records the current gate evidence and its remote-check limitation).
- [x] Gate 4 — unchecked-marker census: pass with two intentional open items (the Gate 5 human
      decision and Task 10's separate live-apply approval; no completed task contains an unchecked
      acceptance or verification item).

### Gate 5 — human decision

- **Pre-decision result:** Gates 0–4 pass for the repository boundary, with the hosted
  Ubuntu/macOS/Windows matrix recorded as an explicit pending acceptance item. The generated
  local `__pycache__` directories are verification artifacts below untracked source/test roots,
  not intended repository deliverables.
- **Live-boundary safeguards:** A GO here does not approve the normal-home apply or rollback
  actions. Task 10 must use the confirmed preserve flags and obtain separate explicit approval for
  each live state-changing action.
- [x] User approved the recorded QA result and the normal-home apply on 2026-09-01; the live
      verification and runtime classifications are recorded in the Task 10 blocks below.

## Review — 2026-09-01 (preserve policy; reviewed at: fc687c2 +dirty)

**Scope:** The post-QA preserve-policy change only: `scripts/sync-skills.py`, both PowerShell
translators, the sync test additions, and the associated root/rule/adapter/spec/task documentation.
The review used three independent sequential passes because native worker fan-out was unavailable.

### Findings

- **Critical:** none at the ≥80 confidence threshold.
- **Important:** none. Pass 1 verified that preserved entries are existing directories or links,
  remain outside the ownership manifest, cannot hide an owned record, and cannot be combined with
  uninstall/prune. Pass 2 verified common CLI and PowerShell forwarding parity plus the explicit
  qualified-check requirement. Pass 3 verified isolated preservation, fail-closed unqualified
  behavior, uninstall retention, and no change to the 31-skill source checker.
- **Follow-up:** the normal-home apply and provider runtime checks remain intentionally pending the
  Gate 5 decision and are not represented as completed by this review.

**Confidence:** 97% — the implementation is covered by isolated tests and a real-home dry-run;
the remaining uncertainty is limited to unexecuted cross-OS/provider runtime evidence and the
not-yet-approved live state change.

## QA — 2026-09-01 (preserve policy; repository boundary)

**Scope:** Preserve-policy implementation and documentation alignment after the earlier prefix QA.
Task 10 was `Not Started` when this repository-boundary QA was recorded; its later live verification
below records the approved apply. No rollback was needed.

### Gate 0 — scope and artifact integrity

- [x] Pass. The reviewed change is limited to the common sync policy, PowerShell argument
      forwarding, isolated sync tests, and the root/rule/adapter/spec/task documentation. The
      source portability contract remains 31 canonical skills.

### Gate 1 — build and test

- [x] Pass. `npm ci --ignore-scripts`, `npm test`, and `npm run check:portability` pass with 31
      skills, 0 errors, and 0 warnings. `python3 tests/test_sync_skills.py` passes 29 tests with
      1 platform-specific skip; Python/Node/POSIX syntax, workflow YAML parsing, and `git diff
      --check` also pass.
- [~] The hosted Ubuntu/macOS/Windows matrix remains unavailable in this Linux session and is
      still required before live provider acceptance.

### Gate 2 — acceptance criteria

- [x] Preserve behavior: isolated fixtures prove two external entries remain real and content-
      preserved, stay out of the manifest, survive uninstall, and are accepted only when explicitly
      named for the managed root.
- [x] Safety behavior: missing, invalid, or already-owned preserved entries fail before mutation;
      unqualified normal-home dry-run still exits 1 with exactly the two expected entries.
- [x] Contract behavior: qualified normal-home dry-run exits 0 with `adopt=31`, `create=29`, and
      `preserved=2`; both PowerShell wrappers expose `-Preserve` forwarding.
- [x] Source contract: the strict portability checker remains source-level and passes the 31-skill
      corpus; no canonical `find-skills` or `teach` body was changed for this policy.
- [~] At the time of this repository-boundary QA, live apply and provider discovery were pending
      Gate 5 and cross-OS/runtime evidence; the later live verification records the actual outcome.

### Gate 3 — cross-cutting invariants

- [x] Pass. No API, schema, auth, data, or production hot-path change is in scope. No explicit
      implementation size budget applies. Preserve flags are rejected with uninstall/prune and do
      not alter manifest schema or legacy-root behavior.

### Gate 4 — documentation consistency

- [x] Pass. Root README, authoring rules, both adapter READMEs/AGENTS files, techspec, analysis
      decision addendum, and Task 10 use the same per-root preserve semantics and population
      counts. The task has a verification block and three observation entries.

### Gate 5 — human decision

- **Result:** Repository-boundary QA passes with the hosted matrix and live-home/provider checks
  explicitly pending.
- **Decision resolved:** approved on 2026-09-01. The normal-home apply used
  `--preserve agents/find-skills --preserve agents/teach`; any rollback remains a separate explicit
  approval.

## QA — 2026-09-01 (post-live migration)

**Scope:** Prefix `linux_portability_cross_agent_coupling`, Tasks 1–10, including the approved
normal-home apply. This is the final prefix QA record; earlier QA blocks retain their pre-live
context.

### Gate 0 — scope and artifact integrity

- [x] Pass. Tasks 1–10 are marked `Done`; the repository change set and the live-home state are
      recorded separately. No legacy provider-private root or canonical target was a mutation
      target.

### Gate 1 — build and test

- [x] Pass. `npm test`, `npm run check:portability`, `python3 tests/test_sync_skills.py` (29 tests,
      1 platform-specific skip), Python/Node/POSIX syntax, workflow YAML parsing, and `git diff
      --check` pass. The qualified normal-home check also exits 0.
- [~] Accepted limitation: the hosted Ubuntu/macOS/Windows matrix cannot be executed from this
      Linux session; its committed workflow remains the external cross-OS verification owner.

### Gate 2 — acceptance criteria

- [x] Pass. The live manifest contains 31 Claude records and 29 Agents records, with no prepared
      transaction; the qualified check accounts for all 31 canonical names through 60 managed links
      plus 2 explicit preserves.
- [x] Pass. `~/.agents/skills/find-skills` and `~/.agents/skills/teach` remain real mode-755
      directories at their original paths and are absent from ownership records. Unqualified check
      fails closed on exactly those entries.
- [x] Pass. Repository tests, strict checker, shell checks, population checks, and the isolated
      rollback/interruption fixtures are green.
- [~] Accepted limitation: Codex and Claude read-only runtime probes were unavailable (Codex HTTP
      401; Claude missing configuration and disabled subscription access); Cursor is unavailable
      because `cursor-agent` is not installed. No provider was marked passed from side effects.

### Gate 3 — cross-cutting invariants

- [x] Pass. The sync engine touched only the two managed roots and the anchored ownership manifest;
      `.codex/skills` and the absent `.cursor/skills` root were not modified. No API, schema, auth,
      data, or production hot-path change is involved. Rollback was not run because acceptance
      passed and remains separately approval-gated.

### Gate 4 — documentation consistency

- [x] Pass. The root README, authoring rule, provider adapters, analysis addendum, techspec, and
      Task 10 all describe the same preserve policy and live population. The live verification,
      review, QA, and observation records are present.

### Gate 5 — human decision

- [x] Pass. The user explicitly approved the live apply on 2026-09-01. The apply completed using
      the two preserve flags; no rollback approval was requested or used.

## Post-review remediation — 2026-09-01

**Target:** Independent read-only review findings across Tasks 1, 2, 3, and 10.

**Implementation:**

- Added durable per-action replacement progress before a retarget/restore unlink. Recovery now
  accepts an absent path only when the prepared manifest records that exact authorized transition.
- Added interruption fixtures after replacement authorization and after unlink for both checkout
  retarget and baseline restore paths.
- Tightened `--preserve` so a directory/link must contain a readable `SKILL.md`; empty placeholders
  fail closed instead of being counted as usable external skills.
- Recovered the two external live skills from their lock-recorded upstream sources. Empty originals
  are retained under `~/.agents/skill-backups/2026-09-01-portability-review/`; `find-skills` is from
  `vercel-labs/skills` and `teach` is from `mattpocock/skills`.
- Added Cursor overlay shape validation for string/list `paths`, non-empty string `icon`, and the
  documented `color` enum, plus malformed-value fixtures.
- Added Python bytecode exclusions, repaired the overview/truncated ledger text, and added manual
  workflow dispatch. The earlier QA block is a dated historical result and is superseded by the
  verification below.

**Acceptance criteria:**

- [x] A retry converges after interruption immediately before or after a replacement unlink, while
  an unrecorded third state still fails closed.
- [x] Empty preserve directories fail; valid external skills pass the qualified live check and stay
  outside the ownership manifest.
- [x] Malformed Cursor overlay shapes fail with field-specific diagnostics; valid documented shapes
  pass.
- [x] Repository tests, strict checks, syntax checks, and diff hygiene pass with generated Python
  caches ignored.
- [x] Documentation distinguishes local verification from the hosted Ubuntu/macOS/Windows matrix;
  the matrix remains required after the workflow is committed and pushed.

**Status:** Implemented; verification recorded below. Hosted cross-OS execution remains an explicit
external evidence item rather than a claimed local result.

## Verify — 2026-09-01

**Task ID:** Post-review remediation

**Prefix:** `linux_portability_cross_agent_coupling`

**Files:** `scripts/sync-skills.py`, `tests/test_sync_skills.py`,
`scripts/check-skill-portability.mjs`, `tests/test_skill_portability.mjs`, `.gitignore`,
`.github/workflows/portability.yml`, `README.md`, `docs/rules/skill-authoring.md`, and the three
prefix documents. Live scope is limited to the two external skill paths and their dated backup.

**Budgets:** no line budget pinned (acceptable). Node 24 and `js-yaml@5.4.1` remain the pinned
toolchain contract.

- [x] Gate 1 — build/test: pass (`npm test`; `npm run check:portability`; sync harness 33 tests,
  one Windows-only skip; Python/Node/POSIX/workflow syntax; `git diff --check`).
- [x] Gate 2 — AC checklist (5 items): pass.
  - [x] AC #1 — interruption after durable authorization and after unlink converges for retarget and
    restore; a real-directory third state is rejected and its sentinel remains unchanged.
  - [x] AC #2 — empty preserve fixture fails; qualified live check passes with 60 managed links and
    two validated external skills; manifest transaction is null and Agents records remain 29.
  - [x] AC #3 — valid string/list/icon/color fixtures pass; malformed values emit
    `cursor-paths-shape`, `cursor-icon-shape`, or `cursor-color-shape`.
  - [x] AC #4 — all repository checks pass; `git check-ignore` attributes both Python cache probes
    to `.gitignore:5`.
  - [x] AC #5 — local evidence is green and the task/techspec explicitly retain hosted matrix
    execution as a publication-time external item.
- [x] Gate 3 — cross-cutting: pass (no environment matrix or line budget; Node `24.x` and
  `js-yaml@5.4.1` match package and lock; replacement authorization preserves rollback safety;
  no API/schema/auth/performance surface; live changes were limited to the two external skill
  paths plus their recoverable empty-directory backup).

## Review — 2026-09-01 (reviewed at: fc687c2+dirty)

**Scope:** Post-review remediation implementation and its new tests.

**Reviewers run:** three independent sequential passes under the Codex fan-out fallback:
correctness/safety, conventions/test coverage, and simplicity/ship readiness. Each pass included
the required deliberate second sweep and reported only findings scoring at least 80.

**Findings:** none at or above the reporting threshold. The replacement transition is durably
authorized before unlink, unexpected third states remain conflicts, preserved entries require a
real skill envelope, and Cursor overlay values now match the documented shapes.

**Ship-ready refactors:** none. Deduplicating the small readable-`SKILL.md` probe would be cosmetic
and was intentionally left out of this focused correction.

**Disposition:** proceed to prefix QA. No follow-up finding remains open from this review.

## QA — 2026-09-01 (verified at: fc687c2+dirty; post-review remediation)

- [x] Gate 1 — build/test: pass (`npm test`; final portability checker 31 skills, zero
  errors/warnings; sync harness 33 tests with one Windows-only skip; Python/Node/POSIX/workflow
  syntax; `git diff --check`).
- [~] Gate 1 — committed: no. The implementation and QA artifact remain in the working tree at
  `fc687c2+dirty`, pending the user's final review and commit decision.
- [x] Gate 2 — AC checklist: pass. The five remediation ACs pass, the qualified live check reports
  60 managed links plus two external skills, the manifest is finalized at 31/29 records, and the
  skills CLI discovers both external entries from `~/.agents/skills`.
- [x] Gate 3 — cross-cutting: pass. No environment asymmetry or line budget applies; Node `24.x`
  and `js-yaml@5.4.1` remain pinned; rollback authorization and third-state refusal are tested;
  bytecode caches are ignored; legacy roots remain outside ownership. Hosted matrix execution is a
  named publication boundary, not local evidence.
- [x] Gate 4 — docs consistency: pass. README, authoring rule, analysis correction, techspec
  correction, task overview, review, and QA agree. Unchecked-box census: zero. Historical
  `Not Started` references occur only inside dated pre-live QA context and are retained as history.
- [ ] Gate 5 — human go/no-go: PENDING. The tree is dirty and the hosted Ubuntu/macOS/Windows
  workflow cannot run until the new workflow and implementation are committed and pushed. Awaiting
  the user's decision whether to commit/push and trigger the external matrix.

## Hosted CI remediation — 2026-09-01

**Run:** `33519064448` at `f0b3ca6` — Ubuntu passed; macOS failed `Check POSIX adapter syntax`;
Windows failed `Run portability fixtures`.

**Root causes:**

- Both POSIX wrappers used Bash 4.2's `[[ -v VAR ]]` even though the macOS runner uses Bash 3.2.
- `find-skills` was locked by its LF byte hash while Markdown checkout EOL was unspecified. A
  Windows CRLF checkout therefore produced a different digest with identical skill text.
- The workflow's multi-path `bash -n` call parsed the first wrapper and passed the second path as a
  positional argument instead of independently checking both files.

**Fixes implemented locally:**

- Replaced `[[ -v VAR ]]` with Bash-3-compatible `${VAR+x}` checks in both POSIX wrappers.
- Normalized CRLF to LF only for the neutral-reference digest and added a CRLF regression fixture;
  the existing semantic-change fixture remains fail-closed.
- Changed the workflow syntax step to iterate over both wrappers independently.

**Local verification:** `npm test`, `npm run check:portability`, 33 sync tests (one Windows-only
skip), both wrapper syntax checks, private-home override exit-2 behavior, and `git diff --check`
pass. A fresh hosted matrix remains required before Gate 5 can be marked complete.
