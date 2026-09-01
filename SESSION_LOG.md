## [2026-09-01] — provider-neutral portability shipped and live-aligned

**Summary:** Shipped and independently reviewed the provider-neutral two-root skill migration: one transactional sync engine, strict portability checks, neutralized canonical skills, and a live Linux apply that exposes all 31 canonical skills through both managed roots while preserving Matt Pocock's `find-skills` and `teach` installs. Final local QA is green (38 sync tests with one Windows-only POSIX-fixture skip; strict checker: 31 skills, 0 errors, 0 warnings), and hosted run `33546826508` passed Ubuntu, macOS, and Windows at exact commit `2e7b855`.
**Next:** No portability implementation work remains. Optional future evidence: repeat direct provider runtime/UI attribution when all provider binaries and authenticated runtimes are available; this is not a migration blocker.
**Blockers:** none for repository portability or this machine's alignment. Direct provider runtime attribution remains unavailable locally, but qualified live checks, installer discovery, and the three-OS matrix are green.
**Didn't work:** The first preserve rule accepted empty directories; the first transaction retry model did not durably authorize unlink-to-replacement; `npx skills check -g` did not resolve the legacy global lock; hosted CI then exposed Bash-3, Windows-CRLF, macOS `/var` alias, Windows junction quoting/namespace/dangling-target, and Python-hook assumptions. Per-test annotations made the remote tracebacks actionable, and the final implementation now has executable regressions for every failure plus one-read state snapshots.
**Artifacts:** `linux_portability_cross_agent_coupling_tasks.md` · `linux_portability_cross_agent_coupling_analysis.md` · `linux_portability_cross_agent_coupling_techspec.md` · `linux_portability_hosted_ci_investigation.md` · `scripts/sync-skills.py` · `tests/test_sync_skills.py` · [hosted run 33546826508](https://github.com/jimmyrleung/ai-kit/actions/runs/33546826508) · `~/.claude/observations/2026-09-01-ai-kit-{preserve-policy,post-review-remediation}.md`
<!-- close-receipt: 2026-09-01 16:04 · memory:0 · rules:1 · skills:0 · obs:16 -->

## [2026-08-31] — provider-neutral portability design + tasks reviewed

**Summary:** Mapped ai-kit’s Windows and Claude Code coupling, then produced and independently reviewed the analysis, implementation techspec, and 10-task breakdown. The approved design uses one provider-neutral Python sync surface for per-skill links in `~/.claude/skills` and `~/.agents/skills`, baseline-safe rollback, surgical edits to 29 canonical skills, 51 QA scenarios, staged portability enforcement, and approval-gated live migration. Final tasks review: **Approved with notes** (97% confidence).
**Next:** Start `$implement-task` with Task 1 in `linux_portability_cross_agent_coupling_tasks.md`.
**Blockers:** none for Task 1. Later completion needs Windows/macOS CI evidence and explicit approval before any live collision backup, apply, or rollback.
**Didn't work:** The initial techspec rollback model would have erased adopted links, and its first Phase 3 map promoted a contextual inventory into blanket scope. The first tasks breakdown also derived symmetric parallel lists from explicit dependencies while its acceptance criteria introduced hidden dependencies; review moved `teach` metadata earlier, split the oversized batch, serialized documentation closure, and assigned final fail-closed CI explicitly.
**Artifacts:** `linux_portability_cross_agent_coupling_lay-of-the-land.md` · `linux_portability_cross_agent_coupling_analysis.md` · `linux_portability_cross_agent_coupling_techspec.md` · `linux_portability_cross_agent_coupling_tasks.md`
<!-- close-receipt: 2026-08-31 22:44 · memory:0 · rules:0 · skills:0 · obs:5 -->

## [2026-08-26] — breakout-session ported from second_brain + audit run 12

**Summary:** Ported second_brain's `raw/system_design/.claude/commands/breakout_session.md` into ai-kit as `/breakout-session` (15-min oral-exam learning checkpoint: user explains studied material, coach probes Socratically → honest go/no-go; roles reversed from onboard-me; two flagged additions — /teach-workspace calibration + self-assess-before-verdict, offered to strip). Tier-1 Opus + tier-2 Haiku sims 6/6 each. Codex sync applied (also healed the stale analyze-work junction from the rename session). Audit run 12 (FOCUSED): 2 findings, both applied — P39 INVENTORY row+count (the population-sync miss, 4th instance) and P40 write-skills now carries the INVENTORY step in its Output-file checklist (executes 08-24 obs-3's proposal). analyze-work tier-2 Haiku test run from the queue: 6/6, queue cleared. Keep-two: 2026-08-13 dir deleted (user-approved). Population 31 real; desc budget 18,702 (+2.1%, accounted). ai-kit `1e9d9dd`, claude-home `9e45d69` — neither pushed.
**Next:** user decides whether to delete the now-duplicated source command in second_brain (`raw/system_design/.claude/commands/breakout_session.md`). Push both repos (ai-kit also carries unpushed `97811a3` + rename-close commits). Carried from the rename session: techspec decoupling decision, Cursor sync in WSL; carried backlog: 38 (shims), 29 (cc-looper), 14 (docs-tasks-creator marker-vs-split).
**Blockers:** none.
**Didn't work:** Glob again blind to the 3 junction dirs in skills/ during the pre-audit sibling check (4th instance; the Codex sync summary surfaced them) — audit Phase 1 used Get-ChildItem per the known rule; the 08-24 observation proposing an audit-skills Phase-1 wording fix still stands for /improve.
**Artifacts:** `skills/breakout-session/SKILL.md` (ai-kit `1e9d9dd`) · audit packet `~/.claude/improvements/2026-08-26/` (REVIEW + P39/P40, claude-home `9e45d69`) · `last-audit.txt` run-12 entry · obs `~/.claude/observations/2026-08-26-breakout-session-port.md` (2).
<!-- close-receipt: 2026-08-26 21:20 · memory:0 · rules:0 · skills:0 · obs:2 -->

## [2026-08-26] — analyze → analyze-work: rename, clarity rewrite, chain decoupling

**Summary:** Assessed the user's manual analyze rewrite (honest old-vs-new: caught reflow corruption, a dead internal ref, dropped `{work_name}` rule, find-replace-mangled trigger sentence), then landed the agreed change set — rename to `analyze-work`, Execution-profile section deleted (techspec owns approach; chain couples via stable artifact contracts only), 25-ref sweep across 7 skills + README/INVENTORY/filename-contract/both adapter AGENTS.md, triage desc trimmed back ≤800, strict-YAML 8/8, tier-1 trigger sim 7/7 (both naming fears cleared). Committed `97811a3`, NOT pushed.
**Next:** user updates `techspec` with the same decoupling pass (its line-40 "inherit the analysis header's Execution profile when present" was left deliberately — legacy analysis docs may still carry the section; decide keep-or-trim there). Then: push, re-run `adapters/codex/sync.ps1 -WhatIf` + Cursor sync in WSL (junctions still carry the old `analyze` name), tier-2 Haiku trigger test for analyze-work (queued in pending-trigger-tests.txt). Carried: enforcement decision, backlog 38, backlog 29.
**Blockers:** none.
**Didn't work:** batching `npm ls || npm install` with suppressed output in one call — silently no-op'd twice (known scratchpad js-yaml pattern: `npm init -y` first, keep output visible).
**Artifacts:** ai-kit-cleanup `97811a3` (rename change set) + close commit (this entry + 2 rules in `docs/rules/skill-authoring.md`: rename legs on the consumer-grep rule, new diff-manual-rewrites-against-HEAD rule) · obs `~/.claude/observations/2026-08-26-analyze-work-rename.md` (3) · memory `kit-refactor-status` (2026-08-26 entry + bite-5 update) · `~/.claude/improvements/pending-trigger-tests.txt` (analyze-work tier-2).
<!-- close-receipt: 2026-08-26 17:11 · memory:1 · rules:2 · skills:0 · obs:3 -->

## [2026-08-24] — triage-learning-content shipped (first post-v2 net-new skill) + audit run 11

**Summary:** Built `/triage-learning-content` (content-consumption router: TTS / TTS_PLUS_REVIEW / READ for articles/URLs) from the user's AI-iterated spec via /write-skills. Discovery re-scoped the spec's assumed "second-brain code repo with extraction/TTS infra" to reality (markdown vault, no infra) → prose-skill MVP; user placed it ai-kit-global over spec-literal repo-local (fires anywhere + Codex-synced; AskUserQuestion decision). Full authoring flow: tier-1 + tier-2 (Haiku) trigger sims 6/6 each (incl. /triage boundary + "summarize" distractor), live dry-run with agent feedback folded back (narratable-words listening rule — killed a 2× estimate error; dedupe + ~40% band; no prompt-mediated fetchers; NN placeholders), two live runs matching the spec's eval corpus (PostHog → TTS_PLUS_REVIEW, Litt → TTS). Audit run 11 (FOCUSED): clean — 0 proposals; one real finding → **backlog 38**: `grill-me` / `grill-with-docs` / `improve-codebase-architecture` are junctions into `~/.agents/skills` whose bodies call skills resolving NOWHERE ("grilling" / "domain-modeling" / "codebase-design"); user: keep + decide later. Keep-two prune of 2026-08-06 executed (user-approved). Population 30; desc budget 18,319 (+5.0%, accounted).
**Next:** decide backlog 38 (install missing targets / remove junctions / adopt) — until then **never `git add skills/` wholesale** (public repo; rule refreshed in docs/rules/skill-authoring.md). First real `/triage-learning-content` runs calibrate the ~40% visual-share band. Prior bites stand: enforcement decision (top), backlog 29 (cc-looper loop skills), trigger tests.
**Blockers:** none.
**Didn't work:** Glob-based enumeration of skills/ — silently missed all 3 junction dirs (3rd lived instance of Glob link-blindness, now INSIDE skills/); readdir/Get-ChildItem only (obs 2, audit-skills Phase-1 fix suggested). Population-sync rule missed again at authoring (INVENTORY/README bumped only at close — 3rd instance; obs 3 proposes moving it into write-skills' done-definition).
**Artifacts:** `skills/triage-learning-content/SKILL.md` (ai-kit `4d900f0`) · audit packet `~/.claude/improvements/2026-08-24/REVIEW.md` + `backlog/38-external-skill-pack-shims.md` + `last-audit.txt` run-11 (claude-home `7846d9c`) · INVENTORY.md 30-row sync + README counts + `docs/rules/skill-authoring.md` junction-rule rewrite (close commit) · memory `kit-refactor-status` (2026-08-24 entry + bite 8) + MEMORY.md index · obs `2026-08-24-triage-learning-content-authoring.md` (3).
<!-- close-receipt: 2026-08-24 13:49 · memory:1 · rules:1 · skills:0 · obs:3 -->

