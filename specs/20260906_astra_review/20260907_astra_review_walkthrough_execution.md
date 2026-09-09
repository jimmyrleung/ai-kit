# Walkthrough follow-up execution — 2026-09-07

Scope: WB01–WB03 from [the owner-approved backlog](20260907_astra_review_walkthrough_backlog.md).
Status: WB01–WB03 Done; owner GO granted on 2026-09-08, with commit and push authorized.
The 2026-09-08 QA record supersedes the original staging, commit and publication restrictions.
The owner's pre-existing `SESSION_LOG.md` changes are excluded and preserved.

## Implementation decisions

**WB01:** maintain common rules under `docs/contracts/`, plus the existing provider and filename
references. `scripts/bundle-skill-references.mjs` follows each skill's local shared-reference
links and their transitive document dependencies. It writes owned copies under that skill's
`references/shared/`, with source identity and maintainer instructions. Inline links and
reference definitions retain local destinations and anchors. Generation preflights the graph
and output ownership; unchanged outputs keep their bytes and modification times.

Maintainers run `npm run build:skill-references` after changing shared sources. The normal
`npm run check:portability` path checks copies without writing and rejects missing/stale copies.
Copy the complete skill folder for detached installation. Symlinks expose checkout edits,
including uncommitted edits, but do not fetch upstream changes or generate shared references.
Other invoked skills and tools remain explicit workflow prerequisites. Repository-maintenance
tools run against the target ai-kit checkout; detached users do not need original source docs
to read the skill's supporting rules.

**WB02:** read all 31 canonical skill bodies, retain `teach`'s short description and explicit
invocation metadata, and revise 30 description scalars. Preserve other frontmatter and body
bytes during this pass. Workflow details already present in bodies remain there. The neutral
`find-skills` checksum was deliberately refreshed for its approved description-only change.

Measured against the captured pre-WB tree: parsed descriptions 16,694 → 10,733 characters
(35.71% reduction); complete frontmatter 18,232 → 12,287 characters (32.61% reduction).
These are character measurements, not measured token or cost savings. Body/reference sizes
are tracked separately; generated copies and the explicit scoring reference add stored text.
Main-body characters changed from 401,717 to 406,972 against this captured baseline. There are
79 generated references across 26 skill folders, totaling 490,294 stored characters; this
duplicated distribution text is not a claim that every invocation loads all copies.

**WB03:** add an explicit confidence contract and required local references in nine consumers:
analysis, design, task decomposition, implementation, task verification, QA, artifact review,
implementation review and diagnosis. Each stage has a weighted rubric, evidence, uncertainty
consequences, next checks and an advancement verdict. Normal threshold is 90%; applicable
stricter policy wins. Declared active-P1 threshold/depth survives downstream handoffs, including
QA mode resolution. Scores remain heuristic judgments and cannot substitute for required
evidence, executed checks, causal confirmation or human authorization.

## Verification plan and evidence boundary

The pre-WB snapshot is the comparison base for this incremental change. Git HEAD is
`aeec06bfa0a6b97402b17824d957f29635f40ba7`; the larger Astra implementation predates this snapshot.
This review will not relabel that earlier evidence as covering the new WB bytes. New evidence
will include source/configuration identities, baseline comparisons, model prompts and actual
outputs, review findings/dispositions, and command records.

- WB01: detached file resolution; shared-source propagation; unchanged-run idempotence;
  missing/stale/transitive/ownership/link fixtures; a representative copied-skill agent task;
  existing sync suite and consistent installation/authoring instructions.
- WB02: exact description/frontmatter measurements and byte-preservation checks; fresh blind
  baseline/candidate roster simulations covering positive, neighboring and non-trigger cases;
  metadata/portability validation. Roster simulation does not establish native discovery.
- WB03: actual copied-skill analysis, design and task outputs with private project instructions
  disabled; stricter-policy, missing critical evidence and active-P1 handoff slices; source
  reconciliation across consumers. Reporting slices are not full pipeline executions.

The initial three native trials used an extra filesystem mount fixture and failed before skill
reads because local process launches returned EACCES. Those attempts are retained as blocked,
not successes. Retry trials retain the native workspace-write sandbox and disable project
instruction loading; source-checkout access is outside their explicit scope. File-resolution
tests establish detached paths separately from actual agent behavior.

