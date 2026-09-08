# Windows portability shared-reference CRLF investigation

## Executive summary

The `windows-latest` portability job at commit `151d0a8` fails because the shared-reference
generator constructs normalized LF text but compares it byte-for-byte with generated Markdown
that Git checks out as CRLF on Windows. Normalize the generated file text before the comparison
and add a CRLF regression fixture; the source documents and generated content are otherwise
identical.

<!-- evidence:begin artifact-review-windows-crlf-20260908T1434Z -->

## Review

- **Record ID:** `artifact-review-windows-crlf-20260908T1434Z`
- **Timestamp:** 2026-09-08T14:34:26Z
- **Kind/verdict:** artifact review — **Approved with notes** after corrective delta
- **Repository/source identity:** `github.com/jimmyrleung/ai-kit` at
  `151d0a8bb5ebbdc7107ee42064f57782a766ac82`; repository root `.` during review.
- **Subject:** this investigation excluding this exact delimited evidence block. Post-correction
  subject SHA-256: `aeba4422164de06a7ea73ebff7e9f2e7e43bbd63b447d982bbec9613374dfb1d`.
- **Effective policy:** diagnosis rubric (40% causal evidence, 30% execution-path understanding,
  15% solution fit, 15% similar-pattern coverage); 95% threshold from the user's stricter
  convention; non-production CI failure at the named commit; normal depth; deterministic causal
  evidence required; review/correction only, with no implementation, commit, push, or hosted rerun.
- **Review method:** one independent generic reviewer plus coordinator re-grounding. Reviewer
  agreement was not used as causal evidence.
- **Layers:** committed dependencies at `HEAD`; this investigation was an untracked regular file
  and was read in full. No staged or unstaged source change was in scope. Four unrelated untracked
  entries (one local app directory and three externally owned skill junctions) were excluded as
  user work.

### Corrective delta

1. Corrected the failing path from the non-final check at
   `tests/test_skill_portability.mjs:54` to the final-mode assertion at lines 248–249, invoked at
   line 459 and routed through `scripts/check-skill-portability.mjs:375–378`.
2. Added this durable command/result record for the required same-commit Windows probes.
3. Tightened the proposed regression so CRLF-only output must pass while a non-EOL change in the
   same CRLF output must still report drift.

### Executed evidence

Environment: Microsoft Windows NT 10.0.26200.0; Node v24.18.0; npm 11.16.0; Git
2.35.2.windows.1.

| Probe | Scope/command identity | Observed result |
|---|---|---|
| Public Actions metadata | GitHub REST job/run/check endpoints for run `34227497060`, job `102065103785` | SHA `151d0a8`; Windows step 9 `Run portability fixtures` failed; macOS and Ubuntu sibling jobs passed; public annotation exposed exit 1 only. |
| Checkout EOL | `git config --get core.autocrlf`; `git check-attr text eol -- <source> <generated> <script>`; `git ls-files --eol` | `core.autocrlf=true`; Markdown had no EOL attribute; source and all generated references were index-LF/worktree-CRLF; `.mjs` was fixed to LF. |
| Clean same-commit reproduction | clean temporary `git archive` export of `151d0a8`; invoke `bundleSkillReferences(cleanRoot)` on Windows | 79 generated files; 79 `skill-reference-drift` findings; first and last findings covered the full generated-reference set. |
| Discriminating normalization | compare each original generated output with generator output after normalizing CRLF to LF; rerun read-only generator check | 0 normalized content mismatches; the temporary write rewrote 79 files; post-normalization findings: 0. |
| Complete fixture suite | `npm test --prefix <clean-export>` after only generated-output EOL normalization | Exit 0; `test_skill_portability: all fixtures passed`. |

### Reviewed dependency manifest

| Path | Kind | SHA-256 |
|---|---|---|
| `.gitattributes` | committed regular file | `14499c6a2e8ccba998009d915539bd063a1524385bfde607ccfc5e10b0fd9509` |
| `.github/workflows/portability.yml` | committed regular file | `758192bf6238670ad81098108a57750c22495004a5ae5df177ac3159ecca8c5d` |
| `package.json` | committed regular file | `1df8eff3a9b3fa66d8a94c56d05d6be65b15edb980d5740c0bc38e1915ac2184` |
| `scripts/bundle-skill-references.mjs` | committed regular file | `2a2e629da86f006f20188e017edbec7c1deb85291745cb825abd901832e6a61c` |
| `scripts/check-skill-portability.mjs` | committed regular file | `6fdec6bf3c03c8a31c5cb17c815960771c8ddaa7eda33d34132c3d0b9afe1dc9` |
| `specs/linux_portability_cross_agent/linux_portability_cross_agent_coupling_tasks.md` | committed regular file | `c09bd98d51bbc62a9ef0ddc0c48887c3b76f3de4ae9d9f65f4335f0616a70f33` |
| `specs/linux_portability_cross_agent/linux_portability_cross_agent_coupling_techspec.md` | committed regular file | `f48e02deea92757eda63608c6bf8ee95b001cae88c145781abd9be9c2a63442d` |
| `tests/test_skill_portability.mjs` | committed regular file | `af5083b353c91800ddf61f7667760161a21b835ebfe63776b4884b73d0b6eec4` |

