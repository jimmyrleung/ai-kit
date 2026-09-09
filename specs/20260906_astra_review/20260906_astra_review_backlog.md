# Astra review backlog — 2026-09-06

Repair evidence and handoff contracts first. Establish a small task-outcome baseline before broad prompt simplification. Keep the kit's source checks, ownership-aware deployment, and distinct user workflows.

This backlog follows the [review report](20260906_astra_review_report.md) and [original brief](20260906_astra_review.md), against source commit `aeec06b`. **Execution started 2026-09-07; acceptance remains open until proven in the [execution record](20260906_astra_review_execution.md).** The active execution goal authorizes backlog implementation and delegation without commits; private conventions, publication, live deployment, and destructive operations remain outside this handoff. No owners or dates have been invented.

**Consolidated 2026-09-06:** this is the canonical execution backlog, incorporating the engineering addendum and the [independent review](20260906_astra_review_independent_review.md). R1 is incorporated into B08; the optional B22 refinement is incorporated as separately checkable required alignment and experimental simplification. These are completed planning corrections; the execution record now tracks the underlying changes separately from these planning corrections.

## How to execute

- **P1:** false evidence, broken handoffs, persistence risk, or an essential evaluation foundation. **P2:** maintainability, usability, and bounded product improvements. **P3:** lower-risk specialized improvements. No P0 incident was established.
- **Repair** means a current contradiction or executable defect. **Design** means a proposed contract/feature needing a bounded design decision. **Experiment** means the expected outcome benefit remains unmeasured.
- Dependencies concern the proposed final implementation, not permission to investigate. Independent items may proceed together only when their writes/resources do not conflict. Shared-file items need coordination.
- At execution, re-open current sources and rebase each finding. Line numbers are hints at the reviewed commit; the named heading/behavior is authoritative. Read affected siblings and existing specs before editing.
- Each item ends with observable acceptance evidence. A prompt change needs representative behavior trials as well as shipping checks. Code changes need relevant regression tests; structural checks alone do not establish skill quality.
- Split an item further if its bounded scope becomes too large during design. Do not turn this inventory into one bulk rewrite. Record accepted alternatives and residual gaps against the relevant item.

## Engineering change requirements — user addendum, 2026-09-06

Source: the user's follow-up screenshot and explicit request to apply its guidance to design, implementation, and review. Adopt this as a provider-neutral requirement across the engineering chain, including bug fixes:

- Read applicable repository instructions and inspect nearby production code, tests, documentation, and CI before designing or changing the implementation.
- Follow established repository conventions and reuse suitable existing utilities, helpers, fixtures, and test files.
- Add or extend tests where the changed behavior needs coverage. Create a new test file only when repository conventions require it or no existing file is a suitable home. Avoid unnecessary test-file proliferation without sacrificing meaningful coverage.
- Keep changes focused on the requested outcome. Avoid unrelated cleanup, speculative abstractions, and unnecessary complexity.
- Aim for clean, mergeable code: a coherent change that fits its repository and satisfies the relevant checks. File count alone is not a quality measure.

| Stage | Skills in scope | Required application |
|---|---|---|
| Analysis and design | `analyze-work`, `bug-investigation`, `techspec` | Inspect the surrounding implementation and identify suitable reuse and test locations before proposing new structures. |
| Decomposition and artifact review | `tasks-breakdown`, `review-artifact` | Carry the requirement into task/file plans; challenge unnecessary files, duplicated helpers, and unrelated work before implementation. |
| Implementation | `implement-task`, changes made during `walkthrough-implementation` | Extend suitable existing code/tests; create files only for a justified need; keep the patch within scope. |
| Verification and code review | `verify-task`, `qa-gates`, `review-implementation` | Check both behavioral coverage and repository fit; flag unnecessary complexity or file proliferation without requesting cosmetic rewrites outside scope. |

B22 owns the concise shared wording and propagation to these callers; B24 owns reviewer application; B25 owns test-placement and verification behavior. B21 evaluates cases with a suitable existing test file, a convention-required new file, and no suitable existing home, plus an unnecessary helper/cleanup proposal. Adopt the requirement now in the backlog; experiments decide how to express it effectively, not whether to honor it. Keep one maintained contract with concise caller references instead of repeating the full passage in every skill.

## Suggested sequence

| Wave | Items | Exit evidence |
|---|---|---|
| Establish truth | B01–B06, B13–B16; start B21 | Scope, review identity, lifecycle, causality, and feedback records have explicit contracts |
| Repair domain and public-use contracts | B07–B12, B17–B20, B32–B33 | Documentation, Terraform, KB, provider behavior, and tooling have focused fixtures |
| Evaluate simpler defaults | B22–B25, B28, B31 | Paired task results support the adopted default; essential obligations retained |
| Finish specialized improvements | B26–B27, B29–B30, B34–B35 | Feature-specific acceptance evidence; no forced broad redesign |

Waves are guidance; item dependencies below control ordering. B19 and B32 are small independent tooling repairs and can move earlier. B21 does not block fixing a demonstrated defect with a focused regression case.

## B01 — Review the complete intended change set

