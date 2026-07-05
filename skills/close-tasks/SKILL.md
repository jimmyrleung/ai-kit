---
name: close-tasks
description: End-of-tasks-doc closeout. Artifact-aggregation, NOT context-distillation — reconstructs a tasks-doc's run from durable artifacts (per-task completion notes, `## Verify`/`## Review`/`## QA` blocks, sibling `_qa.md` / `_checkpoint-*_review.md`, `.cc-loop/state.json`, `git log`) rather than scanning live conversation. Emits observations (tagged with the skill that actually ran, so `/improve` finally sees loop runs) + a roll-up SESSION_LOG entry, idempotently via a harvest marker. Run once when a tasks-doc's implementation run is complete — possibly spanning multiple sessions, possibly manual, possibly cc-looper headless — where per-session `/close` did not run. Invoke as /close-tasks. Sibling of `/close` (which distills live context for design/research sessions).
---

# Close-tasks — end-of-tasks-doc closeout

You are closing out a **tasks-doc's implementation run**, not a session. The run may have spanned
2–3 sessions, been driven by hand or by cc-looper headless, and the conversation context of the
earlier sessions is gone. So this skill does **not** retrospect on live context the way `/close`
does — it **reconstructs the run from durable artifacts** and harvests the improvement signal that
would otherwise be stranded (the cc-looper / multi-session blind spot in the `close → /improve`
pipeline).

**Consumer-agnostic.** It reads artifacts, so it does not care whether the tasks were implemented
manually (`/implement-task`), by cc-looper (`implement-task-loop`), or a mix.

**It is lossier than `/close` for *narrative* friction** ("this cost me 20 min because X" from a
cleared session is gone) — and that is an accepted trade. What survives is **structured** friction:
gate fails, accept-with-reason lines, `Status: Paused` notes, retry counts, doc-drift findings —
all of which the implement / verify / qa machinery writes into artifacts. Reconstruct from those;
don't invent the narrative you can't see.

Four phases. Move through them in order; ask before the git step. This skill reuses `/close`'s
auto-memory conventions, observation format, SESSION_LOG format, and cross-machine sync routing
verbatim — it does not restate them; it points at them.

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| `tasks_doc_path` | yes | The tasks-doc whose run is being closed. Ask the user if not given/discoverable. |
| `since` | no | Commit SHA / date to harvest from. Default = the harvest marker (below); if no marker, the tasks-doc's first commit. |

---

## Phase 1 — Resolve scope & gather artifacts

1. **Read the harvest marker.** Look in `tasks_doc_path` for a line:
   `<!-- close-tasks: harvested through <sha> @ <YYYY-MM-DD> -->`.
   If present, this run's harvest window is `<sha>..HEAD`; only tasks/commits after it are new.
   If absent, the window is the whole run (first commit that touched the doc → `HEAD`).
   This marker is what makes `/close-tasks` **idempotent and re-runnable** — running it twice, or
   running it after the doc gains more tasks later, harvests only the delta.