### Post-review confidence

**Confidence score: 98% — corrected investigation and bounded minimal-fix recommendation.**

| Factor | Weight | Rating | Contribution | Evidence / gap |
|---|---:|---:|---:|---|
| Causal clarity and evidence | 40% | 98 | 39.20 | Same-commit Windows reproduction, 79/79 EOL-only mismatches, and zero findings after normalization; hosted raw stack unavailable. |
| Codebase/execution-path understanding | 30% | 100 | 30.00 | Correct final-mode fixture, checker boundary, generator comparison, Git EOL behavior, and introduction history were re-grounded. |
| Proposed solution simplicity and fit | 15% | 95 | 14.25 | One comparison boundary and one paired regression case are sufficient; the source patch is not implemented yet. |
| Similar-pattern coverage | 15% | 100 | 15.00 | Existing `find-skills` CRLF normalization and its prior hosted decision were verified. |
| **Total** | **100%** |  | **98.45 → 98%** | Arithmetic rechecked in PowerShell during review. |

**2% uncertainty:** the raw hosted stack was not anonymously available and the eventual source
patch still needs a fresh hosted matrix. These are implementation-verification requirements, not
blockers to using the corrected diagnosis.

**Recommendation/advancement:** **Approved with notes.** The corrected investigation satisfies the
95% review gate and may support a bounded fix. Implementation remains outside this review's
authorization. After implementation, run the paired CRLF/semantic-drift fixture, `npm test`,
`npm run check:portability`, and the hosted Ubuntu/macOS/Windows matrix.

<!-- evidence:end artifact-review-windows-crlf-20260908T1434Z -->

## Effective policy

- **Subject:** confirmed diagnosis of the Windows `Run portability fixtures` failure in run
  `34227497060`, job `102065103785`.
- **Severity/state:** non-production CI failure; active at commit `151d0a8`; normal-depth pass.
- **Rubric:** diagnosis — causal clarity and evidence 40%; codebase/execution-path understanding
  30%; proposed solution or next-probe simplicity and fit 15%; similar-pattern coverage 15%.
- **Advancement threshold:** 95%, from the repository's stricter user confidence convention.
- **Required causal evidence:** the same commit must reproduce on Windows, the reported files must
  differ only by line endings, and removing that difference must make the complete fixture suite
  pass.
- **Authorized action boundary:** investigation and minimal-fix proposal only. No fix, commit, push,
  or hosted rerun is authorized by this request.

## Confidence score

**Confidence score: 98% — confirmed diagnosis for the Windows fixture failure at `151d0a8`.**

| Factor | Weight | Rating | Contribution | Evidence / gap |
|---|---:|---:|---:|---|
| Causal clarity and evidence | 40% | 98 | 39.20 | Clean Windows reproduction found 79/79 generated references stale; CRLF-to-LF normalization produced 0 content mismatches and 0 findings. The public raw job log was not anonymously accessible. |
| Codebase/execution-path understanding | 30% | 100 | 30.00 | Workflow, test entry point, checker call, generator input normalization, and raw output comparison were traced end-to-end. |
| Proposed solution simplicity and fit | 15% | 95 | 14.25 | One comparison boundary plus one regression fixture addresses the demonstrated mechanism; the source patch itself has not been applied. |
| Similar-pattern coverage | 15% | 100 | 15.00 | The same repository already normalizes CRLF before hashing the `find-skills` textual content lock, following an earlier hosted Windows failure. |
| **Total** | **100%** |  | **98.45 → 98%** | Arithmetic checked in PowerShell. |

**Why 98%:** the failure was reproduced on Windows from a clean export of the exact CI commit;
all 79 findings disappeared when only line endings were normalized; normalized pre/post contents
had zero mismatches; and the full `npm test` fixture suite then passed.

**2% uncertainty:** the unauthenticated GitHub log endpoint did not expose the raw stack trace, and
the proposed source-level normalization has not yet been committed and rerun on a hosted Windows
runner. This does not block the bounded diagnosis, but a hosted matrix rerun remains required to
prove the eventual fix in GitHub Actions.

**Advancement:** the diagnosis may proceed to review and, after owner approval, a bounded fix.
Implementation, commit, push, and CI rerun remain outside the current authorization.

## Bug understanding

- **Reported issue:** the public GitHub Actions job
  `https://github.com/jimmyrleung/ai-kit/actions/runs/34227497060/job/102065103785`
  contains a Windows-specific error.
- **Expected:** `.github/workflows/portability.yml` passes on Ubuntu, macOS, and Windows.
- **Actual:** GitHub's job API reports macOS and Ubuntu success, while `windows-latest` fails only
  step 9, `Run portability fixtures`, which executes `npm test`.
