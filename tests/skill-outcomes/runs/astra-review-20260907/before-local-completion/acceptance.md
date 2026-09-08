# Astra backlog acceptance evidence — 2026-09-07

Exact scope: 35 items and 113 ACs. Outcome evidence: 1 fail, 1 not-adopted, 92 observed-bounded, 19 partial. These are evidence classifications, not owner approval.

[Review summary](acceptance-review-report.md) · [Full source excerpts, evidence hashes and archive locators](acceptance.json) · [Evidence index](README.md)

Source rules are reviewed separately from model behavior. Checked boxes below mean only observed bounded fixture evidence; all owner acceptance remains pending. Failed, partial and unadopted obligations remain unchecked. Synthetic scenario facts, original snapshot limits and unavailable host traces remain in the full record.

## B01 — Review the complete intended change set

- [x] **B01.AC1 — observed-bounded**: A fixture containing all four change types reviews every intended hunk/content once.
  Source: supported. Evidence: Preserved committed/index/worktree transitions and untracked fixture content are separately identified; one review covers Task A only.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B01.AC2 — observed-bounded**: Unborn and short-history repositories work; unrelated earlier commits are not automatically task work.
  Source: supported. Evidence: Unborn empty-tree and single-commit probes executed; unrelated Task B work explicitly excluded.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B01.AC3 — observed-bounded**: Renames and explicit scope exclusions are recorded; status output alone cannot count as content inspection.
  Source: supported. Evidence: Actual staged diff records old.md to new.md; Task B exclusion is explicit; final content and layer hashes are retained.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B02 — Bind approvals to content and scope

- [x] **B02.AC1 — observed-bounded**: A dirty edit at unchanged HEAD and an edited reviewed spec invalidate affected evidence.
  Source: supported. Evidence: Raw hash variants distinguish same-HEAD source edit and reviewed AC edit.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B02.AC2 — observed-bounded**: A task-only review cannot cover another task; rejected or stale reviews cannot advance the chain.
  Source: supported. Evidence: Task B, rejected, and identity-free variants remain unusable despite matching other content.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B02.AC3 — observed-bounded**: Adding the review record itself does not cause endless invalidation; unrelated changes do not unnecessarily invalidate scoped evidence.
  Source: supported. Evidence: Delimited evidence append and unrelated-path edits retain scoped subject/dependency hashes.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B03 — Make per-task verification scope explicit and repeatable

- [x] **B03.AC1 — observed-bounded**: Reverification preserves the exact AC set and historical evidence; neighboring tasks do not leak in.
  Source: supported. Evidence: Original heading/numbered tests preserve neighbors/history; final taskless artifacts retain the same AC mapping in two Verify records and execute local unittest tests. Source/test fixtures and upstream approval remain synthetic setup.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B03.AC2 — observed-bounded**: Both existing heading styles and a reviewed fix without a tasks document work.
  Source: supported. Evidence: Final producer emits stable AC-F1/AC-F2; duplicate returns-2 obligation has both source locators once, negative input remains separate; no-techspec route uses only explicit expected behavior. Two Verify records preserve mappings; actual local tests pass. Original candidate duplication remains historical failure.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B03.AC3 — observed-bounded**: Prefix QA receives prefix scope; task verification receives only the explicit task scope.
  Source: supported. Evidence: Task-only explicit handoff is preserved; prefix handoff is separately described. No real prefix implementation gate execution was supplied.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B04 — Separate repository completion from deployment completion

- [x] **B04.AC1 — observed-bounded**: A task graph containing repository, deployment, and live-rehearsal tasks reaches repository GO without a dependency cycle.
  Source: supported. Evidence: Original acyclic repository/deploy/live graph and final closeout with repository completion/live pending satisfy the bounded lifecycle fixture; supplied QA/runner facts are synthetic.
  Remaining: No new live runner execution is required to claim the graph fixture result; actual deployment remains outside this result and owner judgment is pending.
- [x] **B04.AC2 — observed-bounded**: Pending operational tasks remain visible with their own evidence requirements.
  Source: supported. Evidence: Operational tasks remain pending in graph and closeout with evidence requirements; synthetic QA is labeled supplied.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [ ] **B04.AC3 — partial**: Existing repository-only task documents retain their expected completion path.
  Source: supported. Evidence: Default pre-merge interpretation exists in source and repository-task fixture paths.
  Remaining: No separate complete repository-only task-document workflow execution was demonstrated.

## B05 — Include resource conflicts in parallel-task decisions

- [x] **B05.AC1 — observed-bounded**: Same-file edits and shared database migrations are serialized unless isolation/merge handling is stated.
  Source: supported. Evidence: Same-file Task 1/2 and database Task 3/4 are serialized in the actual graph.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B05.AC2 — observed-bounded**: Independent read-only work remains parallelizable.
  Source: supported. Evidence: Read-only Tasks 5/6 remain potentially concurrent.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B05.AC3 — observed-bounded**: Unsatisfied dependencies prevent execution even when two tasks have no edge between them.
  Source: supported. Evidence: Task 7 remains not ready because Task 2 dependency is unmet despite read-only status.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B06 — Distinguish source-confirmed behavior from runtime causality

