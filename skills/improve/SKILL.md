---
name: improve
description: "Reviews recorded agent/workflow friction and unresolved improvement proposals to find supported patterns and stage changes for owner review. Use for a periodic self-improvement review, recurring workflow problems, or a stale review watermark. Structural skill-population lint belongs to audit-skills."
---

# Improve

You are running the periodic self-improvement review:

- Read the evidence the `close` skill has been logging + past improvement items still open + ad-hoc artifacts provided by the user for this run
- Find what it's telling you, and you produce a backlog of improvements, where each item will be reviewed and approved/rejected/deferred by the user.
- Persist the backlog of improvements and walk the user through the backlog.

**Important notes:**

1. **You do NOT edit live skills, MEMORY.md, or the active harness's loaded private instruction file directly**: you stage everything and present it. The user is the reviewer; that's deliberate (their value-add is the judgement on the diff, not having it automated away).

2. **You are a distiller, not a churner.**: A good run might produce 3 sharp proposals, or zero ("nothing actionable accumulated — here's the fitness table, go enjoy your Friday"). Do NOT manufacture proposals to look productive. The number of changes applied is NOT a success metric — it measures churn.

## Approach

Execute each phase sequentially.

### Phase 1 - Gather context

1. Gather context from `~/.agents/observations/state.json` - if it doesn't exist, create one. It should have:

```json
{
  "lastExecutedAt": ""
}
```

- lastExecutedAt: last time the `improve` skill ran

2. Read all observations after lastExecutedAt: ideally, we should be deleting older observations after an improve run, but if forget to do it, we know the last time we executed so we skip any older ones.

3. Gather context from `~/.agents/improvements/BACKLOG.md` if it exists.

4. When applicable, read or search for any other references that the user provided or asked you to read, like artifacts the user thinks that are valuable for improving their skills, links, etc.

5. Find which SKILLs and repos were mentioned in the latest observations + open/deferred improvement items in the backlog, and gather context on these:

- Read the SKILLs (ai-kit skills)
- Read relevant files for the repos (`AGENTS.md` + rules + local repo skills)

> Go back to the user asking for anything you couldn't find (missing skill, missing repo, etc.)

This step is complete when you have full context: read all observations, existing improvements backlog, relevant SKILLs, and has access to relevant repos with their respective `AGENTS.md` and rules

### Phase 2 - Consolidate improvements

1. Review each observation and its mentioned files or references to confirm if it really is relevant and accurate. Calculate a confidence score for each one.

2. Check each item of the existing improvements backlog against the reviewed observations to see if:

- any of them increase/reduce the confidence score for any open/deferred improvements
- any of them confirm a given improvement item should not be done at all, and should be marked as rejected

> It is not mandatory that improvement items are impacted by observations. If the latest observations doesn't have any impact on the existing backlog of improvements, we should just accept it.

3. Build a list of new improvements to be applied, categorizing them by:

- global `AGENTS.md` improvements
- global ai-kit SKILLs
- repo-specific `AGENTS.md`
- repo-specific rules
- repo-specific local skills

> New improvements are not limited to updating existing files, it could also be writing new skills. New skills should be written with `write-skills`.

4. Calculate the confidence score for each item of the new list of improvements

5. Consolidate a new backlog of improvements:

- Move the existing `~/.agents/improvements/BACKLOG.md` to `~/.agents/improvements/archive/yyyyMMdd_BACKLOG.md`
- Write a new consolidated `~/.agents/improvements/BACKLOG.md` with items ordered by category and confidence score (higher to lower confidence)

6. Update `~/.agents/observations/state.json` `lastExecutedAt` to now as we finished capturing a list of improvements for the observations.

### Phase 3 - Walkthrough

Present a summary of the process + the categorized list of improvements ordered by confidence score (higher to lower) at the end, suggesting a walkthrough for each candidate to be applied.

- Each item should be presented with a confidence score in the following format

  ```
  Confidence: X% - {justification}
  Remaining uncertainty: {justification}
  ```

Items with confidence score lower than 85% should not be part of the walkthrough unless the user says so when reviewing the list before confirming the start of the walkthrough.

For each item of the walkthrough, provide a detailed description for the item with your recommendation to apply or defer at the end.

- Applied items should be documented on `~/.agents/improvements/applied/yyyyMMdd_[slug].md` and removed from `~/.agents/improvements/BACKLOG.md`
- Deferred items should have their status updated within `~/.agents/improvements/BACKLOG.md` to deferred with the reason why

### Phase 4 - Complete

At the end of the process:

- Ensure applied items were documented under `~/.agents/improvements/applied/`
- Ensure `~/.agents/improvements/BACKLOG.md` only contains deferred items with the reason why
- `~/.agents/observations/state.json` `lastExecutedAt`has been updated
- Suggest cleaning up old observations