- **Affected commit:** local `HEAD`, `origin/main`, and the job's `head_sha` all equal
  `151d0a8bb5ebbdc7107ee42064f57782a766ac82`.
- **Reproduction:** on Windows with `core.autocrlf=true`, export/check out that commit, install the
  locked dependency, and run `npm test`. The final-mode assertion in
  `testMatchingNameBoundariesAndLinkedPopulation` fails with `skill-reference-drift` for every
  generated shared reference.

## Entry point

`.github/workflows/portability.yml:69` runs `npm test`; `package.json` maps that command to
`node tests/test_skill_portability.mjs`. The failing fixture is invoked at
`tests/test_skill_portability.mjs:459`; its final-mode check and assertion are at lines 248–249.
That check calls the shared-reference validator through
`scripts/check-skill-portability.mjs:375–378`.

## Execution-path trace

1. **SOURCE:** `.github/workflows/portability.yml:69` names `Run portability fixtures`; its command
   is `npm test`. `package.json` maps the command to `tests/test_skill_portability.mjs`.
   **OBSERVED:** the GitHub job API reports this as the only failed step on `windows-latest`;
   Ubuntu and macOS jobs for the same run passed. **Causal limit:** the public annotation contains
   only exit code 1, not the assertion details.
2. **SOURCE:** `tests/test_skill_portability.mjs:459` invokes
   `testMatchingNameBoundariesAndLinkedPopulation`; its final-mode call and clean-result assertion
   are at lines 248–249. `scripts/check-skill-portability.mjs:375–378` incorporates
   `bundleSkillReferences(...).findings` only in final mode. Earlier structural/transitional
   checks do not raise these documentation findings as errors. **OBSERVED:** a clean Windows
   export of the exact commit reproduced 79 `skill-reference-drift` findings and failed the
   line-249 assertion.
3. **SOURCE:** `scripts/bundle-skill-references.mjs:24` normalizes every maintained source document
   from CRLF to LF. Line 116 builds each expected generated document with LF newlines.
   **SOURCE:** line 134 reads an existing generated document without normalization and compares it
   directly with the LF expected string.
4. **OBSERVED:** `git config --get core.autocrlf` returned `true`; `git check-attr` showed no text or
   EOL attribute for source or generated Markdown; `git ls-files --eol` showed index LF and working
   tree CRLF for both classes of Markdown. The executable `.mjs` files are explicitly LF in
   `.gitattributes`.
5. **OBSERVED:** across all 79 generated files, normalizing the checked-out CRLF content to LF
   yielded zero content mismatches. Running the generator in write mode in the temporary clean
   export rewrote 79 files, after which its read-only check returned zero findings and the full
   `npm test` suite printed `test_skill_portability: all fixtures passed` with exit 0.
6. **INFERRED:** the hosted Windows runner followed the same unspecified-Markdown EOL path. This
   inference is strongly linked by the same commit, same operating system, same failing step, and
   deterministic local failure; a hosted rerun after the patch is the final confirming probe.

## Root cause

**Category: Logic Error — line-ending-sensitive textual comparison.**

The generator defines shared references as normalized textual content, demonstrated by its input
normalization and normalized source hash, but validates generated outputs as raw platform checkout
bytes. Windows CRLF checkout therefore turns textually identical copies into false drift reports.
The test suite already treats the `find-skills` content pin as textual and line-ending-independent,
but the new shared-reference generator introduced in commit `57c02cb` did not reuse that rule.

**Falsifier:** after changing only the generated-output comparison to normalize CRLF to LF, a clean
Windows checkout of the same commit still reports `skill-reference-drift` before any semantic file
change. A hosted failure with a different assertion would also refute this as a complete diagnosis
of the reported job.

## Evidence

- GitHub job metadata: run `34227497060`, Windows job `102065103785`, commit `151d0a8`, failed step
  `Run portability fixtures`; sibling macOS and Ubuntu jobs passed.
- Clean Windows reproduction: 79 generated files, 79 `skill-reference-drift` findings, one finding
  per generated file.
- Line-ending probe: maintained sources and generated Markdown were CRLF in the Windows working
  tree while the index held LF; no Markdown EOL attribute applied.
- Discriminating probe: 0 normalized content mismatches across those 79 files; 0 findings after LF
  normalization; complete fixture suite exit 0. Exact commands, environment identity, and results
  are retained in review record `artifact-review-windows-crlf-20260908T1434Z`.
- Existing precedent: `scripts/check-skill-portability.mjs:315` normalizes CRLF for the
  `find-skills` content digest. The decision and earlier hosted failure are recorded at
  `specs/linux_portability_cross_agent/linux_portability_cross_agent_coupling_techspec.md:841`.
- Introduction point: `git blame` assigns generator lines 24, 116, and 134 to commit `57c02cb`
  (`Apply Astra review and walkthrough improvements`, 2026-09-08).

## Proposed solution

