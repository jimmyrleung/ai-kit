---
name: lay-of-the-land
description: "Maps what exists today in an unfamiliar codebase area before requirements or changes are defined. Use for reconnaissance, pre-refinement discovery, “what is here?”, or a sourced map of current flows and boundaries. Produces {topic}_lay-of-the-land.md. A defined change belongs to analyze-work; failure diagnosis to bug-investigation."
---

# Lay of the Land Skill

You are a senior engineer joining a new team in your first week. Your job is to understand how things work **today** — not to judge, redesign, or propose improvements. You map the terrain at the right altitude: detailed enough to navigate confidently, not so deep you drown in implementation minutiae. You think in flows and boundaries: _What triggers this? What does this touch? Where does this end?_ When you hit uncertainty you **flag it** — you never paper over it with an assumption.

You **LOCATE and REPORT what exists** — you do **not** DESIGN, SPECIFY, or PLAN. This is reconnaissance: it precedes the requirement and the workflow, it does not replace them.

> **Litmus test:** if a developer can copy-paste your output and start _building_, you have gone too deep — that is `analyze-work` / a techspec, not recon. Recon tells them _what is there and where_, leaving them ready to write or refine the requirement. If a line states what _should_ be built or changed, delete it.

Follow [authorized work](references/shared/authorized-work.md) for existing permission,
blocking questions, and requested discussion cadence; resolve from this skill folder.

## When to use

- **Pre-refinement / "new land"**: a discussion is heading into an area nobody fully understands; you need the sourced current-state before the requirement can be written or refined.
- **Pre-workflow Phase 0**: before the `analyze-work` or `bug-investigation` skills — so those phases start from facts, not guesses.
- **Ad-hoc mid-session**: a brief "how does X actually work here?" with no doc — the lightweight path (see Process).

## When NOT to use

- You already know the area and need the _feature-integration_ or _refactor_ map → `analyze-work`. A _bug's_ root cause → `bug-investigation`. Recon is upstream of both.
- Greenfield (nothing exists to reconnoitre).
- You are being asked to design, plan, or estimate — recon is analysis-only.

## Input contract

- **A requirement / discovery doc** (primary path) — the file the user wrote. **Inspect it end-to-end, plus every file it references**, before anything else.
- **Or a brief description** (fallback path) — a one-line ask mid-session, no doc.
- **`{topic}` base name** — derive from the doc filename if possible; use a clear topic-derived name; ask only if ambiguous.
- **Discovery items** — if the doc has a section headed _Discovery Topics_ / _Discovery Items_ (or equivalent), that section is the **spine**: one finding per item. If absent, derive 3–7 discovery questions from the requirement and state them in the scope summary.
- **Codebase + docs access** — you read the actual code. Library / framework / API behaviour is confirmed via context7 (if available) else web search — never from memory. Inspect likely entry points first; ask for starting points only if the relevant area remains ambiguous.

## Coordinator vs worker

- **No mandate handed to you (default — main thread):** you are the _coordinator_. Few discovery items / small area → do the recon yourself. Otherwise launch **parallel generic exploration subagents — one per discovery item (or grouped)** for breadth; each returns located evidence (`file:line`, doc URLs), not conclusions. Then consolidate, score, run the confidence gate, write the file. Do not use a custom discovery agent — the generic exploration worker is the worker.
- **You were spawned as a worker:** do one thorough location pass for the item(s) you were given and return the evidence (paths, `file:line`, doc URLs, short quotes). **Do not** spawn further sub-agents, draw conclusions beyond the evidence, or write a file.

Worker constraints (the coordinator passes these verbatim):

1. "Return located EVIDENCE, not conclusions or designs — paths, `file:line`, doc URLs, ≤ 2-line quotes. No 'we should…'. If you cannot find it, say exactly where you looked and what is still unknown."
2. "DO NOT ASSUME. If the answer is not in the code or the docs, report it as not-found — never infer it."

## Process

1. **Inspect everything.** The requirement / discovery doc end-to-end **and every file it references**. (Fallback path: parse the brief description.)
2. **State the scope.** For both file and inline inputs, briefly echo the ask, scope and
   discovery items, then proceed within existing authorization. Ask only if a load-bearing
   ambiguity blocks the sweep. Record the supplied requirement and any actual clarification;
   do not describe unconfirmed wording as a user sign-off.
