# Loop recipes — pairing ai-kit processes with native loop primitives

**What this is.** The provider-specific overlay between ai-kit's runner-agnostic skills and Claude
Code's loop primitives (`/goal`, `/loop`, `/schedule`, and plain turn-based prompting). Work
skills stay decoupled: they emit deterministic, machine-checkable criteria (pinned `Status:` lines,
`**Recommendation:** go|no-go`, pass/fail gates) and never name a runner. Primitive-specific wiring
lives in this document and the provider adapter mechanics; the `triage` skill points here by runner
category without repeating these spellings.

**Source.** Claude Code team guidance on loop engineering (X post, 2026-07-06), captured at
[`claude_guide_loop_engineering.md`](../claude_guide_loop_engineering.md). Related:
[`agentic_auto_scheduling_experimental_study_research_action_items.md`](../agentic_auto_scheduling_experimental_study_research_action_items.md)
(the AI-1..14 loop-research dispositions) and the loop-role model floors in
[`model-assignments.md`](model-assignments.md).

## The four frames

| Frame | Triggered by | Stops when | Best for |
|---|---|---|---|
| Turn-based (plain prompt) | You, each turn | Claude judges done | Short one-off tasks; skills carry the verification |
| `/goal` | You, once | Evaluator confirms your criterion, or turn cap | Tasks with a *verifiable* exit ("all tests pass", "score ≥ X") |
| `/loop` (local) | Interval | You cancel / the work completes | Recurring work or watching an external system, needs this machine's files |
| `/schedule` (cloud, research preview) | Cron | You turn it off | Recurring work that must survive the machine, no local-FS dependency |

Composition (the guide's "proactive loop"): `/schedule` or `/loop` to trigger, `/goal` + skills to
define done, workflows to orchestrate, auto mode for permissions. Only compose when a single frame
can't cover the job — start with the simplest frame that fits.

## Deciding the frame — three questions (from the guide)

1. **Can you write the verification check?** If not, no loop — make the work verifiable first
   (that's a skill's job, not a runner's).
2. **Is "done" deterministic enough for an evaluator?** → `/goal` with an explicit turn cap.
3. **Does the work recur, or arrive from an external system?** → `/loop` (local) / `/schedule` (cloud).

Pick the frame **before** the inner workflow: a loop wraps invocations, it doesn't replace triaging
what runs inside each iteration.

## Hard constraints

- **`/schedule` runs in the cloud.** It cannot reach `~/.claude/observations`,
  `~/.claude/improvements`, local KB vaults, or private local-only repos. Anything reading those
  must run locally.
- **`/loop` runs on this machine** and dies with it. For unattended cadences on a machine that
  sleeps, use the matching OS scheduler instead:
  - Windows: Task Scheduler.
  - macOS: a `launchd` LaunchAgent.
  - Linux: a `systemd --user` timer (or cron when systemd is unavailable).
  Keep the scheduled command and its local-file assumptions on the same OS/user context.
- **`/goal` availability varies by CLI build** — verify it exists (`/goal` with no arguments) before
  wiring a recipe to it; unverified on this machine as of 2026-07-07, and headless (`claude -p`)
  compatibility is likewise unverified.
- **Current capability caveat:** runner frames, headless execution, permissions, and stdin behavior
  vary by installed provider and version. Check the installed runner's help and its adapter guide
  before wiring a recipe; treat an unverified capability as unavailable rather than inferred.
- **Match the interval to the change rate** of the thing watched; prefer reacting to events over
  polling (the guide's own usage rule).
- **Pilot before a large run** — for tasks-doc streams, `--count 1-2` on a new doc shape first.
- **Model floors** — before assigning a cheaper model to any headless loop role, run the
  structured-output smoke test in [`model-assignments.md`](model-assignments.md).

## Recipes

### 1. Weekly `/improve` staging pass

Status quo: the staleness prompt at session start — which only fires if a session happens to start.
Opt-in upgrade: schedule Phases 1–4 headless. They only *stage* a packet (never edit live files), so
this stays compatible with the skill's "never run unprompted, only offer" rule — the staged packet
**is** the offer; Phase 5 (walk the proposals + apply) stays interactive in your next session.

- Runner: **local only** (reads `~/.claude/observations`, writes `~/.claude/improvements`).
- Wiring: use the matching host scheduler — Windows Task Scheduler, macOS `launchd` LaunchAgent,
  or Linux `systemd --user` timer/cron — to run the provider's verified local headless invocation
  weekly (for example, `claude -p "/improve — phases 1-4 only: stage the packet, do not present or apply"`).
- Guard: if `~/.claude/improvements/last-review.txt` is <7 days old, the run should no-op.

### 2. `/audit-skills` after authoring bursts

The existing >90-day staleness offer is right-sized — don't schedule tighter. If desired, the same
Task Scheduler pattern works quarterly (audit-skills stages proposals, never auto-edits).

### 3. `/compile-kb` for initialized non-Hermes vaults

A compile of an **already-initialized** vault is incremental + idempotent → schedulable locally
(vault paths are local files). Initialization/migration is approval-gated → always interactive;
never schedule a first run against an uninitialized vault.

### 4. `update-workflow-docs` freshness watch

The guide's "watch an external system and react" case: docs go stale as code moves. Its
commit-diff-driven staleness detection makes a no-change run cheap, so a weekly local run — or
`/loop` during an active working stretch — is safe. Match the cadence to the repo's merge rate.

### 5. Bounded fix cycle via `/goal` (pointer — pending AI-6)

`qa-loop` pins `**Recommendation:** go|no-go`; `review-checkpoint` pins
proceed/fix-then-proceed/abort. A fix session wrapped in `/goal` — "re-run the failed gates until
the report reads `Recommendation: go`; stop after 2 attempts" — is the native shape of action item
**AI-6**, potentially collapsing its cc-looper runner work to a prompt convention. The agreed AI-6
backtest gate still governs: this recipe reprices the build, it doesn't skip the gate. Verify the
`/goal` constraint above first.

### 6. When cc-looper, not a native primitive

Tasks-doc streams stay on `/tasks-loop` (cc-looper): plan.json anchoring, checkpoint reviews,
attempted-and-failed ledgers, baseline gates, and fresh-session resume have no native equivalent.
Native primitives *nest* (a `/goal`-wrapped fix cycle can run inside a cc-looper run); they don't
replace the runner.

## The decoupling rule (restated)

Skills emit verifiable, deterministic completion criteria and never name a loop runner. If a recipe
here needs a skill to change, the change is "make the criterion more deterministic," not "mention
the primitive." Provider primitive names appear in this document and the relevant provider adapter
mechanics; the `triage` skill uses runner categories and links here.