**P1 · Repair · Dependencies: none · Confidence: 99%.**

`skills/review-implementation/SKILL.md:35` combines `git diff <base>..HEAD`, status, and untracked files, omitting tracked dirty hunks. `skills/verify-task/SKILL.md:46` suggests `HEAD~3..HEAD`, which also assumes history and misattributes scope. `skills/qa-gates/SKILL.md:56` repeats the committed-only scope.

Define a shared scope contract covering committed, staged, unstaged, and untracked content with an explicit base and task boundary. Update these callers; preserve review-before-commit support.

Acceptance:

- A fixture containing all four change types reviews every intended hunk/content once.
- Unborn and short-history repositories work; unrelated earlier commits are not automatically task work.
- Renames and explicit scope exclusions are recorded; status output alone cannot count as content inspection.

Uncertainty: models may independently recover missing diffs today; no such recovery is assumed.

## B02 — Bind approvals to content and scope

**P1 · Design/repair · Dependencies: B01 · Confidence: 99%.**

`skills/review-implementation/SKILL.md:72` uses SHA plus `+dirty` as a fingerprint; `skills/qa-gates/SKILL.md:64` uses the stamp for review coverage. `skills/review-artifact/SKILL.md:73,81,95` permits downstream reuse from a review heading without content identity.

Specify a minimal review record containing artifact/source identity, scope, verdict, and relevant dependencies. Compare actual content before evidence reuse. Keep old records readable but visibly unverified when they lack identity.

Acceptance:

- A dirty edit at unchanged HEAD and an edited reviewed spec invalidate affected evidence.
- A task-only review cannot cover another task; rejected or stale reviews cannot advance the chain.
- Adding the review record itself does not cause endless invalidation; unrelated changes do not unnecessarily invalidate scoped evidence.

Uncertainty: the smallest suitable identity representation needs design; no stale approval was live-replayed here.

## B03 — Make per-task verification scope explicit and repeatable

**P1 · Repair · Dependencies: B01–B02 · Confidence: 98%.**

`skills/verify-task/SKILL.md:25,35,80` places `## Verify` inside a task often headed `### Task`; `:37` accepts task checkboxes broadly. Its QA call at `:94` does not pass task identity/ACs/files/budgets explicitly, while `skills/qa-gates/SKILL.md:47,79` also extracts scope.

Define authoritative task inputs and a properly nested/delimited record. Read ACs from their designated section, excluding previous evidence. Define the tasks-doc-less fix mapping.

Acceptance:

- Reverification preserves the exact AC set and historical evidence; neighboring tasks do not leak in.
- Both existing heading styles and a reviewed fix without a tasks document work.
- Prefix QA receives prefix scope; task verification receives only the explicit task scope.

Uncertainty: these are prose contracts; no external parser failure is claimed.

## B04 — Separate repository completion from deployment completion

**P1 · Repair · Dependencies: none · Confidence: 99%.**

`skills/tasks-breakdown/SKILL.md:74` places deploy/live work after QA. `skills/implement-task/SKILL.md:118`, `skills/review-implementation/SKILL.md:100`, and `skills/qa-gates/SKILL.md:220` ask for every task Done, despite QA's pending-live allowance at `:72`.

Carry the completion boundary through task selection, final review, QA, and closeout. Repository GO must not imply operations completed.

Acceptance:

- A task graph containing repository, deployment, and live-rehearsal tasks reaches repository GO without a dependency cycle.
- Pending operational tasks remain visible with their own evidence requirements.
- Existing repository-only task documents retain their expected completion path.

Uncertainty: actual runner interpretation is untested; inspect consumers before changing status fields.

## B05 — Include resource conflicts in parallel-task decisions

**P1 · Repair · Dependencies: none · Confidence: 98%.**

`skills/tasks-breakdown/SKILL.md:68` defines parallelism solely by absence of dependency ancestry. Independent graph nodes can still edit the same files or mutate the same environment.

Add write/resource conflict checks or an explicit isolation strategy. Distinguish potentially concurrent tasks from tasks ready now.

Acceptance:

- Same-file edits and shared database migrations are serialized unless isolation/merge handling is stated.
- Independent read-only work remains parallelizable.
- Unsatisfied dependencies prevent execution even when two tasks have no edge between them.

Uncertainty: no real collision was reproduced; the incomplete rule is directly present.

## B06 — Distinguish source-confirmed behavior from runtime causality

**P1 · Repair · Dependencies: none · Confidence: 98%.**

`skills/bug-investigation/SKILL.md:50,58` permits a read code branch to establish a VERIFIED root-cause hop. Incident gating at `:44` and the unconditional threshold at `:60` conflict.

Separate source facts, reproduction/runtime observations, and inference. Require causal evidence appropriate to the diagnosis, retaining falsifiers and next probes. Pass one effective severity policy through review. Label reversible mitigation separately from confirmed remediation.

Acceptance:

- A candidate configuration/race branch cannot become the confirmed incident cause from reading alone.
- A deterministic reproduction can support a minimal fix; missing causal evidence yields a precise next probe.
- A P1 scenario follows one severity policy without silently reverting to the normal threshold.

Uncertainty: past incident outcomes were not replayed.

