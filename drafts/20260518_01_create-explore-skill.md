# Thorough explore SKILL

## Why I want to build this SKILL

I noticed whenever I'm doing codebase exploration work to get answers for a given requirement, I end up "enriching" the explore prompt with some repetitive instructions I think I can just have in a SKILL. The repetitive instructions are:

1. Read the whole requirements document and any referenced files within.
2. Confirm you understand the ask and come back with your understanding for user approval before launching the exploration
3. If the requirements document has a [Discovery Topics] section, your exploration should be focused on that
4. Try to find answers as much as you can before you come back
   - Really explore the codebase and documentations, don't come back with:
     - "x% uncertainty because I didn't explore how {xyz} works"
     - "I didn't read the file {xyz}"
     - "I didn't look the docs to confirm {abc}"
     - "I didn't check the module {fgh} files"
   - In case of documentations, always use context7 (if available) or web search to get real answers.
5. Assumptions are not allowed: do not assume anything - either do a real exploration as mentioned on step 4 to find the answer, or come back with an open question or need for more clarification.
6. Accomplishing step 5 means you should be able to set a confidence score and provide the source that supports your answer, so always provide it.

## Draft instructions

1. SKILL.md with concise instructions and output guidance
2. Additional reference files if content exceeds 500 lines
3. Do not expect a structured input: though most of the time we'll be providing a requirements file, this skill should work just fine if we trigger it in the middle of a coding session or with just a brief description of what needs exploration.

## Naming

I've been looking for a cool name for that skill, similar to Matt Pocock "grill me" skill which is basically a SKILL for the AI to ask a lot of questions about something. For our case, I thought of `leave-no-stone` or `tear-it-apart`, but I'm open to suggestions!

---

## What we ended up building — 2026-05-18

**Shipped as the `lay-of-the-land` skill** (+ thin-shim `/lay-of-the-land` command).

- **Name:** `lay-of-the-land` — chosen over `leave-no-stone` / `tear-it-apart` / `ground-truth` / `receipts`. Decisive factor: the pre-existing `trigger-discovery-phase` command *already* called its output a "lay of the land" document, and it matched the "entering new land" framing.
- **Positioning:** Phase-0 **pre-workflow reconnaissance** — establishes the sourced current-state of unfamiliar territory *before* a requirement is written/refined or a workflow starts. Upstream of, and distinct from, `integration-analysis` (feature-placement, not recon). It **superseded** the mis-described `trigger-discovery-phase` command (git-renamed, body rewritten as a thin shim; its frontmatter `description:` had been copy-paste-broken — only the description, the body was already a good recon command).
- **The key reframe:** the 6 repetitive instructions became *mechanisms*, not exhortations — a mandatory Understanding gate, a coverage ledger (an unchecked area is a visible line item, never a silent omission), and a sourced-findings contract where *no source ⇒ not a finding ⇒ becomes an open question*, which makes "no assumptions" self-enforcing.
- **Execution:** parallel **built-in `Explore`** fan-out (one sub-agent per discovery item). The custom `discovery-agent` was retired (deleted; `INVENTORY/agents.md` updated the same session).
- **Disposition of this draft's own "Draft instructions":** #1 done (concise SKILL.md, ~95 lines). #2 deliberately *not* applied — no reference files; a behavioral contract that long wouldn't be obeyed. #3 done — requirements-file-first with a lighter brief-description / mid-session fallback path; `[Discovery Topics]` had no repo convention, so the skill defines one loosely and derives 3–7 items when absent.
- **Files:** `skills/lay-of-the-land/SKILL.md` (new), `commands/lay-of-the-land.md` (renamed from `trigger-discovery-phase.md`), `INVENTORY/{commands,skills,agents}.md` (new "Discovery (pre-workflow)" section; discovery-agent row removed).
- **Deferred (not done this session):** Codex-adapter propagation (`adapters/codex/`) and `README` / `AGENTS.md` sync.
