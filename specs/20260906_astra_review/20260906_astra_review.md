# 2026-09-06 - Astra Review

Goal: Make a massive review of this kit with Astra

## Description

This is my AI kit, and I use it with the following tools:

- Claude Code
- Codex
- Cursor

Claude Code and Codex I use more heavily - Cursor is more recent so we likely won't have any insights from it yet.

I recently moved from Windows to this Linux machine, so I backed up my .claude and .codex in the following repos, where you can find more insights regarding my usage:

- Current .codex folder: `~/codex`
- Backed up .codex folder: `~/backups/20260902_backup_win/.codex` (portable placeholder)
- Backed up .claude folder: `~/backups/20260902_backup_win/.claude` (portable placeholder)

Your goal is to:

- Explore all references I provided and skills of that repo
- Do not use $audit-skills and $write-skills to audit this repo, you should do it as you just discovered it to avoid any bias, and audit-skills and write-skills are also skills to be audited as they could be outdated too. **This should be an honest and relentless audit/analysis.**
- Create a backlog of fixes/improvements/updates to be done - they will be executed in a separate /goal, so execution is OOO
- You're definitely allowed to spawn agents for also doing some research on best practices out there from authoritative and reliable sources - but I'd lean on the ones that have success evidence. A given tweet or reddit post with some statements from the user that states an opinion, but without success evidences to back it up should be carefully considered.

A few things I'd like you to consider when doing that review, which already bothers me:

- This ai-kit was built when I started coding with AI agents back in September last year where I used mostly Claude Code with Opus 4. I feel recent models are way more sharp, steerable, and of course intelligent, so I feel we need a refresher on the kit
- Conciseness: recently I updated the $analyze and $techspec skills to be more straightforward in list format because I thought they were too verbose. This was a start but I feel there's room for more improvements: reduce verbosity, redundancy, and bureocracy.
- Language and formatting: prefer simplified technical english, but without harming llms understanding, as skills are used by llms.
- Maintainability of the kit: should be easy to maintain and as provider-agnostic as possible. When it is something specific to a given provider, we should have a decision table that covers at least Claude, OpenAI and Cursor models.

> These are just a few things

The goal is to come up with a: simplified, concise, maintainable ai-kit that's optimized to be used with modern agents like gpt 5.6 luna/terra/sol, gpt 6 astra/pro, fable 5/5.1, Opus 4.8/5, Sonnet 5, Grok 4.5/4.6, etc. that can be used by any interested user.
