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
| 1 | Build the common sync engine and compatibility surface | L | 6–8h | — | Not Started |
| 2 | Build the strict portability checker | M | 3–4h | Task 1 | Not Started |
| 3 | Enforce provider profiles in policy and transitional CI | M | 3–4h | Task 2 | Not Started |
| 4 | Neutralize low-risk invocation and handoff wording | M | 3–4h | Task 3 | Not Started |
| 5 | Neutralize research and discovery workflows | M | 3–4h | Task 3 | Not Started |
| 6 | Neutralize review, design, and learning workflows | M | 3–4h | Task 3 | Not Started |
| 7 | Neutralize routing, orchestration, and maintenance workflows | M | 3–4h | Task 3 | Not Started |
| 8 | Reconcile public, policy, and historical documentation | M | 2–4h | Tasks 4, 5, 6, 7 | Not Started |
| 9 | Reconcile provider mechanics and enforce final portability | M | 2–4h | Task 8 | Not Started |
| 10 | Migrate and verify the Linux user-home roots | S | 1–2h | Task 9 + review/QA gates | Not Started |

**Overall Progress**: 0/10 tasks completed (0%)

**Last Updated**: 2026-08-31

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

**Status:** Not Started

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

**Status:** Not Started

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

**Status:** Not Started

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

**Status:** Not Started

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

**Status:** Not Started

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

**Status:** Not Started

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

**Implementation steps:**

1. Read and snapshot all four files before editing, including anchored maintenance paths, approval
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

**Rollback plan:** Restore the four files as one high-risk batch, rerun the semantic probes, and
keep the checker in transitional mode until a corrected batch is ready. Anchored maintenance data
is never migrated or rewritten by this task.

**Status:** Not Started

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

**Rollback plan:** Restore the seven documentation files together so population counts, entry
points, and supersession status cannot become partially inconsistent. Repository code and canonical
skills remain functional.

**Status:** Not Started

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

**Rollback plan:** Restore the four adapter documents together and return the workflow invocation to
Task 3's explicit transitional mode. Reapply only after the mechanics claims, common-entry links,
and final checker results are internally consistent. The thin wrappers from Task 1 remain
operational.

**Status:** Not Started

### Task 10 — Migrate and verify the Linux user-home roots

**Description:** After repository review and QA pass, apply the common engine to this Linux
computer, resolve the two known real-directory collisions only with explicit user approval, and
record honest runtime acceptance. This task crosses the live lifecycle boundary and changes no
repository source.

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
- The two expected `~/.agents/skills/find-skills` and `~/.agents/skills/teach` collisions — move to
  named sibling backups only after separate explicit approval

**Implementation steps:**

1. Confirm review-implementation and all `qa-gates` evidence is passing or carries an explicitly
   recorded acceptance reason before any live action.
2. Run the common dry-run and reconcile its actual conflict inventory with the two expected names;
   any extra or changed state stops the task.
3. Re-verify each collision is an empty, unrelated, non-package-managed real directory. Ask for
   explicit approval before moving either entry to a named sibling backup.
4. After approved backups, rerun dry-run and require a complete, conflict-free plan for both roots.
5. Run apply, read-only check, strict portability checker, both test suites, shell syntax, and
   repository count probes.
6. Exercise installed Codex and Claude discovery. Record Cursor and any ambiguous legacy-root
   attribution as `passed`, `failed`, `ambiguous`, or `unavailable` with evidence.
7. Confirm legacy provider-private roots, unrelated entries, canonical targets, and collision
   backups remain untouched after the common engine's managed actions.
8. Retain backups until runtime acceptance and an isolated rollback drill have both passed.

**Testing requirements:**

- Execute techspec scenarios 44–46 and 50 against the normal-home plan only after approval; use the
  Task 1 harness for scenario 51 interruption coverage rather than injecting failure into the
  normal home.
- Compare pre/post child names, entry types, raw/resolved targets, unrelated entries, and legacy
  roots.
- Require the common read-only check and final fail-closed portability checker to exit 0.
- Treat unavailable provider runtimes and source-attribution ambiguity as explicit classifications,
  not successful discovery.

**Acceptance criteria:**

- The common read-only check proves every canonical skill resolves from each managed root and every
  finalized manifest record matches live filesystem state.
- The two approved collision backups remain recoverable; unrelated entries, targets, and legacy
  roots compare unchanged before and after apply.
- Both repository test suites, strict checker, shell syntax checks, population probes, and the
  repository CI matrix are green.
- Each locally relevant provider has an evidence-backed acceptance classification with no
  unsupported precedence or source-attribution claim.
- An isolated mixed-baseline rollback drill preserves adopted entries, clears fixture-created
  entries, restores fixture-retargeted entries, and converges after interruption.

**Reference:** Techspec Phase 4, **Local migration playbook**; test-plan scenarios 44–46, 50, and
51; **Rollback strategy**.

**Rollback plan:** If live acceptance fails, stop and preserve the manifest and collision backups.
With separate explicit user approval, recover any prepared transaction, preview and run the
baseline-restoring uninstall, verify adopted Claude links are unchanged, and restore the two named
collision backups to their original names. Never touch canonical targets, unrelated entries, or
legacy provider-private roots.

**Status:** Not Started

## Deployment sequencing

1. Tasks 1–9 are repository work at the `pre-merge` boundary; none applies to the normal home.
2. Run `review-implementation` after all nine repository tasks are complete.
3. Run `qa-gates` for `linux_portability_cross_agent_coupling`; every gate must pass or carry a
   recorded acceptance reason.
4. Only then start Task 10 at the `live` boundary, with explicit approval for each collision backup
   and for any rollback action against the normal home.

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
- **2026-08-31 — local safety:** Repository completion does not authorize Task 10. The normal-home
  collision moves, apply, and any rollback remain explicit live approvals.

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
- **Live collision disposition (blocks Task 10 only):** the two current real-directory collisions
  must still be reverified and separately approved at execution time.
