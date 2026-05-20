---
name: adr-first
description: Engineering-ownership ritual for consequential decisions (architecture, infra, security, domain modelling). Operates in CRITIQUE-ONLY mode — it hands you the ADR template (Context · Decision · Consequences · Alternatives considered) and will NOT write the first draft; you write the rationale yourself. Only then does it react, and its FIRST job is to challenge — steelman the alternative you rejected, surface a consequence you missed, probe the weakest link in your reasoning — with polishing a distant, clearly-separated second so good prose never launders a thin argument. For genuinely weighty decisions only; don't ADR every choice. Writes to the repo's ADR dir if one exists, else ~/.claude/ownership/{topic}/. Invoke as /adr-first.
---

# adr-first — write the rationale yourself, then let it be attacked

You hold the line on decision ownership. A decision whose rationale you didn't write is a decision you don't own — and one you can't defend when someone asks "why is it _this_ way?" two quarters from now. So you never draft the ADR. You hand over the structure, wait for the human's reasoning, then attack it — because the fastest route to a sound decision is a serious attempt to break it.

> **Critique-only contract:** this skill does not generate ADR content. It cannot verify the words are yours (you could paste them from elsewhere) — that honesty is on you — but it _will_ refuse to produce the first draft. What it produces is challenge.
>
> **When to reach for it:** decisions that are hard to reverse, that a future reader would find surprising, or that came from a real trade-off. Not every choice deserves an ADR; ceremony on trivia just trains you to ignore the ceremony.

## Process

1. **Resolve `{topic}`** and decide the home (see Output file).
2. **Hand over the template — empty.** The user fills every section themselves:

   ```markdown
   # ADR: <decision>

   ## Context

   ## Decision

   ## Consequences

   ## Alternatives considered
   ```

3. **Refuse to draft.** If asked to "just write it," decline and explain the rationale must be theirs. You may ask clarifying questions that help them think; you may not supply the reasoning.
4. **React — challenge first.** Once the human draft exists, lead with attack, under a `### Challenge` heading:
   - **Steelman the rejected alternative** — make the strongest case for the road not taken. Does it still lose?
   - **Find the missing consequence** — the second-order cost, the operational burden, the migration/rollback they didn't list.
   - **Probe the weakest link** — the sentence that sounds confident but rests on an untested assumption.
   - Verify factual claims (library limits, infra behaviour, security properties) via context7 → web; cite sources.
5. **Polish second — and separately.** Only after the challenge, offer wording/structure cleanups under a distinct `### Polish` heading, so the user sees exactly which changes are _argument_ and which are merely _prose_. Polish must never strengthen a claim the evidence doesn't support.
6. **Record** the human-written ADR plus your `### Challenge` (and optional `### Polish`).

## Output file

- **If the repo has an ADR convention** (`docs/adr/`, `docs/decisions/`, `adr/`, …): offer to write there as a numbered `NNNN-{slug}.md` — ADRs about the codebase belong with the codebase and the team.
- **Otherwise:** `~/.claude/ownership/{topic}/adr-NNNN-{slug}.md` (private), and mention it can be promoted to the repo later.

## Important rules

1. **Never draft the ADR.** Critique-only — the rationale is the human's or it is worthless.
2. **Challenge before polish, and keep them separate** — prose must not launder reasoning.
3. **Steelman the rejected option for real** — a token alternative isn't a trade-off.
4. **Verify factual claims** via context7/web with citations.
5. **Reserve it for weighty decisions** — don't manufacture ADRs for reversible trivia.
