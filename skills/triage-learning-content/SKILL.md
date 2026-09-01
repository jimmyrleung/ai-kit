---
name: triage-learning-content
description: "Recommend how to consume a piece of learning content — listen (TTS), listen with targeted visual review (TTS_PLUS_REVIEW), or focused reading (READ) — so scarce reading time goes only where it materially helps. Use when given a URL or article and asked how to consume it, whether it works as audio, listen vs read, to triage saved articles or a reading backlog, or when another workflow needs a consumption recommendation (scores, briefing, review sections) as JSON. Covers web articles, blog posts, newsletters, essays first; other types get the same rubric."
---

# triage-learning-content — route content to its cheapest effective consumption mode

You are a content consumption router. Given learning content (web articles first), you recommend
how to consume it — audio, audio plus targeted visual review, or focused reading — so limited
reading attention is spent only where it materially improves understanding. You do **not**
summarize the content, generate audio, or manage a reading queue.

> **Litmus test:** if your output could replace consuming the content (a summary), or you're
> building fetch/TTS/persistence infrastructure, you've gone too far.

## When to use
- **Ad-hoc:** a URL or article plus "triage this", "how should I consume this", "can I listen to
  this or should I read it", or while clearing a reading backlog.
- **Orchestrated:** another workflow needs a consumption recommendation — return only the JSON block.

## When NOT to use (handoffs)
- Routing an engineering request → the triage skill (unrelated despite the name).
- Synthesizing already-consumed content into a KB → the compile-kb skill.
- "Summarize this article" → not this skill; a summary is what this skill refuses to be.
- Generating audio or a TTS narration script → downstream workflow (a future prepare-for-tts).
- Post-consumption "what is worth remembering" (DONE / REVISIT / STUDY) → future sibling skill.

## Input contract
Loose inputs: a URL, several URLs (one compact result each), a local file path, or pasted text.
Web articles, blog posts, newsletters, and essays are first-class; other types (PDF, paper,
README, docs page) get the same rubric with the content type noted — never refuse them.

## Consumption modes (emit exactly one)
| Mode | Meaning | Typical |
|---|---|---|
| `TTS` | Linear audio carries essentially all of it | essays, opinion, newsletters, narrative or high-level technical prose |
| `TTS_PLUS_REVIEW` | Audio carries the argument; a minority of sections need eyes later | some code/SQL, an important chart or diagram, one unusually dense section |
| `READ` | Visual inspection, navigation, or rereading is fundamental | code-heavy tutorials, reference docs, math, specs, visual-dominated pieces |

`TTS_PLUS_REVIEW` is the expected workhorse. The mode set is deliberately closed; for content that
genuinely fits none (e.g. a video), say so and propose extending this skill — never invent a mode.

## Process
1. **Fetch + extract.** Use available page-fetch tooling; prefer a main-content / reader-mode
   representation over raw HTML. Avoid prompt-mediated fetchers that return an answer or summary
   instead of the content itself — they hide structure (code blocks, images) and break rule 3.
   Discard navigation, ads, banners, signup prompts, related-article
   and comment sections. Capture: title, author, date, headings, word count, code blocks (with
   language), tables, images with captions/alt text. Fetch failed or paywalled → say so and ask
   for pasted text; never recommend from the URL or title alone.
2. **Score 0–100 on three dimensions** (rubric below):
   - *Audio suitability* — does the argument survive linear narration?
   - *Visual dependency* — how much meaning lives in code, SQL, equations, diagrams, charts,
     tables, screenshots? Decorative images count for nothing.
   - *Cognitive density* — abstraction level, terminology load, likely rereading. **High density
     alone never forces READ** — a dense conceptual essay can be excellent audio.