## B07 — Carry source and documentation roots through the workflow

**P1 · Repair · Dependencies: none · Confidence: 99%.**

`skills/docs-tasks-creator/SKILL.md:9,58,93,199` supports chosen output directories; `skills/document-workflow/SKILL.md:109` forces source git-root output. `skills/update-workflow-docs/SKILL.md:28` already supports separate source/docs repositories.

Define source root, docs root, workspace, entry reference, and resolved output as explicit handoff values. Preserve git-root output as a default; honor the generated task's resolved destination.

Acceptance:

- Execute a generated documentation task in co-located, separate-docs, and multi-workspace fixtures.
- Exactly the promised file satisfies its AC; refresh resolves source paths in the source repository.
- Source code remains read-only when documentation is written elsewhere.

Uncertainty: the contract representation needs design; the path contradiction is explicit.

## B08 — Make documentation freshness a bounded evidence claim

**P1 · Repair · Dependencies: B02, B07 · Confidence: 98%.**

`skills/document-workflow/SKILL.md:124` records HEAD despite dirty source. `skills/update-workflow-docs/SKILL.md:33` treats an empty path-limited commit log as Current. `skills/document-workflow/references/output-template.md:170` overstates drift completeness.

The independent review's R1 extends this finding to `skills/document-terraform/SKILL.md:124–125`: its Summary/Source Files contract also uses HEAD and a path-limited log to claim exact freshness. Sibling module inspection at `:95` can introduce source content that the root repository's SHA does not identify.

Record repository/source identity, validate ancestry, inspect relevant dirty state, and include controlling registration/configuration inputs. Trigger a scoped retrace when those boundaries change. Apply the bounded identity contract to workflow and Terraform documentation, including Terraform's Summary/Source Files fields and relevant reference text. Identify each inspected sibling module's source/content separately or mark the affected freshness claim unverified. B08 owns documentation freshness; B10 owns effective-state evidence and B11 owns resolution/provenance semantics. Coordinate their shared-file edits without adding a separate freshness framework.

Acceptance:

- Dirty source never receives a false Current result; inaccessible/non-ancestor revisions are Unverifiable.
- Handler moves and changed dispatch/configuration prompt a scope check.
- Truly unchanged documentation retains its dates and prose; irrelevant code-only changes need no rewrite.
- Dirty root HCL invalidates the affected Terraform document's freshness even when HEAD is unchanged.
- A resolved sibling module changing independently of the root SHA is detected through its recorded source/content identity, or the document is explicitly unverified; the root SHA alone cannot establish freshness.
- Any Terraform stable-contract shape change follows its existing Schema-version rule and keeps older records readable with explicit verification limits.

Uncertainty: indirect dependency coverage requires representative fixtures; no complete static dependency oracle is proposed.

## B09 — Correct detector activation and expose incomplete scans

**P1 · Repair · Dependencies: B07 · Confidence: 97%.**

`skills/docs-tasks-creator/SKILL.md:66,72,207` restricts Next activation to root layouts and ASP.NET to explicit references, then treats unmatched handlers as absent for v1. `references/detectors.md:7,15,21,45,52` supplies restrictive recipes. Official Next and ASP.NET sources in the report corroborate `src` layouts and implicit Web SDK references.

Add expected-inventory fixtures for supported forms and a partial/unsupported state. Fix proven activation gaps first; verify additional forms against current official docs before broadening coverage.

Acceptance:

- Fixtures recognize root/src Next layouts and implicit Web SDK projects.
- Validate export/directive variations, grouped/mounted route prefixes, and Function/FunctionName as separate coverage cases.
- Dynamic/unsupported registrations yield an explicit coverage boundary, never an empty completeness claim.

Uncertainty: additional framework forms are validation targets, not all independently reproduced defects.

## B10 — Make Terraform evidence states honest

**P1 · Repair · Dependencies: none · Confidence: 98%.**

`skills/document-terraform/reference/heuristics.md:188` treats unconfirmed permission checks as red; `skills/document-terraform/SKILL.md:80,128` combines opt-in live access with an effective-status matrix. Default output at `:39,158` conflicts with the no-write rule at `:112`.

Distinguish declared wiring, planned/applied evidence, effective verification, unknown, and proven failure. Clarify docs-write permission separately from source-code immutability. A missing credential or probe is not broken access.

Acceptance:

- No-credentials fixtures report unknown effective state and still produce useful declared topology.
- A proven denial differs from an unrun check; HCL alone cannot earn live-green status.
- Docs inside/outside the source repository follow the declared output boundary without changing infrastructure source.

Uncertainty: provider-specific authorization semantics need provider documentation and scoped probes during implementation.

## B11 — Repair Terraform resolution and provenance semantics

**P1 · Repair · Dependencies: B10 · Confidence: 97%.**

`skills/document-terraform/SKILL.md:53,63,71–72,95,130` misclassifies absent backends, mixes input scopes, uses weak producer identity, treats registry documentation as resolution, and equates distinct module sources with distinct repos. Its reference at `:13,65,103,138,221` adds conflicting examples. Official Terraform sources in the report confirm root/child input separation and default local backend behavior.

