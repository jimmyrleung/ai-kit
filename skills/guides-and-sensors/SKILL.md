---
name: guides-and-sensors
description: "Performs a deep scan of a given repository to establish a set of guides and sensors to be reviewed by the user and later linked from AGENTS.md. The goal is to anticipate and guide agent behavior within a repository, increasing the likelihood of more accurate and effective results. Use when asked to analyze a repository and establish general project context, guidelines, and rules."
---

# Guides and Sensors

Goal: define a set of rules linked from `AGENTS.md` that agents should always "keep in mind" (e.g., coding standards, basic project information, project structure, architecture, design, etc.), together with local skills (e.g., how to test XYZ, front-end and back-end conventions, how to approach a particular investigation, etc.) that help anticipate and guide agent behavior so they can work more effectively.

## Definitions

### Guides

Guides anticipate agent behavior and direct its actions before it operates, increasing the likelihood of achieving a good result on the first attempt.

- Basic information such as commands, ports, and dependencies
- Coding standards
- Folder structure
- Design and architecture blueprints
- Best practices
- Anti-patterns
- Etc.

### Sensors

Sensors observe the outcome after the agent acts and help with self-correction. They work best when they produce LLM-friendly signals, such as custom linter messages with clear remediation instructions (a "positive" form of prompt injection).

- Automated tests
- Compilers/transpilers/builds
- Linters
- Browser tooling (Playwright/DevTools MCP)
- Logs
- Databases
- Emulators/simulators
- Etc.

## Approach

1. **Exploration:** Perform an in-depth exploration of the current repository to extract as much relevant information as possible. For very large repositories, or monorepos containing multiple projects, use subagents to divide the exploration work.
   - The goal is to identify as much relevant information as possible related to the [Guides] and [Sensors] defined above.

2. **Interview the user** about any information that could not be discovered. Just as important as identifying relevant information is explicitly understanding what does not exist and/or what should not be supported.

3. **Consolidate the findings and write an exploration draft**, indicating:
   - What was explored
   - What was discovered
   - Suggested rules to be written under `./rules/` and linked from `AGENTS.md`
   - Suggested local skills

4. **Perform an adversarial review** with one or more subagents, depending on the size of the scope, to challenge, refine, and polish the draft.

5. **Write the final proposal for guides and sensors.** Write within `proposed-rules/[slug]/`:

- `AGENTS.md` - what additions you recommend to the local repo `AGENTS.md`.
- `skills/[skill-name]/SKILL.md` - what local skills you suggest for the local repo. If it include additional files referenced in the skill, add them to `skills/[skill-name]/references/`
- `rules/[rule-group-name].md` - what rules you suggest for the repo based on the [Guides] and [Sensors]
- `SUMMARY.md` - A summary of the process: exploration and conclusions. Also, include a list of everything you recommend high-level and why it is important.