- [x] **B06.AC1 — observed-bounded**: A candidate configuration/race branch cannot become the confirmed incident cause from reading alone.
  Source: supported. Evidence: Source-only race remains candidate; precise per-key trace/falsifier is written.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B06.AC2 — observed-bounded**: A deterministic reproduction can support a minimal fix; missing causal evidence yields a precise next probe.
  Source: supported. Evidence: Local fee(-1) command returned -0.02; bounded fix is supported and no production causality is claimed.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B06.AC3 — observed-bounded**: A P1 scenario follows one severity policy without silently reverting to the normal threshold.
  Source: supported. Evidence: Original incident scenario uses active-P1 threshold70; final conditional-worker-input.json explicitly retains threshold70 and causal requirements without substituting90. Dispatch is simulated; no actual worker handoff was executed.
  Remaining: The requested severity-policy scenario is represented consistently. This does not certify native delegation or real incident causality; no broader proof is demanded for the fixture claim.

## B07 — Carry source and documentation roots through the workflow

- [ ] **B07.AC1 — partial**: Execute a generated documentation task in co-located, separate-docs, and multi-workspace fixtures.
  Source: supported. Evidence: Final W1 generated task outputs in co-located/separate/multi-workspace layouts and actual resolved refresh reads exist; nine output documents fail full required Summary conformance.
  Remaining: Concrete fixture gaps: output Summary fields are missing; standalone workspace roots were locators inside one parent Git repository, so strict standalone source-root identity was not independently established.
- [ ] **B07.AC2 — fail**: Exactly the promised file satisfies its AC; refresh resolves source paths in the source repository.
  Source: supported. Evidence: Exact promised files exist and refresh reads their recorded source paths; full task output-format AC fails because Source Root, Docs Root, Workspace Root, Trigger, Entry Point and Success Response are absent from Summary.
  Remaining: Preserve this one-run generated-artifact failure for owner review. Handoff/evidence fields elsewhere do not satisfy the missing required Summary fields; no source-contract absence is inferred.
- [x] **B07.AC3 — observed-bounded**: Source code remains read-only when documentation is written elsewhere.
  Source: supported. Evidence: Final source-hash checks retain original source bytes while all selected documentation outputs are written under the promised docs roots; output schema failure is separate.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.

## B08 — Make documentation freshness a bounded evidence claim

- [ ] **B08.AC1 — partial**: Dirty source never receives a false Current result; inaccessible/non-ancestor revisions are Unverifiable.
  Source: supported. Evidence: Original dirty workflow variants are Stale; final dirty Terraform root/sibling variants are Stale and an actual denied sibling file read is Unverifiable.
  Remaining: Existing but non-ancestor revision variant remains unexecuted; original ffffffff test proves inaccessible revision only. Standalone source-root identity is the documented W1 unavailable case.
- [x] **B08.AC2 — observed-bounded**: Handler moves and changed dispatch/configuration prompt a scope check.
  Source: supported. Evidence: Moved entry and untracked route boundary explicitly trigger scoped retrace.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B08.AC3 — observed-bounded**: Truly unchanged documentation retains its dates and prose; irrelevant code-only changes need no rewrite.
  Source: supported. Evidence: Final refresh JSON records actual source reads and identical doc_before/doc_after hashes; original unrelated-code no-rewrite case retained. Current freshness here does not imply the independently failed W1 output schema is complete.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B08.AC4 — observed-bounded**: Dirty root HCL invalidates the affected Terraform document's freshness even when HEAD is unchanged.
  Source: supported. Evidence: Final dirty-root fixture records actual changed main.tf hash with primary_head_unchanged true and classifies Stale.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B08.AC5 — observed-bounded**: A resolved sibling module changing independently of the root SHA is detected through its recorded source/content identity, or the document is explicitly unverified; the root SHA alone cannot establish freshness.
  Source: supported. Evidence: Final readable sibling change records different bytes at unchanged root HEAD and Stale; actual permission-denied sibling read becomes Unverifiable. Orchestration locator lacks version ancestry and remains bounded/unverifiable accordingly.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [ ] **B08.AC6 — partial**: Any Terraform stable-contract shape change follows its existing Schema-version rule and keeps older records readable with explicit verification limits.
  Source: supported. Evidence: Original artifacts emit Terraform schema v4 and source defines readable legacy records as Unverifiable.
  Remaining: No older-document reader/refresh migration outcome trial was preserved.

## B09 — Correct detector activation and expose incomplete scans

- [x] **B09.AC1 — observed-bounded**: Fixtures recognize root/src Next layouts and implicit Web SDK projects.
  Source: supported. Evidence: Final complete frozen detector inputs yield root/src Next and implicit Web SDK inventories. Pages underscore route is emitted. W1 summary-format failure does not erase observed route activation.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [ ] **B09.AC2 — partial**: Validate export/directive variations, grouped/mounted route prefixes, and Function/FunctionName as separate coverage cases.
  Source: supported. Evidence: Original and final variants show const/sync/async exports, grouped path, literal MapGroup and separate Function/FunctionName entries; final Pages underscore/root route included.
  Remaining: Not all requested mounted route-prefix/export-directive variants have separate preserved fixtures, notably mounted Express/Fastify/Nest forms; this is exact coverage absence, not a universal framework-proof demand.