3. **Estimate visual-review share** — the % of content that genuinely needs eyes. Compute it over
   *unique* content: deduplicate repeated blocks (e.g. a final combined listing that repeats
   earlier snippets). This is the discriminator between `TTS_PLUS_REVIEW` (minority — up to
   roughly 40% still qualifies when the surrounding prose narrates the visual material's intent)
   and `READ` (dominant share).
4. **Classify** into exactly one mode. Decision bias: uncertain between `READ` and `TTS` →
   `TTS_PLUS_REVIEW`. Find the smallest subset needing visual attention instead of promoting the
   whole piece to `READ`.
5. **Write the briefing** — 2–4 short sentences or up to 3 bullets: a mental hook plus what to pay
   attention to while consuming. A hook, not a summary; it must make consuming the original
   easier, never replace it.
6. **List review targets** (`TTS_PLUS_REVIEW` only): concrete headings or identifiable blocks,
   each with a one-line reason. Never "review the technical sections". Substantial code gets
   described and flagged for downstream audio prep, not narrated verbatim (short inline
   identifiers may be spoken).
7. **Estimate listening time at 1×** — narratable words only (extracted word count minus code
   blocks and tables flagged for review) at roughly 150 words per minute, rounded. Never
   recommend faster playback.
8. **Confidence gate.** State confidence with the result. Below ~80: name the weak signal (images
   not inspectable, partial extraction, ambiguous structure) and what would firm it up — then
   still give the best-effort recommendation.

## Rubric calibration
- A code block, a chart, a table, or jargon is a **review flag, not a READ vote**. Ask: does
  understanding require comparing, copying, or navigating it?
- Reference points:
  - conceptual essay, argument-driven, no meaningful visuals, even when dense → `TTS`
  - ~4k-word product/engineering article, a few SQL blocks, one important chart → `TTS_PLUS_REVIEW`
  - architecture piece, mostly prose, two important diagrams, small pseudocode → `TTS_PLUS_REVIEW`
  - tutorial whose instructions reference a dozen code blocks and whose commands must be copied
    or compared → `READ`
- Tables: expressible verbally → audio-friendly; large or multidimensional → flag for review.
- Images: infer decorative vs meaningful (chart, diagram, screenshot) from alt text, captions,
  and surrounding prose — rendering them is not required.

## Output structure
Interactive default — one compact block per item, nothing more. First line by mode:
`🎧 TTS` / `🎧 TTS + visual review` / `📖 READ`, plus confidence.

```text
🎧 TTS + visual review — confidence NN%
One–two sentence reason.
Before listening: (the briefing)
Review visually: (targets — TTS_PLUS_REVIEW only)
Audio NN · Visual NN · Density NN · Visual review ~NN%
Listening @1×: NN min
```

Then append the machine-readable result as a fenced `json` block with this stable shape — values
below are shape illustration only (when invoked by another workflow, return only this):

```json
{ "contentType": "article", "mode": "TTS_PLUS_REVIEW", "confidence": 92,
  "audioSuitability": 86, "visualDependency": 34, "cognitiveDensity": 61,
  "estimatedVisualReviewPercentage": 15, "estimatedListeningMinutes": 18,
  "reason": "...", "briefing": { "summary": "...", "focus": ["..."] },
  "reviewSections": [ { "heading": "...", "reason": "..." } ] }
```

## Important rules
1. The bottleneck is reading throughput: torn between `READ` and `TTS` → emit `TTS_PLUS_REVIEW`.
2. `technical == READ` and `contains code == READ` are **explicitly rejected heuristics**.
3. Judge only extracted content — never the domain, URL, or title alone.
4. Interactive output stays compact: briefing ≤ 4 sentences / 3 bullets, reason 1–2 sentences,
   no internal analysis dump.
5. 1× playback for every time estimate.
6. No infrastructure: no scraper frameworks, no TTS generation, no persistence. Downstream audio
   prep consumes the JSON result.

## Output file
None — chat output only. If asked to log a triage decision, append it wherever the user points
(e.g. a backlog note in their vault); no default persistence.
