# Loop-Engineering Action Items — from the COMPILOT study + Dec 2025–Jul 2026 research

**Input for a `/improve` session.** Each item names the target asset(s), the proposed change, the evidence behind it, and — per the AHE falsifiable-contract discipline this very list recommends — a **prediction** to verify against subsequent run outcomes before the change counts as settled.

**Provenance:** derived 2026-07-05 from `agentic_auto_scheduling_experimental_study.pdf` (PACT 2025, arXiv 2511.00592) and a 3-vote adversarially-verified deep-research sweep of the Dec 2025 – Jul 2026 literature. Full source notes and caveats: [`agentic_auto_scheduling_experimental_study.md`](agentic_auto_scheduling_experimental_study.md). Evidence tags used below: **[COMPILOT]**, **[Magellan]**, **[KernelSkill]**, **[KernelPro]**, **[llvm-autofix]**, **[ACCLAIM]**, **[AHE]**, **[AutoPass]**, **[Anthropic]** — links in the companion doc.

**Scope note:** items marked *(cc-looper)* need runner changes in the sibling cc-looper repo; ai-kit owns the skill-side contract. Validate skill edits with `npm test` and `npm run check:portability`, then deploy the common roots with `python3 scripts/sync-skills.py` per the standing sync rule.

---

## Already validated — no action

The research confirms these existing designs; do not "fix" them:

- Pinned-line structured-output contracts (`Status:`, `**Recommendation:**` regex lines) — the `<schedule>`-tag lesson. [COMPILOT]
- Mechanical QA gates and the "a build that never ran is *unverified*, not *passed*" rule in `skills/implement-task-loop/SKILL.md`. [COMPILOT RQ7], [llvm-autofix]
- Forced analysis-before-action phases (`lay-of-the-land`, investigation-before-fix). [COMPILOT RQ10]
- 230K soft budget + fresh-session resume; review-at-checkpoint (not per-task) cadence. [COMPILOT RQ9], [ACCLAIM]
- Tasks-doc → `map-tasks` plan.json → incremental per-task spawns = Anthropic's spec-initializer + incremental-executor pattern, first-party validated. [Anthropic]
- 3-way exploration phases in `integration-techspec` / `integration-tasks` — the K>1 diversity mechanism, exactly where the best-of-K curve is steepest. [COMPILOT RQ9]

---

## DO NOW — apply and benefit immediately

### AI-1 · Baseline gate at task start
- **Target:** `skills/implement-task-loop/SKILL.md` (Workflow 1); `skills/verify-task/SKILL.md` (Gate 1); `skills/qa-loop/SKILL.md` (run-level).
- **Change:** before touching anything, run the build/fast test suite and record the result in the task notes (`Baseline: green` / `Baseline: N pre-existing failures — <names>`). At run level, record a run-start baseline so `qa-loop`'s go/no-go can mechanically check "did this run regress the tree" (never-worse-than-baseline).
- **Evidence:** [COMPILOT] gives the agent the initial execution time so every later measurement is attributable; [AutoPass] builds never-worse-than-baseline into loop termination. The skill's existing "don't reclassify regressions as pre-existing" rule exists precisely because baseline state is currently a judgment call.
- **Prediction:** disputes over pre-existing-vs-introduced failures in Paused/Blocked notes and QA reports drop to zero in the next 2–3 loop runs; Gate 1 failures become attributable without re-derivation.
- **Confidence:** 95%.

### AI-2 · One push-to-continue pass in reviewer fan-outs
- **Target:** `skills/review-checkpoint/SKILL.md`, `skills/qa-loop/SKILL.md`, `skills/qa-loop-docs/SKILL.md` (subagent prompts).
- **Change:** each spawned reviewer, after producing findings, must take exactly one more deliberate pass over what it hasn't covered before concluding. Cap at one push — no open-ended loops.
- **Evidence:** [COMPILOT RQ11] — LLMs systematically quit early; parity with full exploration only past the 5th quit attempt, but diminishing returns and ~2% pathological never-quit cases justify the hard cap. Checkpoint reviews are the only per-checkpoint quality gate in loop mode, so their recall matters disproportionately.
- **Prediction:** findings-per-checkpoint rises measurably (via AI-7 metrics) with <15% added review cost; at least one post-push finding per run is rated blocker/major.
- **Confidence:** 90% (effect size in the review domain is extrapolated from the optimization domain).

### AI-3 · Distilled, machine-actionable findings contract
- **Target:** `skills/qa-loop/SKILL.md`, `skills/qa-loop-docs/SKILL.md`, `skills/review-checkpoint/SKILL.md` (findings format).
- **Change:** every finding must carry `file:line`, the exact failing command or AC, and a one-line expected-vs-actual. **Explicitly forbid pasting raw build/test/log output** into findings or any downstream retry/fix prompt — distill first.
- **Evidence:** [KernelPro] 3-arm ablation (p=0.0007): raw profiler dumps performed *worse than no feedback at all* (1.77× vs 3.35×); distilled directives reached 4.00×. Interpretation quality, not volume, is load-bearing. [COMPILOT]'s five feedback categories each carry the specific reason, never raw output.
- **Prediction:** a future fix cycle (AI-6) can act on a QA report with zero re-derivation of diagnoses; retry spawns stop re-running discovery the report already did.
- **Confidence:** 92%.