Resolve root inputs and module arguments separately; require orchestration evidence for that backend label. Include root/provider/account/region context in producer matching. Represent same-root references and actual module source/version identity, including local leaves and repository subdirectories.

Acceptance:

- Fixtures cover local backend, ordered root inputs, child arguments, and unresolved values honestly.
- Identically named resources in different provider contexts are not merged; same-root and cross-root links differ.
- Multiple subdirectory modules in one repo, multi-module wrappers, local leaves, and unresolved pinned bodies receive accurate provenance; registry prose does not imply a complete resource inventory.

Uncertainty: exact expression resolution boundaries need design; preserve unknowns instead of building a speculative Terraform interpreter.

## B12 — Reconcile KB conversion, ownership, and resume rules

**P1 · Repair/design · Dependencies: none · Confidence: 98%.**

`skills/compile-kb/SKILL.md:143,179,211` combines moving tracked files into raw with a rule never to stage/commit raw. Existing raw directories suppress migration at `:181`; compile/seed write boundaries at `:85–89,228` need reconciliation.

Specify compile, seed, and convert write sets, tracked-file migration policy, and resumable per-file state. Preserve source links and history. Keep normal compilation idempotent.

Acceptance:

- A tracked-source conversion produces a coherent reviewable Git state under the chosen raw policy.
- An interrupted partial conversion resumes without skipping remaining files, duplication, or lost references.
- An unchanged compile is a no-op; seeded/status writes are explicit permitted operations.

Uncertainty: no data loss was observed; the intended migration policy requires an owner decision before implementation.

## B13 — Stop treating observations as invocation telemetry

**P1 · Repair · Dependencies: none · Confidence: 99%.**

`skills/improve/SKILL.md:85–90,149` labels observation counts as invocations/non-use. `skills/close/SKILL.md:68–80,264–265` and `skills/close-tasks/SKILL.md:96–98` allow clean runs with no observations; verify-task can produce several entries for one run.

Label existing data as observations and coverage. If actual invocation telemetry is desired, make it explicit, deduplicated, and optional. No retirement proposal may infer non-use from missing selective observations.

Acceptance:

- A clean unlogged run is unknown usage, not non-use; several observations from one run do not become several invocations.
- Backup copies do not become independent evidence.
- Fitness reports distinguish selected outcomes, measured invocations, and unavailable coverage.

Uncertainty: reliable cross-provider invocation attribution needs an evaluated source; no universal logger is assumed.

## B14 — Preserve unresolved improvement work across review windows

**P1 · Repair · Dependencies: B13 · Confidence: 98%.**

`skills/improve/SKILL.md:23–25,46–61,123–124,216` combines dated windows, deferred work, advancing the watermark, and keep-two retention. `skills/audit-skills/SKILL.md:229–234` also has packet retention.

Separate discovery watermarks from unresolved-item state. Always revisit deferred/open predictions regardless of source age. Retention must preserve unresolved evidence or an explicit archive/locator before discarding dated packets.

Acceptance:

- Defer an item, advance review date, create later packets: the item and its evidence remain reachable.
- Resolved items are not restaged; zero-new-observation runs still handle open predictions.
- Repeating a review does not duplicate unresolved entries.

Uncertainty: historical stores vary; inspect existing records before choosing migration rules.

## B15 — Identify a close by its actual session/work boundary

**P1 · Repair · Dependencies: none · Confidence: 99%.**

`skills/close/SKILL.md:23–34` treats any top receipt as an already-completed close and extends that entry, without first establishing that it belongs to the current session/day.

Distinguish a repeated close, an interrupted current close, and a new session close. Preserve delta harvesting within a close and append new history at a genuine boundary.

Acceptance:

- Repeating close without new work is a no-op; new work in the same session extends its receipt.
- A later session/day creates a new correctly dated entry.
- An interrupted close resumes without duplicate observations or a premature receipt.

Uncertainty: the host may lack a stable session identifier; define and test a documented fallback.

## B16 — Verify close-tasks provenance and harvest freshness

**P1 · Repair · Dependencies: B02, B04 · Confidence: 97%.**

`skills/close-tasks/SKILL.md:42–56,161–165` uses loop-state presence for attribution and commit-based harvest freshness. Mutable task/QA records can change at the same HEAD; a nearby state file may belong to different work.

Bind the target tasks document/run to its actual execution evidence. Use relevant artifact content identity, not HEAD alone. Compose the observation validation/receipt boundary explicitly.

Acceptance:

- Unrelated or stale runner state cannot label a manual run as runner-owned.
- Changed task evidence at unchanged HEAD is harvested exactly once.
- Closeout respects repository/live boundaries and cannot claim completion before enabled record checks pass.

Uncertainty: the external runner schema was not read in this audit; inspect it before naming fields or changing its consumers.

## B17 — Define portable, optional feedback and memory contracts

**P1 · Design/repair · Dependencies: B13–B16 · Confidence: 97%.**

`skills/close/SKILL.md:88–96` assumes known auto-memory rules. `skills/verify-task/SKILL.md:123` and `skills/qa-gates/SKILL.md:255–259` disagree about observation shape/ownership; QA depends on a private taxonomy file. `audit-skills:32–45` uses an unresolved active store abstraction.

