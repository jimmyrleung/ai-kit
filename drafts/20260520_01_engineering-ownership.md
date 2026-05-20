# Skills for keeping staff-level engineering judgement sharp while still using AI

## Context

North star: **Outsource the typing, not the understanding.** (Karpathy)

> Core mindset: AI can draft, accelerate, challenge, and review — but for code I will own long-term, I must be able to explain the design, failure modes, and trade-offs without the chat history.

> Core warning: If I need AI to explain code I shipped last week, I have cognitive debt to repay.

> Core operation mdoe: AI to increase throughput while preserving engineering ownership through tests, ADRs, debugging discipline, and knowledge systems

Problem being resolved: "How do I keep my Staff-level engineering judgment sharp while using AI to multiply execution?"

Coding is not a differentiator anymore, anyone with agentic coding tools can produce a lot of code. What is a real differentiator now is:

- understanding domain systems deeply
- seeing infrastructure/security/migration risks
- debugging production-ish systems
- explaining trade-offs clearly
- making good architectural decisions
- mentoring or influencing others
- turning messy ambiguity into stable systems

This AI kit has a lot of commands/subagents/skills that help capture, throughput, and automation, but we're lacking one layer of optimization that helps:

- recall
- self-explanation
- decision ownership
- “can I reproduce this without AI?”
- “do I still know why this exists?”

in a way that this whole kit not only help on collecting and executing, but also periodically forcing me to retrieve and explain.

Considering AI moves fast, pressure been increasing on businesses with all AI adoption, life-and-work balance, mental health, etc. the idea is not to introduce a huge "study more" burden. Instead, introduce small rituals embedded into work, like lightweight defaults.

## Action Items

Since during my day I usually have claude code or codex opened, I'm thinking of building small skills that I can just run on fresh sessions to help me with all of that, even if they just return me a template, because the thing is: if Ihave this template somewhere else like notion or obsidian, I'll probably forget... but if I have in Claude Code / Codex on a terminal that's open the entire day, I can just /clear and ref the skill

### pre-AI prediction SKILL

Short skill that I'll run before triggering any workflows with AI that will return me the following template:

```markdown
## My prediction before AI

- I think the change should touch:
- The main invariant is:
- The risky edge case is:
- I expect the implementation shape to be:
- I am unsure about:
```

Important to notice that the point here is not documentation quality. The point is forcing my brain to generate before consuming.

> Goal: create retention without requiring "no AI"

### pre-AI debugging SKILL

Short skill for debugging bugs, production issues, failing tests, weird infra behavior, or code I don’t understand. The idea is that I spend some time alone investigating and writing what I observed and my hypotheses before using AI for that type of task:

```markdown
## Debug attempt before AI

Observed:

-

Hypotheses:

1.
2.

What I tried:

-

Question for AI:

-
```

### ADR-time SKILL

Short skill for using when I need to record anything architectural, infra-related, security-related, or domain-sensitive, make yourself write the rationale.

1. It should hand-me off the following template:

   ```markdown
   # ADR: <Decision>

   ## Context

   ## Decision

   ## Consequences

   ## Alternatives considered
   ```

2. I write the initial version with NO AI.

3. After that, AI can polish, link, or challenge it. AI should refuse to do anything with this ADR if not human-written.

### challenge-me SKILL

Short skill for me to use once a given feature is code complete. I'll provide to the AI the plan/specs so it can gather context on the implementation, and then it should quiz me on that code/design, like asking me 5 questions that reveal whether I actually understand it. The AI should not answer it until I try.

### onboard-me SKILL

A short skill to simulate an onboarding session where AI acts as an experienced staff-engineer giving a cold-read walkthrough of a given feature, workflow, module, project. A couple important things:

- It should really feel like a real conversation between a new teammate and an experienced engineer on the project, so no "here's the summary of that feature" and then 100 lines of text for me to read. It should take step by step, explain something, wait for any questions/comments, then proceed
- For every message you send, you must list the assumptions you made so I can double check them.

---

## What we ended up building — 2026-05-20

Acted on this draft in a Claude Code session. Outcome: **all five skills built** — decided after scoping `debug-first` to non-incident bugs and `onboard-me` to other people's code, which neutralized the two adherence risks raised in review.

**Shipped** (`skills/<name>/SKILL.md`, no command shims — matches the `close`/`improve`/`triage` precedent for standalone rituals; auto-synced to Codex):

- `predict-first` — pre-AI prediction **+ a reconciliation back-half** (predict → AI works → diff vs. reality, tag the miss). Closing the loop was the main thing the draft was missing.
- `debug-first` — pre-AI debugging, scoped to non-incident sprint bugs; AI engages each hypothesis with evidence instead of bypassing it.
- `adr-first` — **critique-only** (skill never drafts; you write the rationale), AI challenges the rejected alternative first, polishes a distant second.
- `challenge-me` — judgment-targeting quiz (failure modes / alternatives / invariants / blast radius), won't answer until you try, grades against code **and your saved prediction**.
- `onboard-me` — Socratic cold-read of unfamiliar code, one step at a time, lists assumptions every message.

**Key design decisions:**
- **Persistence = durable artifacts** in `~/.claude/ownership/{topic}/` (private claude-home, not this public repo). `{topic}` resolves arg → branch → doc → ask, identically everywhere, so `predict-first` ↔ `challenge-me` pair up (saved prediction = answer key).
- Reconciliation / debug misses are **tagged** (`blast-radius` / `missed-invariant` / `unknown-unknown` …) now, so the artifacts are mineable later.
- ADRs write to the repo's ADR dir if one exists (a buried ADR isn't an ADR), else ownership.

**Deferred (the "durable + retention-review" option):** a `retention-review` skill — the human-facing counterpart to `/improve` that mines the saved artifacts for patterns ("you keep under-estimating migration blast radius"). Build it only if the daily rituals prove sticky — deliberately not built up front to avoid the month-1-graveyard risk.

**Also:** catalogued in `INVENTORY/skills.md` (new "Engineering ownership" section). Cursor adapter NOT yet synced (needs WSL-vs-native confirmation).
