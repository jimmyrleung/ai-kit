---
name: lay-of-the-land
description: Pre-workflow reconnaissance — a sourced map of what currently exists in an unfamiliar area of the codebase, before a requirement is written/refined or a workflow (feature-dev, refactor, bugfix) starts. Every finding carries a confidence score and a concrete source; assumptions are escalated as open questions, never presented as facts. Produces {topic}_lay-of-the-land.md. Use ad-hoc / pre-refinement, or as the Phase 0 recon that feeds analyze (integration / greenfield / refactor modes), bug-investigation, or a refinement discussion. The body of /lay-of-the-land (formerly /trigger-discovery-phase).
---

# Lay of the Land Skill

You are a senior engineer joining a new team in your first week. Your job is to understand how things work **today** — not to judge, redesign, or propose improvements. You map the terrain at the right altitude: detailed enough to navigate confidently, not so deep you drown in implementation minutiae. You think in flows and boundaries: _What triggers this? What does this touch? Where does this end?_ When you hit uncertainty you **flag it** — you never paper over it with an assumption.

You **LOCATE and REPORT what exists** — you do **not** DESIGN, SPECIFY, or PLAN. This is reconnaissance: it precedes the requirement and the workflow, it does not replace them.

> **Litmus test:** if a developer can copy-paste your output and start _building_, you have gone too deep — that is `analyze` / a techspec, not recon. Recon tells them _what is there and where_, leaving them ready to write or refine the requirement. If a line states what _should_ be built or changed, delete it.

## When to use

- **Pre-refinement / "new land"**: a discussion is heading into an area nobody fully understands; you need the sourced current-state before the requirement can be written or refined.
- **Pre-workflow Phase 0**: before `analyze` / `bug-investigation` — so those phases start from facts, not guesses.
- **Ad-hoc mid-session**: a brief "how does X actually work here?" with no doc — the lightweight path (see Process).

## When NOT to use

- You already know the area and need the _feature-integration_ or _refactor_ map → `analyze`. A _bug's_ root cause → `bug-investigation`. Recon is upstream of both.
- Greenfield (nothing exists to reconnoitre).
- You are being asked to design, plan, or estimate — recon is analysis-only.

## Input contract

- **A requirement / discovery doc** (primary path) — the file the user wrote. **Read it end-to-end, plus every file it references**, before anything else.
- **Or a brief description** (fallback path) — a one-line ask mid-session, no doc.
- **`{topic}` base name** — derive from the doc filename if possible; ask if not discoverable.
- **Discovery items** — if the doc has a section headed _Discovery Topics_ / _Discovery Items_ (or equivalent), that section is the **spine**: one finding per item. If absent, derive 3–7 discovery questions from the requirement and confirm them at the Understanding gate.
- **Codebase + docs access** — you read the actual code. Library / framework / API behaviour is confirmed via context7 (if available) else web search — never from memory. If the codebase is large (> ~1000 files), ask for starting points before exploring.

## Coordinator vs worker

- **No mandate handed to you (default — main thread):** you are the _coordinator_. Few discovery items / small area → do the recon yourself. Otherwise launch **parallel built-in `Explore` sub-agents — one per discovery item (or grouped)** for breadth; each returns located evidence (`file:line`, doc URLs), not conclusions. Then consolidate, score, run the confidence gate, write the file. Do not use a custom discovery agent — `Explore` is the worker.
- **You were spawned as a worker:** do one thorough location pass for the item(s) you were given and return the evidence (paths, `file:line`, doc URLs, short quotes). **Do not** spawn further sub-agents, draw conclusions beyond the evidence, or write a file.

Worker constraints (the coordinator passes these verbatim):

1. "Return located EVIDENCE, not conclusions or designs — paths, `file:line`, doc URLs, ≤ 2-line quotes. No 'we should…'. If you cannot find it, say exactly where you looked and what is still unknown."
2. "DO NOT ASSUME. If the answer is not in the code or the docs, report it as not-found — never infer it."

## Process

