---
name: close-tasks
description: "Closes a manual, multi-session, or headless tasks-doc run by reconstructing its results from task, verification, QA, review, runner, and Git artifacts. Use at a real run stopping point when per-session close did not cover that execution. Accepts a tasks-doc path; live-session wrap-up belongs to close."
---

# Close-tasks — end-of-tasks-doc closeout

You are closing out a **tasks-doc's implementation run**, not a session. The run may have spanned
2–3 sessions, been driven by hand or by cc-looper headless, and the conversation context of the
earlier sessions is gone. So this skill does **not** retrospect on live context the way the close skill
does — it **reconstructs the run from durable artifacts** and harvests the improvement signal that
would otherwise be stranded (the cc-looper / multi-session blind spot in the `close → improve skill`
pipeline).

**Consumer-agnostic.** It reads artifacts, so it does not care whether the tasks were implemented
manually (the implement-task skill), by cc-looper (`implement-task-loop`), or a mix.

**It is lossier than the close skill for *narrative* friction** ("this cost me 20 min because X" from a
cleared session is gone) — and that is an accepted trade. What survives is **structured** friction:
gate fails, accept-with-reason lines, `Status: Paused` notes, retry counts, doc-drift findings —
all of which the implement / verify / qa machinery writes into artifacts. Reconstruct from those;
don't invent the narrative you can't see.

Four phases. Move through them in order; ask before the git step. Resolve recorder/store/schema and
run identity from [the feedback contract](references/shared/feedback.md), and content identities
from [the change-evidence contract](references/shared/change-evidence.md). This skill reuses the
close skill's SESSION_LOG placement/archive rules and cross-machine sync routing. Its roll-up entry
is deliberately richer than the close skill's slim continuation entry (see 3c).

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| `tasks_doc_path` | yes | The tasks-doc whose run is being closed. Ask the user if not given/discoverable. |
| `since` | no | Explicit historical boundary. A prior verified harvest receipt is preferred; a commit/date alone is supporting context, not freshness proof. |

---

## Phase 1 — Resolve scope & gather artifacts

1. **Resolve the prior harvest record.** Inspect versioned `feedback-harvest` evidence blocks in
   `tasks_doc_path`. Recompute their sorted artifact manifests using the change-evidence contract.
   A passed receipt with matching current bytes means no new harvest for that covered evidence.
   Failed, unavailable, or incomplete records cannot suppress unfinished persistence; resume using
   the matching harvest/execution ID and existing record IDs. Changed task/QA/review/
   digest/runner bytes create a delta even when HEAD is unchanged. A legacy
   `<!-- close-tasks: harvested through <sha> @ <date> -->` line is readable historical context but
   unverified; it cannot establish freshness or suppress changed artifact content.

2. **Detect what actually ran without adopting nearby state.** Discover runner-state candidates
   under the repository's runner artifact area; do not assume one fixed `.cc-loop/state.json` path.
   Accept a state record only when its canonical `tasksPath` identifies `tasks_doc_path`, its
   timestamps/window are compatible with the target run, and its recorded action/task IDs agree
   with the task artifact. Treat its map-time tasks-document hash as lineage, not the final mutable
   task-content identity. If zero or several candidates survive, label runner attribution
   `unverified` and use task/QA evidence without claiming runner ownership.

   A verified state record supplies `action`, `mode`, task `terminalStatus`/`attempt`, and QA/
   checkpoint records. Map those to the actual workflow names. Without verified state, use explicit
   producer metadata in task/QA records; otherwise label the workflow `inferred` rather than silently
   defaulting to manual execution.

3. **If a runner close digest is present** — `<dirname(tasks_doc_path)>/<base>_close.md`
   (the in-repo digest cc-looper's headless `close-tasks-loop` sibling writes; see Notes →
   "The in-repo digest contract") — **prefer it**: it already holds structured friction the
   headless run extracted at the time, with live context this skill no longer has. Verify its
   target/window against the bound run and include its current bytes in the artifact
   manifest. Distill it directly only for the evidence it explicitly covers. Missing provenance,
   stale source locators, or a mismatched window make it a candidate input that must be checked
   against raw artifacts, not authoritative coverage.