- [x] **B09.AC3 — observed-bounded**: Dynamic/unsupported registrations yield an explicit coverage boundary, never an empty completeness claim.
  Source: supported. Evidence: Unresolved export and runtime-prefix route explicitly mark Partial coverage instead of empty completeness.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B10 — Make Terraform evidence states honest

- [x] **B10.AC1 — observed-bounded**: No-credentials fixtures report unknown effective state and still produce useful declared topology.
  Source: supported. Evidence: Final useful declared topology is produced without cloud credentials; unsupported effective axes stay unknown.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B10.AC2 — observed-bounded**: A proven denial differs from an unrun check; HCL alone cannot earn live-green status.
  Source: supported. Evidence: Final evidence-axis artifact distinguishes applied-only unknown effectiveness from a dated intended-identity/read-operation denial. Both records explicitly supplied synthetic; HCL earns no live-green.
  Remaining: This establishes fixture evidence classification, not live cloud authorization. No live cloud probe is required by the bounded fixture claim.
- [ ] **B10.AC3 — partial**: Docs inside/outside the source repository follow the declared output boundary without changing infrastructure source.
  Source: supported. Evidence: Outside-source docs were produced without HCL edits.
  Remaining: Both inside and outside Terraform documentation destinations are not independently demonstrated in original trial.

## B11 — Repair Terraform resolution and provenance semantics

- [x] **B11.AC1 — observed-bounded**: Fixtures cover local backend, ordered root inputs, child arguments, and unresolved values honestly.
  Source: supported. Evidence: Final root/default/tfvars and child-argument mapping, default local backend and unresolved pinned bodies are explicit, with separate source identities.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B11.AC2 — observed-bounded**: Identically named resources in different provider contexts are not merged; same-root and cross-root links differ.
  Source: supported. Evidence: Final producer index separates default/secondary provider configurations and retains entry/local provenance; root and dependency context remain explicit.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B11.AC3 — observed-bounded**: Multiple subdirectory modules in one repo, multi-module wrappers, local leaves, and unresolved pinned bodies receive accurate provenance; registry prose does not imply a complete resource inventory.
  Source: supported. Evidence: Final wrapper and both child resources appear with declaring-body provenance; package/subdirectory identities, local leaf and unresolved pinned bodies remain distinct; registry semantics do not generate invented resources.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.

## B12 — Reconcile KB conversion, ownership, and resume rules

- [x] **B12.AC1 — observed-bounded**: A tracked-source conversion produces a coherent reviewable Git state under the chosen raw policy.
  Source: supported. Evidence: Tracked alpha relocation preserves intended tracking and untracked beta stays outside tracked relocation set; scratch Git state is reviewable, no staging claimed.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B12.AC2 — observed-bounded**: An interrupted partial conversion resumes without skipping remaining files, duplication, or lost references.
  Source: supported. Evidence: Final initialized scaffold resumes approved beta while alpha stays compiled; beta retains untracked intent, two source notes exist, link/hash checks and unchanged rerun are retained. Blocked unknown origin remains unaccepted.
  Remaining: Requested approved-file resume fixture is covered. Full secret scanning unavailable and unknown-origin owner classification remain separate conversion completion limits; no universal losslessness claim.
- [x] **B12.AC3 — observed-bounded**: An unchanged compile is a no-op; seeded/status writes are explicit permitted operations.
  Source: supported. Evidence: Final approved-terminal unchanged rerun records writes0 and identical full before/after manifests; permitted source/status/wiki writes occurred earlier under explicit supplied approval, blocked unknown remains pending.
  Remaining: No further fixture proof required for no-op/write-boundary behavior; full conversion does not become complete while scanner/owner classification are unavailable.

## B13 — Stop treating observations as invocation telemetry

- [x] **B13.AC1 — observed-bounded**: A clean unlogged run is unknown usage, not non-use; several observations from one run do not become several invocations.
  Source: supported. Evidence: Two observations sharing an execution do not become measured invocations; missing telemetry stays unavailable.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B13.AC2 — observed-bounded**: Backup copies do not become independent evidence.
  Source: supported. Evidence: Physical replica records are deduplicated by obs-a/obs-b IDs.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B13.AC3 — observed-bounded**: Fitness reports distinguish selected outcomes, measured invocations, and unavailable coverage.
  Source: supported. Evidence: Fitness artifact separates selected partial outcomes, observation count and unavailable invocation coverage.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B14 — Preserve unresolved improvement work across review windows

