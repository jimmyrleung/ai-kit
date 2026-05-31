---
name: write-skills
description: Author a new Claude skill — or fix one that won't fire — so it triggers reliably, reads like the ai-kit corpus, and passes /audit-skills by construction. Covers pinning the one job, a trigger-rich third-person description (the part that decides whether a skill fires), degrees of freedom (prose vs script), the house single-file body skeleton, and a fresh-context trigger test. Use when creating, writing, building, or authoring a skill or SKILL.md, or when an existing skill isn't triggering. Invoke as /write-skills; the build sibling of /audit-skills' lint.
---

# write-skills — author a skill that triggers and passes the lint

You are a skill author. You produce ONE focused `SKILL.md` that does a single job, **triggers reliably**, reads like the rest of the ai-kit corpus, and passes `/audit-skills` by construction. You write *for the model that will run the skill* — terse, trigger-rich, no narrative. You do **not** cram two jobs into one skill, write a tutorial a human would read, or split a short body into reference files because a guide said "100 lines."

> **Litmus test:** if you're writing *how you solved something once* (a narrative), encoding a rule a regex or hook could enforce, or splitting a 120-line body into `references/` — stop, you've left the lane. Skills are reusable techniques, not stories and not lint rules.

## When to use
- **Ad-hoc:** creating, writing, building, or authoring a new skill — or fixing one that won't trigger.
- The **build** sibling of `/audit-skills` (which lints the whole population). Author here; lint there.

## When NOT to use
- **Pervasive, always-relevant guidance** (a convention that applies to most tasks) → put it in `CLAUDE.md`, not a skill. Always-loaded context beats an optional skill for ubiquitous rules (Vercel evals: 100% vs 53%).
- **A mechanical constraint** enforceable by a regex, formatter, or hook → make it a hook, not a skill.
- **A one-line tweak** to an existing skill → just edit it; no ceremony.

## The limits that actually bind (Claude Code)
| Field | House target | Hard cap | Portable cap |
|---|---|---|---|
| `description` | ≤ 600 chars | 1536 (Claude Code truncates the listing) | 1024 (claude.ai / API reject) |
| body | ≤ 150 lines | 250 → split or mark intentionally-long | 500 (Anthropic ceiling) |
| `name` | kebab-case · == directory · ≤ 64 · **not** ending `-skill` | | |

The description is the only thing the model sees when choosing a skill, and all descriptions share a small startup budget — short is not cosmetic, it's what makes the skill *fire*. There is no "500-character" rule anywhere; that's a myth conflating the 500-*line* body cap with the 1024-*char* description cap.

## Input contract
Before drafting, pin down:
- **The one job** — one sentence. If you need an "and", it's two skills.
- **Trigger phrases** — the exact words a user would say when they want this. These become the description's "Use when …".
- **Artifact?** — if it writes a doc, name the `{token}.md` (and check `docs/output-filename-contract.md` if it joins a workflow family).
- **Scripts?** — only if some step is deterministic, fragile, or regenerated every run (see Process 3).

## Process
1. **Pin the one job.** Name what it does and, explicitly, what it does *not* — the latter becomes a `## What this does NOT do` handoff to sibling skills.
2. **Write the description FIRST — it decides whether the skill ever fires.** Third person. Sentence 1 = what it does; sentence 2 = `Use when <symptoms / keywords / file types>`. Lead with *symptoms*, not a workflow summary (a summary makes the model follow the description instead of reading the skill). Fold trigger synonyms inline. Keep ≤ 600 chars. Add `Invoke as /name` if it's deliberately invoked.
3. **Choose degrees of freedom.** Prose for judgement calls; an exact bundled script only when an operation is deterministic, fragile, or regenerated each run. Scripts: label each `read-only` / `bootstrap` / `mutating`, forward-slash paths only, *solve don't punt* (handle errors inside the script), no unexplained magic numbers. Most skills here need **zero** scripts.
4. **Draft the body to the house skeleton (single file, ≤ 150 lines)** — see below. Second person ("You are a …"); end the Process with a **confidence gate** if the skill makes judgement calls. If it genuinely needs > 250 lines, either move the *largest* block to `references/` (one level deep; add a table of contents if that file exceeds 100 lines) or add a top-of-file `<!-- intentionally-long: <reason> -->` marker — the same escape the corpus already uses.
5. **Test on a fresh context (the step that matters most).** In a clean session: **(a) trigger check** — give a realistic user request and confirm the model selects this skill from its description alone; if it doesn't, the description is wrong — fix it. **(b) dry-run** — have it follow the body on one real task and watch where it stalls, re-reads, or ignores a section; tighten those. Skills auto-trigger far less reliably than the docs imply — never ship one untested.
6. **Confidence gate, then finish.** Score per the global CLAUDE.md format (Why-N% bullets / 100−N% uncertainty bullets); at ≥ 90% write the file, then run `/audit-skills` and Codex-sync per the standing rule.

## House body skeleton (copy; delete what doesn't apply)
```
# {name} — {one-line tagline}
You are a {persona}. You {mandate}, you do **not** {the thing one step beyond}.
> **Litmus test:** if {over-reach}, you've gone too far.
## When to use              — Ad-hoc / Orchestrated bullets
## When NOT to use           — each case → the sibling skill that owns it
## Input contract            — required/optional inputs; {token} base name
## Process                   — numbered; final step = confidence gate (if it judges)
## Output structure          — the sections the produced artifact must contain
### What this IS / IS NOT     — paired bullets + a Bad-vs-Right-level example
## Important rules            — numbered hard rules
## What this skill does NOT do — handoffs to sibling skills
## Output file                — where it writes; ask if no base name
```
Omit a section rather than leave a placeholder.

## Important rules
1. **One skill, one job.** Two jobs → two skills.
2. **The description is the whole ballgame.** Third person, ≤ 600 chars, symptoms-first, trigger-rich. The *body* may be second person ("You are a …") — never confuse the two voices.
3. **Single-file by default.** `references/` is the escape past ~250 lines (one level deep, TOC if long), not the starting point.
4. **No time-sensitive content** ("as of August…") and **consistent terminology** — one term per concept, kept throughout.
5. **Scripts are the exception**, not the rule; when used, label and harden them (Process 3).
6. **Pass `/audit-skills` by construction** — kebab dir == `name`, 2-key frontmatter, differentiated from siblings, no dead paths.
7. **Never ship untested** — a skill that doesn't trigger is worse than no skill; it adds noise.

## What this skill does NOT do
- **Structural lint of the whole population** — `/audit-skills` owns that; this is its build sibling.
- **Routing** — deciding *which* skill to run is `/triage`'s job.
- **Your domain logic** — you bring the one job and the trigger phrases; this skill shapes them into a skill that fires.

## Output file
`skills/<name>/SKILL.md` in ai-kit, dir name == `name`. It is directly invocable as `/<name>` — no `commands/` wrapper needed (matches `/predict-first`, `/improve`, `/close`). After writing, run `/audit-skills`, then dry-run `adapters/codex/sync.ps1` to propagate the new skill to Codex.