4. **Gather the raw artifacts** (the reconstruction inputs, for the window with no digest):
   - `tasks_doc_path` itself — per-task `Status:`, completion notes, and any
     `## Verify` / `## Review` / `## QA` blocks inside task sections; the tasks-overview table.
   - Sibling artifacts in the prefix folder — `*_qa.md`, `*_checkpoint-*_review.md`,
     and the techspec/analysis (for AC cross-reference context only).
   - The verified runner state + its bound run artifacts — best-effort; never fatal if absent.
   - `git log --oneline <since>..HEAD` and `git diff --stat <since>..HEAD` (read-only; safe) for
     each repo declared in the tasks-doc header (or CWD repo if none declared).
   - Build a sorted content manifest for every consumed artifact and relevant section. Include
     consumed Verify/QA/review evidence; exclude only this harvest's own start/receipt regions,
     naming their exact IDs under the change-evidence contract. This manifest,
     not the Git window, is the harvest freshness boundary.

---

## Phase 2 — Reconstruct friction & triage

From the gathered artifacts, derive the run's improvement signal. Map artifact evidence → friction,
**evidence-cited to `file:line` or a state.json field** (so the improve skill can weight artifact-
reconstructed signal honestly against live-context signal):

| Artifact evidence | → friction (tag) |
|-------------------|------------------|
| `## Verify` / `_qa.md` gate `FAIL` with `accepted: <reason>` | the accepted-debt reason, tagged per the gate (`line_budget_overrun`, `sdk_version_drift`, `doc_drift`, …) |
| Unresolved gate `FAIL` in `_qa.md` (Recommendation: no-go) | `buggy_code` / `wrong_approach` per the failing gate |
| `Status: Paused` + blocker note | `misunderstood_request` / capability gap — quote the blocker |
| Verified runner state `attempt > 1` on a task | retry churn — quote terminalStatus + attempt count |
| `terminalStatus !== "Done"` at run end | partial outcome — which task, why (from completion notes) |
| Doc-drift finding in `_qa.md` Gate 4 | `doc_drift` |
| Checkpoint review `abort` / `fix-then-proceed` | quote the recommendation + the blocking finding |

Then **categorize** each item exactly as the close skill's Phase 1 does — (a) → configured memory
store (user-scoped or cross-repo durable), (b) → observations, (c) → repo memory, (d) → SESSION_LOG
roll-up, (e) → chat only. Apply the close skill's ADR gate and **don't-manufacture** rule.

Resolve the lifecycle boundary before describing completion. Report repository tasks and
deploy/live tasks separately using the task lifecycle metadata from the change-evidence contract.
Repository GO cannot imply deployment or live rehearsal. Pending operational work remains visible
in `Next` with its evidence unmet. A clean repository run yields zero observations; it may still
have pending operational tasks.

---

## Phase 3 — Persist

Before writing any store or roll-up, persist a `started` marker with the execution ID and a
unique `harvest_id` under the feedback contract. Resume only a matching boundary, checking
stable record IDs before appends. Mark that start complete only after the enabled writes validate
and the harvest receipt persists; retain failed or interrupted state visibly.

### 3a — Observations (the point of this skill)

If an observation recorder is configured, `close-tasks` owns this composed harvest. Write each (b)
item to that store using the public feedback schema plus any compatible store-local additions. The
preferred `~/.agents` profile writes under `~/.agents/observations/`; a legacy store remains usable
when explicitly configured. Per observation:

- assign stable `record_id`, `recorded_at`, the tasks-run `execution_id`, `producer: close-tasks`,
  and `recorder: close-tasks`;