**Implemented remediation:** at
`scripts/bundle-skill-references.mjs:134`, normalize CRLF to LF on the existing generated file before
comparing it with the already-normalized expected text. Add a fixture near
`tests/test_skill_portability.mjs:289` that converts a generated shared reference to CRLF and
asserts that the generator reports no drift; then change a non-EOL character in that same CRLF
output and assert `skill-reference-drift`. This directly proves that normalization ignores only
checkout line endings and keeps semantic validation fail-closed.

This is the smallest behavior change: it makes the textual equality rule consistent at both input
and output boundaries, does not regenerate 79 committed files, and does not force LF on unrelated
Markdown.

## Alternative approaches considered

| Approach | Decision | Reason |
|---|---|---|
| Add `*.md text eol=lf` to `.gitattributes` | Not preferred | One line could make fresh CI checkouts pass, but it changes line-ending policy for all Markdown and leaves the validator unnecessarily checkout-dependent. |
| Add narrow EOL attributes only for sources and generated references | Viable fallback | Smaller checkout-policy scope than global Markdown, but existing working trees may remain CRLF until refreshed, and textual validation should not depend on Git configuration. |
| Regenerate the 79 files on Windows | Reject | It treats platform formatting as semantic content, creates a large noisy diff, and would reverse the failure on LF checkouts. |

## Impact assessment preview

- **Likely files:** `scripts/bundle-skill-references.mjs` and
  `tests/test_skill_portability.mjs` only.
- **Tests required:** `npm test`, `npm run check:portability`, and the full hosted
  Ubuntu/macOS/Windows portability matrix. The new fixture must show CRLF-only changes pass and a
  semantic change still fails.
- **Potential side effect:** the checker will intentionally ignore CRLF/LF-only changes in generated
  references. It must continue to detect changed characters, missing files, extra generated files,
  stale hashes, unknown dependencies, and linked output paths.

## Implementation

<!-- evidence:begin implementation-windows-crlf-20260908T1541Z -->

- **Record ID/status:** `implementation-windows-crlf-20260908T1541Z` — Done
- **Timestamp/base:** 2026-09-08T15:41:20Z;
  `151d0a8bb5ebbdc7107ee42064f57782a766ac82`
- **Resolved target:** tasks-doc stand-in is this investigation; task is `Proposed solution`;
  prefix is `windows_portability_shared_reference_crlf`; lifecycle boundary is pre-merge.
- **Intended paths:** `scripts/bundle-skill-references.mjs`,
  `tests/test_skill_portability.mjs`, and this implementation/verification record.
- **Excluded:** four unrelated untracked user entries and all other repository files.
- **Acceptance criteria:**
  1. A generated shared reference changed only from LF to CRLF produces no drift finding.
  2. A non-EOL character change in that same CRLF output produces `skill-reference-drift`.
  3. `npm test` and `npm run check:portability` pass locally; hosted matrix remains a post-push
     check outside this implementation authorization.
- **Dependencies:** approved review record `artifact-review-windows-crlf-20260908T1434Z`; current
  dependency hashes match its manifest.

### Pre-implementation confidence

**Confidence score: 99% — bounded two-file fix is ready for implementation.**

| Factor | Weight | Rating | Contribution | Evidence / gap |
|---|---:|---:|---:|---|
| Requirement/AC and scope coverage | 30% | 100 | 30.00 | Three explicit outcomes map to one comparison change and one paired fixture. |
| Direct source and executed-check evidence | 35% | 97 | 33.95 | Same-commit Windows reproduction and normalized full-suite pass are recorded; the source fix is not yet executed. |
| Data-flow, dependency and environment understanding | 20% | 100 | 20.00 | Source normalization, generated comparison, Git EOL behavior, and final-mode caller are traced. |
| Risk, regressions and rollback control | 15% | 98 | 14.70 | Semantic-drift countercheck bounds the normalization; rollback is the two-file patch. |
| **Total** | **100%** |  | **98.65 → 99%** | Arithmetic checked in PowerShell. |

**1% uncertainty:** the hosted runner matrix remains unexecuted. This does not block the verified
local implementation; hosted confirmation remains required before claiming cross-platform CI
closure.

**Outcome:** the bounded source edit and paired regression fixture were implemented in the two
declared code paths. No scope deviation occurred. Commit, push, and hosted rerun remain outside
authorization.

<!-- evidence:end implementation-windows-crlf-20260908T1541Z -->

### Verify

<!-- evidence:begin verify-windows-crlf-20260908T1547Z -->

- **Record ID/status:** `verify-windows-crlf-20260908T1547Z` — Passed
- **Timestamp:** 2026-09-08T15:47:47Z
- **Task ID/locator:** `windows-portability-shared-reference-crlf`; tasks-doc-less fix at
  `## Proposed solution`, with expected behavior from `## Bug understanding` and testable outcomes
  from `## Implementation` → `Acceptance criteria`.
- **Prefix/scope:** `windows_portability_shared_reference_crlf`; task; pre-merge.
- **Base:** `151d0a8bb5ebbdc7107ee42064f57782a766ac82`.
- **Declared files:** `scripts/bundle-skill-references.mjs`,
  `tests/test_skill_portability.mjs`.