Document explicit recorder/store/schema ownership, a no-recorder path, and fresh-user bootstrap. One composed execution owns its observations. Keep this user's anchored `~/.claude` paths as supported configuration. Cover ownership/decision/learning logs consistently; do not migrate private data automatically.

Acceptance:

- A fresh home can run the promised workflow without hidden taxonomy or auto-memory instructions.
- Composed verification emits no duplicate observations; enabled records share task/run identity and validation.
- Existing configured Claude stores remain usable from Claude, Codex, and Cursor; absent recording does not falsely pass an enabled gate.

Uncertainty: the smallest public schema/configuration needs design; existing private consumers must be inspected first.

## B18 — Maintain one capability-based provider reference and detect mirror drift

**P1 · Design/repair · Dependencies: none · Confidence: 98%.**

`adapters/codex/AGENTS.md:47–59` universally denies structured questions; this session exposes them. Public common sync at `docs/rules/skill-authoring.md:44–78` differs from current private copied mechanics. Adapter worker/recurrence sections already contain useful capability checks to retain.

Implement the report's Claude/OpenAI/Cursor decision table with source/version/check dates and explicit unavailable states. Separate host tools from model choices. Provide a read-only comparison for copied mechanics; private policy remains owner-controlled. Include literal-input and bounded-output probe guidance.

Acceptance:

- Discovery, invocation, questions, delegation, model inheritance, recurrence, and memory resolve from actual capabilities.
- A stale copied block is detected without overwriting private instructions.
- Provider probes prove intended inputs and discovery mechanism, or record unavailable; no universal claim follows from one host.

Uncertainty: capabilities change by version, mode, and account. Named model rankings require B21 evidence.

## B19 — Add missing metadata boundary fixtures

**P2 · Repair · Dependencies: none · Confidence: 99%.**

`scripts/check-skill-portability.mjs:123–136` accepts consecutive name hyphens and empty compatibility. This audit reproduced a structural pass for matching `analyze--work` and `compatibility: ""`; the current Agent Skills specification forbids both.

Correct these checks and test valid/invalid boundaries using the existing fixture framework. Reconcile the common sync source-envelope validation with the intended division of responsibility; do not fork another full schema implementation.

Acceptance:

- Both reproduced invalid inputs fail with clear codes; valid boundary inputs continue to pass.
- Existing checker and sync tests pass, including linked canonical directory enumeration.
- The checker still reports structural conformance separately from runtime skill quality.

Uncertainty: exhaustive standards conformance is broader than these two demonstrated gaps; bound the initial patch.

## B20 — Give authoring and audit policy one owner

**P2 · Repair/design · Dependencies: B19 · Confidence: 98%.**

`skills/write-skills/SKILL.md:31–40,81` has its own field description; `skills/improve/SKILL.md:88–100` carries old limits/check counts; `skills/audit-skills/SKILL.md:55,86,112` embeds local parser history, guaranteed startup-loading language, and a PowerShell-specific metric.

Use the shipping checker for executable schema policy and a single maintained reference for semantic guidance. Separate catalog routing, body evaluation, and final-tree validation. Contextualize the Vercel claim at `write-skills:21`; make overlap/line heuristics investigation leads. Check actual inventory membership, not only totals, when refreshing inventory validation.

Acceptance:

- Authoring, improve, and audit agree on fields, limits, check ownership, and exact validation commands.
- A wrong inventory member with an unchanged count is caught by the agreed check.
- No stale local-machine anecdote is a public prerequisite; recent staged-tree/tag validation fixes remain intact.

Uncertainty: some house heuristics may earn retention after evaluation; no automatic deletion/merge follows from size.

## B21 — Establish outcome evaluation and verify recent improvements

**P1 · Design/enabler · Dependencies: none · Confidence: 97%.**

Existing tests establish schema/sync behavior, not skill outcomes. Selected usage evidence U-A–U-E in the report shows trigger success can coexist with body defects and that recent completion-dependency/tag fixes already landed.

Build a small anonymized, reusable task corpus from confirmed failure and success cases. Cover routing/non-triggering, procedure execution, artifacts, and final outcomes separately. Compare no-skill where meaningful, current, and candidate instructions under recorded provider/model/settings. Include repeated trials and human review for judgment-heavy outputs.

Acceptance:

- Seed cases include dirty review scope, consumer-contract closure, malformed tags, completion dependencies, wrong output roots, and a clean no-op.
- Preserve prompts, source state, traces, final artifacts, grader criteria, failures, and unavailable cases; record cost/time/tokens only when measured.
- Before adopting broad simplification, define acceptable outcome tradeoffs and compare missed obligations, interruptions, retries, and artifact size.
- September 4 applied fixes receive new outcome evidence rather than duplicate implementation tickets.
- Exercise the engineering addendum's reuse/new-file cases; grade behavioral coverage, repository fit, and unnecessary complexity together, without rewarding fewer files at the expense of correctness.

Uncertainty: the corpus is initially personal and small; results must state task/provider coverage and variation.