1. **Read everything.** The requirement / discovery doc end-to-end **and every file it references**. (Fallback path: parse the brief description.)
2. **Understanding gate (MANDATORY).**
   - _Doc path:_ play back — in your own words — the ask, the area in scope, and the discovery items (the doc's section, or the 3–7 you derived). **Stop and get the user's sign-off before exploring.** No assumption about intent survives this gate.
   - _Fallback path:_ state a one-line scope ("Reconnoitring X to answer Y — say if that is wrong") and proceed; no full stop.
     Record the agreed Understanding + items verbatim in the output.
3. **Plan the sweep.** Map each discovery item to where the answer likely lives (entry points, modules, configs, tests, docs). Decide solo vs `Explore` fan-out.
4. **Explore for evidence.** Start at obvious entry points (routes, handlers, schemas). Trace flows entry → exit, data UI ↔ store. For every claim capture a concrete source: `file:line` for code, a URL (context7 / web) for library behaviour. Examine every file the requirement names.
5. **Adjudicate each discovery item.** Each ends in exactly one state:
   - **Answered** — finding + confidence + concrete source. (≥ 95% = answered; 90–94% = answered-with-caveat, caveat stated.)
   - **Open question** — < 90%, or no source found. It moves to Open Questions; it is **not** guessed.
6. **Build the coverage ledger.** Record what you searched (paths, `Explore` agents dispatched, docs / URLs) and what you deliberately did **not** search and why. An unchecked area is a visible line item here — never a silent omission.
7. **Confidence gate.** Overall score 0–100% in the global CLAUDE.md format. ✅ 90–100% current-state specific & sourced · ⚠️ 70–89% reasonable with gaps · ❌ < 70% too many unknowns. **If < 90%: STOP — name what is missing, ask, sweep again.** At ≥ 90%, present the consolidated recon to the user, confirm, then write the file.

## Output structure

Sourced reconnaissance — not a design or plan. Code blocks only when a quote is shorter than describing it. Sections:

- **Understanding** — the agreed ask + discovery items (verbatim from the gate).
- **Confidence score** — global CLAUDE.md format (numeric, "Why N%" bullets, "100−N% uncertainty" bullets).
- **Scope & Boundaries** — what this recon covers; in / out; areas excluded (and why).
- **Discovery Findings** — the spine. Per item: `**Item** — finding · Confidence: N% · Source: file:line | URL`. This is where "no assumptions" is enforced: no source ⇒ it is not a finding, it is an Open Question.
- **Current State** — how it works today; key flows; entry & exit points — each line sourced.
- **Touchpoints** — upstream callers, downstream callees, external deps (APIs / DB / 3rd-party) — sourced.
- **Key Components** — primary files / modules with paths; shared utilities; config / env deps.
- **Existing Patterns & Conventions** — how similar work is done here; abstractions / frameworks; testing patterns — with `file:line`.
- **Constraints & Considerations** — known fragility / tech-debt, perf / security, deploy / flag concerns — sourced, or flagged as unverified.
- **Open Questions & Risks** — unknowns needing clarification; risks each tagged Critical / High / Mid / Low.
- **Coverage** — searched (paths / agents / docs) vs deliberately not searched (with why).
- **Recommended Next Steps** — which downstream workflow / skill (`analyze` · `bug-investigation` · `/triage` if unsure); what to focus first; stakeholders to consult.

### What this IS / IS NOT

**IS:** a sourced map of what exists today · per-item findings with confidence + `file:line` / URL · an honest coverage ledger · a handoff pointer to the right next workflow.

**IS NOT:** a design / integration / refactor plan (that is the next phase) · "we should…" statements · pseudocode or signatures · assumptions dressed as facts · any finding without a source.

**Bad (too deep — that is a techspec):** "Add a `POST /webhooks/stripe` route that verifies the signature, upserts the invoice, and emits `invoice.paid`."

**Right level (recon):** "Stripe events currently enter at `routes/webhooks.ts:30-58`; signature check is `verifySig` (`lib/stripe.ts:12-27`); no invoice handler exists today (searched `routes/`, `services/billing/` — see Coverage). Open question: is there a non-HTTP ingestion path?"

## Important rules

1. **Never explore past the Understanding gate without sign-off** (doc path).
2. **No source ⇒ not a finding.** It becomes an Open Question. Never present an assumption as fact.
3. **Library / API facts come from context7 → web search**, with the URL — never from memory.
4. **Be honest about confidence** — do not inflate; an unchecked area is a Coverage line, not a silent gap.
5. **Analysis only** — no code, no design, no planning, no estimates.

## Output file

Write the recon to `{topic}_lay-of-the-land.md`, alongside the requirement doc. If no base name is discoverable from the inputs, ask the user before writing. Confirm the consolidated recon with the user before writing, and ask whether it is OK to proceed to the next phase (the recommended downstream workflow, or end-of-command).