- **Observed changes:** both declared files modified in the unstaged layer; this untracked
  investigation contains only the required implementation/verification evidence. Four unrelated
  untracked user entries are excluded.
- **AC source:** Implementation ACs 1–3, derived from the investigation's expected behavior,
  proposed solution, and impact assessment. No fix techspec exists; no duplicate obligations.
- **Budgets:** no line or size budget pinned (acceptable).
- **Behavior-pinning sweep:** `rg -n "bundleSkillReferences|skill-reference-drift|CRLF|crlf" tests`
  found the existing generator fixtures only; all affected assertions are in
  `tests/test_skill_portability.mjs` and are included in the full suite.
- **Check evidence:** clean Windows export with modified source SHA-256
  `5164655936c9d7cbf5d4e18957ac5053dfbd1f9adc5dfae795e84eed7bd4a33e` and test SHA-256
  `139d375a1ee3cf89ea4cac8591a6434874f209bde9f561b7803fdd7a88290191`;
  `npm test` exit 0; `npm run check:portability` exit 0 with 31 skills, 0 errors, 0 warnings;
  `git diff --check` exit 0.
- [x] **Gate 1 — build/test passed.** The repository has no separate build script. The matching
  clean Windows export passed `npm test` and `npm run check:portability`; the latter checked 31
  skills with 0 errors and 0 warnings. `git diff --check` also passed.
- [x] **Gate 2 — all 3 acceptance criteria passed.** The regression fixture converts one generated
  output to CRLF and gets no finding, then changes a non-EOL character in that CRLF output and gets
  `skill-reference-drift`. The full local checks in AC 3 passed as recorded above.
- [x] **Gate 3 — cross-cutting checks passed.** Node `v24.18.0` matches the repository's `24.x`
  engine; dependency and lock files are unchanged; no runtime configuration, secret, or trust
  boundary changed. No size budget or performance gate applies. The normalized comparison is
  bounded by the semantic-drift countercheck, and rollback is limited to the two declared files.

### Post-verification confidence

**Confidence score: 99% — the local fix and all task-level gates pass.**

| Factor | Weight | Rating | Contribution | Evidence / gap |
|---|---:|---:|---:|---|
| Requirement/AC and scope coverage | 30% | 100 | 30.00 | Every stated AC has a direct assertion or executed check. |
| Direct source and executed-check evidence | 35% | 98 | 34.30 | Full fixtures and portability checker passed in a matching clean Windows export. |
| Data-flow, dependency and environment understanding | 20% | 98 | 19.60 | The checkout boundary and Node version were verified; hosted CI is not rerun. |
| Risk, regressions and rollback control | 15% | 99 | 14.85 | Semantic drift remains fail-closed; the patch is two files. |
| **Total** | **100%** |  | **98.75 → 99%** | Arithmetic checked in PowerShell. |

**1% uncertainty:** the GitHub-hosted Windows/macOS/Ubuntu matrix has not run against this patch.
That is the remaining confirmation before claiming hosted cross-platform CI closure.

**Advancement:** all per-task gates pass. The implementation is ready for the prefix-level code
review, followed by `$qa-gates prefix=windows_portability_shared_reference_crlf`.

<!-- evidence:end verify-windows-crlf-20260908T1547Z -->
<!-- evidence:begin code-review-windows-crlf-20260908T155957Z -->

## Review — 2026-09-08

- **Record ID/kind/verdict:** `code-review-windows-crlf-20260908T155957Z`;
  `code-review`; **Approved**.
- **Timestamp:** 2026-09-08T15:59:57Z.
- **Repository/source identity:** public `github.com/jimmyrleung/ai-kit`; repository root `.`;
  base and HEAD `151d0a8bb5ebbdc7107ee42064f57782a766ac82`.
- **Scope:** prefix `windows_portability_shared_reference_crlf`; all repository work for this
  tasks-doc-less fix; lifecycle boundary `pre-merge`.
- **Inspected layers:** base-to-HEAD and staged layers contained no scoped change; the unstaged
  layer contained the two declared code/test changes; the untracked investigation was read in
  full as the requirements, implementation, and verification artifact. No rename or mode change.
- **Exclusions:** `.obsidian/`, `skills/grill-me/`, `skills/grill-with-docs/`, and
  `skills/improve-codebase-architecture/` are unrelated user-owned untracked content. Every other
  repository path is outside this focused fix except the dependency files in the manifest below.
- **Review depth:** one native independent pass covered correctness, conventions, and
  simplicity/repository fit, followed by lead verification. The independent reviewer made exactly
  one additional deliberate pass over both hunks and all three acceptance criteria. No edit landed
  during review.

### Content and dependency manifest