### AI-4 · Attempted-and-failed ledger on pauses, blocks, and retries
- **Target:** `skills/implement-task-loop/SKILL.md`, `skills/document-workflow-loop/SKILL.md` (Paused/Blocked note format + session-start reading discipline).
- **Change:** Paused/Blocked notes must record *approaches attempted and why each failed* (not just done/remaining). A retry/resume spawn must read this ledger first and is forbidden from re-proposing an approach the ledger marks failed, unless it names what changed.
- **Evidence:** [KernelSkill] introduces a short-term repair memory "to discourage repeated revisits of known-failing edits," breaking the observed "cyclic repair" failure mode; [COMPILOT RQ3] shows in-context learning from failure feedback is what drives the illegal-proposal rate down.
- **Prediction:** on multi-attempt tasks, attempt #2 stops repeating attempt #1's failed approach (checkable by comparing ledger entries across attempts in the next runs that hit retries).
- **Confidence:** 92%.

---

## DO SOON — clear benefit, moderate build cost

### AI-5 · Restart-with-carryover retry policy *(cc-looper)*
- **Target:** cc-looper runner retry logic; ai-kit side defines the carryover contract (what a fresh retry spawn receives: best prior state + AI-4 ledger + AI-3 distilled failure summary — never the full stuck transcript, never a blank slate).
- **Evidence:** [Magellan] — seeding a fresh run with the stalled run's best artifact escaped a plateau that both continued grinding *and* a blank-slate restart with a stronger model failed to escape; [COMPILOT RQ9] restarts beat grinding; [KernelPro] fresh-seed injection +26% over greedy.
- **Prediction:** tasks that previously needed human rescue after a failed attempt succeed on seeded attempt #2 at a visibly higher rate than the historical blank-resume behavior.
- **Confidence:** 88% (Magellan is a single case study, partially confounded by a model upgrade — but the from-scratch control failing makes the seeding contribution credible).

### AI-6 · Bounded automated fix cycle after `no-go` / `fix-then-proceed` *(cc-looper + one small skill)*
- **Target:** cc-looper runner; new small fix-task skill consuming `_qa.md` / `_checkpoint-*_review.md` findings (formatted per AI-3).
- **Change:** on `no-go` or `fix-then-proceed`, spawn a fix session with only the distilled findings + failing-gate evidence; re-run failed gates only. **Hard cap 1–2 cycles**, then surface to the human. Sequence the spend per [ACCLAIM]: within a budget, verifier-fed iterations first — parallel sampling never before iteration is exhausted.
- **Evidence:** [COMPILOT RQ6] closing the loop is the single biggest effect (23–40%); [ACCLAIM] compute-matched: n=1,k=4 iteration (1.19×) beats n=4,k=1 sampling (1.11×); [COMPILOT RQ11] the ~2% never-converging tail justifies the hard cap.
- **Prediction:** ≥⅓ of historical `no-go` runs would have converted to `go` within one automated fix cycle (backtestable against past `_qa.md` reports before building).
- **Confidence:** 85% (highest-ceiling item, but real runner work; sits next to the pending close-tasks Part B in cc-looper).

### AI-7 · Exploration-efficiency metrics in `close-tasks` → `/improve`
- **Target:** `skills/close-tasks/SKILL.md` (harvest), `skills/improve/SKILL.md` (fitness table).
- **Change:** emit per-run observation fields: attempts-per-task, gate failures per run, findings-per-checkpoint, pause/block causes. Adopt the now-standard conventions: **infra-crashed attempts count as failures (r=0), never silently dropped**, and any before/after comparison of loop configurations uses k≥2 rollouts, not a single anecdotal run.
- **Evidence:** [COMPILOT RQ3]'s runnable/invalid/illegal ratios were the main diagnostic predicting where the approach struggles; [AHE] formalizes the r=0 and k≥2 conventions.
- **Prediction:** the next `/improve` cycle can rank loop skills by waste trend (not just friction anecdotes) and flags at least one hotspot the anecdotes missed.
- **Confidence:** 90%.