Hosted Windows/macOS/Python-3.12 CI remains owner-deferred from B32. Claude Code and Cursor
native proof remain under the earlier B17 limitations. Linux checks and Codex trials cannot
be promoted into proof for those environments. Final owner GO and any commit remain pending.

## Review — 2026-09-07

Independent lanes cover (1) packaging/tooling/installation and (2) description and confidence
semantics. Authors are separate from these reviewers. Each lane performs one additional pass
over initially skipped scope, distinguishes severity from certainty, and records actual hashes.
Both lanes concluded with no open supported in-scope findings after targeted correction checks:

| Finding | Effect | Disposition |
|---|---|---|
| WB01-PKG-01 — reference-style Markdown links missed | Generation could retire required copies and still pass validation | Fixed; original direct/transitive reproductions and added regression fixtures pass |
| SEM-01 — inherited P1 depth did not explicitly set QA mode | A policy-only handoff could fall back to full depth | Fixed; source re-read and the P1 reporting slice preserve streamlined QA mode |
| WB03-ARITH-01 — model summed task factors incorrectly | A displayed score could disagree with its own calculation | Fixed procedure requires available calculation tooling; failed output retained; fresh full task trial executes arithmetic and reports the correct total |

Record `WB01-packaging-review-20260907-03` covers generator, checker integration, tests,
packaging links, generated graph and installation/authoring guidance. The separate semantic
review covers all description pairs, preserved metadata, the scoring contract and nine complete
consumer bodies. Their original findings, corrected verdicts and inspected-byte manifests are
preserved in the evidence archive. Source identities were rechecked during consolidation.
Subsequent backlog status/evidence additions are documentation closeout, with unchanged ACs;
they do not silently replace the original reviewed requirement bytes.

## Acceptance evidence

Full prompts, fixtures, frozen procedure bytes, actual outputs, grading, source manifests and
command logs are in [the evidence index](tests/skill-outcomes/runs/walkthrough-20260907/README.md).
The source/check manifest contains 149 relevant input files; `SESSION_LOG.md` is excluded and
verified unchanged from the captured pre-WB snapshot.

| Criterion | Result and evidence |
|---|---|
| WB01.1 — detached required documents and representative task | PASS within tested scope: independent local-target checks plus actual copied-skill analysis/design/tasks. Successful traces read local procedures; none accessed the source checkout. Physical source absence was not established by the blocked mount attempt. |
| WB01.2 — shared edits propagate; unchanged generation stays unchanged | PASS: source mutation updates every affected copy; unchanged writes preserve bytes and mtimes in executed fixtures. |
| WB01.3 — normal validation detects stale/missing dependencies | PASS: final-check fixtures exercise direct/transitive missing/stale copies, unknown sources, reference definitions and ownership/link rejection. |
| WB01.4 — whole-checkout install and consistent guidance | PASS locally: sync suite plus isolated-home preview/apply/check; 31 skills resolve in each managed root. Root/adapter/authoring docs describe generation, symlinks and detached updates. |
| WB02.1 — purpose/triggers/neighbor boundaries retained | PASS in source review and fresh blind roster trials; process details remain in bodies. |
| WB02.2 — all descriptions inspected; metadata preserved | PASS: 31 paired inspections, 30 approved scalar edits, `teach` retained; non-description metadata and its explicit-invocation overlay unchanged. |
| WB02.3 — measured size, separate body/reference accounting | PASS: before/after measurements above; no token, cost or load-all claim. |
| WB02.4 — fresh positive/neighbor/non-trigger trials | PASS for this fixture: baseline 99/100; candidate 100/100 against the prewritten key. The baseline miss was the committed-but-unshipped implementation tour. Roster simulation is not native discovery. |
| WB02.5 — shipping checks, no broad analyzer rewrite | PASS: strict metadata/portability checks and scoped diff; analyzer structure retained. |
| WB03.1 — explicit score, rubric, evidence, gaps and next checks | PASS in source and three real document outputs; no private confidence format supplied. |
| WB03.2 — workflow rubrics and stricter applicable policy | PASS: analysis 40/40/20, design 30/25/20/15/10 and decomposition 35/25/25/15 applied; stricter fixture retains 98 and calculates 94. |
| WB03.3 — thresholds, handoffs and independent evidence gates | PASS: stricter case blocks dependent approval while permitting independent work; missing real-database integration stays BLOCKED despite earlier score 97; policy-only P1 handoff selects streamlined QA. |
| WB03.4 — severity, certainty, causality and permission separate | PASS in source review and P1 reporting slice: possible branch remains a candidate, with a discriminating probe and no remediation permission. |
| WB03.5 — bundled scoring, public-context outputs and boundary cases | PASS within tested Codex scope: three documents plus three reporting/handoff slices. Public copies and `project_doc_max_bytes=0` were used; no private policy/store reads appear in successful traces. |