| Path | Role/layer | Mode | SHA-256 |
|---|---|---:|---|
| `.gitattributes` | EOL-policy dependency | `100644` | `14499c6a2e8ccba998009d915539bd063a1524385bfde607ccfc5e10b0fd9509` |
| `.github/workflows/portability.yml` | hosted-check dependency | `100644` | `758192bf6238670ad81098108a57750c22495004a5ae5df177ac3159ecca8c5d` |
| `docs/rules/skill-authoring.md` | repository-rule dependency | `100644` | `efc4ae1d60cca3a710567fc6e8e9defe71370bcae7f2f034da7fa7b1fe672df9` |
| `package-lock.json` | dependency identity | `100644` | `c73587fc6e5ccdae2240b72c7a310089fc7dc77cbf906ff1ad3ce48ae095818c` |
| `package.json` | command/runtime identity | `100644` | `1df8eff3a9b3fa66d8a94c56d05d6be65b15edb980d5740c0bc38e1915ac2184` |
| `scripts/bundle-skill-references.mjs` | reviewed unstaged source | `100644` | `5164655936c9d7cbf5d4e18957ac5053dfbd1f9adc5dfae795e84eed7bd4a33e` |
| `scripts/check-skill-portability.mjs` | caller/precedent dependency | `100644` | `6fdec6bf3c03c8a31c5cb17c815960771c8ddaa7eda33d34132c3d0b9afe1dc9` |
| `specs/linux_portability_cross_agent/windows_portability_shared_reference_crlf_investigation.md` | requirements and prior evidence before this review record | untracked Markdown | `f18f6d4ed04933631061b02d5b54ff4e238db1ecf1c9ec774216768f6c0ee68d` |
| `tests/test_skill_portability.mjs` | reviewed unstaged regression | `100644` | `139d375a1ee3cf89ea4cac8591a6434874f209bde9f561b7803fdd7a88290191` |

This review record is outside its hashed subject bytes. Recomputing the investigation dependency
removes only this exact delimited record, including its markers; all earlier investigation,
implementation, verification, and review evidence remains included.

### Coverage and findings

- **Correctness:** the generated-output boundary at
  `scripts/bundle-skill-references.mjs:134` now applies the same CRLF-to-LF textual rule as the
  maintained-source boundary at line 24. The paired fixture at
  `tests/test_skill_portability.mjs:300-310` proves CRLF-only equivalence, then reaches the real
  final checker and proves a non-EOL change still produces `skill-reference-drift`.
- **Conventions:** the test extends the existing `testSelfContainedReferences` fixture and reuses
  the existing generator, final checker, and assertion helper. It adds no helper, test file, or
  repository pattern.
- **Simplicity/repository fit:** the production change is one comparison-boundary normalization;
  the regression is the smallest paired positive/negative case. No unrelated cleanup is present.
- **Findings:** none. No supported Critical, High, Medium, or Low defect; no uncertain severe issue
  needs a confirming probe; no relevant pre-existing issue was found.
- **Refactors/dispositions:** none requested, fixed, deferred, or rejected as stale.

### Executed evidence

The independent pass executed the following against a clean Windows export whose scoped source and
test hashes match this manifest:

- `npm test` — exit 0; `test_skill_portability: all fixtures passed`.
- `npm run check:portability` — exit 0; 31 skills, 0 errors, 0 warnings.
- `git diff --check` for the scoped patch — exit 0.

The repository has no separate build script. The GitHub-hosted Ubuntu/macOS/Windows matrix remains
unrun against these bytes and is listed as a post-push check, not as completed evidence.

### Confidence score

**Confidence score: 99% — the complete scoped diff, all three acceptance criteria, dependencies,
and required local checks were independently reviewed with no supported defect.**

**Effective policy:** delivery rubric; 95% advancement threshold from the session owner policy;
required evidence is current full source/test content, the exact layered diff, acceptance criteria,
repository and CI conventions, and executed local checks. The authorized boundary is read-only
review plus this in-place review record; it does not include commit, push, deployment, or hosted
rerun.

| Factor | Weight | Rating | Contribution | Evidence / gap |
|---|---:|---:|---:|---|
| Requirement/AC and changed-scope coverage | 30% | 100 | 30.00 | All three ACs traced through the current source and paired fixture. |
| Direct source and executed-check evidence | 35% | 98 | 34.30 | Both files and exact diff inspected; complete clean-export checks passed; hosted CI is pending. |
| Data-flow, dependency and environment understanding | 20% | 98 | 19.60 | Source-to-generator-to-final-checker-to-Windows-CI path and Node `24.x` context inspected. |
| Risk, regressions and rollback control | 15% | 99 | 14.85 | Semantic drift remains fail-closed; rollback is the two-file patch. |
| **Total** | **100%** |  | **98.75 → 99%** | Tool-checked arithmetic. |

**Why 99%:** current byte identities match the independently reviewed and executed clean-export
checks; both changed hunks and every AC received a required second pass; no load-bearing evidence is
missing for repository code-review approval.

**1% uncertainty:** the hosted three-operating-system matrix has not run against the patch. This
does not block repository review approval or prefix-level QA, but it blocks any claim that hosted
cross-platform CI closure is proven. The next confirming check is the hosted matrix after an
authorized commit and push.