- `skill_or_workflow` is the verified or explicitly `inferred` value from Phase 1 step 2;
- set `evidence_kind: artifact-reconstructed` and bind `evidence_identity` to the current manifest;
- cite the artifact evidence (`file:line` / verified runner-state field) in `friction_observed` and
  state that it is reconstructed, not lived;
- use exactly one public baseline or configured-extension tag at the end of that field.
- **Run-metrics block (loop/multi-session runs):** append one fenced block at the top of the
  observations file, reconstructed from artifacts:

      run-metrics:
        tasks: N done / M total
        attempts-per-task: <mean; list any task with attempt > 1>   (state.json `attempt`)
        gate-failures: <count + gate ids>                            (_qa.md / ## Verify blocks)
        findings-per-checkpoint: <count per checkpoint review>       (_checkpoint-*_review.md)
        pauses-blocks: <count + one-line causes>                     (Status: Paused/Blocked notes)

  Two conventions are binding: **an infra-crashed attempt counts as a failed attempt (r=0) — never
  silently dropped from the counts**; and any before/after claim about a loop-skill/config change
  needs k≥2 runs — a single run is an anecdote, mark it as such.

Run metrics describe the verified execution; they are not invocation counts. Deduplicate by stable
observation ID and evidence identity before appending. Then run the close skill's tag validator
against the public contract or configured compatible tag document; use its verified empty-inventory
branch for zero observations. Write the harvest receipt only
after this check passes. If recording is disabled, write no observations and report
`observations: disabled`; if enabled but unavailable/invalid, the harvest record cannot claim PASS.
**Don't manufacture** — see Phase 2.

### 3b — User/cross-repo memory (rare for an implementation run)

For each (a) item, use the configured memory store and the feedback contract's scope and ownership
rules. Check for an existing record first. If no memory recorder is configured, report the candidate
without inventing a path. Implementation runs rarely produce durable rules — usually zero here.

### 3c — SESSION_LOG.md roll-up entry

Find the git root (`git rev-parse --show-toplevel`; fall back to `~/SESSION_LOG.md`). **Prepend**
one entry for the **whole tasks-doc run** (not per session/task). The roll-up keeps
`Done:`/`Decisions:` — deliberately richer than the close skill's slim continuation entry, because a
multi-session run's net delivery and completion-note decisions aren't recoverable from any single
session's context:

```
## [YYYY-MM-DD] — <tasks-doc name>: run closeout (N/M repository tasks done across K sessions)

**Summary:** 1–2 sentences — what this run delivered and where it landed.
**Done:** <the net of completed tasks — roll up, don't transcribe per-task notes>
**Decisions:** <only load-bearing decisions surfaced in completion notes> X because Y.
**Didn't work:** <Paused/abandoned/aborted items — or "—">
**Next:** <unfinished repository tasks and separate deploy/live work — or "repository work complete; operations: none">
**Blockers:** <unresolved, needing a decision — or "none">
**Artifacts:** <tasks-doc, _qa.md, checkpoint reviews, key commits>
```

Apply the close skill's archive rule if SESSION_LOG is getting long (~30+ entries → oldest half to
`SESSION_LOG_ARCHIVE.md`).

### 3d — Append the content-bound harvest receipt

Append a versioned record in `tasks_doc_path`, outside the hashed task subject, using the
change-evidence markers:

```
<!-- evidence:begin <record_id> -->
feedback-harvest:
  schema_version: 1
  record_id: <record_id>
  record_kind: feedback-harvest
  recorded_at: <ISO-8601>
  execution_id: <verified runner id or generated tasks-run id>
  producer: close-tasks
  recorder: close-tasks
  project: <public-safe repository identity>
  source_record_ids: <consumed record IDs; identify legacy-derived inputs explicitly>
  evidence_identity: <identity of the sorted artifact manifest below>
  validation: passed | failed | unavailable
  verdict: passed | failed | unavailable
  supersedes: <prior-record-id or none>
  runner_attribution: verified | inferred | unavailable
  repository_status: <complete or incomplete>
  operational_status: <complete, pending, or none>
  artifact_manifest: <sorted scoped content identities>
  observation_ids: <stable ids, empty, or disabled>
  gaps: <none or explicit gaps/accepted reasons>
<!-- evidence:end <record_id> -->
```