- [x] **B14.AC1 — observed-bounded**: Defer an item, advance review date, create later packets: the item and its evidence remain reachable.
  Source: supported. Evidence: Final later-window packet preserves actual deferred proposal and source observation bytes; retention-check validates their existence/unchanged identity. Original absent packet limitation remains in history.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B14.AC2 — observed-bounded**: Resolved items are not restaged; zero-new-observation runs still handle open predictions.
  Source: supported. Evidence: Later-window REVIEW with no new observations leaves item9 actioned and pred2 no-evidence; actual old packets/evidence stay reachable.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B14.AC3 — observed-bounded**: Repeating a review does not duplicate unresolved entries.
  Source: supported. Evidence: Final unchanged-repeat manifest shows identical store bytes and writes0; no duplicate unresolved entry or new proposal. Synthetic historical input and separate watermark file are explicit.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.

## B15 — Identify a close by its actual session/work boundary

- [x] **B15.AC1 — observed-bounded**: Repeating close without new work is a no-op; new work in the same session extends its receipt.
  Source: supported. Evidence: Final same-session no-op preserves bytes; supplied contentful decision creates a superseding receipt only after real empty intended-observation inventory validation. No fabricated observation.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B15.AC2 — observed-bounded**: A later session/day creates a new correctly dated entry.
  Source: supported. Evidence: Distinct later-session ID prepends its correctly supplied dated entry and preserves prior session entries; scenario times are synthetic.
  Remaining: The later-session alternative is covered; no claim of wall-clock day rollover or universal session detection.
- [x] **B15.AC3 — observed-bounded**: An interrupted close resumes without duplicate observations or a premature receipt.
  Source: supported. Evidence: Preserved interrupted-started artifact contains no premature delta receipt; resumed log has one completed receipt after enabled empty-inventory validation; repeat is unchanged.
  Remaining: Zero intended observations is the executed close branch; nonempty observation dedup is separately demonstrated in harvest. No actual host crash claim.

## B16 — Verify close-tasks provenance and harvest freshness

- [x] **B16.AC1 — observed-bounded**: Unrelated or stale runner state cannot label a manual run as runner-owned.
  Source: supported. Evidence: Final matching/stale runner artifacts are compared on canonical tasks path/window/action/task; stale input rejected. Parent actual external writeState probe independently narrows serialization compatibility.
  Remaining: Required stale-attribution fixture is covered. No live headless run is claimed or needed to grade this fixture; final worker external-consumer unavailable reflects its own bounded scope, not parent discovery.
- [x] **B16.AC2 — observed-bounded**: Changed task evidence at unchanged HEAD is harvested exactly once.
  Source: supported. Evidence: Final harvest-actions records initial harvest, identical no-op, changed consumed Verify hash/new harvest, then identical no-op; two duplicate candidates emit one observation for each distinct finding identity.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B16.AC3 — observed-bounded**: Closeout respects repository/live boundaries and cannot claim completion before enabled record checks pass.
  Source: supported. Evidence: Actual tag-check exit0 and required envelope inventory precede persisted receipts; repository/live statuses remain separate. Supplied QA/runner provenance remains synthetic.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.

## B17 — Define portable, optional feedback and memory contracts

- [x] **B17.AC1 — observed-bounded**: A fresh home can run the promised workflow without hidden taxonomy or auto-memory instructions.
  Source: supported. Evidence: Empty isolated home completes continuation close with recording disabled; no hidden taxonomy, telemetry, or private-store writes.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B17.AC2 — observed-bounded**: Composed verification emits no duplicate observations; enabled records share task/run identity and validation.
  Source: supported. Evidence: Enabled final recorder emits one actual observation from two duplicate candidates per finding; common execution/task/source/evidence fields and real frozen tag checker output are preserved.
  Remaining: Bounded composition/dedup fixture is covered; no native multi-provider or private-store write claim.
- [ ] **B17.AC3 — partial**: Existing configured Claude stores remain usable from Claude, Codex, and Cursor; absent recording does not falsely pass an enabled gate.
  Source: supported. Evidence: Portable no-store path and existing profile are specified; unavailable evidence is not promoted.
  Remaining: No actual enabled configured-store workflow across Claude, Codex and Cursor; native probe is one existing Codex host.

## B18 — Maintain one capability-based provider reference and detect mirror drift

- [x] **B18.AC1 — observed-bounded**: Discovery, invocation, questions, delegation, model inheritance, recurrence, and memory resolve from actual capabilities.
  Source: supported. Evidence: Current capability table uses observed availability rather than universal provider assertions; native Codex catalog/read, explicit unavailable model/settings and other-host execution, and corrected canonical adapter references are recorded.
  Remaining: Capability resolution and its explicit unknown states are supported; an all-host certification is not an added AC requirement.
- [ ] **B18.AC2 — partial**: A stale copied block is detected without overwriting private instructions.
  Source: supported. Evidence: Read-only comparison implementation hashes delimited block and has no writes; corrected-placement probe preserves private fixture boundaries.
  Remaining: This pass did not locate and re-ground a dedicated stale-block mutation/exit assertion; do not infer from current-block equality alone.
