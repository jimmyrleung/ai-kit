## [2026-05-31] — compile-kb: defer dead-end → generic baseline fallback head

**Summary:** Follow-up to the same-day root-canonical session. The re-run on ai_vault exposed that compile-kb's "defer unbuilt-head domains" behavior dead-ends a vault (stuck half-converted; idempotent no-op re-runs). Added a generic **baseline fallback head** so every domain converts + gets honest baseline wiki; drafted the SKILL.md changes and validated the first real run.

**Done:**
- Diagnosed the "didn't compile everything" report: the `discussions` pilot was complete + correct (7→7→8, all `integrated`, no drift — proved a re-run is a zero-candidate no-op); the other 8 domains were deferred *by design*.
- With the user, identified the deferral as a dead-end violating `prefer-extensible-self-evolving-designs`; chose a **generic baseline fallback head** (convert + honest baseline wiki, upgradeable; keep the "never fake synthesis" guard).
- Captured **ADR-0001** (`~/.claude/ownership/compile-kb/adr-0001-baseline-fallback-head.md`, ai-drafted · UNREVIEWED).
- Drafted **`skills/compile-kb/SKILL.md`** (+36/−16, 9 sections; new `## Process (baseline fallback head)` B1/B2/B3; preflight 4/5 propose-then-convert; rules 3 & 9; SCHEMA `## Compile` + `baseline_depth`; description triggers). Folded in 2 consistency fixes (`sha256`→`sha256_prefix`; L129 STOP→baseline). **Uncommitted.**
- User re-ran on ai_vault: discussions synthesis recovered + 8 domains baselined (committed `54cfebf`); `insights` extracted the 16 real `.md` from the exhaust folder (743 JSON left behind), honest baseline markers spot-verified. **Uncommitted.**

**Decisions:** baseline fallback head over (B) decouple-convert-only and (C) build-real-heads-now — a fallback is needed regardless under an open taxonomy, and it composes with C later (ADR-0001). compile-kb now **executes approval-gated migration in-skill**, reversing the prior "kb-init deferred / migration outside the skill" + "unbuilt→defer" stances.

**Didn't work:** initial worry that the run violated the exhaust guard — checked, disproven (it correctly left the 743 JSON behind).

**Next:** (1) own ADR-0001 (rewrite Rationale, optionally `/adr-first`); (2) commit SKILL.md (ai-kit, public — secret-scan hook); (3) tighten the B1/orient-path wiring (declared-but-unconverted domain seen from step 4 has no step-5 gate); (4) reconcile `ideas/kb-skill-proposal.md` (forward-pointer to ADR-0001) + `init-proposal.md`/`SCHEMA.md` (insights = real domain, not exhaust — resolves init-proposal Q2; add to `domains:` map); (5) optional `/audit-skills`.

**Blockers:** none.

**Artifacts:** `skills/compile-kb/SKILL.md`; `~/.claude/ownership/compile-kb/adr-0001-baseline-fallback-head.md`; ai_vault commit `54cfebf` + uncommitted `insights/`; observations `2026-05-31-compile-kb-baseline-head.md`.

---

## [2026-05-31] — compile-kb review → open taxonomy + root-canonical model

**Summary:** Double-checked the bloated-context (~400–500K) compile-kb build for degradation, fixed a real routing bug, then iterated the design with the user through first real tests on ai_vault — landing an **open archetype taxonomy** and a **root-canonical one-KB-per-vault** layout.

**Done:**
- Audited compile-kb → found + fixed the **Hermes guard misplacement** (only in the orient branch a flat Hermes vault never reaches → **hoisted to run first, provenance-gated**); hardened the "Partial" branch (populated-flat → migrate, not repair).
- Made the **archetype taxonomy OPEN** (rule 9): unknown archetype → **propose a new one + the concrete skill update**, persist to a vault-local note; **never improvise a compile for an unbuilt head**. Probabilistic classification, deterministic safety rails.
- Made the **`kb-init` references honest** — vaporware (referenced 4×, never built, never in the family); onboarding (init+ingest) is now a **guided manual step**; extract a skill once the shape is proven.
- **Root-canonical layout** (reverses per-subtree): every vault root = `SCHEMA`+`raw/`+`sources/`+`wiki/`; mixed vaults stay one KB with archetypes as **domains** (`domains:` map → heads, shared `wiki/`). Added per-domain dispatch (step 4) + complete-inventory migration (step 5) + first-party-code-as-study-source.
- Grounded on the real ai_vault (added to workspace): course_files = **76 real notes + 1922 code-repo files**; the earlier pilot had **already executed** at the `discussions_articles_researches/` subtree.
- Proposal refinements #3–5; memory (`second-brain-kb-initiative` + new `prefer-extensible-self-evolving-designs`) + 5 observations.

**Decisions:**
- **Open taxonomy — probabilistic classification / deterministic safety; propose-don't-dead-end** (rejected closed enum + hard stop).
- **Onboarding deferred to guided-manual; `kb-init` not built yet** — prove the per-archetype shape by hand first (rejected build-now / fold-into-compile-kb = bulk file-move fights rule 3).
- **Root-canonical, one KB per vault, archetypes as domains** — consistent navigation across all vaults (rejected per-subtree mini-vaults = scattered, fragmented cross-links).
- **First-party lesson code = study source** (extract learning); only vendored/build is exhaust.