2. **Detect what actually ran** (sets the `skill_or_workflow` tag on every observation — this is
   the field `/improve`'s fitness table counts, and the whole reason this skill exists):
   - `.cc-loop/state.json` present → read it: `action`, `mode`, per-task `terminalStatus` /
     `attempt`, `qa` / `checkpoints` records. `skill_or_workflow` = `implement-task-loop`
     (+ `qa-loop` if a `qa` record exists, + `review-checkpoint` per checkpoint).
   - No `.cc-loop/` → manual execution. `skill_or_workflow` = `implement-task` /
     `gf-implement-task` / `implement-bug-fix` (infer from the tasks-doc / prefix family).

3. **If a cc-looper close digest is present** — `<dirname(tasks_doc_path)>/<base>_close.md`
   (the in-repo digest the future headless `close-tasks-loop` sibling writes; see Notes →
   "The in-repo digest contract") — **prefer it**: it already holds structured friction the
   headless run extracted at the time, with live context this skill no longer has. Distill that
   digest into observations directly (Phase 3) and skip the raw reconstruction in step 4 for any
   window it already covers.

4. **Gather the raw artifacts** (the reconstruction inputs, for the window with no digest):
   - `tasks_doc_path` itself — per-task `Status:`, completion notes, and any
     `## Verify` / `## Review` / `## QA` blocks inside task sections; the tasks-overview table.
   - Sibling artifacts in the prefix folder — `*_qa.md`, `*_checkpoint-*_review.md`,
     and the techspec/analysis (for AC cross-reference context only).
   - `.cc-loop/state.json` + `.cc-loop/runs/*/` (cc-looper case) — best-effort; never fatal if absent.
   - `git log --oneline <since>..HEAD` and `git diff --stat <since>..HEAD` (read-only; safe) for
     each repo declared in the tasks-doc header (or CWD repo if none declared).

---

## Phase 2 — Reconstruct friction & triage

From the gathered artifacts, derive the run's improvement signal. Map artifact evidence → friction,
**evidence-cited to `file:line` or a state.json field** (so `/improve` can weight artifact-
reconstructed signal honestly against live-context signal):

| Artifact evidence | → friction (tag) |
|-------------------|------------------|
| `## Verify` / `_qa.md` gate `FAIL` with `accepted: <reason>` | the accepted-debt reason, tagged per the gate (`line_budget_overrun`, `sdk_version_drift`, `doc_drift`, …) |
| Unresolved gate `FAIL` in `_qa.md` (Recommendation: no-go) | `buggy_code` / `wrong_approach` per the failing gate |
| `Status: Paused` + blocker note | `misunderstood_request` / capability gap — quote the blocker |
| `.cc-loop/state.json` `attempt > 1` on a task | retry churn — quote terminalStatus + attempt count |
| `terminalStatus !== "Done"` at run end | partial outcome — which task, why (from completion notes) |
| Doc-drift finding in `_qa.md` Gate 4 | `doc_drift` |
| Checkpoint review `abort` / `fix-then-proceed` | quote the recommendation + the blocking finding |

Then **categorize** each item exactly as `/close` Phase 1 does — (a) → auto-memory (certain &
durable), (b) → observations (skill/workflow-performance evidence for `/improve`), (c) → SESSION_LOG
roll-up, (d) → just say it in chat. Apply `/close`'s ADR gate for (a) and its
**don't-manufacture** rule: a clean run — all tasks `Done`, no gate fails, no pauses, no retries —
yields **zero observations, zero memory, one thin SESSION_LOG roll-up line**, and that is correct.

---

## Phase 3 — Persist

### 3a — Observations (the point of this skill)

For each (b) item, append to `~/.claude/observations/{YYYY-MM-DD}-{short-slug}.md` using the
**exact format in `~/.claude/observations/README.md`** (do not restate it here — read it). One file
per close; `{short-slug}` describes the tasks-doc (e.g. `auth-oauth-tasks-close`). Per observation:

- `skill_or_workflow:` = the value **detected in Phase 1 step 2** — this is the load-bearing field;
  it is what makes `implement-task-loop` / `qa-loop` / `review-checkpoint` finally show up in
  `/improve`'s fitness table and pattern-mining instead of counting as zero.
- `friction_observed:` — cite the artifact evidence (`file:line` / `state.json` field). If it is
  reconstructed-not-lived, say so plainly in the free-text so `/improve` weights it accordingly.
- Tags from the `~/.claude/observations/README.md` list; align with the `/insights` taxonomy.
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

Numbered within the file. **Don't manufacture** — see Phase 2.

### 3b — Auto-memory (rare for an implementation run)

For each (a) item, follow `/close`'s auto-memory conventions **exactly** (the `~/.claude/projects/<project>/memory/`
files, right `type:`, `**Why:**`/`**How to apply:**`, `[[links]]`, the `MEMORY.md` pointer, the
check-for-existing-file rule). Implementation runs rarely produce durable rules — usually zero here.

### 3c — SESSION_LOG.md roll-up entry

Find the git root (`git rev-parse --show-toplevel`; fall back to `~/SESSION_LOG.md`). **Prepend**
one entry for the **whole tasks-doc run** (not per session/task), `/close`'s SESSION_LOG format:

```
## [YYYY-MM-DD] — <tasks-doc name>: run closed (N/M tasks done across K sessions)

**Summary:** 1–2 sentences — what this run delivered and where it landed.
**Done:** <the net of completed tasks — roll up, don't transcribe per-task notes>
**Decisions:** <only load-bearing decisions surfaced in completion notes> X because Y.
**Didn't work:** <Paused/abandoned/aborted items — or "—">
**Next:** <unfinished tasks / follow-ups — "start here" — or "run complete">
**Blockers:** <unresolved, needing a decision — or "none">
**Artifacts:** <tasks-doc, _qa.md, checkpoint reviews, key commits>
```