- [x] **B18.AC3 — observed-bounded**: Provider probes prove intended inputs and discovery mechanism, or record unavailable; no universal claim follows from one host.
  Source: supported. Evidence: Native literal sentinel is exact and discovery source read is observed; record states existing authenticated/global setup and other hosts unavailable.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B19 — Add missing metadata boundary fixtures

- [x] **B19.AC1 — observed-bounded**: Both reproduced invalid inputs fail with clear codes; valid boundary inputs continue to pass.
  Source: supported. Evidence: Current fixture suite asserts name-bounds and compatibility-bounds failures with 1/500 valid and 501 invalid boundaries; final suite exit 0.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B19.AC2 — observed-bounded**: Existing checker and sync tests pass, including linked canonical directory enumeration.
  Source: supported. Evidence: Current checker and 41-test sync suite pass with linked canonical enumeration; one actual Windows junction lifecycle case skipped.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B19.AC3 — observed-bounded**: The checker still reports structural conformance separately from runtime skill quality.
  Source: supported. Evidence: Final checker reports structural errors/warnings only; policy explicitly separates routing, procedure outcomes and final-tree checks.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B20 — Give authoring and audit policy one owner

- [x] **B20.AC1 — observed-bounded**: Authoring, improve, and audit agree on fields, limits, check ownership, and exact validation commands.
  Source: supported. Evidence: Current shared policy owns binding checker limits/commands, and three callers reference it; corrected description target is advisory.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B20.AC2 — observed-bounded**: A wrong inventory member with an unchanged count is caught by the agreed check.
  Source: supported. Evidence: Existing fixture suite executes same-count wrong-member assertion for inventory-membership-drift.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B20.AC3 — observed-bounded**: No stale local-machine anecdote is a public prerequisite; recent staged-tree/tag validation fixes remain intact.
  Source: supported. Evidence: Current shared policy keeps local anecdotes out of prerequisite policy; retained staged-tree rules and canonical tag checks remain present, final structural suite and malformed/canonical tag probes provide bounded regression evidence.
  Remaining: No new source conflict or failing required control identified here; ordinary human review remains pending. This does not certify every possible authoring run.

## B21 — Establish outcome evaluation and verify recent improvements

- [x] **B21.AC1 — observed-bounded**: Seed cases include dirty review scope, consumer-contract closure, malformed tags, completion dependencies, wrong output roots, and a clean no-op.
  Source: supported. Evidence: JSON corpus enumerates all six named controls, with actual original engineering/domain artifacts for them; clean no-op is informed diagnostic evidence.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [ ] **B21.AC2 — partial**: Preserve prompts, source state, traces, final artifacts, grader criteria, failures, and unavailable cases; record cost/time/tokens only when measured.
  Source: supported. Evidence: Prompts, frozen sources, available shell traces, outputs, failures and null telemetry are preserved; both no-skill repetitions are complete.
  Remaining: Complete host trace unavailable; original domain froze four fewer references; requested effective model identity unverified.
- [ ] **B21.AC3 — partial**: Before adopting broad simplification, define acceptable outcome tradeoffs and compare missed obligations, interruptions, retries, and artifact size.
  Source: supported. Evidence: Predeclared zero-missed-obligation rule exists; current/candidate repeated outputs and interruption/retry/size records preserved; broad simplification not adopted.
  Remaining: Literal/order deviations block attributable analyzer savings; human judgment pending, no cost data.
- [x] **B21.AC4 — observed-bounded**: September 4 applied fixes receive new outcome evidence rather than duplicate implementation tickets.
  Source: supported. Evidence: Fresh tag/consumer-closure/completion controls exist as outcome artifacts for already applied September 4 fixes; no new duplicate implementation claim.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B21.AC5 — observed-bounded**: Exercise the engineering addendum's reuse/new-file cases; grade behavioral coverage, repository fit, and unnecessary complexity together, without rewarding fewer files at the expense of correctness.
  Source: supported. Evidence: All three test-placement alternatives and needless helper proposal are exercised; parent independently reran candidate/current/no-skill artifacts across both repeats, with preserved source hashes and meaningful test outputs.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B22 — Carry engineering requirements and evaluate shorter skill bodies

- [x] **B22.AC1 — observed-bounded**: Every named engineering stage accounts for repository instructions, nearby code/tests/docs/CI, suitable reuse, focused scope, and justified test-file creation. This remains required if the simplification experiment is inconclusive or retains current wording.
  Source: supported. Evidence: Current source excerpts and reviewed caller references place the shared addendum at each named stage; existing/new test-home and reviewer fixtures plus final fix producer/verification preserve context, reuse, scope and coverage requirements.
  Remaining: The criterion requires every stage to account for the contract, not independent Cartesian trials of every stage and fixture. Human review remains pending; no universal adherence claim.
- [ ] **B22.AC2 — not-adopted**: For an adopted simplification, small tasks produce shorter complete artifacts; complex cases retain consumer closure, rollback, uncertainty, and test obligations.
  Source: not-adopted. Evidence: Parent comparison retains original analyzer structure; no simplification adoption and no savings claim.
  Remaining: Conditional adopted-simplification AC is not invoked; do not turn inconclusive pilot into failure or success of an adopted design.