## B22 — Carry engineering requirements and evaluate shorter skill bodies

**P2 · Required alignment + experiment · Dependencies: B20–B21 (simplification only) · Confidence: 95% in testing simplification; benefit unmeasured.**

`skills/analyze-work/SKILL.md:199` mandates a large output set; `skills/tasks-breakdown/SKILL.md:37,67,118–120` repeats fields and conflicts on sizing. `skills/techspec/SKILL.md:136,146,213` retains internal wording/reference drift. Dense Terraform/KB prose shows why line counts are insufficient.

**Required alignment:** include the user-added engineering change requirements above in the shared contract and propagate them through the named design, task, execution, and review callers. Preserve existing equivalent guidance and resolve contradictions instead of layering on duplicate instructions. This work can proceed without B20/B21 completion; its acceptance is independent of whether shorter prompts improve outcomes.

**Simplification experiment:** after B20–B21, pilot a short core: purpose/scope, required evidence, conditional decisions, checks, and handoff. Move substantial conditional examples/history to references with explicit loading conditions. Use simple technical English; repair stale labels while preserving consumer contracts. Expand family by family only after B21 results.

Acceptance — record the required-alignment result separately from the experiment's adopt/revise/retain-current decision:

- Every named engineering stage accounts for repository instructions, nearby code/tests/docs/CI, suitable reuse, focused scope, and justified test-file creation. This remains required if the simplification experiment is inconclusive or retains current wording.
- For an adopted simplification, small tasks produce shorter complete artifacts; complex cases retain consumer closure, rollback, uncertainty, and test obligations.
- References load when needed, including negative/error cases; required fields still resolve for downstream callers.
- Report actual size/cost/outcome changes; no target is met merely by packing longer lines or dropping evidence.

Uncertainty: optimal length and reference boundaries are model/task dependent. Keep distinct learning rituals.

## B23 — Honor existing authorization and make approval cadence proportional

**P2 · Experiment/design · Dependencies: B21 · Confidence: 95% in the proposal; benefit unmeasured.**

`analyze-work:97`, `lay-of-the-land:48–49`, `bug-investigation:60`, and `techspec:146` add routine drafting pauses. `compile-kb:36,58–82` asks before establishing no-op work. Confidence arithmetic and worker agreement also drive gates (`analyze-work:89`, `document-workflow:63`). Paths refer to their canonical `SKILL.md` files.

For authorized local work, produce the reviewable draft and ask only for blocking facts, scope changes, or real owner decisions. Keep explicit user-required approvals. Replace arithmetic agreement as proof with evidence coverage; optional percentage reporting remains presentation policy. Preserve one-item discussion when requested and allow explicit batch authorization.

Acceptance:

- Equivalent inline/file inputs have equivalent paths; a no-op does not require generic confirmation.
- Missing load-bearing information still raises a precise question; authorization is never inferred from a score.
- Comparison runs measure interruptions and retained decision quality; user-directed walkthrough cadence remains intact.

Uncertainty: private convention changes require separate owner scope; do not silently rewrite them.

## B24 — Scale independent review and separate severity from certainty

**P2 · Experiment/design · Dependencies: B02, B21 · Confidence: 96% in the finding; benefit unmeasured.**

`skills/review-implementation/SKILL.md:38,52,64` fixes three lanes, requires refactor suggestions, and combines certainty/severity/frequency in one cutoff. `skills/techspec/SKILL.md:156` and `skills/document-workflow/SKILL.md:60` impose additional agent work.

Test review depth based on scope/risk and independent coverage. Keep suspected high-impact issues visible with their next confirming probe; make unrelated refactors opt-in. Use native workers only when available/authorized, with an honest sequential fallback.

Acceptance:

- Small isolated changes avoid automatic three-agent review; cross-boundary risk retains independent checks.
- A severe uncertain issue is reported with uncertainty rather than silently scored out.
- Compare missed defects, false positives, latency, and measured cost; preserve parent re-grounding.
- Reviewers apply the engineering addendum: flag avoidable new test files, duplicated utilities, unrelated cleanup, and unnecessary complexity with repository evidence; accept justified new files and preserve needed coverage.

Uncertainty: fewer agents are not assumed to be better; historical review successes are positive controls.

## B25 — Reuse fresh check evidence and select relevant gates

**P2 · Design/repair · Dependencies: B01–B03, B17, B21 · Confidence: 97%.**

`skills/implement-task/SKILL.md:91` runs build/tests before composed QA requires them again at `qa-gates:96`. QA imposes environment-comment syntax at `:185` and routes UI checks to the user at `:172`, despite browser verification support in `verify-task:71`.

Reuse results only when source/config/environment identity and test scope match. Run checks appropriate to the actual contract; document intentional environment differences in the established artifact. Use available browser evidence for observable UI criteria.

Acceptance:

- Unchanged implementation-to-verification does not rerun identical checks; relevant changes invalidate reuse.
- Blocked/incomplete suites cannot become pass; recorded evidence names actual coverage.
- Required missing environment keys fail, deliberate unrelated differences do not; observable UI checks can use recorded browser evidence.
- Required test additions extend a suitable existing test file; a new file is used only when repository conventions require it or no suitable home exists. Both paths retain meaningful coverage and use the repository's fixtures/helpers where suitable.