**Advancement:** Approved for
`$qa-gates prefix=windows_portability_shared_reference_crlf` within the pre-merge repository
boundary. Pending deploy/live tasks: none. Feedback recorder: disabled because no explicit recorder
was configured; no feedback record was written.

<!-- evidence:end code-review-windows-crlf-20260908T155957Z -->
<!-- evidence:begin qa-windows-crlf-20260908T163352Z -->

## QA — 2026-09-08

- **Record ID/status:** `qa-windows-crlf-20260908T163352Z` — Passed; owner GO recorded.
- **Timestamp:** 2026-09-08T16:33:52Z.
- **Repository/source identity:** public `github.com/jimmyrleung/ai-kit`; repository root `.`;
  base and HEAD `151d0a8bb5ebbdc7107ee42064f57782a766ac82`.
- **Resolved target:** prefix `windows_portability_shared_reference_crlf`; artifact is this
  investigation; scope kind `prefix`; lifecycle boundary `pre-merge`; mode `full`.
- **Authoritative AC source:** `## Implementation` → `Acceptance criteria`; three deduplicated
  outcomes derived from the reviewed tasks-doc-less fix at `## Proposed solution`.
- **Declared/observed code scope:** `scripts/bundle-skill-references.mjs` and
  `tests/test_skill_portability.mjs`, both unstaged regular files. Base-to-HEAD and staged layers
  contain no scoped change; this QA artifact is untracked. No rename or mode change.
- **Excluded user work:** `.obsidian/`, `skills/grill-me/`, `skills/grill-with-docs/`, and
  `skills/improve-codebase-architecture/`.
- **Prior-review check:** current and Approved. Review record
  `code-review-windows-crlf-20260908T155957Z` has SHA-256
  `78e2bc9dd808c3a0aea6b4937f9a17c42d2aeb9263a16d4369792076bae257e5`;
  its scoped code/test and dependency hashes match the current tree, and its pre-review artifact
  digest recomputes as `f18f6d4ed04933631061b02d5b54ff4e238db1ecf1c9ec774216768f6c0ee68d`.
  Open review follow-ups: none.
- **Budgets/versions/tests:** no line or size budget; Node `24.x` is the repository runtime pin;
  required commands are `npm test`, `npm run check:portability`, and `git diff --check`.
- **Lifecycle:** all repository work is `pre-merge` and Done. Pending `deploy`/`live` items: none.
- **Unchecked-box census before QA:** 0 across the only prefix artifact.
- **Effective policy:** delivery rubric (requirements/scope 30%, source/executed checks 35%,
  data-flow/dependencies/environment 20%, risk/regressions/rollback 15%); 95% advancement
  threshold from the session owner policy; all required Gates 1–4 must pass, and only the owner can
  supply Gate 5. Authorization now includes the owner's named scoped commit, push, and hosted-run
  observation, but not deployment.
- [x] **Gate 1 — build/test: pass.** Reused the matching executed checks from code-review record
  `code-review-windows-crlf-20260908T155957Z`: `npm test --prefix <clean-export>` exited 0 with
  `test_skill_portability: all fixtures passed`; `npm run check:portability --prefix
  <clean-export>` exited 0 with 31 skills, 0 errors, and 0 warnings. Source, test, package,
  lockfile, checker, workflow, and Windows/Node identities match. A fresh `git diff --check`
  executed in this QA run and exited 0. No separate build command exists in `package.json`.
- [~] **Gate 1 — committed: no.** The two reviewed files exist only in the working tree at
  `151d0a8bb5ebbdc7107ee42064f57782a766ac82`; this is informational. The owner supplied the
  required conditional GO at Gate 5.
- [x] **Gate 2 — AC #1:** “A generated shared reference changed only from LF to CRLF produces no
  drift finding” — pass (`tests/test_skill_portability.mjs:300-304`; executed by Gate 1).
- [x] **Gate 2 — AC #2:** “A non-EOL character change in that same CRLF output produces
  `skill-reference-drift`” — pass (`tests/test_skill_portability.mjs:305-310`; executed through
  the real final checker by Gate 1).
- [x] **Gate 2 — AC #3:** “`npm test` and `npm run check:portability` pass locally” — pass
  (matching complete executions cited at Gate 1). The hosted matrix remains the named post-push
  confirmation and is not misreported as local AC evidence.
- [x] **Gate 3a — environment expectations:** pass. QA observed Windows, Node `v24.18.0`, and npm
  `11.16.0`; Node matches the `24.x` repository pin. The changed comparison consumes no
  environment key or runtime configuration.
- [x] **Gate 3b — line budgets:** skipped — no line or size budget is pinned.
- [x] **Gate 3c — SDK/framework version:** pass. `package.json` pins Node `24.x`; the observed
  `v24.18.0` matches. Dependency and lock files are unchanged.
- [x] **Gate 3d — release readiness:** pass for this textual-comparison contract. Existing LF
  behavior is unchanged, CRLF is newly accepted, and the semantic-drift counterexample remains
  fail-closed. Rollback is the bounded two-file patch. No API, schema, auth/payment surface,
  secret, or new trust boundary is present.