- [ ] **B22.AC3 — partial**: References load when needed, including negative/error cases; required fields still resolve for downstream callers.
  Source: supported. Evidence: Final taskless producer/consumer required AC fields resolve correctly and complete frozen domain references are loaded.
  Remaining: W1 final output still drops required Summary fields despite loading the template; broad downstream-field completeness is not satisfied by this trial.
- [x] **B22.AC4 — observed-bounded**: Report actual size/cost/outcome changes; no target is met merely by packing longer lines or dropping evidence.
  Source: supported. Evidence: Actual artifact byte records and prompt hashes are preserved; cost/tokens unavailable; compared runs do not justify savings or denser-line target claims.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B23 — Honor existing authorization and make approval cadence proportional

- [x] **B23.AC1 — observed-bounded**: Equivalent inline/file inputs have equivalent paths; a no-op does not require generic confirmation.
  Source: supported. Evidence: Inline/file variants take equivalent authorized draft paths; informed no-op case makes no generic confirmation request.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B23.AC2 — observed-bounded**: Missing load-bearing information still raises a precise question; authorization is never inferred from a score.
  Source: supported. Evidence: Retention rule absence produces a precise blocking question; score is not used to infer authority.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [ ] **B23.AC3 — partial**: Comparison runs measure interruptions and retained decision quality; user-directed walkthrough cadence remains intact.
  Source: supported. Evidence: Runs record interruptions separately from needed clarification; requested walkthrough stops at item 1.
  Remaining: Judgment-heavy decision quality review remains pending; no controlled benefit claim from protocol-deviating runs.

## B24 — Scale independent review and separate severity from certainty

- [ ] **B24.AC1 — partial**: Small isolated changes avoid automatic three-agent review; cross-boundary risk retains independent checks.
  Source: supported. Evidence: Small isolated change gets one pass; cross-boundary auth change gets separate scoped checks.
  Remaining: Native independent workers forbidden within original trial; sequential fallback has explicitly weaker independence, not an actual multi-worker comparison.
- [x] **B24.AC2 — observed-bounded**: A severe uncertain issue is reported with uncertainty rather than silently scored out.
  Source: supported. Evidence: Severe possible auth bypass remains INFERRED and visible with confirming/refuting probe despite missing runtime path.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [ ] **B24.AC3 — partial**: Compare missed defects, false positives, latency, and measured cost; preserve parent re-grounding.
  Source: supported. Evidence: Fixture missed-obligation/false-positive judgments and batch times exist; source is re-grounded; cost is null.
  Remaining: Controlled per-review latency/cost and owner-validated defect comparison unavailable; no review-depth savings established.
- [x] **B24.AC4 — observed-bounded**: Reviewers apply the engineering addendum: flag avoidable new test files, duplicated utilities, unrelated cleanup, and unnecessary complexity with repository evidence; accept justified new files and preserve needed coverage.
  Source: supported. Evidence: Actual evidence-based review rejects duplicate test/helper/cleanup and retains justified existing/convention-new/no-home paths with meaningful coverage.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B25 — Reuse fresh check evidence and select relevant gates

- [x] **B25.AC1 — observed-bounded**: Unchanged implementation-to-verification does not rerun identical checks; relevant changes invalidate reuse.
  Source: supported. Evidence: Executed full unit/build record reused under matching identity; source/config changes invalidate affected check; no fresh execution is fabricated.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B25.AC2 — observed-bounded**: Blocked/incomplete suites cannot become pass; recorded evidence names actual coverage.
  Source: supported. Evidence: Executed positive-only subset remains subset; blocked integration never becomes full gate PASS.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [ ] **B25.AC3 — partial**: Required missing environment keys fail, deliberate unrelated differences do not; observable UI checks can use recorded browser evidence.
  Source: supported. Evidence: Required production key probe exits 1 and irrelevant staging difference is allowed.
  Remaining: Actual current-build browser evidence for this engineering AC is unavailable. Teaching-export browser evidence is a different AC and cannot satisfy check-reuse.
- [x] **B25.AC4 — observed-bounded**: Required test additions extend a suitable existing test file; a new file is used only when repository conventions require it or no suitable home exists. Both paths retain meaningful coverage and use the repository's fixtures/helpers where suitable.
  Source: supported. Evidence: Preserved source/tests and parent reruns show meaningful negative/zero/positive coverage in all three allowed file-placement paths.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B26 — Refresh documentation tasks without losing progress

- [x] **B26.AC1 — observed-bounded**: An unchanged scan is a no-op; an alphabetically earlier addition does not remap completed tasks.
  Source: supported. Evidence: Existing completed ID retained despite alphabetically earlier additions; reported identical second reconciliation keeps hash stable.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B26.AC2 — observed-bounded**: Renames/retirements are surfaced for review; manual notes survive.
  Source: supported. Evidence: Original manual note and Verify text survive; possible rename does not inherit status and retirement stays reviewable.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [ ] **B26.AC3 — partial**: Independent flows in one file remain separable; a connected cross-file flow can remain one workflow.
  Source: supported. Evidence: Same-file health/POST/Functions flows remain separate.
  Remaining: Connected cross-file flow grouping was not independently demonstrated by original model artifact.