Uncertainty: invalidation granularity needs careful design; optimization must not weaken evidence.

## B26 — Refresh documentation tasks without losing progress

**P2 · Design/feature · Dependencies: B07, B09 · Confidence: 95%.**

`skills/docs-tasks-creator/SKILL.md:147,162,226` uses positional IDs and explicitly requires manual progress restoration after regeneration; `:149` can group by physical file.

Choose stable workflow identity and reconcile the inventory with existing task status/evidence/notes. Treat additions, changed entries, and retirement as explicit changes. Group by execution boundary where appropriate.

Acceptance:

- An unchanged scan is a no-op; an alphabetically earlier addition does not remap completed tasks.
- Renames/retirements are surfaced for review; manual notes survive.
- Independent flows in one file remain separable; a connected cross-file flow can remain one workflow.

Uncertainty: this deliberately adds product behavior; validate identities against real inventories before committing a schema.

## B27 — Evaluate discovered skills by inspected evidence

**P2 · Design/repair · Dependencies: B20 · Confidence: 96%.**

`skills/find-skills/SKILL.md:44–50,66–72` uses leaderboard/popularity language as quality evidence; its broad trigger can interrupt ordinary help. The checker pins its content at `scripts/check-skill-portability.mjs:29,304`.

Require source/provenance and relevant body/script inspection before a substantive recommendation. Treat popularity as discovery metadata, not proven task success. Keep installation a distinct authorized action. Deliberately resolve the existing content pin if changing the skill; do not bypass it silently.

Acceptance:

- A popular but mismatched candidate is not ranked as proven merely by stars/downloads.
- A recommendation states inspected compatibility and outcome evidence, or its absence.
- Ordinary how-to questions without discovery intent do not automatically become installation searches.

Uncertainty: third-party quality often lacks outcome data; report that gap rather than invent a quality score.

## B28 — Route from current intent and valid artifact state

**P2 · Repair/design · Dependencies: B02, B04, B21 · Confidence: 97%.**

`skills/triage/SKILL.md:21–42` routes from recent artifacts/review-heading presence before matching the active request. `:121–137` always stops at a suggestion; `skills/walkthrough-implementation/SKILL.md:3,23–26` can activate extra ceremony before commit.

Preserve explicit recommendation-only triage, but prevent unrelated/stale/failed artifacts from hijacking a new request. Define optional continuation only when the user's request authorizes it. Make unrequested owner tours an offer instead of a mandatory stage.

Acceptance:

- A new unrelated task is not forced back into an old chain.
- Failed/stale review cannot advance work; lifecycle routing respects repository/live boundaries.
- Explicit “recommend only,” explicit execution, and requested walkthrough prompts each follow their intended route.

Uncertainty: continuation changes the product contract and requires a deliberate decision, not a silent behavior switch.

## B29 — Add durable decision lifecycle metadata

**P2 · Repair · Dependencies: B17 · Confidence: 97%.**

`skills/record-decision/SKILL.md:38–50` omits dates used by `skills/close/SKILL.md:43–51` for aging/escalation. Rationale ownership is valuable and should remain.

Record creation/review state and provenance. Preserve supplied human rationale; clearly mark drafted rationale/consequences until reviewed. Keep superseding records separate from historical decisions.

Acceptance:

- Aging is derived from an actual date; an undated legacy record is explicitly unknown.
- Human-owned rationale is not relabeled as invented text; draft fields cannot appear approved by implication.
- A superseding decision preserves the earlier record and its relationship.

Uncertainty: legacy record migration should be bounded and owner-reviewed.

## B30 — Clarify teaching artifact portability

**P2 · Repair/design · Dependencies: B21 · Confidence: 97%.**

`skills/teach/SKILL.md:18,49` promises self-contained HTML while `:65–69` requires shared assets. A glossary format exists but is missing from the format inventory; `:110` prescribes exact answer-length equality.

Choose and document the default workspace bundle versus single-file export contract. Index every supported format. Use quiz alternatives that avoid obvious answer clues without mechanical word equality.

Acceptance:

- The promised export opens after relocation/offline with required assets intact; render it and inspect the result.
- All supported formats are discoverable from the skill; explicit-only provider behavior remains intact.
- Quiz alternatives remain semantically sound without forced padding.

Uncertainty: the preferred export default is a product choice; neither packaging form is inherently wrong.

## B31 — Complete parallel work by coverage, not majority

**P2 · Repair · Dependencies: B18 · Confidence: 98%.**

`skills/orchestrate/SKILL.md:34` permits agreeing-majority consolidation when a slow worker remains, even though charters can own disjoint coverage. The durable persistence and parent verification rules are strengths.

Track required charter coverage. Recover or explicitly bound missing work; agreement among other lanes cannot supply an unexamined domain. Keep runtime-specific recovery advice in provider references.

Acceptance:

- If the sole security/domain lane stalls, its coverage remains missing until recovered or explicitly excluded.
- Completed outputs survive context changes and are not needlessly rerun.
- Parent verification still distinguishes source inspection from runtime evidence and records unresolved conflicts.

