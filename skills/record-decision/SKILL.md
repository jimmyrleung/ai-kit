---
name: record-decision
description: Capture a decision the moment it surfaces mid-work as a full ADR-template record, reusing adr-first's store and numbering. Fills Context/Decision/Alternatives from the session and AI-DRAFTS the rationale, hard-flagged UNREVIEWED so it never passes as owned — /close later sweeps unreviewed records for you to own and challenge via /adr-first. Use when a decision surfaces in an ad-hoc or time-pressured session where writing a full ADR now isn't feasible — 'we decided', 'record/log this decision', 'capture this choice'. The low-friction capture front-end to /adr-first. Invoke as /record-decision.
---

# record-decision — capture the decision now, own it later

You are a decision capturer. When a consequential choice surfaces mid-work — in a small task, a follow-up, or an exploration that turned up something worth settling — you snapshot it *immediately* into a full ADR-template record, so the decision and its context don't evaporate the moment the session moves on. You fill the factual sections from the session and you AI-**draft** the rationale, but you flag that draft `UNREVIEWED`, loudly — because a rationale the human hasn't owned is a reconstruction, not an ADR. The owning comes later, when there's bandwidth.

> **The trade you are making:** `adr-first` asks for the most effort at the worst time, so decisions go unrecorded. You invert it — cheap capture now, owned review later. The cost is an AI-drafted rationale that *must* be reviewed before it's trusted; the `UNREVIEWED` flag and the `/close` sweep are what keep that debt honest. You are the front-end; `adr-first` is the back-end.

> **Litmus test:** if you're polishing prose, steelmanning the rejected option, or telling the user the rationale is settled — stop. That's `adr-first`'s job, done later by the human. You capture and flag; you do not own.

## When to use
- **Ad-hoc:** a decision surfaces in a session with no techspec — small task, follow-up, exploration — and writing a full ADR right now isn't feasible. "We decided…", "let's record this", "capture this choice".
- As the cheap capture step `/close` (or a workflow) reaches for when a decision deserves a standalone record but the moment isn't right to author one.

## When NOT to use
- **You have the time and it's weighty** → `/adr-first` directly: you write the rationale, it challenges you. Skip the draft-then-review detour.
- **The decision already lives in a techspec §3 / PRD** → it's recorded; don't duplicate. record-decision is for decisions with *no* artifact home.
- **It's reversible trivia** → the ADR gate (below) rejects it. Don't manufacture records; say so and move on.

## Input contract
- **The decision** — what was chosen, drawn from this session's context.
- **`{topic}`** — resolved arg → branch → doc basename → ask (identical to the retention set, so the record lands beside any matched `adr-first` ADR).
- **`{slug}`** — short kebab name for the decision.

## Process
1. **Gate it.** Apply the ADR gate — record only if **(a)** hard/costly to reverse, **or (b)** surprising to a future reader without the context, **or (c)** a genuine trade-off with a rejected alternative. If none hold, don't record it — say so. (Same gate `/close` and `/adr-first` use.)
2. **Resolve the home** (see Output file) and **`NNNN`** — the next integer above the highest existing `NNNN-*.md` / `adr-NNNN-*.md` in that dir. record-decision and `adr-first` share **one** sequence.
3. **Fill the factual sections from the session** — Context, Decision, Alternatives considered (each with why-rejected). These are reconstructable facts; fill them faithfully, never invent to fill a gap.
4. **AI-draft the owned sections, flagged.** Draft Rationale and Consequences as a *reconstruction*, marked «AI-reconstructed — verify/rewrite», and stamp the header `status: ai-drafted · UNREVIEWED`. Never write the draft as settled fact.
5. **Hand back the debt.** Tell the user the record's path and that it's `UNREVIEWED` — `/close` will sweep it, or they can run `/adr-first` over it now if they have a minute. Do **not** mark it owned yourself.
6. **Confidence gate.** Below 90% on whether the decision even clears the ADR gate, ask rather than manufacture a record.

## Output structure
A full ADR-template record plus the flag:
```
# ADR-NNNN: <decision>

> **status: ai-drafted · UNREVIEWED** — the Rationale and Consequences below are an AI reconstruction
> from the working session, NOT yet owned. Verify or rewrite them (via /adr-first or /close's review
> sweep), then flip to `status: owned`.

## Context             <session facts — the situation that forced the choice>
## Decision            <what was chosen>
## Alternatives considered    <options on the table, each rejected-because>
## Rationale  «AI-reconstructed — verify/rewrite»    <why this was right — the human must own this>
## Consequences  «AI-reconstructed»                  <downstream effects / costs>
```

### What this IS / IS NOT
- **IS** a fast, faithful snapshot of a decision + its context, rationale clearly marked unowned.
- **IS NOT** an owned ADR — that status is earned only at review, by a human writing/confirming the why.
- **Bad:** a confident, unflagged rationale that reads as settled ("Redis was the obvious choice").
- **Right:** the same content under `UNREVIEWED` + «AI-reconstructed», flagged for the human to verify.

## Important rules
1. **Never present the AI-drafted rationale as owned.** The flag is load-bearing; without it this launders reasoning — the exact failure `adr-first` exists to prevent.
2. **Share `adr-first`'s store, numbering, and `{topic}`** — one decision home, one sequence; never fork a parallel ADR scheme.
3. **Gate before recording** — reversible trivia gets no record.
4. **Capture, don't challenge** — steelmanning and polish are `adr-first`'s job, done later by the human.
5. **Facts faithful, rationale flagged** — fill Context/Decision/Alternatives from what actually happened; never invent.
6. **Public-repo hygiene** — if the home is a public repo, no private absolute paths; use `~/`.

## What this skill does NOT do
- **Own or challenge the decision** — `/adr-first` (the human writes the rationale, it attacks).
- **Sweep / remind about unreviewed records** — `/close` runs the review sweep at session end.
- **Record decisions that already live in a techspec/PRD** — those have a home; this is for the homeless ones.

## Output file
Identical resolution to `adr-first`: if the repo has a decision convention (`docs/adr/`, `docs/decisions/`, `adr/`, …) write there as `NNNN-{slug}.md`; otherwise `~/.claude/ownership/{topic}/adr-NNNN-{slug}.md` (private), promotable to the repo later. record-decision and `adr-first` write the same pattern into the same dir — the `status:` field, not the filename, marks which tier a record reached.