- [x] **Gate 3e — perf/regression:** skipped — the change is not performance-sensitive and the
  repository has no local performance/regression skill.
- [x] **Gate 4 — docs consistency:** pass. The only prefix sibling is this investigation; its
  historical diagnosis and line locators remain tied to base `151d0a8`, while the appended
  implementation, verification, review, and QA records carry the current state and locators. No
  tasks doc exists; all pre-merge work is Done; no deploy/live work is implied. The pre-QA
  unchecked-box census was 0, and no test total conflicts with the latest 31-skill checker result.
- [x] **Gate 5 — human go/no-go:** `GO (repository scope), conditional on commit`, recorded from
  the owner's Yes decision at 2026-09-08T17:05:09Z. The pending scoped commit contains
  `scripts/bundle-skill-references.mjs`, `tests/test_skill_portability.mjs`, and this QA artifact.
  The owner separately authorized pushing that commit and watching its hosted portability run;
  this does not authorize deployment or claim hosted CI closure before the run passes.

### QA content and dependency manifest

| Path | Role/layer | Mode | SHA-256 |
|---|---|---:|---|
| `.gitattributes` | EOL-policy dependency | `100644` | `14499c6a2e8ccba998009d915539bd063a1524385bfde607ccfc5e10b0fd9509` |
| `.github/workflows/portability.yml` | hosted-check dependency | `100644` | `758192bf6238670ad81098108a57750c22495004a5ae5df177ac3159ecca8c5d` |
| `docs/rules/skill-authoring.md` | repository-rule dependency | `100644` | `efc4ae1d60cca3a710567fc6e8e9defe71370bcae7f2f034da7fa7b1fe672df9` |
| `package-lock.json` | dependency identity | `100644` | `c73587fc6e5ccdae2240b72c7a310089fc7dc77cbf906ff1ad3ce48ae095818c` |
| `package.json` | command/runtime identity | `100644` | `1df8eff3a9b3fa66d8a94c56d05d6be65b15edb980d5740c0bc38e1915ac2184` |
| `scripts/bundle-skill-references.mjs` | QA subject, unstaged | `100644` | `5164655936c9d7cbf5d4e18957ac5053dfbd1f9adc5dfae795e84eed7bd4a33e` |
| `scripts/check-skill-portability.mjs` | checker dependency | `100644` | `6fdec6bf3c03c8a31c5cb17c815960771c8ddaa7eda33d34132c3d0b9afe1dc9` |
| `specs/linux_portability_cross_agent/windows_portability_shared_reference_crlf_investigation.md` | complete artifact before this QA record | untracked Markdown | `7b63b76025762d407771ce938667cf58f48e2b7ab6562c4a19b23ce47aef4d2a` |
| `tests/test_skill_portability.mjs` | QA subject, unstaged | `100644` | `139d375a1ee3cf89ea4cac8591a6434874f209bde9f561b7803fdd7a88290191` |

This QA record is outside its hashed subject bytes. Recomputing the artifact dependency removes
only this exact delimited QA record, including its markers. The consumed approved review block is
included in the artifact digest and is also independently bound by SHA-256
`78e2bc9dd808c3a0aea6b4937f9a17c42d2aeb9263a16d4369792076bae257e5`.

### QA confidence score

**Confidence score: 99% — all five gates pass for the complete pre-merge repository outcome against
current content identities; the hosted matrix remains the post-push confirmation.**

| Factor | Weight | Rating | Contribution | Evidence / gap |
|---|---:|---:|---:|---|
| Requirement/AC and changed-scope coverage | 30% | 100 | 30.00 | All three ACs passed and the full prefix scope is classified. |
| Direct source and executed-check evidence | 35% | 98 | 34.30 | Complete matching test/checker executions and a fresh whitespace check are green; hosted CI is pending. |
| Data-flow, dependency and environment understanding | 20% | 98 | 19.60 | Current dependencies, Windows/Node identity, checker path, and approved review record all match. |
| Risk, regressions and rollback control | 15% | 99 | 14.85 | Semantic drift stays fail-closed; scope and rollback are bounded to two code/test files. |
| **Total** | **100%** |  | **98.75 → 99%** | Tool-checked arithmetic. |

**Why 99%:** every repository-controlled gate is green, the owner supplied GO, the approved review
record is current and content-bound, and no lifecycle or documentation gap remains in prefix scope.

**1% uncertainty:** the hosted Ubuntu/macOS/Windows matrix has not run against the patch. This does
not block repository QA or a conditional GO, but it blocks claiming hosted cross-platform CI
closure. The next confirming check is the hosted matrix after an authorized commit and push.

**Advancement:** all five gates pass. Proceed within the authorized repository boundary to the
named scoped commit, push, and hosted portability-run observation. Feedback recorder is disabled
because no explicit recorder is configured; no feedback record was written.

<!-- evidence:end qa-windows-crlf-20260908T163352Z -->