### AI-8 · Structured-output smoke test as a model floor for loop roles
- **Target:** `docs/model-assignments.md` (policy addition).
- **Change:** before assigning a cheaper/faster model to any headless loop role, run a ~5-prompt test of the pinned-line contracts (`Status:` flip, `**Recommendation:**` line). Below-threshold format adherence disqualifies regardless of benchmark scores.
- **Evidence:** [COMPILOT RQ4] — format adherence was the leading indicator of everything downstream (codestral's 64.5% invalid rate predicted last place; older models were disqualified outright for format non-adherence).
- **Prediction:** zero runner regex-parse failures after any future model swap that passed the smoke test.
- **Confidence:** 93%.

### AI-9 · Falsifiable `/improve` proposals (predict → verify → revert)
- **Target:** `skills/improve/SKILL.md` (proposal template + next-cycle check).
- **Change:** each staged proposal adds a one-line **prediction** ("this edit should eliminate friction X in the next N runs"). The next `/improve` cycle checks predictions of previously-applied items before anything else; a missed prediction stages a revert-or-revise proposal. (This document practices the format.)
- **Evidence:** [AHE] — pairing every harness edit with a self-declared prediction verified against next-round outcomes, with revert-on-miss, beat a hand-engineered harness (77.0% vs 71.9% on Terminal-Bench 2). The toolkit-level analogue of the existing `predict-first` ritual.
- **Prediction:** within two `/improve` cycles, at least one applied change is caught not delivering its predicted effect and gets revised/reverted instead of silently persisting.
- **Confidence:** 90%.

---

## DO SOMEDAY — plausible benefit, needs testing, low priority

### AI-10 · True best-of-K for high-variance generative phases
K independent same-prompt runs (e.g. `bug-investigation` on genuinely hard bugs), cross-checked by the existing review phase. Only *after* a feedback loop plateaus — [ACCLAIM] demoted this: under fixed budget, iteration dominates sampling. [COMPILOT RQ9] caps useful K at ~5. Confidence: 75%.

### AI-11 · Blind-review variant
Reviewers see diff + ACs but not the implementer's completion notes / `Status:` claims (anchoring risk) — the inverse of [COMPILOT]'s identifier anonymization. Cheap experiment, unproven benefit. Confidence: 65%.

### AI-12 · Richer "why" feedback in gates
Coverage deltas, perf numbers, which-dependency-broke — not just pass/fail. The [COMPILOT] hardware-counters future-work item. Only worth it once AI-3/AI-5/AI-6 exist to consume it, and always distilled per AI-3's rule. Confidence: 70%.

### AI-13 · Hysteresis rule for keeping skill changes
Only mark an applied `/improve` change "settled" when its observed improvement clears a noise margin over ≥2 subsequent runs ([KernelSkill]'s ≥30%-to-promote pattern, adapted). Formalizes the keep/revert side of AI-9; complements the existing ≥3-observations-per-pattern rule. Confidence: 72%.

### AI-14 · A/B benchmark harness for skill edits
Fixed benchmark tasks-doc + sample repo, old vs new skill, k≥2 rollouts, pooled results. The honest-measurement analogue of [COMPILOT]'s pools/medians/CIs — but heavyweight for a personal toolkit. Confidence: 60%.

---

## DO NOT DO

| Temptation | Evidence against |
|---|---|
| Stuff more static context into loop-spawn prompts (repo architecture overviews, env details) | [COMPILOT RQ8]: zero measurable effect; the empirical loop swamps static description. Keep only context the agent must *act on*. |
| Switch loop roles to code-specialized models because "it's coding" | [COMPILOT RQ4]: code-specialized models underperformed general instruction-followers at structured agentic work. |
| Soften mechanical gates toward LLM/reviewer judgment as a *substitute* for running the build | [COMPILOT RQ7]: 17.9% false positives from output-comparison; [llvm-autofix]: **>60% of test-passing patches wrong on expert review**. Tests + review are complements, never substitutes for each other or for the build. |
| Raise the 230K soft budget / max-turns so a stuck session can grind longer | [COMPILOT RQ9]: ~+14% for 2.5× the iterations at non-linearly growing token cost. Spend residual budget on feedback iterations ([ACCLAIM]), then seeded restarts (AI-5). |
| Remove the 3-way exploration phases to save cost | They are the K>1 diversity mechanism at the steepest part of the best-of-K curve ([COMPILOT RQ9]). |
| Feed raw logs/tool dumps to agents as "more feedback" | [KernelPro]: raw dumps were *worse than no feedback at all* (1.77× vs 3.35×). |
| Reuse the three refuted claims | llvm-autofix's "60% domain drop" and "22% mini-agent gain" attribution claims, and KernelSkill's sample-efficiency-vs-STARK comparison — refuted/unverifiable in adversarial verification. |

---

## Overall confidence

**90%.** Every numeric claim traces to the study PDF (read in full) or a finding that survived 3-0 adversarial verification with verbatim quotes. The 10%: (a) all 2026 sources except COMPILOT are unreplicated preprints; (b) effect sizes transfer directionally, not 1:1, from compiler/kernel loops (cheap objective verifiers) to general coding and docs tasks; (c) [ACCLAIM]'s iterate-beats-sample result is a single capped ablation on one capable model — treat as a strong default, not settled law; (d) checkpoint cadence and reviewer fan-out size remain unquantified by any source — current ai-kit choices there are neither confirmed nor challenged.
