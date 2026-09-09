# Astra review — 2026-09-06

The kit should keep its evidence checks and distinct task purposes, repair the contracts between skills, and make ceremony proportional to the work. A blanket rewrite for newer models is not supported by the evidence. The clearest immediate problems are incomplete change coverage, stale approval markers, conflicting output paths, misleading evidence states, and unreliable feedback accounting.

The execution handoff is [the prioritized backlog](20260906_astra_review_backlog.md). Every item is proposed; this review implements no fixes. The [original brief](20260906_astra_review.md) remains unchanged.

**Consolidated 2026-09-06:** the backlog incorporates the user's engineering addendum and the [fresh independent review](20260906_astra_review_independent_review.md). Its required R1 correction is now assigned to B08, including dirty Terraform root files and independently changing sibling modules. Its optional B22 refinement is also incorporated: required engineering alignment is checked separately from experimental prompt simplification. No required correction from that review remains unassigned in the plan; implementation and independent re-review of these edits have not run.

## Scope and method

Reviewed source: commit `aeec06b`, with no tracked working-tree edits at the start. The review covered all 31 canonical skill bodies, their local supporting resources, public instructions, provider adapters, common sync implementation, portability checker, tests, and relevant history. `audit-skills` and `write-skills` were examined as subjects; neither supplied the review method.

Three independent workers used the session's inherited model and separate persisted reports. The parent read all reports, checked load-bearing claims against current source, resolved overlaps, researched technical claims, and ran shared checks. The orchestration skill supplied dispatch/persistence discipline only.

| Lane | Charter | Coverage and verification |
|---|---|---|
| Engineering | Trace engineering and documentation contracts | Full reads of the 15 assigned skills and local references; parent re-grounded accepted findings |
| Support | Examine maintenance, learning, knowledge, and coordination skills | Full reads of the other 16 skills and support files; parent re-grounded accepted findings |
| Usage | Examine supplied local/backup evidence without exposing private contents | Metadata inventory, deduplication, selected whole observation reads, and tool-call metadata; historical outcomes were not replayed |
| Parent | Integrate evidence; inspect deployment/checker; verify external facts | Current-source reads, existing test suites, isolated negative probes, authoritative documentation, final artifact checks |

All lanes completed. Worker agreement was not used as proof. Scratch reports were persisted outside the repository; the findings and acceptance criteria needed for execution are carried into these two deliverables.

### Coverage limits

- The requested `~/codex` does not exist. Current `~/.codex` was examined as an explicitly labeled fallback, alongside current `~/.claude` and both supplied Windows backup roots.
- Private transcripts were screened through metadata and selected observations. This was not a semantic review of every historical conversation. Credentials, private databases, unrelated application contents, and raw transcript publication were excluded.
- No new Claude, Codex, or Cursor model comparison ran. There is no current Cursor usage sample sufficient for outcome claims. Available tools in this session prove this session's capabilities only.
- Linux tests ran here. No fresh Windows hosted run, cloud-permission probe, Terraform execution, or generated application-workflow run was performed.
- Archived v1 material and historical specs were consulted selectively, not audited as a second live product. Current canonical skills are the complete skill population under review.

## Findings that should drive the work

| Finding | Concrete evidence | Backlog |
|---|---|---|
| Reviews can miss the work being approved | `review-implementation:35` uses a committed diff plus status/untracked files; `verify-task:46` uses `HEAD~3..HEAD`. Neither command covers tracked live edits. | B01 |
| Review stamps do not identify reviewed content | `review-implementation:72` calls SHA plus `+dirty` a fingerprint; `review-artifact:73,81,95` trusts a review heading without content identity. | B02–B03 |
| Completion rules can form a cycle | `tasks-breakdown:74` puts operations after QA, but `implement-task:118` waits for every task to be Done before final review/QA. | B04 |
| Documentation producers and consumers disagree | `docs-tasks-creator:93,199` resolves outputs under its chosen output directory; `document-workflow:109` forces the source git root. | B07–B09 |
| Terraform documentation shares the freshness gap | `document-terraform:124–125` stamps HEAD and relies on path-limited history, including when inspected sibling sources are outside that identity. | B08 |
| Unknown state can become a false factual claim | Source reading counts as a verified incident hop in `bug-investigation:50`; Terraform reference `:188` makes unresolved permission checks red. | B06, B10–B11 |
| Feedback metrics do not measure invocations | `improve:85–90` counts observations as usage; `close:68–80` allows successful work to produce no observations. | B13–B17 |
| Public use depends on private deployment conventions | `close:88–96` assumes known auto-memory conventions; QA expects a private observation taxonomy; current private Codex mechanics lag the public two-root deployment rule. | B17–B18, B33 |
| Existing checks leave real gaps | Isolated schema fixture passed with an invalid name/empty compatibility; sync created a prepared manifest while claiming no changes. | B19, B32 |
| Fixed ceremony has no local performance baseline | Mandatory pauses, fixed reviewer counts, repeated tests, and long output contracts are present; their net value on newer models has not been measured. | B21–B25 |

