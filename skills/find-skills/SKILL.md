---
name: find-skills
description: "Finds and compares installable agent skills when the user asks to discover a skill or extend agent capabilities. Use for “find a skill for X” or “is there a skill that can…”. Ordinary how-to and implementation requests stay with direct assistance. Installing a candidate requires authorization for that skill and destination."
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## When to Use This Skill

Use this skill when the user explicitly wants to find or compare skills, extend agent
capabilities, or install a named candidate. An ordinary how-to or implementation
request does not imply discovery intent. Help with the requested task directly.

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query] [--owner <owner>]` - Search for skills interactively or by keyword, optionally scoped to a GitHub owner
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Find candidate sources

Use the [skills.sh catalog](https://skills.sh/) or the source repository to discover
candidates. Popularity is discovery metadata, not evidence of task success or fit.
Record the source URL and revision/date inspected; verify the current CLI interface
before running a command. A catalog description alone supports a candidate listing,
not a substantive recommendation.

### Step 3: Search for Skills

Search for the requested capability:

```bash
npx skills find [query] [--owner <owner>]
```

For example:

- User asks "find a skill for React performance" → `npx skills find react performance`
- User asks "find a skill for PR reviews" → `npx skills find pr review`
- User asks "find a skill for changelogs" → `npx skills find changelog`

### Step 4: Verify Quality Before Recommending

Open the candidate's `SKILL.md` in full, relevant bundled scripts, dependencies, and
license/provenance. Check whether its inputs, outputs, host capabilities, permissions,
and write boundaries fit the requested task. Inspect scripts before running them.

Prefer observed task results with inspectable methods. If outcome evidence is absent,
say so and offer a bounded trial; don't invent a quality ranking from installs, stars,
or publisher identity. A popular but incompatible candidate is a mismatch. An
unreadable candidate remains unverified, with the inaccessible scope stated.

### Step 5: Present Options to the User

For each useful candidate, give its purpose, source/revision inspected, compatibility
and write requirements, and available outcome evidence (or its absence). Link directly
to the inspected source. Include an installation command only after checking its
current interface and identifying the intended project or user scope.

### Step 6: Offer to Install

Install only when the user authorized the selected candidate and destination. Preserve
existing user-owned skills; inspect conflicts before changes. Global installation
requires that scope to be authorized. For a verified CLI supporting these flags:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Inspect provenance**: catalogs and source identity help locate candidates; inspected compatibility and task evidence justify a recommendation.

## When No Skills Are Found

If no relevant skills exist:

1. State which catalogs/repositories and queries were searched; no result is bounded to that search
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