## B27 — Evaluate discovered skills by inspected evidence

- [x] **B27.AC1 — observed-bounded**: A popular but mismatched candidate is not ranked as proven merely by stars/downloads.
  Source: supported. Evidence: Final comparison opens both candidate bodies/metadata and referenced Maven script; popular Java candidate is rejected for Python, compatible Python candidate has outcome/license limits, and ordinary unittest help stays direct. No install or real marketplace quality claim.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B27.AC2 — observed-bounded**: A recommendation states inspected compatibility and outcome evidence, or its absence.
  Source: supported. Evidence: Final comparison opens both candidate bodies/metadata and referenced Maven script; popular Java candidate is rejected for Python, compatible Python candidate has outcome/license limits, and ordinary unittest help stays direct. No install or real marketplace quality claim.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B27.AC3 — observed-bounded**: Ordinary how-to questions without discovery intent do not automatically become installation searches.
  Source: supported. Evidence: Final comparison opens both candidate bodies/metadata and referenced Maven script; popular Java candidate is rejected for Python, compatible Python candidate has outcome/license limits, and ordinary unittest help stays direct. No install or real marketplace quality claim.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.

## B28 — Route from current intent and valid artifact state

- [x] **B28.AC1 — observed-bounded**: A new unrelated task is not forced back into an old chain.
  Source: supported. Evidence: New search task and old unrelated billing/incident artifacts remain separate in routing outputs.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B28.AC2 — observed-bounded**: Failed/stale review cannot advance work; lifecycle routing respects repository/live boundaries.
  Source: supported. Evidence: Related stale identity halts advancement; repository GO does not authorize or complete deployment.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B28.AC3 — observed-bounded**: Explicit “recommend only,” explicit execution, and requested walkthrough prompts each follow their intended route.
  Source: supported. Evidence: Recommend-only, authorized continuation subject to valid evidence, and explicit tour take their respective routes; missing implementation/tour inputs remain unavailable.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B29 — Add durable decision lifecycle metadata

- [x] **B29.AC1 — observed-bounded**: Aging is derived from an actual date; an undated legacy record is explicitly unknown.
  Source: supported. Evidence: New ADR has actual supplied date; legacy undated age is explicitly unknown, not file-time inferred.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B29.AC2 — observed-bounded**: Human-owned rationale is not relabeled as invented text; draft fields cannot appear approved by implication.
  Source: supported. Evidence: Synthetic user-provided rationale is preserved as human-supplied within fixture; generated consequences remain draft and review unreviewed.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B29.AC3 — observed-bounded**: A superseding decision preserves the earlier record and its relationship.
  Source: supported. Evidence: Old ADR body remains with appended lifecycle relationship; new record carries supersedes link.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B30 — Clarify teaching artifact portability

- [x] **B30.AC1 — observed-bounded**: The promised export opens after relocation/offline with required assets intact; render it and inspect the result.
  Source: supported. Evidence: Actual model HTML relocated byte-identically; parent browser probe offline reports no request failures/errors or desktop/mobile overflow and tests correct/incorrect choices.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B30.AC2 — observed-bounded**: All supported formats are discoverable from the skill; explicit-only provider behavior remains intact.
  Source: supported. Evidence: Current teach body links all four supported format files; explicit-only Cursor metadata and Codex policy are retained in source and pass the final portability checks. Original teaching invocation was explicit.
  Remaining: Format discoverability and retained explicit-only configuration are supported. No fresh native-host selection experiment is claimed or added as a new requirement.
- [x] **B30.AC3 — observed-bounded**: Quiz alternatives remain semantically sound without forced padding.
  Source: supported. Evidence: HTML quiz uses meaningful retry/idempotency alternatives; parent interaction probe distinguishes correct and incorrect choices without artificial padding.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B31 — Complete parallel work by coverage, not majority

- [x] **B31.AC1 — observed-bounded**: If the sole security/domain lane stalls, its coverage remains missing until recovered or explicitly excluded.
  Source: supported. Evidence: Final supplied control-plane snapshot retains required security as running/missing, preserves returned outputs byte-identically, withholds completion and unauthorized exclusion, and labels source findings separately from runtime proof. Recovery is a proposed synthetic-handle operation; no live agent controlled.
  Remaining: Bounded missing-charter/persistence/classification fixture is covered; actual host recovery and compaction reliability are not claimed and are not added as universal acceptance requirements.
- [x] **B31.AC2 — observed-bounded**: Completed outputs survive context changes and are not needlessly rerun.
  Source: supported. Evidence: Final supplied control-plane snapshot retains required security as running/missing, preserves returned outputs byte-identically, withholds completion and unauthorized exclusion, and labels source findings separately from runtime proof. Recovery is a proposed synthetic-handle operation; no live agent controlled.
  Remaining: Bounded missing-charter/persistence/classification fixture is covered; actual host recovery and compaction reliability are not claimed and are not added as universal acceptance requirements.