Uncertainty: recovery tools vary; require a documented fallback instead of a universal resume command.

## B32 — Make sync conflict diagnostics reflect transaction state

**P2 · Repair · Dependencies: none · Confidence: 99%.**

`scripts/sync-skills.py:1055` always says no filesystem/manifest changes were made for `PlanConflict`. The existing action-time race fixture at `tests/test_sync_skills.py:530` leaves a prepared transaction; this audit reproduced the contradictory stderr and manifest.

Distinguish non-mutating preflight failure from action-time conflict with durable recovery state. Preserve the transaction/recovery design; correct diagnostics and next-step guidance.

Acceptance:

- Preflight conflicts accurately report no mutation.
- The race fixture reports prepared/recovery state and never claims an unchanged filesystem.
- Existing recovery, ownership, idempotency, and relevant hosted platform checks remain green.

Uncertainty: no evidence shows broken recovery; this item targets truthful diagnostics only.

## B33 — Verify the public bootstrap and distribution surface

**P2 · Design/repair · Dependencies: B17–B20 · Confidence: 97%.**

`README.md:80–93` describes validation/adapters; `:103` says MIT, but tracked-file enumeration found no license file. The skills also rely on private conventions covered by B17. Existing isolated sync tests are a strong foundation.

Document prerequisites and the smallest fresh-user path; verify it in an isolated home without private policy files. Make the stated license available with owner-confirmed attribution. Keep provider authentication/availability separate from installation correctness.

Acceptance:

- A fresh user can install, validate, discover, and attempt a representative workflow from documented steps.
- Unavailable provider execution is explicit; setup does not overwrite user-owned instructions or roots.
- Repository license text agrees with the README; shipped examples contain no private names/paths.

Uncertainty: provider credentials and license attribution are owner-supplied facts; do all reviewable preparation before requesting missing approval/input.

## B34 — Improve learning recommendation evidence and concise presentation

**P3 · Experiment/design · Dependencies: B21 · Confidence: 95% in the proposal; benefit unmeasured.**

`skills/breakout-session/SKILL.md:27–30,46–49` gives progression verdicts without an explicit next-topic prerequisite contract. `skills/triage-learning-content/SKILL.md:89–113` can infer decisive visuals from captions and duplicates human output with full JSON.

Scope readiness to demonstrated knowledge and known prerequisites. Inspect decisive visuals or flag the recommendation uncertain. Keep the machine-readable interface stable; offer concise human presentation separately.

Acceptance:

- A readiness verdict states what was tested and does not certify unknown next-topic prerequisites.
- A diagram-dependent article receives visual inspection or a clear uncertainty-based recommendation.
- Interactive output is concise while existing structured consumers still receive their expected schema.

Uncertainty: no learning-outcome study or consumer failure was observed. Inspect actual structured consumers before any schema change.

## B35 — Allow post-mortems to refine the causal record

**P2 · Design/repair · Dependencies: B06 · Confidence: 96%.**

`skills/post-mortem/SKILL.md:32,38–40` allows reconstruction but forbids revisiting the reviewed cause and requires every finding to become an action.

Allow later contradictory evidence to qualify the causal record and create a focused investigation follow-up. Select actionable risks instead of forcing tickets for every observation/strength. Distinguish proposed owners/dates from confirmed commitments.

Acceptance:

- Missing evidence produces an honest draft; later contradiction is recorded and routed, not suppressed.
- Selected actions have verification and explicit ownership/date status.
- Informative observations can remain observations without manufactured prevention work.

Uncertainty: the best action-selection depth needs trials on real incident artifacts; remediation remains outside this skill's scope.

## Consolidation and exclusions

Fresh-review dispositions: **R1 accepted and incorporated into B08** with Terraform root/sibling-module freshness cases and the report's skill mapping updated. **Optional B22 refinement accepted**: required engineering alignment has its own acceptance result and does not wait for the simplification experiment. The independent review's original verdict and findings remain preserved as review history; no new independent re-review is claimed.

The independent engineering lane's E01–E17 map respectively to: B01; B02; B07; B03; B04; B05; B25; B06; B23; B24; B08; B09; B26; B10–B11; B22; B17; B35.

The support lane's S01–S15 map respectively to: B13; B14–B15; B16; B17–B18; B19–B20; B22; B12; B23; B27; B31; B28; B29; B30; B34; B34. Parent tooling/distribution findings supply B19, B32, and B33; usage evidence supports B18, B20–B23, and B33. Accepted findings are fully restated above, so scratch reports are not execution prerequisites.

Already-applied strict-YAML, common-sync recovery/platform, staged-tree audit, observation-tag, and task-completion dependency improvements are retained as regression/evaluation cases. Do not reopen them as absent features. No skill retirement, blanket merger, provider/model ranking, feasibility-spike skill, global performance gate, or sync-engine replacement is proposed without further evidence.

Overall confidence: **96%**, using the factors and limits in the report. Demonstrated repairs have focused acceptance checks; broader simplification remains experimental until B21 supplies outcome evidence. Nothing in this backlog claims those future checks have already passed.
