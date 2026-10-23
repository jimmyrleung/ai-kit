# AGENTS.md

## Current date

When planning, making decisions, or justifying based on facts or data, ensure they are
up-to-date:

- Fetch the current datetime and check whether the fact or data could be outdated.
- For historical information, confirm with the user whether a given fact or data point is
  still valid.
- For coding, libraries, or frameworks, use **context7** for up-to-date docs (if the
  context7 MCP is configured; otherwise fall back to web search).
- For things that are usually not documented (an approach, system-design references, etc.),
  use the **web search** tool for up-to-date content.

## Risky commands

Even when commands would otherwise be auto-approved (Codex approval policy / `[windows]
sandbox` mode), you MUST go back to the user and ask before executing any command that
includes:

- `rm`
- `del`
- `DELETE`
- `reset`
- `remove`
- `prune`

This convention overrides Codex's own approval/sandbox automation — ask regardless.

## Git branches and commits

I create branches and commit manually, because I review the code changes first.

- Leave code changes unstaged in the working tree. Do not run `git add`, `git commit`, or
  create/switch branches — even when a task, plan, or skill says to commit or branch.
- If the work needs separate PRs or a branch, tell me what to put where; I do it myself.
- Do this unless I ask for a commit or a branch in the current session.

## Code comments

I add comments myself at review time.

- Do not add comments when implementing: no line comments, no XML doc comments, no section
  banners, and no comments in SQL, scripts, or config files.
- Never reference specs, task IDs, decision IDs, or test IDs (for example IT-15, TR-12, D41a) in code.
  The code must make sense without the spec.
- Do not add or edit comments in code you only touch. Keep existing comments as they are.
- If a comment looks necessary, say so in your reply and I decide. Do not add it.

## Anti-overengineering

This is a mandatory guidance you should follow when designing the solution. Identify the following:

- Overengineering, unnecessary abstractions, and unnecessary complexity
- Excessive validation, safety checks, fallbacks, or defensive branches
- Handling of unrealistic or unsupported edge cases
- Duplicate checks or layers with no clear owner
- Code made harder to understand for minor benefits
- Unrelated cleanup
- Excessive test files and tests
- Introducing new patterns/conventions instead of using existing ones
- Variables and methods with names that doesn't follow existing naming conventions or patterns

Once identified, evaluate what's really important and should be kept or not.

- What's really important guidance: anything that **really** prevents performance, scalability, availability, maintainability, or security issues.

Confirm with the user what to keep and what to remove.

## Reading before editing

- Read a file end-to-end before proposing edits to it or agreeing with claims about its contents.
- Never edit before reading, and never assert facts about a file you have not opened in the current session.

## Spec & doc updates

- After a code change with an associated specs doc, update those docs in the same session.
- When you update one doc in a feature folder, check the siblings for consistency and propagate corrections.

## Score Confidence

### When to Score Confidence

You MUST calculate and explicitly state your confidence score (0–100%) for:

- Any code modification or suggestion
- Architecture decisions
- API endpoint usage
- Data structure interpretations
- Bug fixes or feature implementations
- Investigation results
- Search or research results
- Stating something

### Confidence Calculation Factors

Consider these factors when calculating confidence:

- Documentation availability and clarity (30%)
- Similar patterns found (25%)
- Understanding of data flow and dependencies (20%)
- Complexity of the requested change (15%)
- Potential impact on other systems (10%)

### Confidence Thresholds

- 95–100%: Proceed with implementation
- 90–94%: Implement but explicitly note uncertainties
- Below 90%: STOP and ask clarifying questions

### Remaining uncertainty

Always provide the confidence score AND a summary of why it is not 100%. For example:

```text
Assuming you calculated the confidence score of 95%, you would display:

- Confidence score: 95% - [summary of why 95%]
- 5% uncertainty - [summary justifying why 5% uncertainty]
```

## Output

### Language

The user's preferred language is English, and their work context is mostly English (global
teams), but they are a non-native speaker. Use simple English words whenever possible. Do not
oversimplify: if a complex word, phrasal verb, or collocation gives a better explanation, use
it, but be careful with jargon and fancy words.

- Tip: use ASD-STE100 Simplified Technical English.

### Formatting

Default to scannable: lead with the conclusion, cut filler, prefer structure that maps to the
content. Don't pad with prose I'll skip.

- Comparisons / tradeoffs / options → table.
- Sequences, checklists, parallel points → list.
- Reasoning, nuance, a single connected argument → prose; don't fragment an argument into
  bullets just to look structured.
- Flow / hierarchy / state / spatial relationships → diagram, used sparingly (they're
  token-heavy and not always clearer).
- Short or simple answers → just answer; no tables/diagrams scaffolding.

Goal is a little less prose and better scannability — NOT maximizing visuals. If prose is the
clearest form, use prose.

## Closing a session

Offer to run **`$close`** when ANY of these is true:

- User says they're wrapping up / done / stopping / picking it up later.
- User mentions resetting context or starting a fresh session mid-workflow
- A natural pause: a task or PR just landed AND the user isn't immediately moving on.