Skill shorthand above means `skills/<name>/SKILL.md`; detailed paths and anchors are in each backlog item. These are instruction-contract findings unless an executable probe is explicitly named. They do not establish that a model always follows the faulty instruction or that a past production incident resulted from it.

## What to preserve

The evidence supports preserving these mechanisms while changing their presentation:

- Inspect original sources before accepting inherited claims; check the resulting file after a write. Historical usage includes successful detection of damaged command arguments and incomplete consumer contracts.
- Distinguish pass, fail, blocked, and unavailable. The current QA and portability work already records important execution boundaries.
- Review independently at meaningful boundaries. Consumer/deployment review and platform tests found defects that producer-side reasoning missed.
- Keep minimal implementation scope, consumer-to-provider mapping, acceptance-criterion ownership, completion dependencies, and genuine rollback evidence.
- Preserve append-only decision history, in-place documentation preservation, private/public separation, secrets exclusion, and ownership-aware sync recovery.
- Keep learning interactions distinct: a learner's explanation, unfamiliar-code onboarding, owner walkthrough, and item-by-item decisions serve different user intents. Similar headings are not a reason to merge them.

These strengths are grounded in `review-artifact:63–88`, `tasks-breakdown:69–103`, `qa-gates:96–149`, `update-workflow-docs:43–45`, the common sync tests, and selected usage evidence below.

### User-added engineering requirement — 2026-09-06

The user's follow-up screenshot adds an explicit requirement across analysis/design, task planning, implementation, and review: inspect repository instructions and nearby code, tests, documentation, and CI; follow established conventions; reuse suitable utilities and test files; avoid unrelated cleanup and unnecessary complexity; deliver clean, mergeable code. New test files are justified only by repository conventions or the absence of a suitable existing home. Meaningful behavioral coverage remains required where the change needs it.

