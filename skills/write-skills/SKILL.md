---
name: write-skills
description: "Authors a focused, portable skill or fixes one that does not trigger reliably. Use when creating, writing, building, or authoring a skill / SKILL.md, or when an existing skill will not fire. Finding installable skills belongs to find-skills."
---

# write-skills — author a skill that triggers and passes the lint

## Goal

Create, write, build or author a new skill / `SKILL.md` that:

- does a single job
- triggers reliably
- is `ai-kit` compatible

You write _for the model that will run the skill_ — terse, trigger-rich, no narrative. You do **not** cram two jobs into one skill, write a tutorial a human would read, or split a short body into reference files because a guide said "100 lines."

## Input contract

The input can be any of:

- An inline prompt with details of what to build
- An inline prompt asking to retrospective on a given session and extract a given skill
- Artifact(s) that provide useful context for writing a given skill

## Process

1. **Pin the one job.**:
   - Establish **the one job** that the skill should do, one sentence. If you need an "and", it's two skills.
   - Name what it does and, explicitly, what it does _not_ do.
   - **Trigger phrases**: the exact words a user would say when they want this. These become the description's "Use when …".

2. **Write the description FIRST - it decides whether the skill ever fires.**:

- Third person.
- Sentence 1 = what it does;
- Sentence 2 = `Use when <symptoms / keywords / file types>`. Lead with _symptoms_, not a workflow summary (a summary makes the model follow the description instead of reading the skill). Fold trigger synonyms inline. Follow the shared policy's 600-character review target; preserve useful longer triggers within the checker's binding bounds. Add an explicit-invocation note only if the skill is deliberately invoked.

3. Write the skill body following the [General Skill Guidance]

- Local skills should be written under `.agents/skills/<name>/`
- Global skills should be written on `skills/<name>/` in ai-kit

## General Skill Guidance

1. **Reference ai-kit** Always look at sibling skills and references in this kit.
2. **One skill, one job.** Two jobs → two skills.
3. **The description is the whole ballgame.** Third person, symptoms-first, trigger-rich; apply the shared policy's review target and the repository checker's binding limits.
4. **Scripts are the exception** Prose for judgement calls; an exact bundled script only when an operation is deterministic, fragile, or regenerated each run.
5. **Focused core by default.** Follow the shared policy for conditional references; no automatic line-count split.
6. **Rot-resistance.** No time-sensitive content ("as of August…"), no baked-in runtime specifics (counts, versions, other files' line numbers); point at a single source of truth (a path or URL) rather than duplicating content that drifts.
7. **Consistent terminology** — one term per concept, kept throughout.
8. **References** The skill should describe the general process, and any specific processes or routing should live under `skills/<name>/references` and referenced in `skills/<name>/SKILL.md`
9. **Templates** Any templates the skill should follow should be defined under `skills/<name>/references` and referenced under `skills/<name>/SKILL.md`
10. **Never ship untested** — a skill that doesn't trigger is worse than no skill; it adds noise.
11. **Regenerate, don't patch.** When a skill has accumulated several ad-hoc exception clauses or fix-on-fix edits, rewrite the body from its one-job spec instead of patching again — layered fixes blur a skill's focus until it stops firing cleanly.