Native retry outputs: analysis score 99; design 98. Their factor arithmetic checks pass.
The initial tasks output reported 98 from contributions totaling 99.05: a failed arithmetic
result, preserved in evidence. The contract now requires a calculator/executed expression when
available and labels unavailable arithmetic verification. The fresh full tasks trial executed
`awk` arithmetic, reported 100 from checked contributions 35+25+25+15, preserved scope limits,
and left implementation/tests Not Started. Its procedure copies match final source bytes.
Analysis/design and boundary outputs predate this arithmetic-only refinement; their unchanged
factor/policy semantics were rechecked against source, and their arithmetic was independently
recalculated. Those earlier runs are not presented as executions of the later instruction.
The boundary slice returns stricter analysis 94/98 (blocked), migration verification 37 with
required integration BLOCKED, and candidate P1 diagnosis 39/70 (causality still unconfirmed).
These selected numbers are observations, not expected-score targets or calibration evidence.
Native CLI requested `gpt-5.6-sol`; provider-resolved model identity was not independently
exposed. Independent review/routing workers inherited the parent session configuration.

The main task trials used a tiny stdlib fixture and explicit invocation of copied procedures.
They establish representative local task behavior, not broad reliability, native discovery,
cross-provider parity or a full incident/review/QA pipeline. The task-decomposition trial used
the explicitly selected, supported spec-carrying path with an approved locked plan.

## QA — 2026-09-07

- [x] Gate 1 — build/test: `npm ci`, `npm test`, final portability and bundle checks, Python compilation, and sync suite passed. Sync suite ran 41 tests, with one Windows-only test skipped. Linux execution only; hosted matrix remains deferred.
- [x] Gate 2 — AC checklist: all 14 scoped criteria mapped above; no provider/native-discovery overclaim.
- [x] Gate 3 — cross-cutting: strict metadata and generated ownership checks pass; Node 24 requirement and locked dependency verified; no arbitrary size quota. Isolated-home dry-run/apply/check succeeds. No source/check-input drift after validation.
- [x] Gate 4 — docs consistency: root/adapter/authoring guidance matches implementation; backlog and this record reconcile current WB status while preserving earlier Astra evidence and pending owner/platform boundaries.
- [ ] Gate 5 — human go/no-go: reserved for owner review; no GO or commit inferred.

Final affected validation is `WB-check-12` through `WB-check-17`; earlier dependency installation
and Python compilation are recorded in `WB-check-01` and `WB-check-05`, with their unchanged
relevant inputs. Corrected isolated-home setup is `WB-check-09` through `WB-check-11`, followed
by the current completeness check. `WB-check-08` failed because its fixture home did not yet
exist; that setup failure is preserved. The home was created before a new preview and apply.
All checks ran on the uncommitted tree. No release/deployment or perf-sensitive application
surface changed. There is no separate compiled application build; Node and Python entrypoints
are exercised by the repository's validation commands. Rollback is the scoped pre-WB snapshot
plus regeneration of maintained references, preserving unrelated original Astra work.

## Confidence and remaining boundaries

Confidence: **96%** in readiness for owner review. Effective policy is the owner's supplied
30/25/20/15/10 rubric and 90% minimum, within already authorized local implementation/validation.

| Factor | Weight | Rating | Contribution | Evidence / gap |
|---|---:|---:|---:|---|
| Documentation clarity | 30 | 98 | 29.40 | Explicit WB criteria and reconciled install/authoring guidance |
| Inspected suitable patterns | 25 | 96 | 24.00 | Existing checker/test/sync structure reused; independent review |
| Dependencies and data flow | 20 | 96 | 19.20 | Transitive graph, caller policy chain, metadata and detached traces |
| Complexity understood | 15 | 95 | 14.25 | Bounded generator, focused scalar changes, corrected parser/depth cases |
| Cross-system impact | 10 | 90 | 9.00 | Linux/native-Codex evidence; hosted platforms and other providers deferred |
| **Total** | **100** | | **95.85 → 96** | Heuristic judgment, not a success probability |