The [backlog's engineering change requirements](20260906_astra_review_backlog.md#engineering-change-requirements--user-addendum-2026-09-06) map this to the affected skills and B21, B22, B24, and B25. This is an adopted user requirement; evaluation will test its implementation, not gate its acceptance. The screenshot supplies the requested guidance, not an additional measured performance result for this kit.

## Size and maintainability

Measured this session by explicit directory enumeration, strict frontmatter parsing through the existing checker, and full-file text counts:

| Metric | Result | Meaning |
|---|---:|---|
| Canonical skills | 31 | Directory entries with `SKILL.md`; links were accounted for during enumeration |
| Total `SKILL.md` lines | 4,610 | `splitlines()` over complete files |
| Total whitespace words | 57,552 | Includes frontmatter; not model tokens |
| Description characters | 17,663 | Parsed description strings; not guaranteed loaded context |
| Descriptions over 600 characters | 12 | House guidance, not 12 standards violations |

Line count alone hides density. `compile-kb` has 5,396 body words in a 228-line file; `document-terraform` has 4,855 body words in 158 lines. Conversely, a well-spaced checklist can be long in lines and easy to use. B22 therefore evaluates required information and generated results, not a universal line cap.

There are also concrete policy copies to reconcile: `improve:88–100` still describes a 1,536-character threshold and ten audit checks; `audit-skills:50–90` now describes twelve checks and a 1,024-character portable limit. `write-skills:31–40,81` has a separate field description that disagrees with the checker. The September fixes to audit validation already exist and should be retained; these are remaining seams, not a claim that the entire recent repair is absent.

## Usage evidence: useful, but not a success-rate dataset

Aliases: **CC** = current Claude home; **CX** = current Codex home; **BC/BX** = the supplied Windows backups. Private names and mount locations are intentionally absent.

| Measured source | Current | Backup | Interpretation |
|---|---:|---:|---|
| Claude observation files | 609 | 599 | 505 byte-identical contents are shared; summing roots overstates evidence |
| Selected Claude ai-kit JSONL files | 38 | 37 | 7,972 / 7,556 parsed records |
| Selected prior Codex ai-kit JSONL files | 26 | 5 | 17,547 / 446 parsed records |

Selection used recorded ai-kit working directories/project paths and excluded this audit's current Codex sessions. All selected JSONL parsed successfully. Counts include child-agent files and migration overlap; they are not distinct user sessions. Claude tool metadata contained 27 deduplicated canonical skill calls, concentrated on kit maintenance. Codex explicit-request extraction did not yield usable routing evidence. Neither absence supports retiring a skill.

Selected whole observations supply these privacy-safe evidence groups:

| Evidence | Locator | Use in this review |
|---|---|---|
| U-A: validation and actual mechanism | CC `2026-06-04-codex-skill-yaml.md` obs. 1–2; `2026-07-10-codex-machine-link.md` obs. 1–3 | Preserve strict parsing and verify intended probe input/invocation; historical repairs are regression cases |
| U-B: inspect the final artifact | CC `2026-06-18-codex-doc-cmd-mapping.md` obs. 1; `2026-08-24-triage-learning-content-authoring.md` obs. 1–3 | Trigger success did not establish body correctness; post-write checks caught corruption |
| U-C: independent consumer review | CC `2026-08-31-provider-neutral-portability-analysis.md` obs. 1–2; `2026-08-31-portability-techspec-review.md` obs. 1–2 | Preserve targeted independent review, scope distinctions, and restoration provenance |
| U-D: real platform execution | CC `2026-09-01-ai-kit-preserve-policy.md` obs. 1–6; `2026-09-01-ai-kit-post-review-remediation.md` obs. 3–10 | Keep fresh-home tests, failpoints, and platform boundaries; unavailable is not pass |
| U-E: recent changes need follow-up | CC `2026-09-04-improve-audit-close.md` obs. 1–5; September 4 improvement proposals 02 and 05 | Observation-tag and task-completion dependency changes are already applied; measure their next outcomes under B21 |
| U-F: current mirror drift | Complete current/backup private instruction comparison; public `docs/rules/skill-authoring.md:44–78` and `adapters/codex/AGENTS.md:14–24` | Private Codex copies retain old Windows/one-root mechanics; propose a drift check, preserving private policy |

The source reports include successful prevention as well as mistakes. Writer-assigned tags are inconsistent and observations are selective, often agent-authored. They support regression scenarios and investigation priorities; they cannot establish causal benefits, per-skill failure rates, or a model ranking. The user's current conciseness preference stands on its own and does not need a fabricated historical frequency.

## External evidence and its limits

Sources were checked on 2026-09-06. Recommendations below distinguish specification, provider capability, and task-outcome evidence.

| Source | Supported conclusion | Limit and application |
|---|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | Portable metadata rules and progressive disclosure have an explicit contract. | Conformance does not prove task quality. B19 adds missing boundary fixtures. |
| [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills), [Claude skill documentation](https://code.claude.com/docs/en/skills) | Hosts load skill content progressively and can budget/truncate catalog descriptions. | `audit-skills:86` must not assume every description always reaches startup context. Measure the effective catalog. |
| [Anthropic: agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Evaluate tasks, repeated trials, execution traces, and final outcomes with suitable graders. | Method guidance, not a benchmark of this kit. B21 separates routing, procedure, and outcome checks. |
| [Vercel: AGENTS.md versus skills](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) | A compact always-available documentation index beat tested skill variants on Vercel's Next.js evaluation. | Version-specific tasks and packaging; not proof all procedures belong in global instructions. Contextualize `write-skills:21`. |
| [Evaluating AGENTS.md](https://arxiv.org/html/2602.11988v1) | Repository instructions can add cost without improving outcomes in the studied coding settings. | Python-heavy repository benchmarks and tested model versions, not all current models or skill workflows. Supports local ablation, not universal removal. |
| [Anthropic: context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | High-signal context and appropriate instruction detail are useful design principles. | Engineering guidance; B22 still needs comparative trials. |
| [Anthropic: multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system) | Parallel agents improved a particular research system with a substantial token tradeoff. | Research outcomes do not justify fixed fan-out for every code change. B24 tests task-specific review depth. |
| [Terraform variables](https://developer.hashicorp.com/terraform/language/block/variable), [modules](https://developer.hashicorp.com/terraform/language/modules/configuration), [backends](https://developer.hashicorp.com/terraform/language/backend) | Root inputs differ from child module arguments; absent explicit backend configuration can mean the default local backend. | Official semantics corroborate B11; effective cloud state remains unobserved. |
| [Next.js source directory](https://nextjs.org/docs/app/api-reference/file-conventions/src-folder), [ASP.NET Core shared framework](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/target-aspnetcore?view=aspnetcore-10.0) | `src/app`/`src/pages` and implicit Web SDK framework references are supported forms. | They expose restrictive activation rules in B09. Other detector forms remain fixture-validation targets. |

No evidence here ranks the newer model families named in the brief. Their inclusion should be configuration and a recorded evaluation result, not a permanent name-based quality ladder.

## Proposed provider decision table

This is the direction for B18, not a claim that each feature was live-tested. Keep task semantics in canonical skills; place versioned host mappings in one maintained reference. A model's reasoning ability does not determine which tools its host exposes.

| Decision | Claude Code | OpenAI / Codex | Cursor |
|---|---|---|---|
| Discovery and explicit invocation | Resolve installed skill catalog and native invocation | Resolve catalog and `$skill`/native picker | Resolve catalog and native skill command; account for compatibility roots |
| Automatic selection | Use documented description/opt-out behavior | Use description selection and supported overlay | Use documented selection/explicit-only behavior |
| Questions | Use the active structured tool if exposed; text fallback | Same capability check; current public adapter's blanket “none” is too broad | Same capability check; surface/mode may differ |
| Delegation | Native workers if available and authorized | Native workers if available and authorized | Native workers if available and authorized |
| Worker model | Inherit by default; explicit supported override only | Same; record effective model and settings | Same; documented default is inheritance |
| Goal / recurrence | Check installed runner, persistence, and stop controls | Check actual tools; no assumption from provider name | Check installed `/loop` support and stop controls |
| Memory / feedback | Explicit store and schema; existing Claude paths supported | Same store contract; no assumed Claude auto-memory API | Same store contract; no private setup prerequisite |
| Validation | Record provider/version, discovery mechanism, task outcome | Same; unavailable stays explicit | Same; duplicate catalog entries are not a precedence guarantee |

Capability grounding: [Claude skills](https://code.claude.com/docs/en/skills), [OpenAI skills](https://learn.chatgpt.com/docs/build-skills), [Cursor skills](https://prod.cursor.com/docs/skills), and [Cursor subagents](https://prod.cursor.com/docs/subagents). This session also exposed structured questions, native workers, and a goal tool, directly disproving a universal “Codex has none” claim; that observation is limited to this host.

## Complete skill disposition

Every row was fully read. “Keep” means keep the distinct purpose while applying the linked repair or evaluation; it does not certify every future execution.

| Skill | Disposition | Backlog |
|---|---|---|
| analyze-work | Keep consumer mapping; simplify gated drafting/output | B21–B23 |
| audit-skills | Keep structural role; align policy and evaluate behavior separately | B19–B22 |
| breakout-session | Keep oral checkpoint; scope readiness evidence | B34 |
| bug-investigation | Keep trace/falsifier; distinguish causal evidence | B06, B23 |
| close | Keep durable closeout; fix run identity and portable storage | B13, B15, B17 |
| close-tasks | Keep artifact harvesting; verify provenance and content changes | B13, B16–B17 |
| compile-kb | Keep synthesis/source boundary; repair migration/resume and pauses | B12, B22–B23 |
| docs-tasks-creator | Repair output/detection; add deliberate progress-preserving refresh | B07, B09, B26 |
| document-terraform | Preserve topology/provenance; repair freshness, evidence, and resolution | B08, B10–B11, B22 |
| document-workflow | Repair path/freshness; evaluate proportional tracing/review | B07–B08, B24 |
| find-skills | Keep explicit discovery; inspect candidate evidence | B27 |
| implement-task | Keep bounded implementation; repair lifecycle and check reuse | B01, B03–B04, B25 |
| improve | Repair metrics, unresolved queue, and copied policy | B13–B14, B17, B20–B21 |
| lay-of-the-land | Keep current-state map; align equivalent input paths | B22–B23 |
| onboard-me | Keep Socratic purpose and durable map; portable store | B17, B22 |
| orchestrate | Keep persistence/re-grounding; replace majority completion | B18, B31 |
| post-mortem | Keep blameless record; allow later evidence and selected actions | B35 |
| qa-gates | Keep evidence gates; repair scope/freshness/lifecycle/recorder | B01–B04, B17, B25 |
| record-decision | Keep rationale ownership; add lifecycle metadata | B17, B29 |
| review-artifact | Keep independent checks; bind review to source/artifact | B02, B23–B24 |
| review-implementation | Repair diff/stamp; separate severity and certainty | B01–B02, B04, B24 |
| tasks-breakdown | Keep completion closure; repair lifecycle/concurrency/sizing | B04–B05, B22 |
| teach | Keep explicit teaching workflow; clarify export contract | B22, B30 |
| techspec | Keep minimal design/test map; evaluate optional depth/review | B22–B24 |
| triage | Match active intent and valid artifact state | B02, B28 |
| triage-learning-content | Preserve output interface; improve visual evidence/presentation | B34 |
| update-workflow-docs | Keep preservation/no-op behavior; bound freshness claim | B07–B08 |
| verify-task | Repair task-local scope; share fresh check evidence | B01, B03, B17, B25 |
| walkthrough | Keep explicit one-item mode; obey user-requested batching | B22–B23 |
| walkthrough-implementation | Keep owner explanation; make default activation proportional | B23, B28 |
| write-skills | Keep authoring purpose; align schema and evaluation claims | B19–B22 |

No skill retirement or merger is justified by the usage sample. A new feasibility-spike skill, global performance ceremony, a model-name ladder, and replacing the sync engine are deferred: no fresh requirement or comparative evidence establishes their value.

## Verification performed

| Check | Result | Boundary |
|---|---|---|
| `npm test` | All checker fixtures passed | Existing deterministic fixtures only |
| `npm run check:portability` | 31 skills; 0 errors, 0 warnings | Current final-mode structural/profile checks |
| `python3 tests/test_sync_skills.py` | 38 tests: 37 passed, 1 skipped | Windows junction lifecycle skipped on Linux; 28.078 seconds |
| Isolated schema negative fixture | Unexpected pass: `analyze--work`, matching name, `compatibility: ""`; no structural errors | Reproduces B19 without changing canonical files |
| Isolated sync race hook | Exit 1; manifest exists and transaction is prepared; diagnostic says no filesystem/manifest changes | Reproduces B32; recovery state is intentional, wording is false |

Runtime: Node `v24.20.0`, Python `3.14.7`. The package has no build target. Fresh hosted Windows verification remains an execution-task requirement for later sync changes. Historical hosted success in the existing portability investigation is not reported as today's result.

Reproduction anchors: checker field validation at `scripts/check-skill-portability.mjs:123–136`; a temporary repository fixture with the changed directory/frontmatter passed `checkRepository(root, 'structural')`. Sync probe reused the existing action-time hook setup at `tests/test_sync_skills.py:530`, then checked the manifest and stderr; the unconditional diagnostic is at `scripts/sync-skills.py:1055`. All probe writes were to temporary roots.

Artifact checks at initial handoff: 35 unique backlog items (19 P1, 15 P2, 1 P3), each with acceptance criteria and uncertainty; all 31 canonical skills covered; dependencies acyclic; no undefined item IDs, broken local Markdown links, trailing whitespace, or private absolute-path patterns in the new documents. These checks parsed both complete files and compared coverage with current `skills/` directory enumeration. Both documents were reread. The later independent review and consolidation preserve the backlog IDs and record the new dispositions without changing implementation. Consolidation validation is recorded in the independent review's disposition section.

## Recommendation and confidence

Start with bounded correctness repairs and the evaluation baseline in parallel where their files/resources do not conflict. Then use the baseline to choose shorter defaults, fewer interruptions, and review depth. Preserve the same-source tests and high-value source checks throughout. The backlog provides dependencies and acceptance evidence; it is ready for a separate execution goal, with design choices still labeled as such.

Confidence: **96%** for this review and prioritization. Weighted factors: documentation 98, comparable patterns 96, dependency understanding 96, complexity 92, external impact 94; weights 30/25/20/15/10 give 95.8%, rounded. The remaining 4% concerns unexecuted skill scenarios, selective historical evidence, provider/runtime differences, and the unmeasured benefits of simplification. Confidence percentages are judgment summaries, not calibrated success probabilities.