Append a new record for a real delta; never rewrite prior evidence. Exclude only these exact evidence
regions when hashing the tasks subject, so the receipt does not invalidate itself. A repeat with a
matching manifest and no new evidence is a no-op. Keep any legacy commit marker as history.

---

## Phase 4 — Housekeeping & close

1. **Show the diff** — `git status --short` and `git diff --stat <since>..HEAD` (read-only).
2. **Ask before committing.** Conventional-Commits message
   (e.g. `chore: close-tasks roll-up for <doc> — N observations, receipt appended`). On approval
   `git add <files>` + `git commit`. Never `reset`/`clean`/`checkout --`/force-push. If the user
   declines, leave the tree as-is.
3. **Cross-machine sync routing** — identical to the close skill's Phase 3.3: feedback-store edits
   route to the configured maintenance tree (`~/.agents/` under the preferred profile); tasks-doc /
   `_qa.md` / source route to the target repo. One commit
   per repo, **ask before each commit and each push**, never auto-push, run the ai-kit secret-scan
   before pushing ai-kit.
4. **Print the close summary** — `observations: N|disabled · skill_or_workflow: <verified/inferred> ·
   memory: N|disabled · repo rules: N · repository: <status> · operations: <status> · SESSION_LOG:
   rolled up · harvest: <record_id> · commit: <hash or "skipped">`.

---

## When to use / When NOT

**Use** when a tasks-doc's implementation run is finished (or at a real stopping point) and the
per-session close did *not* run for the sessions that did the work — the canonical cases being
(a) a multi-session manual run where you deliberately skipped per-session close, and (b) a
cc-looper headless run (which has no interactive close at all).

**Don't use** for:
- A design / research / planning session with live context worth distilling — that's the close skill
  (context-distillation; this skill deliberately does not scan conversation).
- A run where you *did* run close every session — the observations are already captured; re-harvesting
  via artifacts may double-count. Compare execution/evidence IDs and do not stack recorders on the
  same execution window.
- A single trivial task — the close skill's don't-manufacture rule already covers it; nothing to harvest.

## Notes

- **Relationship to the pipeline.** The close skill is the live-context recorder. `verify-task`
  returns structured candidates to its calling recorder. close-tasks is the artifact-aggregation
  recorder for runs where close did not cover the same execution. All feed the configured
  observation store; the preferred profile uses `~/.agents/observations/`.
- **The in-repo digest contract (the cc-looper hook).** The headless
  `close-tasks-loop` sibling (cc-looper-side; see `specs/close-tasks-loop/close-tasks-loop_integration.md`
  in cc-looper) writes a **neutral in-repo digest** at
  `<dirname(tasks_doc_path)>/<base>_close.md` — *not* directly to a private observation store (a public,
  reusable, machine-portable skill must never hardcode a private path; and the cc-looper spawn runs
  in the target repo where that write is the documented anti-pattern + permission-fragile). This
  interactive close-tasks run is the on-your-machine **promoter**: it reads that in-repo digest
  (Phase 1 step 3) and lands it in the configured observation store. That keeps the runner-coupled
  half decoupled and public-safe.
- **Project-agnostic.** Works for any tasks-doc-shaped run (study pipeline, docs runs, etc.) — it
  reads artifacts, not domain.
- **History-only on git.** Reads `status`/`diff`/`log`/`rev-parse`; at most `add` + `commit`.
  Never rewrites history.
- **Don't manufacture entries.** A clean run produces zero observations, zero memory, zero repo
  rules, one thin SESSION_LOG roll-up — and that's correct (inherited from the close skill).