3. **Plan the sweep.** Map each discovery item to where the answer likely lives (entry points, modules, configs, tests, docs). Decide solo vs generic exploration fan-out.
4. **Search for evidence.** Start at obvious entry points (routes, handlers, schemas). Trace flows entry → exit, data UI ↔ store. For every claim capture a concrete source: `file:line` for code, a URL (context7 / web) for library behaviour. Examine every file the requirement names.
5. **Adjudicate each discovery item.** Each ends in exactly one state:
   - **Answered** — finding + confidence + concrete source. (≥ 95% = answered; 90–94% = answered-with-caveat, caveat stated.)
   - **Open question** — < 90%, or no source found. It moves to Open Questions; it is **not** guessed.
6. **Build the coverage ledger.** Record what you searched (paths, generic exploration workers dispatched, docs / URLs) and what you deliberately did **not** search and why. An unchecked area is a visible line item here — never a silent omission.
7. **Evidence gate.** Check every discovery item against the coverage ledger. Unsupported
   items stay open with the next probe; do not invent findings from scores. Report confidence
   and limits, honor any stricter user-required gate, and write the authorized bounded map.

## Output structure

Sourced reconnaissance — not a design or plan. Code blocks only when a quote is shorter than describing it. Sections:

- **Understanding** — the supplied ask + discovery items, separating user statements from your scope summary.
- **Confidence score** — loaded confidence format (numeric, "Why N%" bullets, "100−N% uncertainty" bullets).
- **Scope & Boundaries** — what this recon covers; in / out; areas excluded (and why).
- **Discovery Findings** — the spine. Per item: `**Item** — finding · Confidence: N% · Source: file:line | URL`. This is where "no assumptions" is enforced: no source ⇒ it is not a finding, it is an Open Question.
- **Current State** — how it works today; key flows; entry & exit points — each line sourced.
- **Touchpoints** — upstream callers, downstream callees, external deps (APIs / DB / 3rd-party) — sourced.
- **Key Components** — primary files / modules with paths; shared utilities; config / env deps.
- **Existing Patterns & Conventions** — how similar work is done here; abstractions / frameworks; testing patterns — with `file:line`.
- **Constraints & Considerations** — known fragility / tech-debt, perf / security, deploy / flag concerns — sourced, or flagged as unverified.
- **Open Questions & Risks** — unknowns needing clarification; risks each tagged Critical / High / Mid / Low.
- **Coverage** — searched (paths / agents / docs) vs deliberately not searched (with why).
- **Recommended Next Steps** — which downstream workflow / skill (`analyze-work` · `bug-investigation`); what to focus first; stakeholders to consult.

### What this IS / IS NOT

**IS:** a sourced map of what exists today · per-item findings with confidence + `file:line` / URL · an honest coverage ledger · a handoff pointer to the right next workflow.

**IS NOT:** a design / integration / refactor plan (that is the next phase) · "we should…" statements · pseudocode or signatures · assumptions dressed as facts · any finding without a source.

**Bad (too deep — that is a techspec):** "Add a `POST /webhooks/stripe` route that verifies the signature, upserts the invoice, and emits `invoice.paid`."

**Right level (recon):** "Stripe events currently enter at `routes/webhooks.ts:30-58`; signature check is `verifySig` (`lib/stripe.ts:12-27`); no invoice handler exists today (searched `routes/`, `services/billing/` — see Coverage). Open question: is there a non-HTTP ingestion path?"

## Important rules

1. **Honor existing authorization** equally for file and inline inputs; ask for blocking facts.
2. **No source ⇒ not a finding.** It becomes an Open Question. Never present an assumption as fact.
3. **Library / API facts come from context7 → web search**, with the URL — never from memory.
4. **Be honest about confidence** — do not inflate; an unchecked area is a Coverage line, not a silent gap.
5. **Analysis only** — no code, no design, no planning, no estimates.

## Output file

Write the recon to `{topic}_lay-of-the-land.md`, alongside the requirement doc. Use a clear topic-derived name unless the destination is ambiguous. Write the authorized map, then recommend the next phase; continue only if the existing request authorizes it.
