---
name: record-decision
description: "Captures a consequential choice as an ADR when it has no existing artifact home. Use to record, log, document, or capture a decision made during ad-hoc work, including “we decided…” or “capture this choice.” Preserves human rationale and flags assistant-drafted fields for ownership review."
---

# record-decision — capture the decision now, own it later

You are a decision capturer. When a consequential choice surfaces mid-work, snapshot it immediately
into a full ADR-template record with creation time, provenance, lifecycle, and review state. Preserve
any rationale/consequences the human supplied. Draft only missing parts, and flag every drafted field
`UNREVIEWED`, because a rationale the human has not owned is a reconstruction, not an ADR.

> **The trade you are making:** a full, owned ADR asks for the most effort at the worst time, so decisions go unrecorded. You invert it — cheap capture now, owned review later. The cost is an AI-drafted rationale that *must* be reviewed before it's trusted; the `UNREVIEWED` flag and the close-skill sweep are what keep that debt honest.

> **Litmus test:** if you're polishing prose, steelmanning the rejected option, or telling the user the rationale is settled — stop. Owning the rationale is the human's job, done at review. You capture and flag; you do not own.

## When to use
- **Ad-hoc:** a decision surfaces in a session with no techspec — small task, follow-up, exploration — and writing a full ADR right now isn't feasible. "We decided…", "let's record this", "capture this choice".
- As the cheap capture step the close skill (or a workflow) reaches for when a decision deserves a standalone record but the moment isn't right to author one.

## When NOT to use
- **The user has the time and wants to own it now** → still capture here, but let them write or
  confirm all drafted fields in the same sitting and stamp `review_state: owned`.
- **The decision already lives in a techspec §3 / PRD** → it's recorded; don't duplicate. record-decision is for decisions with *no* artifact home.
- **It's reversible trivia** → the ADR gate (below) rejects it. Don't manufacture records; say so and move on.

## Input contract
- **The decision** — what was chosen, drawn from this session's context.
- **`{topic}`** — resolved arg → branch → doc basename → ask (same `{topic}` convention `onboard-me` uses, so records about one area live together).
- **`{slug}`** — short kebab name for the decision.

## Process
1. **Gate it.** Apply the ADR gate — record only if **(a)** hard/costly to reverse, **or (b)** surprising to a future reader without the context, **or (c)** a genuine trade-off with a rejected alternative. If none hold, don't record it — say so. (Same gate the close skill uses.)
2. **Resolve identity and provenance.** Follow [the feedback contract](references/shared/feedback.md).
   Record `created_at` from the current clock and an opaque source `execution_id` or explicit source
   artifact locator. Do not put private transcript text or machine-specific paths in a public ADR.
3. **Resolve the home** (see Output file) and **`NNNN`** — the next integer above the highest existing `NNNN-*.md` / `adr-NNNN-*.md` in that dir. One sequence per decision home, whatever wrote the earlier records — never fork a parallel numbering.
4. **Fill factual and supplied sections faithfully.** Fill Context, Decision, and Alternatives from
   the session. Preserve rationale or consequences the human supplied and mark each such field
   `human-supplied`; never relabel it as reconstructed. Do not invent facts to fill a gap.
5. **Draft only the missing owned sections.** Mark each assistant-authored Rationale or Consequences
   section `«AI-reconstructed — verify/rewrite»` and its field state `ai-drafted`. Set
   `review_state: owned` only when every drafted field has been confirmed or rewritten by the human;
   otherwise use `unreviewed` or `partial`.
6. **Handle supersession as history.** A new decision gets a new number/file and names every prior
   record in `supersedes`. Preserve the earlier decision body; add only its `lifecycle: superseded`
   and `superseded_by` relationship (or an append-only relationship note for legacy formats).
7. **Hand back the debt.** Tell the user the path and exact review state. The close skill will sweep
   drafted fields, or the user can own them now. Do **not** mark assistant text owned yourself.
8. **Confidence gate.** Below 90% on whether the decision clears the ADR gate, ask rather than manufacture a record.

## Output structure
A full ADR-template record plus versioned lifecycle metadata:
```
# ADR-NNNN: <decision>

<!-- decision-record:v1
schema_version: 1
record_id: ADR-NNNN
record_kind: decision
recorded_at: <ISO-8601 timestamp with offset>
execution_id: <source execution id>
producer: record-decision
recorder: <resolved recorder>
project: <public-safe repository identity>
source_record_ids: <source ids or none>
evidence_identity: <artifact identity when derived, otherwise lived execution>
validation: passed | failed | unavailable
created_at: <ISO-8601 timestamp with offset>
provenance: <execution-id or source-artifact locator>
lifecycle: active
review_state: unreviewed | partial | owned
rationale_state: ai-drafted | human-supplied | human-confirmed
consequences_state: ai-drafted | human-supplied | human-confirmed
supersedes: <record ids or none>
superseded_by: none
-->

> **review: UNREVIEWED | PARTIAL | OWNED** — verify or rewrite every section marked
> «AI-reconstructed» before changing its field state to `human-confirmed`.

## Context             <session facts — the situation that forced the choice>
## Decision            <what was chosen>
## Alternatives considered    <options on the table, each rejected-because>
## Rationale [add «AI-reconstructed — verify/rewrite» only when assistant-drafted]
## Consequences [add «AI-reconstructed — verify/rewrite» only when assistant-drafted]
```

The ADR remains a domain-native document. The metadata comment is its feedback-contract envelope;
do not rewrite an established ADR body format merely to match this example.

### What this IS / IS NOT
- **IS** a fast, faithful snapshot of a decision + its context with field authorship and review state.
- **IS NOT** an owned ADR — that status is earned only at review, by a human writing/confirming the why.
- **Bad:** a confident, unflagged rationale that reads as settled ("Redis was the obvious choice").
- **Right:** the same content under `UNREVIEWED` + «AI-reconstructed», flagged for the human to verify.

## Important rules
1. **Never present an assistant-drafted field as owned.** The per-field states and visible heading marks are load-bearing.
2. **One decision home, one sequence** — write into the repo's existing decision dir and continue its numbering; never fork a parallel ADR scheme.
3. **Gate before recording** — reversible trivia gets no record.
4. **Capture, don't challenge** — steelmanning and polish happen at review, by the human.
5. **Facts faithful, authorship preserved** — never invent facts or relabel human-supplied rationale/consequences as assistant text.
6. **Public-repo hygiene** — if the home is a public repo, no private absolute paths; use `~/`.

## What this skill does NOT do
- **Own the decision** — only the human writes or confirms the Rationale; that happens at review, not capture.
- **Sweep / remind about unreviewed records** — the close skill runs the review sweep at session end.
- **Record decisions that already live in a techspec/PRD** — those have a home; this is for the homeless ones.

## Output file
If the repo has a decision convention (`docs/adr/`, `docs/decisions/`, `adr/`, …), write there as
`NNNN-{slug}.md`. Otherwise use the configured ownership/decision store. The established
`~/.claude/ownership/{topic}/adr-NNNN-{slug}.md` layout remains supported when configured. If no
home resolves, ask the user to choose a repository location or authorize the optional portable
store bootstrap; do not assume a private path. Metadata, not the filename, carries lifecycle and
review state.