- [x] **B31.AC3 — observed-bounded**: Parent verification still distinguishes source inspection from runtime evidence and records unresolved conflicts.
  Source: supported. Evidence: Final supplied control-plane snapshot retains required security as running/missing, preserves returned outputs byte-identically, withholds completion and unauthorized exclusion, and labels source findings separately from runtime proof. Recovery is a proposed synthetic-handle operation; no live agent controlled.
  Remaining: Bounded missing-charter/persistence/classification fixture is covered; actual host recovery and compaction reliability are not claimed and are not added as universal acceptance requirements.

## B32 — Make sync conflict diagnostics reflect transaction state

- [x] **B32.AC1 — observed-bounded**: Preflight conflicts accurately report no mutation.
  Source: supported. Evidence: Current preflight fixture asserts untouched root and nonmutating conflict message; final sync suite passes.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B32.AC2 — observed-bounded**: The race fixture reports prepared/recovery state and never claims an unchanged filesystem.
  Source: supported. Evidence: Current action-time race fixture asserts prepared transaction, conflict diagnostic and absence of false unchanged message; final sync suite passes.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [ ] **B32.AC3 — partial**: Existing recovery, ownership, idempotency, and relevant hosted platform checks remain green.
  Source: supported. Evidence: Linux recovery, ownership, idempotence suite passes; source and log hashes match current final validation inputs.
  Remaining: No live hosted final-tree macOS/Windows/Python3.12 run; Windows junction lifecycle explicitly skipped locally.

## B33 — Verify the public bootstrap and distribution surface

- [ ] **B33.AC1 — partial**: A fresh user can install, validate, discover, and attempt a representative workflow from documented steps.
  Source: supported. Evidence: Isolated install/dry-run/check and local validation work; actual existing Codex native catalog/source read and representative task attempt are preserved.
  Remaining: Not one fresh authenticated-home install/discover/task workflow; other providers unavailable, no universal bootstrap proof.
- [x] **B33.AC2 — observed-bounded**: Unavailable provider execution is explicit; setup does not overwrite user-owned instructions or roots.
  Source: supported. Evidence: Provider records disclose unavailable execution and existing global state; isolated ownership tests and corrected-placement probe preserve foreign/private entries.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [ ] **B33.AC3 — partial**: Repository license text agrees with the README; shipped examples contain no private names/paths.
  Source: partial. Evidence: MIT text exists and README explicitly states pending attribution.
  Remaining: Copyright year/holder remain owner-required placeholders; this pass does not claim exhaustive public example privacy certification. Final license acceptance pending user answer.

## B34 — Improve learning recommendation evidence and concise presentation

- [x] **B34.AC1 — observed-bounded**: A readiness verdict states what was tested and does not certify unknown next-topic prerequisites.
  Source: supported. Evidence: Readiness result names demonstrated concepts and excludes unspecified consensus/next-topic prerequisites.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B34.AC2 — observed-bounded**: A diagram-dependent article receives visual inspection or a clear uncertainty-based recommendation.
  Source: supported. Evidence: Arrow-order-dependent article result is based on rendered supplied diagram and explicitly asks targeted visual review.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.
- [x] **B34.AC3 — observed-bounded**: Interactive output is concise while existing structured consumers still receive their expected schema.
  Source: supported. Evidence: Concise interactive recommendation plus unchanged structured consumer fields/mode are both present in original artifact.
  Remaining: Final human acceptance remains pending; bounded fixtures do not establish general model reliability.

## B35 — Allow post-mortems to refine the causal record

- [x] **B35.AC1 — observed-bounded**: Missing evidence produces an honest draft; later contradiction is recorded and routed, not suppressed.
  Source: supported. Evidence: Actual final postmortem is an honest85% draft with missing impact/time evidence, dated contradiction and falsifying next probe, preserved original investigation, proposed/unassigned verifiable actions, and escalation kept as observation. Incident/log/owner inputs are synthetic.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B35.AC2 — observed-bounded**: Selected actions have verification and explicit ownership/date status.
  Source: supported. Evidence: Actual final postmortem is an honest85% draft with missing impact/time evidence, dated contradiction and falsifying next probe, preserved original investigation, proposed/unassigned verifiable actions, and escalation kept as observation. Incident/log/owner inputs are synthetic.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.
- [x] **B35.AC3 — observed-bounded**: Informative observations can remain observations without manufactured prevention work.
  Source: supported. Evidence: Actual final postmortem is an honest85% draft with missing impact/time evidence, dated contradiction and falsifying next probe, preserved original investigation, proposed/unassigned verifiable actions, and escalation kept as observation. Incident/log/owner inputs are synthetic.
  Remaining: No additional fixture obligation identified from the inspected artifacts. Human judgment remains pending; the bounded result is not universal reliability or native-host proof.

Confidence: 95%; uncertainty concerns bounded evidence and owner judgment, not a runtime success probability.