**Didn't work:**
- **Per-subtree SCHEMAs** (adopted #3, reversed in #5) — fragmented navigation; replaced by root-canonical domains.
- **"Exclude all repos/ as exhaust"** — too blunt; first-party lesson code IS study material.
- **`kb-init` as a delegation target** — never built/planned; made honest.

**Next:** User resets ai_vault + re-runs `/compile-kb` (oracle: complete-inventory root-canonical proposal with a `domains:` map, course=study-deferred, STOPs without migrating). Then: execute root-canonical seeding (relocate/recreate the discussions pilot at root as a domain); **build the `study` head** (the real unlock for course_files's lesson code). Per-domain dispatch + `domains:` contract only fully prove out once a real mixed vault compiles through them.

**Blockers:** none — model agreed; next step is the user's clean-state re-test.

**Artifacts:** `skills/compile-kb/SKILL.md` (uncommitted); `ideas/kb-skill-proposal.md` refinements #3–5 (gitignored); memory `second-brain-kb-initiative` + `prefer-extensible-self-evolving-designs`; observations `2026-05-31-kb-compile-skill.md` (obs 5–9).

---

## [2026-05-31] — KB "Compile" skill: proposal + compile-kb v0 + first brain-kb compile

**Summary:** Acted on `drafts/20260531_01_kb_skill.md`. Re-read Karpathy's gist + replies, fanned out 12 agents over `~/projects/vaults`, and discovered the "KB skill" already half-exists (Hermes `llm-wiki` v2.1.0 → `brain-kb`). Reframed the task to "find the gap + generalize," wrote a proposal, then built `compile-kb` v0 and ran a first real compile on brain-kb (left uncommitted for review).

**Refinement (later same session):** adopted **full `wiki/` segregation** for the synthesis-wiki archetype (root = `SCHEMA.md`+`raw/`+`sources/`; *everything synthesized* — `index.md`, `log.md`, `_meta` maps, pages, `_compilations` — under `wiki/`, making the KB a literally-regeneratable build artifact) and **scoped compile-kb to non-Hermes KBs** (Hermes-managed vaults like brain-kb keep raw+compiled together under their cron → out of scope, via a Hermes-guard + handoff; `wiki/`-presence is the marker). Re-committed the skill (`cd9e966`). **Consequence:** the brain-kb dry compile is now obsolete (POC + out-of-scope + old flat shape) → **discard it**; the real first compile moves to a **non-Hermes** vault (ai_vault/investments), which exercises the `wiki/` init for real.

**Done:**
- Web re-read of Karpathy v1 gist + comments + v2 fork → new affordances: adversarial review, claim-level provenance, 5-state lifecycle, trust-tiering (first 3 adopted).
- 12 parallel agents profiled all vaults → **5 archetypes** (synthesis-wiki / study / journal / content-gen / client-technical); found brain-kb = Hermes llm-wiki output, mktool_kb = document-workflow output, system_design = its own study pipeline.
- Verified canonical sources directly (brain-kb `SCHEMA.md`, Hermes `llm-wiki/SKILL.md`, templates).
- Wrote `ideas/kb-skill-proposal.md` (gitignored, pre-decision).
- Authored `skills/compile-kb/SKILL.md` via `/write-skills` (127 lines, audit-clean): synthesis-wiki head + spine + detect-and-guide init preflight + the 3 new affordances + a SCHEMA `## Compile` archetype-plug contract.
- First dry compile on brain-kb: synthesized 32 AI-digests → `topics/agent-reliability-and-governance-over-autonomy.md` + `_meta/compilations/2026-05-31-compile.md`; updated index/ai-map/log. Shown as a diff, **left uncommitted**.
- Housekeeping: `/audit-skills` (clean; removed a needless intentionally-long marker), Codex sync dry-run (compile-kb = would-link, 0 issues), memory de-staled.

**Decisions:**
- **Architecture B — shared spine + pluggable archetype "compile heads"** (rejected A single-adaptive skill = bloated conditional; rejected C sibling-family = today's drift). Heads are genuinely divergent (flashcards vs idea-backlogs vs code-derived docs).
- **Home = ai-kit + keep Hermes cron** — decoupled siblings sharing each vault's `SCHEMA.md` as the data contract (rejected extend-Hermes-in-place = not usable from CC/Codex/Cursor). Building in ai-kit *reduces* Hermes/Nous coupling.
- **The gap is periodic Compile, not staleness detection** — staleness already exists in the Hermes llm-wiki Lint (sha256 drift + >90d). Corrected the stale `second-brain-kb-initiative` memory.
- **Scoped the first compile to one flagship trend + 3 watched** (page-creation threshold), uncommitted, so the user validates real-KB output before trusting it.

**Didn't work:** `Glob` with a `path` arg + relative pattern returned empty for an existing dir (`sources/ai-digests`, 34 files) on Windows — switched to PowerShell `Get-ChildItem` (authoritative). Cost one verification round-trip.

**Next:**
- Review the brain-kb compile in Obsidian → commit / tweak / discard (separate repo, uncommitted).
- Apply the Codex sync for real (`adapters/codex/sync.ps1`, no flags) to create the compile-kb junction.
- Fresh-context **trigger test** for compile-kb (the one write-skills gate left).
- Ratify a `## Compile` block + `status` field in brain-kb `SCHEMA.md`.
- Increments: promote watched trends (MCP-control-plane / memory-substrate / security-counterweight); build study + journal heads; populated-vault migration (`kb-init`) for ai_vault/investments.
- keep-two pruning of `~/.claude/improvements/` dated dirs (needs approval; preserve 2026-05-14's pending proposals).

**Blockers:** none.

**Artifacts:** `ideas/kb-skill-proposal.md` · `skills/compile-kb/SKILL.md` · brain-kb: `topics/agent-reliability-and-governance-over-autonomy.md` + `_meta/compilations/2026-05-31-compile.md` (uncommitted) · `~/.claude/improvements/2026-05-31/REVIEW.md` · memory `second-brain-kb-initiative.md` + `karpathy-llm-wiki-gist.md`.

## [2026-05-31] — Built /record-decision (cheap-capture front-end to /adr-first)

**Summary:** From an ad-hoc "honest opinion" ask about a proposed `record-decision` skill, grounded the design with a 5-reader Workflow over the decision-capture surface, reframed the proposal (the real gap was adr-first's *ergonomics*, not a missing artifact), then built + wired + audited + Codex-synced the skill. Not yet committed or trigger-tested.

**Done:**
- 5-parallel-reader Workflow mapped the decision-capture surface (adr-first, close, techspec/analysis steps, the offer-surface, aggregation precedent) — all grep-sourced this session.
- Authored `skills/record-decision/SKILL.md` (single-file, ~95 lines, ~599-char desc).
- Wired the `/close` review sweep (close Phase 1 now sweeps `status: ai-drafted · UNREVIEWED` records → own + challenge via adr-first → flip to `owned`); cross-referenced `adr-first` (stub back-end note); updated `INVENTORY/skills.md` (new row + capture→author pair framing).
- `/audit-skills` focused run: clean, 0 findings across 11 checks. Codex-synced (`record-decision linked`, issues 0). Grep-verified the `status:` flag is byte-consistent across all 4 files.

**Decisions:**
- **Build record-decision as a cheap-capture FRONT-END to adr-first, not a standalone auto-ADR writer** — because the real gap was adr-first's ergonomics (most effort, worst time, least convenient trigger), not a missing artifact (rejected: the original 3-auto-mechanism standalone skill — heavy overlap with /close's ADR gate + techspec §3; rejected: a terse decision-log tier — user wants the full ADR template).
- **Decouple capture from authoring** — capture (factual, AI-fillable, cheap) split from owning the rationale (human, expensive, deferred). The load-bearing principle.
- **Default dial = AI-drafts-rationale-flagged-`UNREVIEWED`** (user pick via AskUserQuestion; rejected: context-only stub; per-capture prompt) — trades ownership purity for the doc existing; the **/close review sweep is the checkpoint** that keeps the debt honest (without it an AI draft launders reasoning — the exact thing adr-first forbids).
- **Reuse adr-first's store/numbering/`{topic}`/ADR-gate — one decision home, `status:` field marks the tier** (rejected: a parallel ADR scheme — would fork the record).

**Didn't work:** My first recommendation (a terse "decision-log tier" + "thin nudge") misdiagnosed the gap — the user wants the full ADR template, and adr-first's ergonomic failure was the real problem. Course-corrected after their pushback.

**Next:**
- **Fresh-context trigger test** — confirm a clean session selects `record-decision` vs `adr-first` from the description alone (write-skills Process 5; not run).
- Restart Codex to pick up the new junction; **Cursor sync still pending (run in WSL)**.
- Pre-existing doc drift: `adapters/codex/README.md` skill count "(41)" → real count 43 (flagged, not fixed).
- Optional dogfood: capture these design decisions via `/record-decision` itself.
- Commit pending: ai-kit (`skills/record-decision/` + close + adr-first + INVENTORY + this SESSION_LOG); claude-home (memory + observations).

**Blockers:** none.

**Artifacts:** `skills/record-decision/SKILL.md` · edits to `skills/close/SKILL.md`, `skills/adr-first/SKILL.md`, `INVENTORY/skills.md` · memory `engineering-ownership-skills.md` · obs `~/.claude/observations/2026-05-31-record-decision-skill.md`.

## [2026-05-31] — Built /write-skills (skill-authoring skill, build sibling of /audit-skills)

**Summary:** Researched skill-authoring best practices (3 parallel subagents: Anthropic official docs, community/practitioner, ai-kit corpus scan), gave an honest assessment correcting the user's "500-char max" premise, then authored `write-skills` — a single-file procedural authoring skill that passes `/audit-skills` by construction. Codex-synced; not yet committed or trigger-tested.

**Done:**
- 3-subagent research → triangulated findings (official + community + corpus), all sourced this session.
- Honest assessment: the "500-character max" the user liked is a **myth** — conflation of the 500-*line* body cap + the 1024-*char* description cap. Real limits are surface-dependent: 1024 hard (open standard / claude.ai / API, rejects) vs 1536 soft (Claude Code, `maxSkillDescriptionChars`, truncates).
- Authored `skills/write-skills/SKILL.md` — 560-char desc, 73-line body; passes audit-skills Checks 1/2/4/10 by construction (measured, not eyeballed).
- Codex-synced (additive: `write-skills linked`, issues 0).
- Persisted 1 memory + 2 observations.

**Decisions:**
- **Single-file-default; `references/` split only as the escape past ~250 lines** — because the ai-kit corpus splits 0/35 and aggressive splitting risks Anthropic's documented partial-read (`head -100`) failure (rejected: Anthropic's ~100-line aggressive-split orthodoxy, which is where the user initially leaned).
- **Procedural authoring shape** (house archetype) + **lightweight fresh-context trigger test** (rejected: concise-checklist shape; full eval-first TDD) — user picked all three via AskUserQuestion.
- **No command wrapper** — skills are directly invocable as `/name` (matches `/predict-first`, `/improve`, `/close`); keeps scope to one file.

**Didn't work:** —

**Next:**
- **User will trigger-test `/write-skills` in a fresh session** (its own Process step 5 — not runnable in this context-saturated session).
- User will author another skill, then run `/audit-skills` over the population.
- Commit pending: ai-kit (`skills/write-skills/` + this SESSION_LOG); claude-home (memory + observations).

**Blockers:** none.

**Artifacts:** `skills/write-skills/SKILL.md` · `~/.claude/projects/C--ai-kit/memory/write-skills-skill.md` · obs `~/.claude/observations/2026-05-31-write-skills-authoring.md` · refs: [Anthropic best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Claude Code skills](https://code.claude.com/docs/en/skills), [agentskills.io spec](https://agentskills.io/specification), [obra/superpowers](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md), [Vercel agents-md-vs-skills eval](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals).

## [2026-05-29] — Backlog #18 applied: proposal-doc / analysis-doc pattern → CLAUDE.md

**Summary:** Picked up `/improve` backlog #18 (one of the 3 focused-session items the morning `/improve` run greenlit). Codified the proposal-doc vs. analysis-doc team-decision pattern as a global `~/.claude/CLAUDE.md` note (user pick over a skill / project memory). Found en route that the memory the backlog wanted to "extend" (`preserve-spec-history`) never actually existed.

**Done:**
- Added CLAUDE.md §"Proposal docs vs. analysis docs (team-decision moments)" (lines 50–57): cue phrases ("bring this back to the team") → standalone proposal doc (8-section shape) pre-decision; a fresh analysis doc that supersedes it post-decision; `## Superseded YYYY-MM-DD` preserve-history posture, never rewrite in place.
- Marked backlog #18 APPLIED (kept as history, not deleted) with the resolution + the `preserve-spec-history` finding recorded.
- Updated the 2 source observations' review-markers: ACTIONED → backlog → APPLIED → CLAUDE.md.
- Wrote 1 observation on the missing-memory integrity gap.

**Decisions:**
- Home = global CLAUDE.md note, NOT a skill (rejected: grows an over-budget skill population per backlog #16 + Codex/Cursor sync cost) and NOT a project memory (rejected: user framed the pattern as reusable, so global beats Met.Trap-only). The 8-section shape was compact enough to inline without bloating always-loaded context.
- Single-source (Met.Trap-only) per `improve-defer-single-source`, but the user explicitly approved #18 and framed it reusable → override the defer, go global.

**Didn't work:** —

**Next:**
- Backlog #17 (feasibility-spike-skill) and #19 (study-pipeline post-write reflex) still await focused sessions.
- Optional follow-ups the user deferred: recreate `preserve-spec-history` properly as a Met.Trap memory; propagate the new CLAUDE.md note to the (dormant) `~/.codex/AGENTS.md` mirror.
- The morning run's keep-two prune (hook-blocked `Remove-Item`) is still pending.

**Blockers:** none.

**Artifacts:** `~/.claude/CLAUDE.md` §"Proposal docs vs. analysis docs" · `~/.claude/improvements/backlog/18-proposal-doc-pattern.md` (APPLIED) · obs `2026-05-29-backlog18-proposal-doc.md`.

## [2026-05-29] — /improve review: 5 of 7 proposals applied, 2 deferred (single-source)

**Summary:** Ran `/improve` over the 2026-05-22→05-29 window (25 observation files, ~55 obs — a dense week: Met.Trap LZ feature 236030, secondear greenfield, cc-looper multi-provider, study-vault). Staged 7 proposals; applied 5, deferred 2 single-source, routed 3 candidates to backlog. Both repos committed + pushed; keep-two prune handed to the user (hook-blocked).

**Done:**
- Applied & pushed: **P01** hook `git commit`/`git tag` exemption from broad words (parse-checked, 0 errors); **P02** proxy/adapter consumer-side 1:1 route-mapping (`integration-analysis` Step 5 + `pragmatic-`/`integration-techspec`); **P03** CLAUDE.md "Reading before editing" → synthesis layer; **P04** `qa-gates` Gate 1 `BLOCKED`-state + no-pass-by-inspection + committed-not-present; **P07** CLAUDE.md "Parallel tool batching" (the ≥3 flag I'd dropped, recovered mid-run).
- Staged `~/.claude/improvements/2026-05-29/` (REVIEW + 7 proposals + MARK); annotated 27 observations across 16 files; backlog 17–19 for the greenlit candidates; `last-review.txt` → 2026-05-29.
- Commits: ai-kit **7b65ec7** (4 skills), claude-home **5cadb41** (31 files); both pushed, ai-kit secret-scan passed. 1 feedback memory + 3 observations written this close.

**Decisions:**
- Deferred **P05** (lean-greenfield) + **P06** (Terraform foot-guns) because both are single-source (one project / one feature) — user wants cross-context recurrence before applying, not ≥3-from-one-situation (→ memory `improve-defer-single-source`). Backing obs left un-annotated as DEFERRED → in scope next run.
- Did NOT build the 3 candidates inline; staged to backlog instead — each is its own focused session (new skill / memory / external-skill edits). Building mid-/improve would balloon scope.
- P06 recommended for the project TF memory, not CLAUDE.md (bloat avoidance).

**Didn't work:** Initial cluster pass dropped P07 (a pre-flagged ≥3 pattern from `2026-05-22-improve-review-close.md#2`); recovered it during annotation and staged out-of-band. → observation 1: Phase-1 intake should seed self-flagged "promote next run" notes deterministically.

**Next:**
- Run the keep-two prune via `!` (hook-blocked `Remove-Item`): `git -C ~/.claude rm -r improvements/2026-05-14 improvements/2026-05-19 improvements/2026-05-20 && git -C ~/.claude commit -m "chore: /improve keep-two prune" && git -C ~/.claude push`.
- Next `/improve` (~2026-06-05): re-evaluate P05/P06 if the patterns recur in a 2nd context. Backlog 17 (feasibility-spike) / 18 (proposal-doc pattern) / 19 (study-pipeline post-write reflex) await focused sessions.

**Blockers:** none.

**Artifacts:** `~/.claude/improvements/2026-05-29/` · commits ai-kit `7b65ec7`, claude-home `5cadb41` · memory `improve-defer-single-source` · obs `2026-05-29-improve-review-close.md`.

## [2026-05-20] — Engineering-ownership (retention) skill layer: 5 skills shipped

**Summary:** Assessed the user's draft for a retention/engineering-ownership layer, then built all 5 skills (predict-first/debug-first/adr-first/challenge-me/onboard-me), documented them, synced to Codex, fixed a stale skill-count drift, and ran /audit-skills (1 proposal applied). Layer is live; Cursor sync + a real-use test-drive are the open items.

**Done:**
- 5 new skills at `skills/<name>/SKILL.md` (no command shims — matches close/improve/triage). Deliberately-invoked, friction-adding rituals: generate-before-consume (predict/debug/adr) + test-after (challenge/onboard).
- Persistence: durable artifacts in `~/.claude/ownership/{topic}/`; `{topic}` resolves arg→branch→doc→ask identically across skills → predict-first ↔ challenge-me matched pair (saved prediction = answer key). Misses tagged for future mining.
- Design fixes folded in vs the draft: predict-first reconciliation back-half; challenge-me question-types + grade-vs-prediction; adr-first critique-only / challenge-first; onboard-me Socratic + scoped to unfamiliar code + dated append-only onboarding.md.
- Docs: README new "Engineering ownership" section + intro line; INVENTORY/skills.md new section; "what we built" summary appended to `drafts/20260520_01_engineering-ownership.md`.
- Codex sync applied: 5 skills + a document-terraform catch-up linked; issues 0.
- Drift fix: stale "35 junctioned canonical skills" → 41 in 7 current-state spots (README + codex/cursor adapter READMEs + cursor sync scripts). Left the 2 dated *portability-assessment* snapshots untouched (rewriting a record falsifies it).
- /audit-skills: clean run; proposal 01 applied (onboard-me desc 849→~620, a kit-max regression introduced this session); backlog 16 = kit-wide description-budget question; 2026-05-14 kept (4 unapplied proposals).

**Decisions:**
- Build all 5 now (not sequence one) because scoping debug-first to non-incident bugs and onboard-me to others' code neutralized the two adherence risks raised in review.
- Persistence = durable artifacts; rejected ephemeral templates (no longitudinal loop) and rejected the full retention-review loop / "option C" (defer until rituals prove sticky — month-1 graveyard risk).
- Ownership artifacts live in private claude-home, NOT the public ai-kit repo.

**Didn't work:** —

**Next:**
- **Cursor sync for the 5 new skills — run in WSL** (`bash adapters/cursor/sync.sh --dry-run`, then real); cursor-agent reads the WSL `$HOME`, so the Windows pwsh session can't do it correctly.
- Test-drive `predict-first` on a real change — the actual validation; month-1 adherence is the open risk, not the build.
- Revisit backlog 16 (description budget) at the next /improve.

**Blockers:** none (Cursor sync just needs a WSL shell).

**Artifacts:** `skills/{predict-first,debug-first,adr-first,challenge-me,onboard-me}/SKILL.md` · `drafts/20260520_01_engineering-ownership.md` · `~/.claude/improvements/2026-05-20/` · memory `engineering-ownership-skills`.

## [2026-05-19] — Cursor CLI adapter built; agents CLI-blocked on upstream bug #160426 (wait/monitor)

**Summary:** Researched + built `adapters/cursor/` (ai-kit → Cursor CLI, mirroring the Codex adapter's Category-1 contract), debugged it empirically on the user's `cursor-agent` (WSL). Skills + 8 orchestrators work and list (51, no dupes); agents are blocked by a staff-acknowledged Cursor CLI parity bug — decision: wait, don't pivot.

**Done:**
- `adapters/cursor/{sync.sh,sync.ps1,AGENTS.md,README.md}` + `docs/cursor-portability-assessment.md`; root `README.md` Cursor section; `docs/codex-portability-assessment.md` cross-ref addendum.
- Empirically established the real picture on the binary: Cursor CLI natively reads `~/.claude`/`~/.cursor` skills; the original "lists nothing" was a **WSL `$HOME` mismatch** (cursor-agent under WSL, junctions in Windows home), not a format gap. Cross-checked by installing Claude Code in WSL — it saw all three via the same symlinks, proving links sound.
- Adapter applied + verified in `cursor-agent`: 30 skill symlinks + 8 explicit-only orchestrator skills (`disable-model-invocation:true`) = 51 with built-ins, no duplicates.
- Memories: `cursor-adapter-agents-blocked-160426` (project), `wsl-invocation-from-windows-harness` (feedback). 3 observations written.

**Decisions:**
- **Skills-unified, not `~/.cursor/commands/`** — Cursor deprecated standalone slash-commands (folded into Skills; `/migrate-to-skills` uses `disable-model-invocation:true`); orchestrators generated as explicit-only skills. Rejected the `~/.cursor/commands/` plan after research showed it's a dead primitive.
- **Agents: keep native `~/.cursor/agents/` generation, do NOT pivot to agents-as-skills** — CLI can't load user-level subagents (bug #160426, staff-ack 2026-05-13, no fix date); it works in the IDE and self-heals when fixed. User chose wait/monitor (uses Cursor IDE / cc-looper meanwhile). Rejected Path B (agents→skills) and per-project `.cursor/agents/` bootstrap (user runs cursor-agent from arbitrary repos → per-repo chore). CLI fan-out fallback: invoke the methodology skill by name.
- **Adapter owns exactly one discovery root (`~/.cursor`)** — the diagnostic `~/.claude` WSL symlinks caused double-listing (81 vs 51); torn down.

**Didn't work:**
- Native `~/.cursor/agents/` for the Cursor *CLI* — abandoned (upstream bug #160426; IDE-only until fixed).
- Diagnostic `~/.claude/{skills,agents,commands}` WSL symlinks — served their purpose (proved links sound), then caused duplicate discovery; removed.
- A research sub-agent's claim that `/create-subagent` doesn't exist in the CLI — wrong; user screenshot corrected it (doc lag vs daily-shipping binary).

**Next:** Monitor Cursor bug #160426 on updates; when fixed the 17 subagents work in `cursor-agent` with a one-line doc flip, no rework. Nothing committed yet (awaiting approval).

**Blockers:** Agents in Cursor CLI blocked on upstream #160426 (external; no fix date) — accepted, not blocking the shipped skills/orchestrators.

**Artifacts:** `adapters/cursor/`, `docs/cursor-portability-assessment.md`, memories `cursor-adapter-agents-blocked-160426` / `wsl-invocation-from-windows-harness`, `~/.claude/observations/2026-05-19-cursor-adapter.md`. Loose ends (user): remove `Met.ServiceApps/.cursor/agents/test-subagent.md`; optional WSL Claude Code (`~/.local/bin/claude`) cleanup.

---

## [2026-05-18] — document-terraform: v1→v2 hardened over 5 regen cycles, whole-estate-fact guard, anonymized for public repo

**Summary:** Continued `document-terraform` from its v1 build. Hardened it across **5 dogfood→assess→refine cycles** against the real (private) landing zone, landed at **Schema v2**, then anonymized the worked examples to a synthetic `acme` estate and archived the design draft — because `ai-kit` is public and the validation repo is a client's.

**Done:**
- 5 cycles, each verified by regenerating the real doc-set then honest-assessing: (1) v1 baseline → (2) module-provenance chain + per-component "role in architecture" narrative + newcomer on-ramp, **Schema v1→v2** → (3) Option-A consolidated role block + `(×N)` notation + count-integrity → (4) `[entry]/[wrap]/[priv]` tag taxonomy pinned deterministically + count-integrity widened doc-wide → (5) **whole-estate-fact reconciliation guard**.
- Anonymized SKILL.md (2 spots) + `reference/heuristics.md` (5 spots) → synthetic `acme`; residue grep clean. Methodology was already generic — only example names changed.
- Archived draft → `drafts/20260518_02_document-terraform-skill.md` (original masked + `## What we ended up building` summary, per the drafts convention from `20260518_01`). User deleted the root `document-terraform-skill.md` (move complete).
- Pull handling: stashed only the local uncommitted SESSION_LOG v1 stub to clear a pull conflict; pulled to `8ce7400`.

**Decisions:**
- **Schema v1→v2** (provenance tree + role block + on-ramp) — doc-contract change, hence the explicit version bump so staleness tracking survives.
- **Role block consolidated per single-orchestrator root** (rejected per-sub-module: fragments the architecture story + bloats; rejected a distinct Q4: unnecessary contract churn — folded the on-ramp into Q1).
- **Whole-estate-fact guard = 4 structural touchpoints** (mandatory rule + consolidation ledger-diff + gate hard-stop + worked example), because a prose warning doesn't bind multi-worker behavior (observations evidence: shape-match warnings already failed twice). Overview must DERIVE shared facts from per-env docs, never re-assert independently.
- **Anonymize to a synthetic estate, keep the architecture shape** (rejected gutting the examples — the realistic 3-layer Spacelift shape is the pedagogical value). Established that "methodology coupled" and "contains client strings" are *separate* checks → memory `ai-kit-public-repo-anonymization`.

**Didn't work:** First narrow client-token grep undercounted (made heuristics look ~2 lines) — corrected with a comprehensive pattern. First `git pull` was a no-op (other session hadn't pushed yet); the retry aborted on the uncommitted SESSION_LOG conflict (resolved via stash-only-that-file).

**Next:** (1) Commit the untracked skill set + drafts archive (pending user OK, below). (2) **Propagate `document-terraform` to Codex via `adapters/codex/sync.ps1`** — per the standing rule the user set in the lay-of-the-land session (every new skill gets synced). (3) Deferred: `INVENTORY/{skills,commands}.md` + `README.md` family mentions; optional dedicated `terraform-documentation-agent`; `/audit-skills` structural pass over the new skill.

**Blockers:** `git stash@{0}` holds the prior-session v1 SESSION_LOG stub — superseded by this entry + the `## v1` section inside the archived draft (no data loss); drop it after the commit. Needs a decision: commit + which repos to push.

**Artifacts:** `skills/document-terraform/{SKILL.md, reference/heuristics.md}`, `commands/document-terraform.md`, `drafts/20260518_02_document-terraform-skill.md`; memory `ai-kit-public-repo-anonymization`; observations appended (`2026-05-18-document-terraform-lz.md` Obs 3–4, `…-skill.md` Obs 3).

---

## [2026-05-18] — lay-of-the-land skill: Phase-0 pre-workflow recon, superseding trigger-discovery-phase

**Summary:** Honest-assessed a draft spec for a "thorough explore" skill, converged via 4 clarification rounds, and shipped it as `lay-of-the-land` — Phase-0 pre-workflow reconnaissance — superseding the `trigger-discovery-phase` command and retiring `discovery-agent`.

**Done:**
- New `skills/lay-of-the-land/SKILL.md` (~95 lines): Understanding gate + coverage ledger + sourced-findings contract; parallel built-in `Explore` fan-out.
- `commands/trigger-discovery-phase.md` → `commands/lay-of-the-land.md` (git-renamed, history preserved; body rewritten as a thin shim; broken frontmatter `description:` fixed).
- New "Discovery (pre-workflow)" section in `INVENTORY/commands.md` + `INVENTORY/skills.md`; `discovery-agent` row removed from `INVENTORY/agents.md` (user deleted `agents/discovery-agent.md`).
- Draft archived: `create-explore-skill.md` → `drafts/20260518_01_create-explore-skill.md` with an appended outcome summary (new drafts-tracking convention).
- Memory: created `lay-of-the-land-skill` + `drafts-archiving-convention` + `codex-sync-on-skill-change`; updated `codex-portability`; `MEMORY.md` indexed. Observations: 4 written.
- **Codex propagation (same session, post-`/close`):** ran `adapters/codex/sync.ps1` — `lay-of-the-land` junctioned into `~/.codex/skills`, `discovery-agent` orphan pruned; 60 exposed (35 skills + 17 agents + 8 orch). Fixed a latent `sync.ps1 -Prune` bug (resolve agent existence by frontmatter `name`, not `<name>.md` — it had mis-flagged `code-reviewer` / `integration-review-agent` / `integration-validator-agent`; `-Prune -Force` would have deleted 3 valid agent-skills). Counts propagated in adapter README/AGENTS + top README; dated 2026-05-18 addendum in the assessment.

**Decisions:** Name `lay-of-the-land` because the existing command already used that phrase (rejected leave-no-stone / tear-it-apart / ground-truth / receipts). Built-in `Explore` as the recon worker, retiring `discovery-agent` (rejected a bespoke agent — redundant indirection; instance of prefer-decoupled-designs). Evolve-not-replace (the old command body was sound, only its description was broken). Reframed the draft's exhortations into mechanisms (rejected shipping the spec literally — would've been a low-leverage skill). Codex: established the standing rule "propagate every new/removed skill/agent via sync" (user); fixed the prune bug rather than work around it (rejected targeted-delete-only — leaving the footgun would break the standing rule's safety).

**Didn't work:** Initial read that `trigger-discovery-phase` was *mis-wired* — wrong; only its frontmatter `description:` was copy-paste-broken, the body was already a sound recon command. Corrected by reading the body before acting.

**Next:** Codex §8 pilot — run a workflow (e.g. `bugfix`) end-to-end on Codex with the unchanged `review-artifact` (the recorded next move; *not* more building). `/audit-skills` remains offered-but-skipped.

**Blockers:** none.

**Artifacts:** `skills/lay-of-the-land/SKILL.md` · `commands/lay-of-the-land.md` · `drafts/20260518_01_create-explore-skill.md` · memory `lay-of-the-land-skill.md` / `drafts-archiving-convention.md` / `codex-sync-on-skill-change.md` · observations `2026-05-18-lay-of-the-land-skill.md` · `adapters/codex/sync.ps1` (prune fix) · `adapters/codex/README.md` + `AGENTS.md` + top `README.md` (counts) · `docs/codex-portability-assessment.md` (2026-05-18 addendum)

## [2026-05-17] — Codex adapter EXTENDED + APPLIED: 8 orchestrators generated, personal AGENTS.md created (global-bet), docs synced

**Summary:** Follow-on to the Category-1 build. User returned with 3 questions (command orchestration in Codex / CLAUDE.md→AGENTS.md / README gotchas). Extended the adapter to generate the 8 multi-phase commands as Codex-only skills, applied the sync (52→60 on disk), created the user's private Codex conventions file, and de-stale'd the top-level README. Still Category-1 (Claude provably unaffected); §8 pilot still the next move.

**Done:**

- **Q1 — orchestration:** `sync.ps1`/`sync.sh` now generate **5 family orchestrators + 3 per-task executors** from `commands/` as Codex-only skills (`allow_implicit_invocation:false`; reads `commands/`, canonical `commands/` never modified). Prune/idempotency extended to the new source. Header/section renumber + summary-label fix. `AGENTS.md` gained a *Generated orchestrator / executor skills* section (the `/x`→`$skill` + `the X skill`→`$X` interpretation map). Dry-run then **apply**: 60 exposed, 0 issues; generated `full-bug-fix-workflow` artifact inspected (SKILL.md/openai.yaml/marker correct).
- **Q2 — conventions:** adapter README "Your personal conventions do not transfer" section + `sync` output warning (chosen: doc+warning). **Then** created `~/.codex/AGENTS.md` — faithful Codex-idiomatic mirror of the *live* `~/.claude/CLAUDE.md` (confidence-scoring verbatim; risky-cmd overrides Codex sandbox; AskUserQuestion deferred to kit-mechanics layer, no drift; command refs → `$qa-gates`/`$triage`/`$close`; close/improve paths flagged Anchored). Carries a kit-mechanics include-point.
- **Q3 — READMEs:** main README — added `adapters/`, de-numbered the stale counts (25/34→prose), corrected the "thin shims" line, added a Codex section + gotchas; +3 clarity edits (`## Install (Claude Code)`, "End state in Codex — one primitive" inventory, Anchored-loop note). Adapter README command-claim split into 3 classes. Assessment §5.2/§8.1/decision-log + `codex-portability` memory + `MEMORY.md` propagated.
- Two-perspective filesystem snapshot delivered (Claude = 3 junctions onto `C:\ai-kit`; Codex = 60 one-primitive: 34 implicit-capable + 26 explicit-only).

**Decisions:** **commands ≠ skills — keep `commands/` on Claude, generate only the 8 for Codex** (rejected "collapse commands→skills": loses zero-context-cost + no-implicit-trigger; Codex has no command primitive so it's the only side that mapping is forced) [drove Q1]. **AGENTS.md wiring = global-bet, leave as-is** (rejected per-project / both — user chose zero-maintenance + future-proof over guaranteed-active) [user] — consequence: at codex-0.130.0 global `~/.codex/AGENTS.md` read is `[verify]`, so neither layer is active in Codex yet; fallback documented in-file. ~25 thin shims deliberately **not** generated (their skill is already junctioned).

**Didn't work:** — (no dead ends; verification — dry-run + `bash -n` + apply + artifact inspection — passed first time; the only self-catch was a cosmetic summary-label undercount, fixed immediately).

**Next:** §8 **pilot** — run a family (e.g. `bugfix`) on Codex end-to-end with the *unchanged* `review-artifact` (Codex-only, no gate risk). Re-verify global-AGENTS.md read-location after the next Codex update (flips both layers active if supported). **NOT more building**; `review-artifact` stays quarantined.

**Blockers:** none. The global-AGENTS.md dormancy at 0.130.0 is a known documented `[verify]`, not a blocker (fallback exists).

**Artifacts:** `ai-kit/{README.md, adapters/codex/*, docs/codex-portability-assessment.md}` (6 files, uncommitted pending this close); private `~/.codex/AGENTS.md` (not version-controlled — user's Codex home); memory `codex-portability` + `MEMORY.md`; observations `2026-05-17-codex-portability.md` (Obs 6).

---

## [2026-05-17] — Codex adapter BUILT (Category-1) + §4 path fix + assessment doc corrected from verified binary facts

**Summary:** Implemented Category-1 of the Codex portability initiative. Re-verified Codex specifics on the installed binary (caught a materially-wrong assessment fact), fixed the §4 path defect, corrected the assessment doc, and built the additive Codex adapter. Structurally verified; behavioral pilot deferred. Continuation of the same-day assessment+decision sessions below.

**Done:**

- **Verified `codex-cli 0.130.0`:** skills root `~/.codex/skills`; `SKILL.md` spec identical; **agent binding = per-skill `agents/openai.yaml`, NOT `<name>.toml`** (a *skill IS the agent unit*; no `~/.codex/agents`); `quick_validate.py` allowed frontmatter keys; `codex exec --json`/`--output-schema`; plugin system; `codex mcp-server` exists.
- **§4 path fix:** `skills/bug-investigation/SKILL.md` + `skills/refactor-audit/SKILL.md` absolute `C:\ai-kit\templates\…` → kit-relative (behavior-invariant prose pointers; user-approved).
- **Assessment doc corrected** (`docs/codex-portability-assessment.md`, 14 sites) — `VERIFIED v0.130.0` markers; honest `[verify]` residuals kept; status/decision-log updated.
- **Adapter built:** `adapters/codex/{sync.ps1,sync.sh,AGENTS.md,README.md}` — 34 skills per-skill directory-junctioned + 18 agents **generated as explicit-only Codex skills** (`policy.allow_implicit_invocation:false`); strategy C as `AGENTS.md` instruction (no kit harness); idempotent; **canonical tree pristine** (git-verified zero adapter-caused canonical edits; `.system` untouched).
- Memory `codex-portability` + `MEMORY.md` updated (stale "not implemented"/implied-TOML → Category-1 built + correction). Observations Obs 3–5.

**Decisions:** packaging = **junction** not Codex-plugin bundle (least coupled; rejected plugin: new coupling) [user]. Session scope = doc+pathfix→checkpoint→adapter; **model-tier deferred** (Category-2, edits 18 junctioned agents) [user]. Agents = **generated explicit-only Codex skills** not TOML (verified skill-is-agent-unit; implicit-off prevents 52-desc context bloat; rejected assessment's MD→TOML — falsified on binary). Canonical-skill `openai.yaml` **deferred** (recommended-not-required; would pollute pristine tree / need fragile file-symlinks). Validation **advisory, self-test-gated, fail-open** (rejected first cut that gated the deliverable).

**Didn't work:** assessment's "agents→TOML/`developer_instructions`" (falsified on binary). First validation design (gated sync → 52 false FAILs on a broken host Python) → self-test + graceful degrade. Live `quick_validate.py` — host `C:\Python311` segfaults (`0xC0000005`, kit-independent) → static-validated instead.

**Next:** §8 **pilot** — run `bugfix` on Codex end-to-end with the *unchanged* `review-artifact` (Codex-only, no gate risk). Needs a working Python/Codex env for the live validator. **NOT more building**; do **NOT** resurrect "refactor `review-artifact` now" (quarantined).

**Blockers:** none for the initiative (Category-1 done, Claude-risk-free). Live-validator only: broken host Python (kit-independent).

**Artifacts:** `ai-kit/adapters/codex/*`; `docs/codex-portability-assessment.md` (§3a Decision + §8 = authoritative handoff); memory `codex-portability`; observations `2026-05-17-codex-portability.md` (Obs 3–5). Uncommitted pending this close's commit step.

---

## [2026-05-17] — Codex §3a decision recorded (B dropped; C + externalised verdict-contract; review-artifact quarantined)

**Summary:** Continuation of the same-day Codex portability work. Drove the §3a fan-out decision to a conclusion with the user and recorded it into the assessment doc + memory. Still assessment-only — nothing implemented; user will implement in a fresh session.

**Done:**

- Decision discussion: walked 3 real fan-out sites (`review-artifact` re-run loop / `bug-investigation` disagreement-signal / the 3-way exploration) through options A/B/C to drive the choice.
- Recorded the decision in `docs/codex-portability-assessment.md`: new `#### Decision (recorded 2026-05-17)` block in §3a (two-fan-out-shapes table, dynamic-count-without-harness, the Claude-impact boundary, the `review-artifact` quarantine + re-homing); propagated to header decision-log, §3a intro, §6, §7, §8.
- Memory `codex-portability.md` + `MEMORY.md` pointer updated (stale "open decision blocks implementation" → recorded decision + do-now guidance). Observation 2 logged.

**Decisions:**

- **B (codex-exec fan-out harness) dropped** — user constraint: no kit-owned fan-out harness; rely on the native harness or a cc-looper-class runner *on top of* the native CLI, never an orchestration script in a skill. (Rejected B for permanent harness-maintenance cost.)
- **Per-shape resolution, not a global pick:** divergent + fixed-roster (3-way explorers) → **C** native subagents (no loss); convergent + stateful (`review-artifact`, `bug-investigation` M, `qa-loop`/`review-checkpoint`) → **C** for the parallel passes + the multi-round loop *externalised* as a structured verdict consumed by a human (interactive) or a cc-looper-class runner (headless); small/skip-checked → **A**. Dynamic 1–3 count recovered via conditional by-name invocation off the existing S/M/L/XL classifier (no harness). (Rejected: one global option — convergent vs divergent fan-out genuinely want different answers.)
- **`review-artifact` quarantined** — it's the quality gate for 4/5 families; broken-gate failure = silent quality erosion, not a crash. Canonical file **frozen for this initiative**; Codex runs it from the *unchanged* file in C-mode. The verdict-contract refactor is re-homed to the future cc-looper-runner effort, done later in isolation behind a Claude golden-transcript regression gate. (Rejected: doing the refactor now inside the Codex rollout.)
- **Claude-impact boundary is load-bearing:** Category 1 (additive Codex artifacts) = Claude provably unaffected; Category 2 (verdict-contract refactor of single-source skills junctioned into `~/.claude/`) = no Codex-only copy *by construction* → "Claude unaffected" is only a regression-gated invariant. ⇒ near-term scope = **Category 1 only**.

**Didn't work / superseded:** the earlier same-session "do now: refactor convergent-review skills to emit a verdict" recommendation — superseded by the quarantine decision after the user flagged `review-artifact`'s gate blast-radius. **Do NOT resurrect "just refactor review-artifact now" in the implementation session.**

**Next:** fresh session — implement **Category-1 only** per §8: 3-way explorers via **C** + the additive Codex adapter (agent-def generation, junction, Codex-side A/C selection) — zero canonical-skill edits, `review-artifact` frozen. Prereqs: verify Codex specifics on the installed binary; fix the §4 pre-existing defects (lowest-risk). **Start here:** `docs/codex-portability-assessment.md` §3a "Decision" + §8.

**Blockers:** none — decision made; Category-1 is unblocked and Claude-risk-free.

**Artifacts:** `ai-kit/docs/codex-portability-assessment.md` (§3a "Decision" + §8 = authoritative handoff); memory `codex-portability`; observations `2026-05-17-codex-portability.md` (Obs 1+2). All uncommitted in the ai-kit working tree (user skip-committed earlier this session).

---

## [2026-05-17] — Codex portability assessment for ai-kit (one canonical set + adapters)

**Summary:** User is trialing Codex and asked whether ai-kit's commands/skills/subagents can be reused there from one canonical source (feedback loop OK to stay Claude-anchored for now). Scoped to a **portability assessment**. Delivered an evidence-grounded doc; up-to-date research reframed the problem from a feared big rewrite to a thin-adapter problem.

**Done:**

- `ai-kit/docs/codex-portability-assessment.md` (new) — file-grounded coupling audit (repo-wide greps w/ counts × files read end-to-end) × up-to-date Codex capabilities; 4-tier portability map (Clean/Mechanical/Semantic/Redesign/Anchored); the 2 genuine gaps; pre-existing defects; thin-adapter transform inventory; risks; next steps. Confidence 92%.
- Background general-purpose agent → up-to-date Codex CLI capability research (official docs, 2026-05-17): native skills (same `SKILL.md` spec), native subagents (GA 2026-03-14), Claude-shaped hooks, `AGENTS.md`/`.agents/skills` cross-agent standards.
- Auto-memory: new `codex-portability` (project) + `MEMORY.md` pointer. One observation (`capability_gap` — kit lacks an *inward* meta-analysis skill).

**Decisions:**

- **Canonical = the cross-agent open standard (`SKILL.md` + `AGENTS.md` + `.agents/skills`), NOT "Claude-native source + a Codex transform."** Rejected the Claude-native+adapter framing because Codex now *natively consumes the same `SKILL.md` spec* (+ `AGENTS.md`, native subagents, hooks reusing Claude's field names) — the shared standard is the lowest-drift canonical form and shrinks the adapter to junction/symlink + agent-MD→TOML + 2 gap-rewrites. Extends the existing junction/symlink precedent.
- **Assessment-only scope** (user chose via question): no implementation, defects not fixed, adapter not built — next steps listed, not executed.
- Wrote the durable project memory **in-session** (not deferred to `/close`) because it was clearly durable + matches the established `*-initiative` memory pattern; `/close` found it current and did not duplicate.

**Didn't work / rejected:** the training-data prior "Codex has no skills/subagents → big rewrite" (obsolete — verified obsolete via up-to-date research; this flip is the whole reason the conclusion changed). First absolute-path grep used `\\\\` → matched `\\`, false "no matches"; corrected to `C:\\(ai-kit|Users)`.

**Next:** **Decide §3a** — the subagent autonomous-fan-out substitution: A) degrade to single-thread, B) `codex exec` parallel fan-out, C) explicit named subagents. This is the only decision gating any implementation. Lowest-risk independent first move: fix §4 pre-existing defects (absolute `C:\ai-kit\…` paths → relative; vendor model pins → capability tiers). Then verify the `[verify on installed binary]` Codex specifics; then pilot the `bugfix` family end-to-end on Codex.

**Blockers:** §3a is an unresolved judgment call for the user (a decision, not a technical blocker).

**Artifacts:** `ai-kit/docs/codex-portability-assessment.md`; memory `codex-portability`; observation `2026-05-17-codex-portability.md`. ai-kit (public): assessment doc untracked — commit proposed at close. claude-home: no tracked changes (auto-memory is gitignored-local by design — `.gitignore:13 /*`).

---

## [2026-05-16] — close-tasks skill: feedback-loop blind-spot fix (ai-kit half) + cc-looper handoff

**Summary:** Started from a user question about when to `/close` for task-implementation vs design sessions. Diagnosed (at source level) a real blind spot: multi-session manual + cc-looper headless runs emit ZERO observations, so loop skills are invisible to `/improve`. Designed and shipped the consumer-independent half (`/close-tasks`) in ai-kit; wrote a cc-looper integration analysis for the run-end hook half (Part B) as a separate-session handoff.

**Done:**

- `ai-kit/skills/close-tasks/SKILL.md` (new) — artifact-aggregation closeout (NOT context-distillation): reconstructs a tasks-doc run from completion notes / `## Verify`/`## Review`/`## QA` blocks / `_qa.md` / `.cc-loop/state.json` / `git log`; idempotent via a `<!-- close-tasks: harvested through <sha> -->` marker; emits observations tagged with the *detected* skill_or_workflow + a roll-up SESSION_LOG entry; consumer-agnostic (manual or cc-looper).
- `ai-kit/skills/close/SKILL.md` (mod) — `/close` ↔ `/close-tasks` split pointer in Notes (+ "don't stack both on the same window" guard).
- `~/.claude/observations/README.md` (mod) — documents two writers; flags `/close-tasks` observations as artifact-reconstructed for `/improve` weighting.
- `cc-looper/specs/close-tasks-loop_integration.md` (new) — reference map for Part B (entry points w/ file:line, `runFinalQA` as copy-from template, the binding decoupling constraint, Heavy-vs-Light fork left for the techspec).
- Auto-memory: new `close-tasks-skill-initiative` (project) + reinforced `prefer-decoupled-designs`. One observation logged (verify-task buffer-flush durability hole).

**Decisions:**

- **Separate `/close-tasks` skill, not a `/close` mode.** `/close` = live-context distillation; `/close-tasks` = artifact aggregation (multi-session/headless context is gone by run-end). Rejected: a `--tasks` flag on `/close` (bloats the single-purpose skill), `/close-tasks` subsuming per-session `/close`.
- **One end-of-run `/close-tasks`, skip per-session `/close` during implementation runs.** User consciously accepted the tradeoff: lossier for *narrative* friction (cleared-session detail gone) but *structured* friction (gate fails, completion notes, `_qa.md`) survives in artifacts. Matches the "10 tasks across 2-3 sessions" workflow.
- **Binding contract:** cc-looper's future `close-tasks-loop` writes an in-repo `<base>_close.md` digest ONLY, never `~/.claude/observations/` (spawn cwd = target repo; private path in a public symlinked skill is the anti-pattern + permission-fragile). ai-kit `/close-tasks` is the on-machine promoter.
- **Repo-boundary split** (user's call): build ai-kit now; cc-looper Part B is a handoff doc, picked up in a cc-looper-initiated session.

**Didn't work / rejected:** loop skills emitting observations directly (portability leak); deciding Heavy-vs-Light now (deferred to cc-looper techspec); full `/integration-feature-dev` (too heavy for ~11 items); free-handing both repos in one session (scope-discipline violation).

**Next:** in a session **initiated within cc-looper**, open `specs/close-tasks-loop_integration.md` → run a techspec to settle **Heavy vs Light** → implement (new `close-tasks-loop` skill + ai-kit symlink + `runCloseTasks` phase + `runEndDeliverables` hook; Heavy adds `state.json` schema bump 6→7). Also: `/close-tasks` is unproven until first real use against a finished tasks-doc.

**Blockers:** none.

**Artifacts:** `ai-kit/skills/close-tasks/SKILL.md`, `cc-looper/specs/close-tasks-loop_integration.md`, memory `close-tasks-skill-initiative`, observation `2026-05-16-close-tasks-skill.md`. Nothing committed (working trees clean for review).

---

## [2026-05-15] — Normalize tasks-overview table across task-gen skills

**Summary:** User flagged that `/integration-balanced-tasks` and `/integration-create-tasks` produce a nice summary table (status, size, depends on) and asked to apply it to all task-generating skills. Audited 5 skills; 2 already conformed; updated 2; user opted to skip the 5th. Verified the downstream `map-tasks` parser is column-order agnostic before shipping.

**Done:**

- `skills/refactor-tasks/SKILL.md` — overview-table column spec: `Task | Complexity | Estimated Time | Status` → `Task | Title | Complexity | Est. Time | Depends On | Status`.
- `skills/tasks-creation/templates/tasks_template.md` — greenfield template: added `Depends On` column; renamed `Est.` → `Est. Time` for consistency with the reference shape.
- Verified `map-tasks/SKILL.md:24` reads the table with a wildcard middle (`| # | Title | … | Status |`), so the new column doesn't break the cc-loop runner.

**Decisions:**

- **Skip `docs-tasks-creator`.** Its tasks are uniform-size (one handler doc each) and inherently independent, so `Complexity='S'` and `Depends On='—'` rows would be filler. The existing `Trigger`/`Service` columns carry real domain signal; preserving them beats blind consistency. Rejected the "apply uniformly anyway" option.
- **Normalize column headers to `Complexity` / `Est. Time`** across the touched skills (matches the two reference skills exactly). Rejected leaving the legacy `Estimated Time` / `Est.` headers in place.
- **Didn't touch the worker agents (`integration-tasks-creator-agent`, `refactoring-tasks-creator-agent`) or wrapping commands.** They delegate to the skills ("follow the skill exactly"), so the skill body is the single source of truth — agents/commands inherit.

**Didn't work:** —

**Next:** none — change is self-contained. (The next time someone runs `/create-tasks` or `/refactor-techdebt-dev`'s tasks phase, the new shape will be produced.)

**Blockers:** none.

**Artifacts:**

- `C:\ai-kit\skills\refactor-tasks\SKILL.md` (modified)
- `C:\ai-kit\skills\tasks-creation\templates\tasks_template.md` (modified)

---

## [2026-05-15] — Workflow-doc staleness signals (schema v1) + cc-looper integration check

**Summary:** Added staleness-detection metadata to `document-workflow` (the interactive command) and `document-workflow-loop` (the cc-looper headless skill). Then confirmed the changes don't break cc-looper's runner — discovered ai-kit's loop-related skills/commands are symlinks to cc-looper's `claude-config/`, so edits already propagated. Two real concerns surfaced during the impact check; both fixed.

**Done:**

- Added `Created`, `Last Updated`, `Generated From` (short commit SHA), `Schema: v1` rows to the Summary table of produced workflow docs (in both the command and the loop skill).
- Added `## Source Files` (machine-readable `Role | Path` table — the input to automated staleness detection) and `## Change Log` (`Date | Change | Reason` with an initial-creation row) sections at the end of produced docs.
- Added populate instructions: command's Guidelines + loop skill's Workflow 2 (new step 4 = single Bash call `git rev-parse --short HEAD`, with a fallback clause for denied/failed cases → set `unknown` + `[TODO: verify SHA]` rather than pausing the task).
- Updated `qa-loop-docs` Gate 0 hint list to include the new sections + the four doc-meta Summary rows, with an explicit acceptance rule (`unknown` Generated From with the marker is NOT a Gate 3 finding; literal placeholders left as `YYYY-MM-DD` or `<short-sha>` ARE findings).
- Discovered via `Get-Item -Force` that `C:\ai-kit\skills\{document-workflow-loop, qa-loop-docs, qa-loop, implement-task-loop, map-tasks, review-checkpoint}` and `C:\ai-kit\commands\tasks-loop.md` are all Windows SymbolicLinks to cc-looper's canonical copies — wrote [[cc-looper-symlink-topology]] memory.
- Updated [[second-brain-kb-initiative]] memory to reflect schema v1 + flag staleness detector as the next remaining gap.

**Decisions:**

- **Change Log columns: `Date | Change | Reason`** (chose recommended 3-col over 2-col minimal / 4-col with editor). Rejected the 4-col `Editor` field because no human-vs-skill distinction is needed yet; rejected 2-col because the `Reason` nudge gives future edits context without much cost.
- **`Generated From` advances on every update**, doesn't stay frozen like `Created`. Why: the SHA represents "the state of the codebase this doc was last verified against," not "first generation" — the Change Log is the audit trail.
- **Schema v1 explicit version row**, not implicit. Why: cheap insurance for future template migrations — a 1-line grep finds every doc on an old schema.
- **`git rev-parse` denial → route-around with `unknown`, not pause.** Why: target repos (client codebases being documented) often won't have `Bash(git:*)` in their `.claude/settings.json`, and per the headless preamble a Bash denial would otherwise pause the task. The SHA is a nice-to-have, not load-bearing — the doc is still useful without it.
- **Source Files table as a separate section** (not woven into Sequence of Calls). Why: machine-readable; future detector skill's `git log <generated-from>..HEAD -- <paths>` invocation needs a clean list.
- **Edited via the cc-looper-target paths' ai-kit symlink aliases** once discovered — same physical file, but Read-tracking pinned to whichever path was first opened.

**Didn't work:**

- First Edit attempt on `~/projects/cc-looper/claude-config/skills/qa-loop-docs\SKILL.md` failed with `File has not been read yet` because I'd Read the ai-kit symlink path first. Recovered by re-issuing against the path I'd Read.

**Next:**

- **Build the staleness detector skill** (offered + parked this session). Sketch: read every `workflows/**/*.md`, extract `Last Updated` + `Generated From` + `## Source Files`, run `git log <generated-from>..HEAD -- <paths>` per doc, output a triage list (stale / probably-fresh / unknown). Pairs with `audit-skills` as a structural-quality check for the raw/ layer of the second-brain init.
- Real-world validation of the schema-v1 metadata on a docs run (the `docs-tasks-creator` validation list from the prior session still applies — staleness signals just rode along).

**Blockers:** none.

**Artifacts:**

- `C:\ai-kit\commands\document-workflow.md` — modified (Summary rows + Source Files + Change Log sections + Guidelines populate rule + git-denial fallback)
- `~/projects/cc-looper/claude-config/skills/document-workflow-loop\SKILL.md` (via `C:\ai-kit\skills\document-workflow-loop` symlink) — modified (same additions + Workflow 2 step 4 git-SHA capture with fallback)
- `~/projects/cc-looper/claude-config/skills/qa-loop-docs\SKILL.md` — modified (Gate 0 hint list updated with new sections + Summary doc-meta rows + `unknown` acceptance rule)
- `~/.claude/projects/C--ai-kit/memory/cc-looper-symlink-topology.md` (new — reference memory)
- `~/.claude/projects/C--ai-kit/memory/second-brain-kb-initiative.md` (updated — schema v1 milestone + detector as next gap)
- `~/.claude/observations/2026-05-15-workflow-doc-staleness-signals.md` (new — 3 observations: symlink Read-tracking gotcha, triaged-brainstorm pattern win, runner-allowlist fact-check win)

---

## [2026-05-15] — Built docs-tasks-creator skill (decoupled, multi-stack, monorepo-aware)

**Summary:** Built v1 of the `docs-tasks-creator` skill — the concrete bucket-1 gap from this morning's KB workflow iteration. Scans a codebase, detects HTTP/message/job handlers via pluggable detectors, emits a consumer-agnostic tasks doc (one task per handler) + a synthesized `project-overview.md`. Also deprioritized the `active-context.md` proposal (priorities-doc line 14) — user flagged it as a habit-sustainability risk.

**Done:**

- Read existing `document-workflow-loop`, `map-tasks`, and `document-workflow` skills to ground the design — confirmed how the output-path mechanism works (the consuming tool writes to `<repo>/workflows/...` where `<repo>` is its primary repo).
- Authored `C:\ai-kit\skills\docs-tasks-creator\SKILL.md` (~280 lines):
  - **10 v1 detectors**: Next.js (App Router / Pages API / Server Actions), Express, Fastify, NestJS, ASP.NET Core (attribute + minimal API), GRPC .NET, .NET BackgroundService.
  - **Monorepo handling**: workspace detection (pnpm-workspace.yaml / package.json workspaces / nx.json / lerna.json / rush.json / turbo.json / multi-`.csproj`-from-.sln / heuristic fallback); interactive selection (AskUserQuestion for 2–4 workspaces, plain text for 5+); per-workspace artifacts under `$output_dir/<workspace-slug>/`.
  - **Consumer-agnostic emitted tasks doc** — no cc-loop coupling; each task has `Status:`, `Reference:`, `Files affected:`, `Trigger:`, `Acceptance criteria:`.
  - **Inline project-overview.md generation** in Phase 4 (not a separate cc-loop task).
- Updated [[second-brain-kb-initiative]] memory to reflect docs-tasks-creator v1 built.
- Wrote new feedback memory: [[prefer-decoupled-designs]].

**Decisions:**

- **Consumer-agnostic emitted tasks doc.** Rejected cc-loop-coupled v1 (initial draft included a `## How to run` block with `bun cc-loop ...`, a `**Repos**:` header, and `document-workflow-loop` references). Why: user explicitly said "if someone wants to generate doc tasks but do all of them manually that's fine" — the artifact should serve manual workflows too.
- **Pluggable multi-stack detectors from v1.** Rejected my proposal of "pick one stack first, generalize later." Why: user works across React+TS, Node, .NET — locking to one stack would leave most of their surface unscanned.
- **One tasks doc per workspace in monorepos.** Rejected one giant combined doc. Why: per-workspace isolation matches how docs are consumed (one workspace = one engagement boundary); a 30-workspace doc would be unworkable.
- **One handler per task** (not per-class clustering). Why: matches "one doc per handler" output shape and the priorities-doc framing.
- **Inline setup work, no `Task 0`.** Scaffolding + project-overview.md done by docs-tasks-creator itself in Phase 4, not emitted as a cc-loop task. Why: cc-loop's `document-workflow` action is for tracing workflows, not synthesizing overviews — a Task 0 would have no compatible runner.
- **Deprioritized `active-context.md`** (line 14 of priorities doc). Why: user self-flagged habit-sustainability risk ("I'd stop doing it in a week or two"). Parked.

**Didn't work:**

- Initial Cline-style `active-context.md` proposal — rejected by user on habit-sustainability grounds. The hot/stable section split + decay rules + 300-line cap design was probably fine; the weekly-debrief dependency was the unworkable part.
- Initial single-stack v1 framing — user redirected to multi-stack.
- Initial cc-loop coupling in the emitted tasks doc — user flagged for removal.
- Initial monorepo-blind v1 — missed entirely until user surfaced it.

**Next:**

- Real-world validation on `docs-tasks-creator` against an actual client codebase. Specifically validate: (a) the multi-`--repo` cc-loop invocation works (only inferred from map-tasks' `$repos` plural reference; not verified against `bun cc-loop` CLI); (b) Server Actions detector false-positive rate; (c) service-name derivation on real monorepo layouts; (d) heuristic-fallback workspace detection on `client/`+`server/`-style non-monorepo splits.
- Remaining bucket-1 items: `raw/{client}/{project}/` folder skeleton + weekly debrief cadence.

**Blockers:** none.

**Artifacts:**

- `C:\ai-kit\skills\docs-tasks-creator\SKILL.md` (new, ~280 lines)
- `~/.claude/projects/C--ai-kit/memory/second-brain-kb-initiative.md` (updated — docs-tasks-creator v1 built)
- `~/.claude/projects/C--ai-kit/memory/prefer-decoupled-designs.md` (new — feedback memory)
- `~/.claude/observations/2026-05-15-docs-tasks-creator-build.md` (new — 3 observations on initial-draft missteps)

---

## [2026-05-15] — KB workflow iteration 2: research + prioritized roadmap

**Summary:** Un-parked the second-brain/LLM-wiki KB initiative for iteration 2. Ran three parallel research streams (SOTA / staleness tooling / skeptical), iterated through key design questions with the user, produced two artifacts: iteration 2 section appended to the main idea doc + a new prioritized roadmap doc.

**Done:**

- Three parallel research-agent streams (general-purpose with WebSearch): SOTA for LLM-consumable codebase KBs, doc staleness tooling, critical / failure-history pass.
- Surfaced key findings: Karpathy LLM Wiki pattern is mainstream (~5k stars, ~1:1 to user's `raw/+kb/` design); HackerNoon 6-Rails case study at $10–20/mo; DORA 2024 (AI doc adoption +7.5% quality but −1.5% throughput and −7.2% stability); Karpathy v1 documented month-1 failures + v2 fork by rohitg00; Hansen/Nohria/Tierney HBR 1999 (personalization > codification for customized-engagement consulting).
- Appended **Iteration 2** section to `C:\ai-kit\ideas\knowledge-and-docs-wf.md` (research approach, findings, 4 decisions, kill criteria, strategic reframe, v2-vs-v1, out-of-scope, open items, references).
- Created `C:\ai-kit\ideas\knowledge-and-docs-wf-priorities.md` — 4-bucket prioritized roadmap (do now / do soon / good-to-have / don't do) + sequencing logic + kill-criteria reminder.

**Decisions:**

- **`kb/` is a build artifact, not source of truth.** Rejected SSOT framing. Why: defuses both the staleness rot problem (regenerate, don't maintain) and the Hansen-codification anti-pattern. Contradictions resolve to primary source.
- **Kill criteria ordered c > b > a** (maintenance cost > trust events > re-query rate). Rejected equal weighting. Why: the KB's primary consumer is the user, not the LLM — LLM query rate is a use-pattern indicator, not a fitness test. A KB the LLM ignores but the human uses is still doing its job.
- **Strategic reframe: personal knowledge augmentation, not team codification.** Rejected "this is a docs project for the LLM." Why: weakens DORA / Hansen concerns which are about *teams* producing doc volume for *other readers*.
- **Sequence: build `raw/` + `active-context.md` + `docs-tasks-creator` FIRST; `kb/` consolidation is an experiment LATER.** Rejected "build kb/ first as foundation." Why: minimum viable version delivers value with zero buy-in to the risky bet. If `kb/` never works, the rest still earns its keep.
- **If/when `kb/` is built, adopt Karpathy v2 affordances from day 1.** Rejected v1 unmodified. Why: v1 has documented month-1 failure modes (identity collisions, level collapse, link cascade); v2 (rohitg00 fork) adds confidence scoring, supersession, provenance to address these.
- **HTML output is for the user, not clients.** Relaxes freshness contract since user is the only consumer who knows which pages are stale.

**Didn't work:**

- Visual-explainer integration for HTML output (already rejected iteration 1, re-confirmed: wrong shape — re-generates everything when only incremental updates are needed).
- "kb/ as source of truth" framing — rejected explicitly in iteration 2.
- My initial framing of kill criteria as equally-weighted — user's reordering (c > b > a) was sharper and required reshaping the operational design.

**Next:** Build the `docs-tasks-creator` skill — most concrete bucket-1 item; independent of the `kb/` bet. Scans codebase, emits one document-workflow task per endpoint/job + setup task, feeds cc-loop. Single-approach (not 3-way) per prior memory. See `C:\ai-kit\ideas\knowledge-and-docs-wf-priorities.md` for full sequencing.

**Blockers:** none — iteration 2 captured; #5 (personalization fallback) explicitly parked for further thought with a starting question.

**Artifacts:**

- `C:\ai-kit\ideas\knowledge-and-docs-wf.md` (iteration 2 appended)
- `C:\ai-kit\ideas\knowledge-and-docs-wf-priorities.md` (new)
- `~/.claude/projects/C--ai-kit/memory/second-brain-kb-initiative.md` (updated — un-parked, iteration 2 decisions)
- `~/.claude/projects/C--ai-kit/memory/karpathy-llm-wiki-gist.md` (updated — v2 fork + failure modes)
- `~/.claude/observations/2026-05-15-kb-iteration-2.md` (new — primary-consumer reframe observation)
- Karpathy v2 fork: https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
- HackerNoon case study: https://hackernoon.com/how-i-built-a-self-maintaining-knowledge-base-for-6-projects-using-claude-code-and-karpathys-llm-wiki

---

## [2026-05-15] — Explored second-brain/LLM-wiki KB; parked for think-time

**Summary:** Design-only session. User asked for an honest assessment on a skill that "maps a tasks document but for documentation tasks." Investigation showed the entire docs-loop pipeline (`map-tasks` + `document-workflow-loop` + `qa-loop-docs` + `tasks-loop --action document-workflow`) was already wired end-to-end — the real gap is upstream (a docs-tasks-*creator* skill). Conversation expanded to the broader second-brain / LLM-wiki KB design (Karpathy gist, visual-explainer for HTML view, multi-client vault isolation). User parked the initiative pending more think-time.

**Done:**

- Confirmed existing docs-loop pipeline covers everything except task-list creation. No new skills authored.
- Created `C:\ai-kit\ideas\` as a scratch folder for the parked initiative; gitignored via new `.gitignore` at repo root.
- Wrote two memory files (`karpathy-llm-wiki-gist`, `second-brain-kb-initiative`) + indexed in `MEMORY.md`.
- Logged two observations to `~/.claude/observations/2026-05-15-docs-kb-exploration.md` (pre-build investigation success; parked-initiative handoff).

**Decisions:**

- **Park the second-brain initiative; don't build the docs-tasks-creator yet.** Rejected: jumping straight to authoring the enumeration skill. Why: user wants more think-time on the broader KB design, and the recommended pilot path (handwrite one client's `docs-tasks.md`, run the existing loop, validate output, *then* design the creator) hasn't been run yet. Building upstream tooling before the downstream loop is validated is the wrong order.
- **If/when built, the docs-tasks-creator should be single-approach, not 3-way.** Rejected: cloning the granular/balanced/pragmatic structure from `integration-tasks` / `refactor-tasks`. Why: docs task size is effectively fixed (one workflow = one task), so the 3-way exploration would be cargo-culting. The real value lives in the *enumeration* phase (codebase audit for entry points) — closer to `refactor-audit` than to a tasks decomposer.
- **For the KB layout (when initiative resumes): markdown is canonical; HTML via visual-explainer is a *view* for select high-value docs.** Rejected: HTML-as-canonical. Why: breaks grep/RAG affordance and breaks incremental edit — the two things Karpathy's wiki pattern leans on hardest. HTML earns its keep for onboarding overviews, system maps, complex full-stack workflows — not meeting notes or simple workflow docs.
- **Split trees inside the KB:** machine-owned (`workflows/`, cc-loop overwrites freely) vs human-owned (`docs/meetings`, `docs/decisions`, `docs/runbooks`, never overwritten). Rejected: mixing both in single files. Why: code-derived docs are point-in-time snapshots that get re-derived; human-authored content is source-of-truth and must survive re-runs.

**Didn't work:**

- Initial framing of the new skill as a "tasks doc mapper for docs" — `map-tasks` is already action-agnostic, no docs-specific mapper needed. Cleared by reading `map-tasks/SKILL.md` and asking a clarifying question.
- "LLM persistent memory" framing — collapsed honestly into "well-structured markdown that the LLM can grep / RAG over." No vector store, no special MCP plumbing required.

**Next:** When user returns to this — read `second-brain-kb-initiative` memory first (do not restart the design conversation), then pilot: pick one client app, handwrite `docs-tasks.md`, run `/tasks-loop --tasks docs-tasks.md --action document-workflow`, see what cc-loop actually produces. Only then design the enumeration skill — informed by what the loop's output actually needs.

**Blockers:** none — user is taking think-time, not waiting on external input.

**Artifacts:**

- `C:\ai-kit\ideas\` (scratch folder, gitignored)
- `C:\ai-kit\.gitignore` (new — single entry: `ideas/`)
- `~/.claude/projects/C--ai-kit/memory/second-brain-kb-initiative.md`
- `~/.claude/projects/C--ai-kit/memory/karpathy-llm-wiki-gist.md`
- `~/.claude/observations/2026-05-15-docs-kb-exploration.md`
- Karpathy gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## [2026-05-14] — Discussed SESSION_LOG centralization — deferred

**Summary:** Discussion-only. User asked whether `SESSION_LOG.md` should move to a centralized `~/.claude/session_logs/{repo}/` for cross-repo analysis. Concluded: keep current in-repo behavior; revisit when a future knowledge base lands.

**Done:** No code or skill changes.

**Decisions:**

- **Keep `SESSION_LOG.md` at the git root, committed with the work.** Rejected: moving it entirely to `~/.claude/session_logs/{repo}/`. Why: the commit-with-the-work handoff is half the point — a cross-machine teammate (or future-me on another box) sees the narrative in git history. Also rejected dual-write (repo + central mirror) for now — adds complexity ahead of need.
- **For cross-repo *workflow* analysis, use `~/.claude/observations/` (already centralized).** SESSION_LOG = project narrative (per-repo); observations = workflow meta-evidence (already pooled across all projects). Different corpora, different questions.

**Didn't work:** —

**Next:** When the user builds the planned knowledge base (combines session logs + meeting notes + other non-technical notes), revisit whether `/close` should dual-write or whether the KB ingests from repos. No action until that project starts.

**Blockers:** none

**Artifacts:** none — discussion only.

---

## [2026-05-14] — Broaden /close suggestion triggers in global CLAUDE.md

**Summary:** Discussed how to use `/close` during mid-workflow context resets (user resets at ~200K because Opus degrades past 256K), then widened the `/close` trigger rules in `~/.claude/CLAUDE.md` to fire on more than just "user says they're wrapping up."

**Done:**

- Edited `~/.claude/CLAUDE.md` `## Closing a session` to list four triggers: wrap-up language, pre-`/clear`/`/compact`, natural pause, stale `SESSION_LOG.md`. Added explicit `/compact` vs `/close` disambiguation.
- Committed `ca49856` and pushed to `claude-home` main.
- Wrote `user-context-management` memory + indexed it in `MEMORY.md`.
- Logged two observations to `~/.claude/observations/2026-05-14-close-trigger-broadening.md` (skill description doc-drift; rule-design principle).

**Decisions:**

- **Content-based triggers, not token-threshold** for `/close` suggestions. Rejected: "suggest /close if context > 150K tokens" — I don't have a reliable token counter exposed, so a threshold rule would fire inconsistently. Chose intent signals I can actually observe (user message content, file state).
- **`/compact` ≠ `/close`** explicitly called out in CLAUDE.md so future-me doesn't conflate "context is large" (→ compact) with "session is ending" (→ close).

**Didn't work:**

- Token-threshold trigger (proposed, rejected). Don't re-propose unless the harness starts exposing a live token counter to the model.

**Next:** Consider mirroring the broadened triggers into the `close` skill's own `description:` frontmatter line — currently says only "end of a working session," which is narrower than the CLAUDE.md rule (see observation 1 in `2026-05-14-close-trigger-broadening.md`). `/improve` will likely surface this.

**Blockers:** none

**Artifacts:**

- Commit `ca49856` (claude-home) — `docs: broaden /close suggestion triggers in CLAUDE.md`
- `~/.claude/CLAUDE.md` — `## Closing a session` section
- `~/.claude/observations/2026-05-14-close-trigger-broadening.md`
- `~/.claude/projects/C--ai-kit/memory/user-context-management.md`

---

## [2026-05-13] — Add INVENTORY quick-reference docs (Claude-Code-aware placement)

**Summary:** Added quick-reference inventories for every component kind in the kit (agents, commands, skills, docs, templates). Routed through a discovery-vs-rendering trade-off and landed on a single `/INVENTORY/` folder at repo root.

**Done:**

- Created 11 markdown files under `INVENTORY/` — `README.md` (index) + `agents.md`, `commands.md`, `skills.md`, `docs.md`, `templates.md`, plus per-subfolder `templates-bugfix.md` / `templates-feature-addition.md` / `templates-greenfield-dev.md` / `templates-incident-response.md` / `templates-refactoring-tech-debt.md`.
- Each inventory groups by workflow family (greenfield / feature-integration / bugfix / refactor / incident-response / QA / meta) and includes the registered `name` and model pin for agents.
- Commit `58a18e6` pushed to `origin/main`.

**Decisions:**

- **Centralize inventories in `/INVENTORY/` instead of in each folder** — because `agents/`, `commands/`, `skills/` are auto-scanned by Claude Code via the `~/.claude/` junction, and any `.md` inside those folders gets auto-registered as a command/agent. Rejected alternatives: per-folder `INVENTORY.md` (registered `/INVENTORY` as a slash command — confirmed empirically), per-folder `_INVENTORY.md` (also registered — underscore is not filtered), per-folder extensionless `INVENTORY` (worked for Claude Code, but GitHub won't render markdown without the `.md` extension).
- **Single flat folder over nested mirror** — `templates-bugfix.md` rather than `INVENTORY/templates/bugfix.md`. Trade-off: lose the structural mirror of the source folders; gain a flat folder where every file renders on GitHub from the README.

**Didn't work:**

- `_INVENTORY.md` rename — still registered as `/_INVENTORY` on the next session-reminder. Underscore prefix is NOT a Claude Code filter convention; only the `.md` extension is.

**Next:** Optional — add a short note to `README.md` or a new `CONTRIBUTING.md` explaining the folder semantics ("files in `agents/`, `commands/`, `skills/` auto-register via the junction; place helper docs under `/INVENTORY/` or `/docs/`"). Would prevent the same rediscovery for future contributors / future-me.

**Blockers:** none

**Artifacts:**

- Commit `58a18e6` — `docs: add INVENTORY quick-reference for agents, commands, skills, templates`
- `INVENTORY/README.md` — landing page (auto-renders on folder entry on github.com)