## [2026-08-13] — /audit-skills run 10: first audit of the settled v2 population — 5 proposals applied

**Summary:** Audit run 10, immediately after the same-day `/improve` apply (`a02d5ac`): all 12 checks over the v2 population (29 skills, 0 commands/agents/templates; desc budget re-baselined at 17,473 → 17,442 post-apply, recomposition fully derived: −1,953 departed cc-looper descs + 546 restored update-workflow-docs). P11's doctrine-phrase detector, on its mandated first back-sweep, found the retired three-entity kit taught as current in exactly the GOVERNING texts (improve's inputs, audit-skills' own inputs, the filename contract's framing) — the workflow skills themselves came through v2 clean. 5 proposals staged AND applied same session, batch-approved (all >90%): 23 (Check-4 hard-cap = option (a), marker-with-length-reason covers >250; house decision 2026-08-13), 30 (improve v2 scope, desc 571→540), 34 (audit-skills inputs marked retired, dormant specs kept), 35 (close-tasks-loop sibling is LIVE — present tense + nested spec path; cc-looper writes `<base>_close.md` verbatim, verified), 36 (contract de-orchestrated + lay-of-the-land row). Backlog: 23/30 promoted→closed, 37 NEW (dangling ~/.claude/commands+agents junctions), 9 bumped.
**Next:** decide backlog 37 (keep vs remove the dangling junctions — keep aligns with 34's dormant-spec bet) and backlog 14 (docs-tasks-creator 288, now the SOLE unmarked >250 body under the new rule: marker vs references/ split); backlog 32 is one user answer away (was `/insights` a retired command with no comeback?); cc-looper repair bite (backlog 29) owns the loop-review fix and the retired loop predictions' return.
**Blockers:** none.
**Didn't work:** `node -e` requiring js-yaml by Git-Bash-style absolute path (MODULE_NOT_FOUND ×12) — rerun as a script with cwd in the scratchpad; logged as observation 3.
**Artifacts:** `~/.claude/improvements/2026-08-13/REVIEW.md` (§ Audit-derived findings) + `proposals/{23,30,34,35,36}-[audit]-*.md` · `improvements/last-audit.txt` run-10 entry (applied status + arithmetic) · ai-kit `744036b` (applied edits) · claude-home `8c1fb30` (packet) · observations `2026-08-13-audit-run-10.md` (4 entries).
<!-- close-receipt: 2026-08-13 22:16 · memory:0 · rules:0 · skills:0 · obs:4 -->

## [2026-08-06] — kit-refactor steps 8–11: incident · ownership · dispositions · full archive comparison + absorptions

**Summary:** Incident family dispositioned on the step-2 suggested shape (user-approved): **`post-mortem`** rebuilt as the only new live skill (`skills/post-mortem/SKILL.md` — blameless discipline, owned/dated/verifiable action items, timeline + response metrics; archived `@post-mortem-agent` worker-split dropped (existed only for an Opus pin); loose inputs accept legacy incident-dir shape OR kit-shaped artifacts (investigation + fix-mode techspec + qa-gates artifact) OR a description, missing artifacts = recorded gaps not blockers; desc 582 ≤600 new-tier). **Diagnosis folded into `bug-investigation`** as an orthogonal incident lens (evidence widens to logs/traces/metrics with timeline correlation + cited quantitative claims, 5-Whys depth, severity-aware gate: P1 streamlined one-pass ≥70% / P2–P4 normal ≥90%; desc 579 ≤800 evolved-tier). **Hotfix folded into `techspec` fix mode** as a hotfix variant (implementation map becomes an executable playbook — exact commands, per-action validation, rollback triggers, success criteria; P1 tech-debt hand-off list for /post-mortem; ESCALATION RECOMMENDED flags; desc 789 ≤1024 consolidation-tier). All 4 archived skill bodies + 7 command bodies READ before folding (closing the step-2 doc's filename-only-disposition caveat); wrapper commands confirmed thin shims, stay archived per no-command-wrappers; `start-incident`/`incident-status` scaffolding dropped (loose inputs replace them; `templates/incident-response/incident-report.md` kept as the report-shape reference). `regression-test-plan`/`bug-regression-test` verified absorbed by implement-task's fix lens (bug-scenario + impact-edge-case tests) → killed. **Backlog 28 CLOSED** (qa-gates `mode: streamlined` kept — the "returns as a skill" branch landed; post-mortem mention now a live ref, retired-name FP gone). Trigger test 4/4 via fresh-context subagent (post-mortem review-ask ✓, P1 outage → bug-investigation ✓, remediation plan → techspec ✓, sprint-retro distractor → none ✓). All 3 frontmatters strict-YAML verified (js-yaml from scratchpad). Codex synced: 31 exposed, 0 issues, `post-mortem` junction verified live. **Audit run 7 (focused):** 31/31 strict-YAML, budget 16,929 (+4.8%, delta fully git-HEAD-derived); 1 finding → proposal 01 APPLIED (output-filename-contract: live post-mortem row `{incident_id}`, step-8 addendum resolving the "do not emit" contradiction, legacy incident names → expected non-drift); checks 2-10/12 clean on the delta; keep-two candidates now 07-19/-23/-27/-31 (surfaced, user-run).
**Summary (step 9 — second session):** Ownership family resolved — **partial restore** on the user's real-usage verdict ("theory awesome; under context switches + deadline pressure the friction rituals go unused"): **`onboard-me` + `record-decision` restored** from archive via `git mv` (history kept) and **decoupled** — all `adr-first`/`challenge-me` awareness stripped (onboard-me: 4 spots; record-decision: 10 spots — now owns its store/numbering description directly, one sequence per decision home, UNREVIEWED review path = human directly with a new **own-it-now** path → `status: owned`, or /close's sweep; no adr-first hop). `adr-first`/`challenge-me`/`predict-first`/`debug-first` **stay archived** — individual restore only on felt need. Callers fixed: `close` decision sweep keeps /record-decision + drops the /adr-first challenge hop; `walkthrough-implementation` routes only to onboard-me/walkthrough (litmus, When-NOT, does-NOT-do). INVENTORY/skills.md + README.md ownership sections slimmed to the 2-skill reality. Verified: zero archived-ownership echoes in live surfaces (grep -R, junctions traversed); js-yaml strict 2/2; Codex synced (dry-run → apply, 33 exposed, 0 issues, both junctions confirmed). **Backlog 27 CLOSED** (resolution note in closed/27). **Audit run 8 (focused):** 33/33 strict-YAML, budget 18,019 → 18,052 post-apply (+6.4%, delta = the two restored descs); 2 proposals BOTH APPLIED (02: onboard-me trigger fold get-up-to-speed/inherited/new-to/walk-me-through, 600→594; 03: record-decision fold document/note + "write an ADR for this" — kit's only ADR surface now, 490→529); **backlog 32 NEW** (close:116 `/insights` command exists nowhere — stale name, 80%, survived runs 4/6/7); run-7 P01 verified applied; **keep-two prune EXECUTED** (user-approved: 07-19/-23/-27/-31 deleted, 08-05+08-06 remain). Commits: ai-kit `1cbb0e1` (kit-refactor), claude-home `a0caf07` (pushed).
**Summary (step 10 — third session):** Archive-sweep decision items ALL dispositioned (state doc §3 closed): **`triage` RESTORED** (git mv, history kept) and adapted skill-centric — routes to chain-entry skills (`analyze` / `bug-investigation` / `lay-of-the-land`) instead of the 5 retired orchestrators; Phase-0 mid-flight detection reads kit artifact conventions (`_analysis`/`_techspec`/`_tasks`/`_investigation` + `## Review` stamps) via a next-step state table; short-circuit table rebuilt from live skills; loop-primitive table kept → loop-recipes' "exactly two places" contract healed + global CLAUDE.md "offer /triage" no longer dangling; 0 archived names in the new body (16-name grep). **create-qa-scenarios absorbed into `techspec`** per user shape: post-write **QA-scenario pass** (Process 7) — spec re-read as QA engineer, Test plan gains Priority/Automatable columns, every committed behavior ↦ ≥1 scenario (happy/error/edge/integration), proportionality guard carried; desc +30 ("prioritized QA scenarios"). **roadmap-creation + migrate-notion stay archived**; bug-regression-test confirmed already absorbed (step 8). Codex synced (34 exposed, 0 issues, triage junction verified). **Audit run 9 (focused):** 34/34 strict-YAML, budget 18,846→18,880 post-apply (+4.4%, fully accounted); 3 proposals ALL APPLIED (04: INVENTORY delta-sync — triage + missed step-8 post-mortem rows in, archived migrate-notion row out; 05: contract expected-non-drift entry for triage's Phase-0 artifact refs; 06: triage desc fold which-skill/where-to-start/what-to-run 764→798 — trigger-test phrase-5 miss as evidence); **backlog 33 NEW** (README + INVENTORY still describe the pre-refactor kit: five-workflow table, Codex "41+17+8" vs verified 34+0+0, skills.md was missing 19 live skills — named-bite candidate, sequence with the Codex AGENTS.md rewrite); backlog 29 date-bumped (now the sweep's only open item). Haiku-floor trigger test 3.5/6: triage-target phrase ✓; step-9's requested onboard-me probe RAN — "inherited service" → `walkthrough` collision at weak-model floor (watch); "generate QA scenarios" → `qa-loop` (missing not-user-invoked guard, rides with backlog 29). New repo rule: population changes sync INVENTORY/README in-step (steps 8+10 both missed it).
**Summary (step 11 — fourth session, full archive comparison + absorptions):** User asked for a FULL live-vs-archive comparison ("no I-only-looked-at-a-few") + honest assessment, grounded in real usage. **/orchestrate: 12 Opus workers** (7 comparison — every archived skill/command/agent body read end-to-end, 15 diverged same-name pairs diffed; 5 evidence — all 14 `implementation_history` folders across both private work vaults, 571 files) → run home **`kit_comparison_2026-08-06/`** (12 deliverables + `kit_comparison_synthesis.md`, **do-not-commit**: vault codenames). **Verdict: new kit clearly better — ~70-80% absorbed faithfully or improved, verification layer traceably shaped by the vaults' real failures, 11/17 agents were pointer shells — but "content moved, control didn't"** (between-phase sizing/risk-gates/abort/slice-loop logic died with the commands), and the #1 evidenced failure is **verification abandonment** (trap 10/13, connect 9/10, serviceapps 20/23 prefixes without QA — under the OLD kit, orchestrators included → enforcement problem, deliberately left OPEN). 5 errors found in `kit_refactor_current_state.md` (regression-test-plan "verified absorbed" overstated; update-workflow-docs mapped to a nonexistent skill; incident fold ~85% not 100%; no-command-wrappers not absolute — tasks-loop.md lives; §4 agent-ref caveat confirmed in BODIES). **8 absorptions user-approved and landed** (commits `18feda9` restore · `b581232` absorptions · `0aadc75` hygiene): update-workflow-docs RESTORED as skill (546-char desc, strict-YAML ok, Codex junction verified — trigger test pending); PRD → `analyze` greenfield **`## Slice requirement`** (Done-when + Building on; techspec/tasks-breakdown read it by name — greenfield chain head healed); bug-investigation incident output sections (timeline/scope/ruled-out) + review-artifact **P1 one-reviewer dial** (user call: incidents ride the normal chain, no abbreviated mode); qa-gates **Gate 3d release-readiness + 3e repo-local perf/regression hook** (baselines repo-specific → /close mints local pairs) + **Gate 5 `go-modulo-ops`**; techspec refactor depth (deployment/phase, metric measurement+baseline, transitional-state tests, Contingency & unknowns); close **ADR staleness escalation** (~3 closes → own-or-park, named not neutral); agent rubrics → review-artifact narrative/scope-integrity red flags. **Templates concept KILLED at close** (user deleted all 8; 6 live refs stripped to inline shapes; archive/templates byte-identical; new repo rule). **SECURITY: live access token in `mktool_kb/raw/connect/.../feature_176222_generate_token_endpoint_investigation.md:76,405` — rotate.**
**Summary (step 12 — fifth session, v1 archive → v2 self-description → main → Codex):** Everything pre-refactor moved to `archive/v1/` (`b2e9edc`; the pre-commit secret-scan correctly blocked the step-11 comparison corpus — vault paths + employer refs in never-committed files staged as additions by the move — resolved by gitignoring `archive/v1/kit_comparison_2026-08-06/`, stays local-only). Fresh **root README.md** (v2 skill-centric story, core-chain diagrams, skills-only install, reconciled Codex section, Cursor flagged v1-era-stale) + **single-file root INVENTORY.md** (user choice over the v1 dir shape; 29 rows verified against the tree, hygiene-grepped) with deprecation banners on all 11 v1 README/INVENTORY pages; population-sync rule repointed to `INVENTORY.md` (`52cb451`). **kit-refactor merged to main** (`200944f`, --no-ff, 23 commits, clean) **and pushed — main IS v2.** Codex: dry-run verified 29/29 junctions current, 0 issues (junctions track the working tree, so v2 was already live); **instruction layer rewritten for v2** (`bb43f67`: AGENTS.md — junction-only surface, generic-subagent fan-out reading, `/name` = `$name`, Claude-only primitives, Anchored loop; adapter README; sync.ps1 NONE-in-v2 headers + refresh-between-markers hint), deployed by pasting the kit block between `kit-mechanics:begin/end` markers at the private `~/.codex/AGENTS.md` include point (block verified identical to source; 18.2 KB < 32 KiB cap) — **both Codex layers now active globally**. **Backlog 33 CLOSED (both halves)**. claude-home verified already pushed; `projects/` (auto-memory) confirmed machine-local by design — memories do NOT travel to the other machine. Near-miss caught: "copy `~/.codex/AGENTS.md` over the repo file" — the two are different layers (private conventions vs public mechanics); read-before-overwrite surfaced it (obs 2). At close: 3 stale UNREVIEWED ADRs **all parked** (user call; first live fire of the step-11 staleness escalation — obs 3).
**Summary (step 13 — sixth session, SECOND MACHINE: deployed-surface reconciliation + Cursor adapter v2):** "Confirm codex+cursor ported" surfaced the two-machine gap: steps 1–12's sync receipts described the other machine; this machine's `$HOME` surfaces were v1-stale while repo main was already v2 (deploy state is machine-local — obs 1). **Codex (this machine):** 48 stale entries deleted (21 dangling junctions → archive/v1 targets, 24 orphan generated agent/orch dirs, 3 v1 real dirs shadowing v2 `document-workflow`/`implement-task`/`update-workflow-docs`; every name traceability-checked against archive/v1 before deletion), `sync.ps1` apply → **29/29 junctions, 0 issues**; private `~/.codex/AGENTS.md` rebuilt = v2 kit block between `kit-mechanics:begin/end` markers + personal block preserved byte-for-byte (block-identical/intact verified; 13.2 KB < 32 KiB cap). **Cursor: adapter REWRITTEN for v2** (`bc3e6b7`): skills-only sync with generation paths retained dormant (codex-v2 posture), **prune fixed to catch dangling symlinks** (v1's `*/` glob never matched them — the exact archive-move failure mode; ps1 existence checks now survive dead junctions via `Get-Item -Force`), AGENTS.md + README rewritten on the codex-v2 model (#160426 **moot** — v2 installs nothing at `~/.cursor/agents`; new WSL `~/.claude` single-store caveat), root README Cursor section v2 + outdated codex known-stale banner dropped, INVENTORY assessment row, **new `.gitattributes`: `*.sh text eol=lf`** (autocrlf CRLF breaks bash-in-WSL). Deployed in WSL: 7 linked + **46 v1 orphans pruned** (28 skill entries incl. the 8 generated orchestrators, all 18 generated agents), final 29/29 valid symlinks, `agents/` empty; the `implement-task` shadow dir removed by the user via `!` (the rm-hook blocks approved deletions too — command-text only; script-internal `--prune --force` is the designed path). Windows `~/.cursor/AGENTS.md` kit block → v2 markers (same verify). Memories: codex-adapter + cursor-160426 rewritten to v2 state; wsl-invocation gained the Git-Bash `/mnt/c`-mangling rule. **Both adapters now v2 end-to-end on this machine.**
**Next:** **Enforcement decision first** (cc-looper run-end hook vs hard-wired qa-gates offer at implement-task last-task vs accept-suggest-only — the evidence says this is the kit's #1 real failure; natural home = the backlog-29 cc-looper session). Then: `kit_refactor_current_state.md` superseded-header pass (5 corrections in synthesis §6; note the doc now lives at `archive/v1/kit_refactor_current_state.md`); backlog 29 (loop skills, W7 confirmed body-level refs); trigger tests carried (+ update-workflow-docs new); rotate the connect token (user); **other-machine Cursor deployment (user, if it runs cursor-agent):** pull ai-kit, `bash adapters/cursor/sync.sh --dry-run` then `--prune --force` in its WSL, remove any shadowing generated dirs it reports as `skip`, refresh its AGENTS.md kit block to the `kit-mechanics` markers (its Codex side is already v2); **this machine (user):** restart Codex + `cursor-agent` and spot-check the surface (`$analyze` / 29 skills listed); **teach/find-skills triage** — both are now exposed on Codex AND Cursor surfaces, decide if they belong in the population.
**Blockers:** none
**Didn't work:** `powershell -File sync.ps1` (Windows PowerShell 5.1) misparses the script's UTF-8 em-dashes — always run sync.ps1 in-process under pwsh 7. js-yaml absent from ai-kit node_modules AND global npm root — install into the session scratchpad and run node from there. (Both promoted to `docs/rules/skill-authoring.md` refinements at close.) (step 9) inline `NODE_PATH=<scratchpad>/node_modules node -e` ALSO fails — `cd` into the scratchpad is the only reliable form (rule refined in place); and the failure was a re-derivation: the rule already said so — read docs/rules/ before tooling probes (obs 2). (step 10) `require('./node_modules/js-yaml')` from `node -e` fails even in the right cwd — plain `require('js-yaml')` from the scratchpad is the form; mixing a bash heredoc and an inline node template-literal script in one call breaks on quoting — split into two calls (heredoc → temp file, then concat). (step 11) `npm install --no-save` with no `package.json` walks UP and installs into an ancestor — silent local no-op; `npm init -y` first (rule refined). Re-hit the KNOWN sync.ps1 format-stream collision (Select-Object in the apply call) — second rules-read-after-failure this week (obs 4). W1's "5 of 8 templates orphaned" count was off (bug-report + incident-report had callers) — orchestrator re-derivation caught it; worker counts get a second derivation before use. (step 12) PowerShell-tool cwd persists across calls — a stray location change from an earlier probe left it in `archive/v1/INVENTORY/` and a later `git add README.md` failed on pathspec; anchor repo git ops with `git -C <root>` or re-`Set-Location` first. Do-not-commit prose without a `.gitignore` entry — the comparison corpus only got its guard when the commit failed (obs 1: flag and guard in the same step). (step 13) Git Bash mangles bare `/mnt/c/...` args to `wsl.exe` (prefixes `C:/Program Files/Git`) — wrap the whole command: `wsl.exe bash -c "bash /mnt/c/..."`. The rm safety hook blocks approved deletions too (it inspects command text only, cannot see AskUserQuestion/chat approval) — route removals through a designed script flag (`--prune --force`) and hand the user a `!`-prefix one-liner for any raw `rm`, in the same message that asks approval.
**Artifacts:** `skills/post-mortem/SKILL.md` (new); `skills/bug-investigation/SKILL.md` (incident lens + desc); `skills/techspec/SKILL.md` (hotfix variant + desc); `docs/output-filename-contract.md` (post-mortem row + step-8 addendum + non-drift entries — audit P01); `kit_refactor_current_state.md` (§2 incident resolved, §3 bug-regression-test absorbed, §Recommendation updated); audit packet `~/.claude/improvements/2026-08-06/` (REVIEW.md run-7 + proposal 01 applied) + `last-audit.txt` run-7 entry; `~/.claude/improvements/backlog/closed/28-qa-gates-incident-mode.md` (closed w/ resolution); memory `kit-refactor-status` (step-8 entry); Codex junction `~/.codex/skills/post-mortem`; `docs/rules/skill-authoring.md` (js-yaml scratchpad-install + sync.ps1 pwsh-7/-WhatIf/format-stream refinements); obs `~/.claude/observations/2026-08-06-incident-family-consolidation.md` (3: caveat-as-work-item, contract-row miss, subagent trigger-test tier); (step 9, commit `1cbb0e1`) `skills/{onboard-me,record-decision}/SKILL.md` (restored+decoupled+trigger-folded); `skills/{close,walkthrough-implementation}/SKILL.md` (caller fixes); `INVENTORY/skills.md` + `README.md` (ownership sections); `kit_refactor_current_state.md` (§2 ownership resolved); audit run-8 REVIEW section + proposals 02/03 (applied) + backlog 32 + backlog closed/27 + last-audit run-8 entry (claude-home `a0caf07`, pushed); memories `engineering-ownership-skills` (rewritten: partial-restore state) + `kit-refactor-status` (step-9 entry) + MEMORY.md index; Codex junctions `~/.codex/skills/{onboard-me,record-decision}`; `docs/rules/skill-authoring.md` (NODE_PATH cd-required refinement); obs `~/.claude/observations/2026-08-06-ownership-family-restore.md` (3: restore≠conformance-neutral, rules-index read-skipped, UNREVIEWED-sweep first live exercise); (step 10) `skills/triage/SKILL.md` (restored + rewritten, desc 798) · `skills/techspec/SKILL.md` (Process 7 QA-scenario pass + Test-plan columns + desc) · `kit_refactor_current_state.md` (§3 all five dispositioned, §Recommendation: backlog 29 = only open item) · `INVENTORY/skills.md` (triage + post-mortem + Incident section in, migrate-notion out — audit P04) · `docs/output-filename-contract.md` (triage non-drift entry — audit P05) · `docs/rules/skill-authoring.md` (population-sync rule) · audit run-9 REVIEW section + proposals 04-06 (all applied) + backlog 33 NEW + backlog 29 bump + last-audit run-9 entry; memory `kit-refactor-status` (step-10 entry + desc + next-bites) + MEMORY.md index; Codex junction `~/.codex/skills/triage`; obs `~/.claude/observations/2026-08-06-triage-restore-qa-scenarios.md` (3: surfaces-drift, trigger collisions, absorbed≠reachable); (step 11, commits `18feda9`+`b581232`+`0aadc75`+close commit) **`kit_comparison_2026-08-06/`** (12 worker deliverables + synthesis + README run header — UNTRACKED, do-not-commit) · `skills/update-workflow-docs/SKILL.md` (new) · `skills/{analyze,techspec,tasks-breakdown,bug-investigation,review-artifact,qa-gates,close,document-workflow,post-mortem,orchestrate,write-skills,lay-of-the-land}/SKILL.md` (absorptions + hygiene + template-ref strips) · `README.md` + `docs/model-assignments.md` (historical banner) · `docs/rules/skill-authoring.md` (npm-init refinement + templates-retired rule) · templates/ DELETED (8 files, user) · commands/tasks-loop.md symlink DELETED (user — last command wrapper gone, "no command wrappers" now absolute; canonical stays in cc-looper) · memory `kit-refactor-status` (step-11 entry + desc + next-bites incl. enforcement item 0) + MEMORY.md index · Codex junction `~/.codex/skills/update-workflow-docs` (34 exposed, 0 issues) · obs `~/.claude/observations/2026-08-06-kit-comparison-absorptions.md` (4: orchestrate clean run + hint-refutation, filename-dispositioning overstated ×5, enforcement evidence, npm/rules-read-after-failure); (step 12, commits `b2e9edc`+`52cb451`+merge `200944f`+`bb43f67` — all pushed to main) root `README.md` + `INVENTORY.md` (new, v2) · `.gitignore` (comparison-corpus entry) · `archive/v1/**` (full v1 move + 11 deprecation banners) · `docs/rules/skill-authoring.md` (population-sync rule → root `INVENTORY.md`) · `adapters/codex/{AGENTS.md,README.md,sync.ps1}` (v2 rewrite) · private `~/.codex/AGENTS.md` (header fix + kit-mechanics marker block pasted, both layers active) · memories `codex-portability` (v2-complete, deployment topology) + `kit-refactor-status` (step-12) + MEMORY.md index · obs `~/.claude/observations/2026-08-06-v2-docs-codex-close.md` (3: gitignore-at-creation, layer-mismatch near-miss, staleness-escalation first fire) · backlog 33 → closed/ (resolution note) · 3 ownership records (`compile-kb` 0001/0002, `close-repo-memory` 0001) → `status: parked`; (step 13, SECOND MACHINE, commit `bc3e6b7` + close commit) `adapters/cursor/{sync.sh,sync.ps1,AGENTS.md,README.md}` (v2 rewrite) · `.gitattributes` (new, `*.sh eol=lf`) · root `README.md` (Cursor v2 section + codex banner fix) · `INVENTORY.md` (assessment row) · deployed this machine: `~/.codex/skills` 29 junctions + `~/.codex/AGENTS.md` v2 markers · WSL `~/.cursor/skills` 29 symlinks + `agents/` emptied · Windows `~/.cursor/AGENTS.md` v2 markers · memories `codex-adapter-synced-this-machine` + `cursor-adapter-agents-blocked-160426` (v2 rewrites) + `wsl-invocation-from-windows-harness` (git-bash mangle rule) + MEMORY.md index · obs `~/.claude/observations/2026-08-06-adapter-v2-deployment.md` (3: machine-local deploy state, prune-vs-dangling-links, hook-vs-approval boundary)
<!-- close-receipt: 2026-08-06 17:25 (step-13 session, second machine; extends the step-12 receipt) · memory:4 · rules:0 · skills:0 · obs:3 -->

---

## [2026-08-05] — kit-refactor steps 1–7: implement-task → skill · non-technical paths + full audit · techspec-family · tasks-family · implementation-family + desc-budget decision · QA-family · document-workflow → skill

**Summary (step 1, am):** `commands/implement-task.md` converted 1:1 to `skills/implement-task/SKILL.md` with a loosened input contract (prefix / tasks-doc path / task number / plain description all resolve; triple echoed back).
**Summary (step 2, pm — second session):** non-technical paths consolidated skill-centric: **`analyze`** (one mode-detecting skill — integration / greenfield / refactor; integration-analysis body as base + refactor-audit's scope/contracts/risk lens + prd-creation's anti-scaffolding guards; `{work_name}_analysis.md`), **`review-analysis`** (old command workflow-2 + review-artifact + reviewer agent → one skill; reviews analysis AND investigation docs, in-place `## Review`), **`bug-investigation`** restored skill-only (generic subagents). Codex surface reconciled 1:1 (52 orphans + stale implement-task twin pruned, `$GenCmds` emptied — step 1's Next, done). Then a FULL `/audit-skills` (first post-archive: 27 skills · 14,021 desc chars = new baseline): 17 findings, 8 proposals + 2 echo fixes applied — headline: the agent archive had silently broken `review-implementation`'s `@code-reviewer-agent` fan-out (now generic subagents + the retired agent's ≥80-confidence filter). Commits `d8411ea` + `02043c2`.
**Summary (step 3, eve — third session):** techspec family consolidated skill-centric: **`techspec`** (one mode-detecting skill — integration / greenfield / refactor / fix + an orthogonal risk lens; single-approach pragmatic-balance DEFAULT with 3-way exploration as escalation; folds techspec-creation + integration-techspec + refactor-plan + pragmatic-techspec + impact-analysis + create-techspec's draft-comparison protocol (probe-first prior / convergence-risk / harvest); `{work_name}_techspec.md` for all modes — `_plan.md` / `_impact_analysis.md` retired), **`review-analysis` renamed `review-artifact`** and widened with a techspec contract-check lens + delta rule (reviewed upstream → review the techspec's delta only). User decisions: impact rides inside fix-mode techspec; pragmatic is the default depth; commands incorporated, not kept as templates (all four in the kit-refactor-status memory). 6 consumer skills + INVENTORY + filename contract updated; Codex synced (28 exposed, review-analysis junction pruned). Focused audit run-2: **0 proposals** (clean), backlog 31 new (document-workflow family: live consumers point at the archived interactive command), backlog 16 "consolidation descriptions run hot" pattern.
**Summary (step 4, night — fourth session):** tasks family consolidated skill-centric: **`tasks-breakdown`** (one mode-detecting skill — integration / greenfield / refactor; **balanced sizing DEFAULT** with 3-way granular/balanced/pragmatic as escalation + downshift check; balanced-tasks-creation body as base (enumeration-coupling, derive-parallel-lists, independent-source ACs) + refactor-tasks' per-task risk/rollback + tasks-creation's vertical-ordering/anti-scaffolding + create-tasks' harvest rule + rename call-site sweep; `{work_name}_tasks.md` all modes), **spec-carrying mode** (tasks-as-spec hatch promoted first-class: plan-mode/investigation → tasks with implementation detail + `## Locked decisions`, ~5-decision escalation guard), **`review-artifact`** widened with a tasks-doc decomposition lens + delta rule. All 4 decisions mirrored step 3 (commands incorporated; widen not new-skill; balanced default; mode not combined-skill). Trigger sim 10/10 (2 negatives correct); Codex synced (29 exposed, 0 issues). Audit run-3: 1 finding → proposal 09 APPLIED (implement-task added to contract's expected non-drift list); backlog 16 run-3 recount 10/29 (consolidation-head band 650–800 = concrete option-(c) ceiling candidate). **User directive widened:** loose inputs (high-level description / file-with-draft / detailed prompt) binding for ALL refactor skills; `{token}` mentions = resolution forms, never required invocation shapes (memory `loose-skill-input-contracts`).
**Summary (step 5, fifth session):** implementation family consolidated skill-centric: **`implement-task`** absorbs archived gf-implement-task + implement-bug-fix — **fix lens on a loose bug target** (investigation + fix-mode techspec, tasks doc optional; the investigation stands in as tasks_doc for verify-task; unreviewed investigation → flag + /review-artifact suggest), **scope guard generalized to all work types** (implement-bug-fix's refactoring gate + gf's "while we're here" guard: critical → stop-and-propose, nice-to-have → follow-up), gf's spec-gap-noting + user-observable-behavior check borrowed; slice-close Done-when/smoke extras DROPPED as qa-gates duplicates (3 AskUserQuestion decisions, all recommendations accepted). `verify-task` 4 stale refs fixed (Workflow-2 pointers → Workflow 3; archived-caller mentions dropped — implement-task skill = sole caller, loop variant confirmed non-caller); `review-implementation` verified no-change; INVENTORY rows annotated. Audit run-4 (focused): 29/29 strict-YAML, 0 proposals, 2 Check-2 findings → backlog. **Then the 7-run-old desc-budget question was ASKED and DECIDED: option (c) tiered by role** — ≤600 new / 600–800 evolved+mode-heads note-only / 800–1024 consolidation-heads-only (trim only body-discoverable process detail, never triggers) / >1024 hard fail; canonical spec rewritten into audit-skills Check 2, write-skills limits table points at it; implement-task desc trimmed 856→770 under the policy; backlog 16 closed-decided + 02 closed-won't-do. Codex surface: 29 exposed, 0 issues (junction-live, no sync needed).
**Summary (step 6, night — sixth session):** QA family consolidated skill-centric: **`qa-gates`** skill absorbs both archived command shims — diff-first showed `implementation-quality-assurance` is a strict older subset of the archived `qa-gates` command (no review-skip logic, dead `@code-reviewer-agent` fan-out; nothing unique to borrow). Folded in: **prior-review check in Gate 0** (prefix-close only; `## Review` sha-stamp covers tree → pointer, miss → suggest /review-implementation; NO embedded fan-out — user decision, Gate 5 `go-with-caveat: unreviewed` stays the backstop), **loose target input** (prefix / doc path / description, resolve + echo; composed-caller defaults table — verify-task contract untouched). Body recompressed to exactly 250 (retire-to-fund; Gate-1 incident clauses preserved). **Alias retired everywhere**: skill desc (569), INVENTORY/commands.md, global CLAUDE.md:79, `~/.codex/AGENTS.md`:148 (NOTE: `AGENTS.personal.md` gone — AGENTS.md is the single file now; 07-10 compose model stale). Audit run-5 (focused): 29/29 strict-YAML, desc budget 15,788 (first run-over-run shrink), 1 finding → proposal 10 APPLIED (audit-skills Check 10 taught the retired command-wraps-skill pairing as "the intended pattern" — its example was the exact pair retired this step); backlog 28 bumped (incident mode = qa-gates' only remaining archived-family coupling), 23 bumped 80→85 (third at-cap compression event). Consumer-grep rule gained the **doctrine/convention refinement** (retired patterns cited via live names evade the name sweep).
**Summary (step 7, seventh session):** `document-workflow` command→skill (`f76fe63`) — mode-head (backend default / full-stack opt-in), loose reference input, git-root output anchoring back-ported (audit worklist #3), ~190-line output template extracted **byte-identical** to `skills/document-workflow/references/output-template.md` = the family's canonical contract (diff-verified; loop fork's embedded copy confirmed diverged — stays with the cc-looper bite). Codex junction synced (30 exposed, 0 issues). Two-tier trigger test: session-model 3/3; a Haiku-strength re-run exposed the loop fork's "end-to-end" collision → fixed cross-repo in cc-looper (`5c391ef`: desc says "fork of the skill", runner-only guard). Audit run-6 (focused): 30/30 strict-YAML, budget 16,483 (+4.4% = the new desc); 3 proposals ALL APPLIED (11 loop desc cross-repo; 12+13 discharge the carried >800 re-classification: compile-kb 933→737, review-implementation 842→659 — **zero non-consolidation skills >800, tier spec fully conformant**, final budget 16,157); **backlog 31 CLOSED** (family fate resolved by option (a) verbatim — the conversion; consumer sweep confirms all `/document-workflow` pointers resolve).
**Next:** carried: fresh-context trigger tests for the earlier 6 new/converted skills (`analyze` — try "audit this codebase for tech debt"; `techspec` — "spec out this feature" / "what's the blast radius of this fix"; `tasks-breakdown` — "break the approved spec into tasks" + a spec-carrying ask from plan mode; `review-artifact`; `bug-investigation`; `implement-task` — "implement the fix for BUG-123" fix-lens route; document-workflow itself is DONE, two-tier) + first live `/tasks-breakdown` run on real work; **backlog 15 close pending user word**. Then next refactor bites in priority order: **backlog 29** (cc-looper qa-loop/qa-loop-docs/review-checkpoint still spawn the dead `@code-reviewer-agent`; same bite now also carries the doc-workflow-loop embedded-template drift vs the canonical references/ copy + backlog 22 split question), `adapters/codex/AGENTS.md` mechanics-layer rewrite (pre-archive world; sync.ps1:36-37 header comment joins it — still says "document-workflow has only a stripped -loop fork"), **backlog 27** (ownership-layer refs: restore vs strip), incident family fate (backlog 28). Consider a `update-workflow-docs` re-mint (staleness triage) when the docs family next comes up — named in the new skill's NOT-do as not-yet-re-minted.
**Blockers:** none
**Didn't work:** (step 1) node js-yaml via global require paths — run from `~` per the skill-authoring rule. (step 2) hand-enumerated archived-name grep missed `@code-reviewer-agent` refs — derive sweep lists from the `archive/` dir listing (now a repo rule). (step 3) naive archive-derived sweep self-matched 359/360 hits (archive keeps copies of restored same-name skills — subtract live names first; rule refined); `Measure-Object -Line` for line caps (skips blanks — use `(Get-Content).Count`). (step 4) — (step 5) `sync.ps1` takes `-WhatIf`, not `-DryRun`; a `^---\n` frontmatter regex false-fails on CRLF files — always `\r?\n` in node probes. (step 6) — (step 7) counting chars of backtick-containing strings via node-in-double-quoted-Bash — command substitution corrupts the string silently; write the text to disk first and count from the file. Piping `sync.ps1` output into `Get-Item | Select-Object` in one PowerShell call — format-stream collision exits 1 despite success; verify in a separate call.
**Artifacts:** `skills/{analyze,review-artifact,bug-investigation,implement-task,techspec,tasks-breakdown}/`; audit packet `~/.claude/improvements/2026-08-05/` (run-1: 8 applied; run-2: 0 proposals; run-3: proposal 09 applied, backlog 16 updated); `docs/rules/skill-authoring.md` (consumer-grep rule + archive-minus-live refinement); `docs/output-filename-contract.md` (tasks-breakdown row + expected non-drift list); obs `~/.claude/observations/2026-08-05-{implement-task-skill-conversion,nontechnical-paths-consolidation,techspec-consolidation,tasks-breakdown-consolidation}.md`; memories `kit-refactor-status` (steps 1–5 + decisions), `loose-skill-input-contracts` (widened), `codex-portability` + `engineering-ownership-skills` (updated); (step 5) `skills/{implement-task,verify-task,audit-skills,write-skills}/SKILL.md` + `INVENTORY/commands.md` + `docs/rules/skill-authoring.md` (bidirectional-sweep refinement); audit packet run-4 section + backlog 02/16 → closed/ + last-audit run-4 entry; obs `~/.claude/observations/2026-08-05-implementation-family-consolidation.md`; (step 6) `skills/qa-gates/SKILL.md` (250 exactly) + `skills/audit-skills/SKILL.md` (Check-10 fix) + `INVENTORY/commands.md` + `docs/rules/skill-authoring.md` (doctrine refinement); global `~/.claude/CLAUDE.md`:79 + `~/.codex/AGENTS.md`:148 (alias dropped); audit packet run-5 section + proposal 10 (applied) + backlog 23/28 bumps + last-audit run-5 entry; obs `~/.claude/observations/2026-08-05-qa-family-consolidation.md`; memory `kit-refactor-status` (step-6 entry + desc); (step 7) `skills/document-workflow/{SKILL.md,references/output-template.md}` + `INVENTORY/commands.md` + compile-kb/review-implementation desc trims (all in `f76fe63`); cc-looper `claude-config/skills/document-workflow-loop/SKILL.md` (`5c391ef`); audit packet run-6 section + proposals 11-13 (all applied) + backlog 31 → closed/ + last-audit run-6 entry; obs `~/.claude/observations/2026-08-05-document-workflow-conversion.md`; memory `kit-refactor-status` (step-7 entry, next-bites reshuffle) + MEMORY.md index
<!-- close-receipt: 2026-08-05 22:53 (step-7 session; extends the 22:22 step-6 receipt) · memory:9 · rules:4 · skills:1 · obs:18 -->

---

## [2026-07-31] — /close 2c: repo-local skill minting (Codex-verified dual-write) + focused audit

**Summary:** Partially supersedes the entry below — 2c now ALSO offers minting repo-local skills (offer-gated, ≤2/close) as tier 2 of the promotion ladder (tagged rule → repo-local pair → /improve-minted global skill); a pair = identical SKILL.md dual-written to `.claude/skills/` + `.agents/skills/` (Codex repo-level discovery verified live on 0.146.0; authoring constraints extracted to write-skills' new "Portable profile" section). Same-session focused /audit-skills caught the edit pushing close to 268 > the 250 hard cap (metric calibrated: total lines) → compressed back to exactly 250 via that extraction (P10), and fixed tasks-loop's `<user>` description in the cc-looper canonical (P11, Codex validator rule).
**Next:** first real repo-local mint in a work repo — the live test of `.claude/skills/` project discovery and the 2c offer flow. Then: keep-two prune (improvements/2026-07-19 + -23; command in 2026-07-31/REVIEW.md) and triage the untracked `skills/find-skills` + `skills/teach` dirs in ai-kit's tree. (Carried: adr-0001 close-repo-memory UNREVIEWED → /adr-first; batched-review pipeline live run; cc-looper AI-6 build session.)
**Blockers:** none
**Didn't work:** probing Codex repo-skill discovery via `cmd /c cd` in an uncommitted scratch repo — discovery needs `codex exec -C <dir>` AND ≥1 commit; the first probe false-negatived.
**Artifacts:** improvements/2026-07-31 proposals 10+11 (both applied) + REVIEW.md audit section; skills/close/SKILL.md + skills/write-skills/SKILL.md; cc-looper claude-config/commands/tasks-loop.md
<!-- close-receipt: 2026-07-31 18:31 · memory:1 · rules:0 · skills:0 · obs:2 -->

---

## [2026-07-23] — /close 2c skill-candidate tagging (recurrence-gated promotion)

**Summary:** Resolved "should /close map local skill proposals?" as no-new-mechanism: the rules layer is the proposal inbox — 2c now tags repeatable procedural how-tos `<!-- skill-candidate -->` + a paired (b) observation, and /improve mints the skill only on recurrence evidence (rejected: a dedicated skill-proposal mapping step).
**Next:** unchanged from the entry below — first live run of the batched-review pipeline; port to `gf-implement-task` if it proves out. (Carried: adr-0001 close-repo-memory UNREVIEWED → /adr-first; 2c in a non-kit repo; cc-looper AI-6 build session.)
**Blockers:** none
**Didn't work:** —
**Artifacts:** ai-kit `07b5de3` (skills/close/SKILL.md, +3 lines)

---

## [2026-07-23] — Batched-review topology: review-implementation skill + qa-gates commit-lifecycle fix

**Summary:** Replaced implement-task's per-task reviewer fan-out with a new once-per-prefix `/review-implementation` skill (correctness / conventions / simplicity + ship-ready refactors, sha-stamped `## Review` block) and made qa-gates commit-agnostic (informational committed-check, `GO, conditional on commit`); pipeline is now implement-task (verify-task inline) → review-implementation → qa-gates. Audit run-2 caught and fixed a same-session 255>250 body overrun (P03 applied; qa-gates sits at exactly 250 — next edit must retire lines).
**Next:** first live run of the new pipeline on a real prefix — validates the review-stamp skip rule in qa-gates pre-work and the conditional-GO path; if it proves out, port the same Workflow-2 retirement to `gf-implement-task` (still has embedded per-task review). (Carried: adr-0001 close-repo-memory UNREVIEWED → /adr-first; 2c in a non-kit repo; cc-looper AI-6 build session.)
**Blockers:** none
**Didn't work:** `sync.ps1` via `powershell` 5.1 (UTF-8 em-dash parse errors — `pwsh` only) and a guessed `-DryRun` flag (it's `-WhatIf`) — both were already in the `codex-sync-on-skill-change` memory, unconsulted (obs 4).
**Artifacts:** ai-kit `50e7419` (5 files); `skills/review-implementation/`; packet `~/.claude/improvements/2026-07-23/` (run-2 section, P03 applied); obs `~/.claude/observations/2026-07-23-batched-review-topology.md`; new memory `review-then-commit-workflow`.

---

## [2026-07-23] — /close repo-memory redesign + focused audit + first live 2c run

**Summary:** Redesigned /close around a 4th persistence layer (repo-scoped `docs/rules/` indexed from AGENTS.md; SESSION_LOG slimmed to continuation-only — this entry is the first slim one), ran a focused /audit-skills (2 findings, both applied), and bootstrapped ai-kit's own AGENTS.md + docs/rules/ as the inaugural 2c run.
**Next:** exercise 2c in a non-kit repo's /close (validates the layer outside its birthplace); backlog 26 (close-tasks roll-up slim? repo-rule harvesting?) waits on ≥3 slim-entry sessions; review adr-0001 (UNREVIEWED) via /adr-first. (Carried from 07-19: cc-looper AI-6 build session; vault ops.)
**Blockers:** none
**Didn't work:** node js-yaml from the ai-kit cwd (no node_modules — run from `~`; now a docs/rules/ rule, and the observation notes this fact sat unread in the 07-07 entry below — the redesign's own proof point)
**Artifacts:** ai-kit `5c39acd` (skill edits) + this session's docs commit; claude-home `e1cea84` + packet `~/.claude/improvements/2026-07-23/`; `docs/rules/skill-authoring.md`; `AGENTS.md`; adr-0001 `~/.claude/ownership/close-repo-memory/` (UNREVIEWED)

---

## [2026-07-19] — /improve review (8/8 applied) + orchestrate/walkthrough skills + AI-6 backtest CLEARED

**Summary:** Full /improve cycle over the 07-05→07-19 window (179 obs entries / 67 files via 4-agent fan-out extraction + a user-directed vault scan of second_brain/mktool_kb) — 8 proposals staged, all approved and applied, two new skills built, and the AI-6 backtest run and cleared (build approved).
**Done:**
- First prediction-discipline cycle closed: all 12 prior proposals fingerprint-verified shipped; P09 met on first opportunity (caught P07's orchestrator-half miss → revised as P01, not silently persisted); P12 missed (scoped-negative class recurred ≥5×) → enforced into skills (P03/P06), CLAUDE.md untouched.
- Applied: P01 compile-kb (cadence graduation + dispatch hints-to-verify + orchestrator output under its own gates + contract patches); P02 qa-gates (gate scope from working-tree diff, TRX, hash-stamped gates, canonical obs schema); P03 analysis/techspecs caller closure; P04 balanced-tasks tasks-as-spec escape hatch + independent ACs; P05 kb-update residual gaps (mktool_kb `.agents/` copies); P06 absence-claim protocol (bug-investigation + document-terraform); P07 destructive-hook prose fix (execution-verified 8/8 payloads); P08 improve family-batched rounds.
- Built `skills/orchestrate` (multi-provider fan-out playbook: Opus workers on Claude Code/Cursor; Codex inherits session model per open issue) + `skills/walkthrough` (one-item-per-turn disposition) — strict-YAML clean, 10/10 fresh-context trigger simulation, Codex-synced (75 exposed, 0 issues).
- AI-6 backtest over 31 historical QA artifacts: 5/10 real no-gos (50%) convert in one distilled-findings fix cycle → clears the ≥⅓ bar; report at `cc-looper/specs/ai6-backtest-2026-07-19.md` (uncommitted); build approved with eligibility-gate + env-preflight conditions.
- Bookkeeping: 67 obs files annotated, 41 archived; `last-review.txt` → 2026-07-19; commits pushed — ai-kit `81662cc`, mktool_kb `4121299`, claude-home `fc80232`.
**Decisions:** revise-don't-revert for P07 (its subagent half demonstrably works); enforcement-over-wording for both repeat-violated rules (qa-gates Gate-1, scoped-negative); AI-6 backtest-before-build (user call) — backtest then cleared it; orchestrate must be multi-provider (user requirement).
**Didn't work:** Edit through symlinked skill paths (ENOENT on tmp-rename) — canonical-path recipe recorded in `cc-looper-symlink-topology` memory.
**Next:** fresh session `/audit-skills` (2 new skills authored — user queued it); cc-looper AI-6 build session (check `/goal` repricing first; doubles as the loop run resolving frozen P01–P05/P10/P11 predictions); user-run keep-two prune (2026-07-05 + 2026-07-07 dirs); vault ops (2 UNREVIEWED compile-kb ADRs → /adr-first, sha256 reconciliation, stale "7 cycles" figure, teach Lesson 03).
**Blockers:** none
**Artifacts:** packet `~/.claude/improvements/2026-07-19/` (REVIEW + 8 proposals + MARK); `cc-looper/specs/ai6-backtest-2026-07-19.md`; obs `~/.claude/observations/2026-07-19-improve-run-close.md`; memories updated: loop-engineering-research, cc-looper-symlink-topology, skill-frontmatter-strict-yaml + MEMORY.md index.

## [2026-07-10] — Codex CLI linked on this machine (adapter deployed + verified, personal layer composed)

**Summary:** Codex CLI v0.144.1 was installed on this machine; deployed the existing `adapters/codex` sync (65 entries, 0 issues), composed the global `AGENTS.md` with a private personal-conventions layer, live-verified discovery + explicit `$name` resolution, and closed two long-standing [verify] items across the docs.

**Done:**
- `sync.ps1` applied: 38 junctioned skills + 17 agent skills + 10 command skills into `~/.codex/skills` (advisory validator still skipped — host Python broken, kit-independent).
- `C:\ai-kit` trusted in `~/.codex/config.toml`; `~/.codex/AGENTS.md` composed as kit block + private personal block between BEGIN/END markers (personal source `~/.codex/AGENTS.personal.md`, a Codex-adapted CLAUDE.md mirror; 11.3 KB of the 32 KiB cap).
- Live-verified on the binary: junctioned skills visible in-session (`qa-gates`); generated implicit-off skills correctly invisible until explicit `$name` mention (confirmed via `$bug-investigation-agent`, read-only sandbox, zero shell escapes); personal block live (Codex answered the confidence-threshold and risky-commands trap questions from instructions alone).
- [verify] items resolved and propagated: global `AGENTS.md` read-location = `~/.codex/AGENTS.md` (`AGENTS.override.md` precedence), `project_doc_max_bytes` = 32 KiB → assessment 2026-07-10 addendum + 4 in-body enumerations, README header/Usage/open-items, kit AGENTS.md header, sync.ps1 + sync.sh printed hints (incl. removing the always-failing `mklink /J`-on-a-file suggestion).
- Feature flags re-checked at 0.144.1: `multi_agent` stable/on, `enable_fanout`/`multi_agent_v2` still off — §3a decision holds unchanged.

**Decisions:** `~/.codex/AGENTS.md` is a composed **copy** with markers, not a link — file-symlink needs elevation/Developer Mode, hardlink silently detaches on the next `git checkout`; the personal block gets its own private source file so a kit refresh can never clobber it (rejected: symlink, hardlink, plain single-source copy).

**Didn't work:** backgrounded `codex exec` with open piped stdin (hangs forever on "Reading additional input from stdin…" — always close stdin: `< NUL` / `</dev/null`); first hang misdiagnosed as folder trust (real issue, wrong root cause); `$bug-…` inside a double-quoted PowerShell string (interpolated to empty — the probe passed for the wrong reason; single-quote outer strings); `codex skills list` (no such subcommand).

**Next:** pilot one family end-to-end from Codex (e.g. `$full-bug-fix-workflow` on a small bug) — that exercises the remaining [verify] items (`$ARGUMENTS` arg-binding, `agents.max_depth` counting) and observes C-mode `review-artifact` behaviour (assessment §8 step 4). User: skim `~/.codex/AGENTS.personal.md` for adaptation fidelity.

**Blockers:** none.

**Artifacts:** ai-kit diff (5 files: `docs/codex-portability-assessment.md`, `adapters/codex/{README.md,AGENTS.md,sync.ps1,sync.sh}`); observations `~/.claude/observations/2026-07-10-codex-machine-link.md`; memory `codex-adapter-synced-this-machine`; deployed: `~/.codex/{skills,AGENTS.md,AGENTS.personal.md,config.toml}`.

---

## [2026-07-07] — Loop-primitive adapter layer (/triage + loop-recipes) + full /audit-skills run

**Summary:** Assessed ai-kit against the Claude Code loop-engineering guide (X post 2026-07-06, captured in-repo) — the quality/usage advice was already implemented by the 2026-07-05 run; the real gap was zero native-primitive (/goal, /loop, /schedule) integration. Built the thin adapter layer, then ran a full 11-check /audit-skills: 3 proposals staged and applied same-session.

**Done:**
- Assessment: 7 guide points already validated in-kit; gap grep-confirmed. Highest-leverage insight: pending AI-6 (bounded fix cycle) can likely be repriced as a native `/goal` wrapper over qa-loop's pinned `Recommendation:` line instead of cc-looper runner work.
- `/triage`: loop-primitive route added (Phase-1 signal row + routing sub-table + clarifying question); description 627→783, strict-YAML-verified.
- `docs/loop-recipes.md` (new): 4 frames, the guide's 3-question rubric, hard constraints (cloud `/schedule` can't reach `~/.claude`/local vaults; `/goal` availability unverified), 6 recipes incl. headless /improve Phases-1–4 staging and the AI-6 `/goal` pointer.
- `/audit-skills` full run (46 skills / 38 commands / 17 agents; deterministic checks scripted via node+js-yaml): P01 quoted the only 2 strict-YAML-failing frontmatters (both in commands/ — the 2026-06-04 sweep never covered commands); P02 normalized `{feature}`→`{feature_name}` (contract doc's parked cleanup decision, now closed with an expected-non-drift list); P03 fixed audit-skills' own spec drift (agent `tools`/`color`, 10→11 checks, command-wraps-skill pairs ≠ collisions). Backlog 15→18 (+5 new incl. the never-written 05-31 notes; 2 closed; 4 updated with new data); keep-two prune of 7 dated dirs executed.

**Decisions:** Loop-primitive names confined to exactly two surfaces (triage routing table + docs/loop-recipes.md) because work skills must stay runner-agnostic — their deterministic pinned-line criteria are the loop-legible contract (prefer-decoupled-designs, Codex portability, research-preview churn); rejected: primitive mentions in loop-variant skill bodies. P02: normalize rather than bless `{feature}` (blessing would re-open the one-token-per-family rule the contract enforces).

**Didn't work:** NODE_PATH-based js-yaml resolution on Windows node (cwd-based resolution works); safety hook false-positived on the word "rm" inside a commit message body (reworded — observation logged for a hook-regex refinement).

**Next:** verify `/goal` exists in the installed CLI (+ `claude -p` compat) — it gates loop-recipes recipe 5 and the triage `/goal` row; then append the repricing note to AI-6 in the action-items doc. For a future /improve walk: the `references/`-split pattern decision (backlog 14/22/23) and the description-budget house style (backlog 16, 5 items hang on it).

**Blockers:** none.

**Artifacts:** ai-kit `ad5bd84` (loop work) + `8818806` (audit P01–P03); claude-home `a418adf` (packet + backlog); `~/.claude/improvements/2026-07-07/` (REVIEW + 3 proposals); observations `2026-07-07-loop-adapter-audit.md`; memories `loop-engineering-research` + `cc-looper-symlink-topology` updated.

---

## [2026-07-05] — /improve review 2026-07-05 (12 proposals applied across 3 repos)

**Summary:** Ran `/improve` over the 2026-06-26→07-05 window (45 observations / 19 files) plus the research action-items doc as user-directed input. Staged 12 proposals (7 research-driven: AI-1..4 + AI-7/8/9; 5 observation-driven), all 12 approved and applied, committed + pushed across cc-looper / ai-kit / claude-home.

**Done:**
- Loop skills (cc-looper via symlinks): baseline gate at task start (P01), reviewer push-to-continue pass (P02), distilled findings contract — raw log dumps forbidden (P03), attempted-and-failed ledger on Paused/Blocked + resume-reads-it-first (P04), qa-loop-docs environment-readiness preflight + git-root path convention + codex-review target fix (P05).
- ai-kit: docs-tasks-creator .NET test-project filter + zero-handler guard (P06); compile-kb dispatch conventions / full-tree sweep / PDF fallback / grouped-sha rule (P07); improve self-edits incl. mandatory codename self-grep gate (P08) + falsifiable-predictions discipline (P09) + run-metrics waste column (P10); model-assignments loop-role structured-output floor (P11).
- claude-home: CLAUDE.md scoped-probe-negative verification bullet (P12); 19 obs files annotated via one scripted footer pass; packet at `~/.claude/improvements/2026-07-05/`.

**Decisions:** The window's N=5 qa-loop-docs false no-gos were diagnosed as recurrence-after-application of the 2026-06-26 P04 provenance gate (correct fix, assumed a git-trusted spawn) → **refine (P05), not revert** — the prior-shipped fingerprint check made that distinction. AI-5/6 (cc-looper runner): **backtest-first** — AI-6's ≥1/3-conversion prediction gets judged against historical `_qa.md` no-gos before any build (rejected: build directly). deep-research is harness-bundled → model-tiering enforced via memory + the P11 floor policy, not a skill edit. Parallel-implement convention: formalize next cycle (2nd clean confirmation logged); /harvest-source: not yet (1×).

**Didn't work:** —

**Next:** user runs the keep-two prune (2nd emission — command in `improvements/2026-07-05/REVIEW.md`); AI-6 backtest in a session with the work repos; next `/improve` opens with the predictions-first check of all 12 applied predictions (P09 live).

**Blockers:** none.

**Artifacts:** `~/.claude/improvements/2026-07-05/` (REVIEW + 12 proposals + MARK); commits cc-looper `e8352f9`, ai-kit `f5f65dc`, claude-home `81d0014` (all pushed).

---

## [2026-07-05] — COMPILOT study + loop-engineering deep research → /improve-ready action items

**Summary:** Read the COMPILOT study end-to-end (PACT 2025, arXiv 2511.00592 — Nov **2025**), mapped it against ai-kit's loop assets, ran a 104-agent deep-research sweep of the Dec 2025–Jul 2026 loop-engineering literature (14 findings survived 3-vote adversarial verification; nobody cites COMPILOT — 6 groups converged independently), and consolidated everything into two repo-root docs including 14 falsifiable action items staged for a `/improve` run.

**Done:**
- Extracted + read the full 19pp PDF (PyMuPDF — Read can't render PDFs here, poppler absent); Explore-agent repo map; spot-verified the load-bearing gaps in `implement-task-loop` (no task-start baseline) and `qa-loop` (report-only, no fix cycle).
- Delivered the two-part analysis: 10 transferable lessons + do-now/soon/someday/not-do vs ai-kit assets (several design bets validated: pinned-line contracts, mechanical gates, forced analysis, 230K+fresh-resume, checkpoint cadence, tasks-doc-as-spec-initializer per Anthropic).
- deep-research workflow (5 angles → 15 sources → 25 claims → 3-vote adversarial verify): survived two session-limit crashes via `resumeFromRunId` (89/104 agents cached on final pass); retiered verify voters to Opus 4.8 mid-run, synthesis kept on Fable (user directive).
- Wrote `agentic_auto_scheduling_experimental_study.md` (consolidated study + 2026 research reference) and `agentic_auto_scheduling_experimental_study_research_action_items.md` (AI-1..AI-14 with evidence tags, per-item confidence, falsifiable predictions per the AHE discipline; refuted claims quarantined). Public-hygiene grep clean.

**Decisions:** Restart policy = restart-with-**carryover** (fresh session seeded with best prior artifact + attempted-failed ledger) because Magellan's plateau case refuted blank-slate AND grinding (rejected: my initial restart-fresh spec). Iterate-with-feedback before parallel sampling under fixed budget (ACCLAIM) — demotes best-of-K further. Findings contracts must forbid raw log dumps (KernelPro: raw feedback *worse than none*). Action-items doc practices AI-9's own predict→verify→revert format. Workflow fan-outs on Opus, Fable reserved for synthesis (limits economics).

**Didn't work:** — (journal label-based extraction of the synthesize result — keys are hashed; structure-based scan worked immediately).

**Next:** run `/improve` pointed at `agentic_auto_scheduling_experimental_study_research_action_items.md` + observations (AI-1..AI-4 = do-now skill edits; AI-9 = /improve's own falsifiable-prediction upgrade). cc-looper items AI-5/AI-6 queue behind it, next to close-tasks Part B.

**Blockers:** none.

**Artifacts:** the two repo-root docs; memories `loop-engineering-research` / `workflow-model-tiering` / `pdf-reading-pymupdf`; observations `2026-07-05-loop-engineering-research.md`; sources: arXiv 2511.00592, 2601.21096 (Magellan), 2603.10085 (KernelSkill), 2603.20075 (llvm-autofix), 2604.04238 (ACCLAIM), 2604.25850 (AHE), 2606.20373 (AutoPass), 2606.26453 (KernelPro), Anthropic effective-harnesses post.

---

## [2026-06-26] — /improve review 2026-06-26 (6 proposals applied across 3 repos)

**Summary:** Ran the periodic `/improve` review over the densest window on record (~240 observations / ~104 files, 2026-06-05→06-26). Distilled **6 proposals**, applied all 6 (user-approved one batch), verified, and committed+pushed across ai-kit / cc-looper / claude-home; scrubbed the packet to generic labels and refined a memory.

**Done:**
- Mined the window via **6 parallel extraction subagents** (the `grep -A 3` dump was unusable — Read truncates long friction lines). Built `~/.claude/improvements/2026-06-26/` (REVIEW + 6 proposals + MARK).
- Applied all 6: **P01** `review-artifact` subagent VERIFIED/SUSPECTED + negative-search contract · **P02** `qa-gates` Gate 1 compiled≠executed / name-the-tiers · **P03** `integration-techspec` stable-anchor citations · **P04** `qa-loop-docs` produced-doc provenance+uniqueness + `docs-tasks-creator` `_fullstack/` namespacing · **P05** destructive-hook FP trim (`--rm` flag + read-only-git skip) · **P06** `integration-techspec`/`-tasks` 3-way downshift.
- **Verified P05 by execution** (9/9 hook tests: 3 FPs now allowed, 6 still denied); **confirmed 2026-06-05 P01–P04 already shipped** (fingerprints in live skills) → recurrences are broader gaps, not regressions.
- Annotated 51 backing obs (one consolidated per-file footer via PowerShell); bumped `last-review.txt`→2026-06-26.
- Scrubbed REVIEW.md + proposal-02 of work-project codenames → generic labels; amended the claude-home commit.
- Refined memory `improve-packet-generic-repo-labels` (secret-scan blocklist is a specific 6-name set, scans full staged content → codenames pass; the rule is hygiene, not hook-enforced).

**Decisions:** 6 proposals from 240 obs is distillation not churn (≈2.5%; last run 5/95). P01 framed as the *subagent-contract* successor to the already-shipped 2026-06-05 P03 orchestrator re-grounding (the pattern recurs mostly OUTSIDE review-artifact). P05 kept conservative (only `--rm` + read-only-git; SQL-temp + filename-substring left to skill-side) because the hook enforces an explicit user rule. compile-kb cluster held as a candidate (active-dev). All 6 deliberately avoid CLAUDE.md (now **144 lines**, past the degradation zone).

**Didn't work:** `grep -A 3` over all June obs (209KB persisted; Read rendered long friction lines as `[Omitted long context line]`) → abandoned for the subagent fan-out. Resolving cc-looper via the SKILL.md *file*'s `.LinkTarget` (empty — qa-loop-docs is a directory **junction**; the *dir*'s `.Target` resolves it).

**Next:** 8 candidates await a future call (compile-kb digest-collision/Codex caveats once that build settles · &&-chain expect-zero `grep -c` · tasks-doc 3-source Done-update · close/close-tasks digest accuracy · qa-gates local-only mode · parallel-implement-task disjointness · integration-investigation skill · memory inference-marking). Recommended standalone: a **CLAUDE.md consolidation pass** (144 lines — e.g. compress the 38-line Score-Confidence block).

**Blockers:** none.

**Artifacts:** `~/.claude/improvements/2026-06-26/`; commits ai-kit `44b22a5`, cc-looper `511226b` (rebased onto remote `fc2f658`), claude-home `76bbcec` (+ user's keep-two prune `26fd6b1`); memory `improve-packet-generic-repo-labels.md`; observation `2026-06-26-improve-close.md`.

---

## [2026-06-19] — Reconcile Codex personal-conventions mirror with CLAUDE.md (+ Output-formatting rule)

**Summary:** Added a calibrated `Output formatting` rule to `~/.claude/CLAUDE.md` (lean scannable — tables/lists where they map to content, prose for connected argument, diagrams sparingly; explicitly NOT maximize-visuals), then full-reconciled the private `~/.codex/AGENTS.md` mirror, which had silently drifted 5 sections from CLAUDE.md over ~1 month. Confirmed global `~/.codex/AGENTS.md` read is now active at codex-cli 0.141.0 (was dormant @0.130.0).

**Done:**
- `~/.claude/CLAUDE.md`: new `## Output formatting` section (content→format mapping + an explicit anti-over-formatting clause). Token analysis given to user: lists ↓, tables ≈, diagrams ↑ → net neutral/slightly-down for "less prose + more lists."
- Confirmed CLAUDE.md does NOT auto-sync to Codex/Cursor — `adapters/{codex,cursor}/sync.*` handle skills+agents only; personal conventions are a manual private-`AGENTS.md` "user layer" by design (avoid publishing prefs / mutating `$HOME`).
- Confirmed `.agents/skills/` is read by Codex (reliably) and Cursor (with open CLI bugs — `~/.agents/skills` not loaded; #160426-class). It's a repo-scoped SKILLS dir, not an instructions location — conventions belong in `AGENTS.md`, not under `.agents/`.
- Full-reconciled `~/.codex/AGENTS.md` to current CLAUDE.md: +Output-formatting, +Proposal-docs-vs-analysis-docs, +2 Reading-before-editing bullets, +2 Verification bullets, +Parallel-tool-batching (flagged as a Claude-harness behavior to verify, NOT asserted). Refreshed the stale header placement note. 14 sections, CLAUDE.md order, include-point preserved (grep-verified).
- Public `adapters/codex/AGENTS.md` (kit-mechanics layer) deliberately untouched.
- Updated memory `codex-portability` + `MEMORY.md` index (retired the "dormant@0.130.0" claim).

**Decisions:** Full reconciliation over formatting-only (user chose — mirror was stale on more than the new rule). Parallel-tool-batching added but flagged-not-asserted because the "non-zero exit cancels sibling calls" failure mode is a Claude Code harness behavior, unverified on Codex's tool model (rejected: blind-copy verbatim). Conventions go to the PRIVATE `~/.codex/AGENTS.md`, never the public repo file (README + `ai-kit-is-public` contract).

**Didn't work:** — (linear session; no dead ends).

**Next:** When back on Cursor (in WSL), apply the same reconciliation to its private `AGENTS.md` (deferred — not on this machine). Optional: confirm global-read live on the Codex binary (current claim is doc-sourced, not probed) — open a Codex session and check the conventions surface. Standing item (unrelated): Codex §8 behavioral pilot.

**Blockers:** none.

**Artifacts:** `~/.claude/CLAUDE.md`; `~/.codex/AGENTS.md` (machine-local, not version-controlled); memory `codex-portability.md` + `MEMORY.md`; observation `2026-06-19-codex-agents-mirror-sync.md`.

---

## [2026-06-18] — Codex adapter: map doc-generation commands (update-workflow-docs + document-workflow)

**Summary:** `update-workflow-docs` wasn't appearing as a Codex skill. Root cause: it's a command with no backing junctioned skill, and the adapter's command-generation allowlist was scoped to the feature-dev/bugfix/incident families only. Generalized the rule, added the doc-gen family, propagated across all 4 adapter files, applied + verified on disk.

**Done:**
- Diagnosed: a command reaches Codex only two ways — (a) its same-named skill is junctioned (thin shim, e.g. `document-terraform`), or (b) it's in `sync.ps1`'s generation allowlist (`$OrchCmds`). `update-workflow-docs` has no skill at all and wasn't in the list → invisible in Codex with no error. Sibling `document-workflow` too (only its stripped `-loop` fork is a junctioned skill).
- Generalized the allowlist rule from "5 orchestrators + 3 executors = 8" to **"any command whose capability no junctioned skill owns"** → now **10 generated command skills** (+`document-workflow`, +`update-workflow-docs`).
- Propagated across all 4 adapter files: `sync.ps1` (`$OrchCmds`→`$GenCmds`, Kind `orch`→`cmd`, generic `default_prompt`, summary line), `sync.sh` (POSIX parity), `README.md` (counts + commands-table row + 4 framing refs), `AGENTS.md` (section renamed "Generated command skills" + body).
- Verified: both scripts parse-checked; `-WhatIf` clean; `sync.ps1` applied (`issues: 0`); on-disk inspection of `~/.codex/skills/update-workflow-docs/` (SKILL.md frontmatter, `openai.yaml` `allow_implicit_invocation:false`, marker). Sync was additive — no `-Prune`/`-Force`.
- Updated memory `codex-portability` + `MEMORY.md` index (the stale "8 orchestrator/executor" claim).

**Decisions:** Reframe the allowlist as a general predicate (rejected: a separate parallel `$StandaloneCmds` list — user chose the single generalized rule). Fix both siblings, not just the one asked about (rejected: scope to `update-workflow-docs` only — same one-line root cause). Did NOT touch canonical `commands/*.md` (Category-1 boundary held).

**Didn't work:** First `replace_all 'orch'→'cmd'` used asymmetric whitespace and produced `'cmd''error'` (one PowerShell escaped-quote string, not two args) — silent, caught by re-reading. `bash -n` via the PowerShell tool mangled the backslash path (exit 127); used the Bash tool instead.

**Next:** Commit the 4 adapter files (was pending user approval at session end). Restart Codex to pick up `$update-workflow-docs` / `$document-workflow`. (Pre-existing untracked WIP — `commands/tasks-loop.md` + 6 loop skills — is NOT this session's; left alone.)

**Blockers:** none. The live Codex validator stayed skipped (pre-existing `C:\Python311` segfault, documented) — generation/junctions unaffected; §8 behavioral pilot remains the real Codex run.

**Artifacts:** `adapters/codex/{sync.ps1,sync.sh,README.md,AGENTS.md}`; memory `codex-portability.md`; observations `2026-06-18-codex-doc-cmd-mapping.md`.

---

## [2026-06-04] — Fix 5 SKILL.md frontmatters that broke Codex's strict YAML parser

**Summary:** Codex 0.136.0 was skipping 5 skills with `mapping values are not allowed in this context` errors. Root cause: unquoted `description:` scalars containing `: ` (colon-space). Quoted all 5 (zero wording change); verified with a strict parser.

**Done:**
- Diagnosed: each flagged file's `description:` was an unquoted YAML plain scalar containing `: ` → ambiguous with a key/value mapping under a strict parser (Codex), but tolerated by Claude Code's lenient frontmatter parser (which is why it never broke Claude-side).
- Fixed by double-quoting the `description` value in close / debug-first / onboard-me / qa-gates / verify-task (1 line each); escaped debug-first's internal `"Question for AI"`. No wording changed.
- Verified: regex sweep of **every** `SKILL.md` → 0 remaining unquoted-`: ` descriptions (these 5 were the only offenders); strict **js-yaml** parse of all 5 → `ALL_VALID`.
- No Codex re-sync needed — the `adapters/codex/` junctions read the canonical files in place; content edit, not add/remove.

**Decisions:** quote the value rather than rephrase the `: ` to em-dashes — preserves the user's exact authored wording (rejected rephrasing = silently alters human-facing description text). Captured as memory `skill-frontmatter-strict-yaml`.

**Didn't work:** PyYAML for verification — `import yaml` segfaults (`0xC0000005`) under both git-bash Python and Windows Python 3.11.0a7 alpha. Fell back to Node 22 + temp `npm install js-yaml`; `NODE_PATH` wasn't honored, so the check had to run from inside the temp dir for local module resolution.

**Next:** optional — add a strict-YAML frontmatter validity gate to `/audit-skills` (and the quote-the-colon rule to `/write-skills`) so an unquoted `: ` can't reach Codex again. Standing item (unrelated to this session): own compile-kb ADR-0002 / finish the ai_vault re-run.

**Blockers:** none. Ground-truth confirmation is a `codex` relaunch — the 5 warnings should be gone.

**Artifacts:** 5 × `skills/*/SKILL.md`; memory `skill-frontmatter-strict-yaml.md`; observations `2026-06-04-codex-skill-yaml.md`.

---

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