Apply `/close`'s archive rule if SESSION_LOG is getting long (~30+ entries → oldest half to
`SESSION_LOG_ARCHIVE.md`).

### 3d — Update the harvest marker

Write/refresh in `tasks_doc_path` (a single Edit; place it just under the H1 or at EOF, wherever
it already is): `<!-- close-tasks: harvested through <HEAD-sha> @ <YYYY-MM-DD> -->`. This closes
the idempotency loop — the next `/close-tasks` only harvests what came after.

---

## Phase 4 — Housekeeping & close

1. **Show the diff** — `git status --short` and `git diff --stat <since>..HEAD` (read-only).
2. **Ask before committing.** Conventional-Commits message
   (e.g. `chore: close-tasks roll-up for <doc> — N observations, marker updated`). On approval
   `git add <files>` + `git commit`. Never `reset`/`clean`/`checkout --`/force-push. If the user
   declines, leave the tree as-is.
3. **Cross-machine sync routing** — identical to `/close` Phase 3.3: edits to
   `~/.claude/observations/` (the new file) / `MEMORY.md` / memory files route to the
   `~/.claude/` (private) tree; tasks-doc / `_qa.md` / source route to the target repo. One commit
   per repo, **ask before each commit and each push**, never auto-push, run the ai-kit secret-scan
   before pushing ai-kit.
4. **Print the close summary** — `observations: N written · skill_or_workflow: <detected> ·
   memory: N · SESSION_LOG: rolled up · marker: <sha> · commit: <hash or "skipped">`.

---

## When to use / When NOT

**Use** when a tasks-doc's implementation run is finished (or at a real stopping point) and the
per-session `/close` did *not* run for the sessions that did the work — the canonical cases being
(a) a multi-session manual run where you deliberately skipped per-session `/close`, and (b) a
cc-looper headless run (which has no interactive `/close` at all).

**Don't use** for:
- A design / research / planning session with live context worth distilling — that's `/close`
  (context-distillation; this skill deliberately does not scan conversation).
- A run where you *did* `/close` every session — the observations are already captured; re-harvesting
  via artifacts would double-count (the marker prevents this for *re-runs* of `/close-tasks`, not
  for the `/close`-then-`/close-tasks` overlap — don't stack them on the same window).
- A single trivial task — `/close`'s don't-manufacture rule already covers it; nothing to harvest.

## Notes

- **Relationship to the pipeline.** `/close` = live-context distiller (design/research). `verify-task`
  = per-task structured-signal capture inside the *interactive* implement commands, flushed by
  `/close`. `/close-tasks` = the artifact-aggregation closeout for runs where neither of those flushed
  (multi-session manual / cc-looper headless). All three feed the same `~/.claude/observations/` →
  `/improve` seam; `/close-tasks` is the one that closes the headless / multi-session blind spot.
- **The in-repo digest contract (the seam to the future cc-looper hook).** A future headless
  `close-tasks-loop` sibling (cc-looper-side; see `specs/close-tasks-loop_integration.md` in
  cc-looper) will write a **neutral in-repo digest** at
  `<dirname(tasks_doc_path)>/<base>_close.md` — *not* to `~/.claude/observations/` (a public,
  reusable, machine-portable skill must never hardcode a private path; and the cc-looper spawn runs
  in the target repo where that write is the documented anti-pattern + permission-fragile). This
  interactive `/close-tasks` is the on-your-machine **promoter**: it reads that in-repo digest
  (Phase 1 step 3) and lands it in `~/.claude/observations/`. That keeps the runner-coupled half
  decoupled and public-safe.
- **Project-agnostic.** Works for any tasks-doc-shaped run (study pipeline, docs runs, etc.) — it
  reads artifacts, not domain.
- **Read-only on git history.** Reads `status`/`diff`/`log`/`rev-parse`; at most `add` + `commit`.
  Never rewrites history.
- **Don't manufacture entries.** A clean run produces zero observations, zero memory, one thin
  SESSION_LOG roll-up — and that's correct (inherited from `/close`).