**4% uncertainty:** representative tasks cannot establish general model reliability; native
discovery and the deferred provider/platform checks need their actual environments. Those
limits prevent claims of universal parity or release approval, while the owner-approved
ready-for-review scope is satisfied. Next action is owner review; any eventual commit and
hosted CI keep their existing authorization boundaries. The score does not supply Gate 5 GO.

## Fresh review correction — 2026-09-07

**F1 fixed; independent targeted recheck is clean.** The fresh review found that a
single-quoted Markdown link title could make the bundler overlook a required dependency,
retire its bundled copies, and then report a clean check. Destination extraction now runs
independently of optional title syntax and accepts next-line destinations. It deliberately
collects destination prefixes conservatively; it is not a full Markdown validator.
The syntax context is documented in CommonMark's [link titles](https://spec.commonmark.org/0.31.2/#link-title)
and [reference definitions](https://spec.commonmark.org/0.31.2/#link-reference-definitions).

Regression coverage exercises six forms as direct and transitive dependencies: single-quoted
and parenthesized titles, angle-wrapped destinations with next-line titles, next-line inline
destinations, and plain/angle-wrapped next-line reference definitions, including CRLF/tab
indentation. Required copies, rewritten links, missing-copy detection/repair, and unknown-path
rejection before mutation are asserted. The independent reviewer also checked unused owned
copy retirement and unchanged generation. The maintained bundles need no content changes.

The original multiline review fixture inherited a sentence's trailing period, producing
`feedback.md.` rather than the intended `feedback.md`. The corrected parser properly rejects
that unknown path. A separately newline-terminated fixture verifies the intended case.
The original finding remains supported by the single-title reproduction; failed and confounded
probes are retained with corrected attribution in the independent correction report.

| Current correction check | Result |
|---|---|
| `WB-F1-check-01`: `npm test` | PASS, including the new dependency-syntax regressions |
| `WB-F1-check-02`: `npm run check:portability` | PASS |
| `WB-F1-check-03`: `npm run check:skill-references` | PASS; existing bundles match |
| `WB-F1-check-04`: `python tests/test_sync_skills.py` | PASS; 41 tests, one Windows-only skip |
| `WB-F1-check-05`: `git diff --check` | PASS |
| Independent targeted review | F1 fixed; fresh Node tests and both checks pass |

Current source identities, check logs, original review, correction report and probes are in
[review-correction.zip](tests/skill-outcomes/runs/walkthrough-20260907/review-correction.zip),
identified by its [manifest](tests/skill-outcomes/runs/walkthrough-20260907/review-correction-manifest.json).
This supplement supersedes the earlier parser/test identities and their affected validation
coverage. The original evidence archive remains unchanged as the pre-correction record;
earlier description/confidence trials retain their original scope. The original WB acceptance
criteria are unchanged.

The supplement also records routing dispatch briefs and task identities reconstructed from
the parent conversation. These describe the requested fresh/blind contexts and associate their
outputs, but are **not original raw runtime receipts** or independent proof of hidden context.
No routing or native-provider trial was rerun for this parser correction.

Confidence: **96%** in the targeted correction, using the owner's rubric: ratings
98/97/97/96/90 at weights 30/25/20/15/10 yield 96.45, rounded to 96 (executed arithmetic in
the independent report). **4% uncertainty:** nonexhaustive Markdown coverage and unchanged
native-platform/provider limits. Existing owner GO, hosted CI and commit boundaries remain.

## QA — 2026-09-08 (owner GO)

<!-- evidence:begin walkthrough-shipping-20260908 -->
The owner approved both efforts and instructed committing/pushing everything. This
supersedes the earlier pending GO and commit restrictions in this execution record,
the walkthrough backlog and historical evidence metadata. WB01–WB03 are accepted
within their documented scope; failed trials and external limitations remain visible.

- [x] Gates 1–4 — fresh shipping checks pass and prior reviewed source identities match;
  see [the shared shipping QA](20260906_astra_review_execution.md#qa--2026-09-08-owner-go-and-shipping-checks)
  for commands, results, identity comparison and accepted environment limitations.
- [x] Gate 5 — **GO (repository scope), conditional on commit; push authorized** by
  “okay let's consider both a go and commit/push everything”.

Confidence: **96%**, using the shared shipping QA's calculated owner rubric and evidence.
Remaining 4% is bounded model evidence and pending external checks; hosted CI follows push.
<!-- evidence:end walkthrough-shipping-20260908 -->
