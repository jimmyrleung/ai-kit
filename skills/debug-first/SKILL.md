---
name: debug-first
description: "Engineering-ownership ritual for NON-incident bugs (sprint-work bugs that can wait — never a production fire; if prod is down, use the incident-response workflow instead). Run BEFORE you point AI at a bug. It hands you an investigation template (Observed · Hypotheses · What I tried · Question for AI) and refuses to investigate for you, so you form hypotheses with your own head first. The selfish payoff is immediate: writing a sharp \"Question for AI\" forces you to localize the bug, and a localized question gets a far better answer. Afterward it engages your hypotheses with evidence (confirm/refute each) rather than bypassing them, and records the actual root cause vs. your guesses to ~/.claude/ownership/{topic}/debug-{date}-{slug}.md. Invoke as /debug-first."
---

# debug-first — form the hypothesis before you borrow the brain

You guard the debugging muscle — the one that atrophies fastest when an AI is always within reach. Make the user investigate _first_, then engage their hypotheses as a peer; don't hand them the answer and let the muscle waste.

> **Scope:** for mid/low-risk bugs that enter normal sprint work — failing tests, weird-but-not-urgent behaviour, code you don't understand. **Not for incidents.** If users are down and the clock is running, stop and use the incident-response workflow; investigating-alone-first is a luxury you spend when you can afford it.
>
> **The selfish hook:** even if you don't care about retention today, do this — a question that names _where_ you think the bug is gets a sharper answer than "it's broken, fix it." The ritual pays you back this session.

## Moment 1 — investigate alone (the skill hands over, then waits)

1. **Resolve `{topic}`** (arg → branch → doc basename → ask) and a short `{slug}` for this bug.
2. **Hand over the template — do not start investigating.** Present this for the user to fill themselves:

   ```markdown
   ## Debug attempt before AI — {topic} — {date}

   ## Observed:

   Hypotheses:

   1.
   2.

   ## What I tried:

   ## Question for AI:
   ```

3. **Do not pre-empt.** Don't read the code and volunteer the bug. You may answer a _factual_ question ("where does this log come from?") but not "what's wrong?" — that's theirs to hypothesize.

## Moment 2 — engage, don't bypass

Once the user has filled it in:

1. **Take each hypothesis in turn** and confirm or refute it **with evidence** (`file:line`, a test, a trace) — don't skip past their thinking to your own conclusion. If hypothesis 2 is right, say _why_ and what in the code confirms it. If all are wrong, say what each missed. Lay out the end-to-end causal chain with each hop tagged **`VERIFIED`** (observed — `file:line` / test / trace) or **`ASSUMED`** (inferred — say what would verify it), and before endorsing any fix, state the observation that would disprove the diagnosis. The tags show the user which parts of the story are still assumption — that visibility is part of the teaching.
2. **Answer their actual question** — now you help fully; the ritual has done its job.
3. **Close the loop (encouraged).** Once the bug is solved, append the **actual root cause vs. their hypotheses** — were any right? what was the tell they could have followed? Tag the gap: `wrong-layer` · `missed-evidence` · `right-instinct-wrong-detail` · `unknown-unknown`.
4. **Write** `~/.claude/ownership/{topic}/debug-{date}-{slug}.md` — the filled template plus the root-cause-vs-hypotheses note.

## Output file

`~/.claude/ownership/{topic}/debug-{date}-{slug}.md` (many per topic; dated).

## Important rules

1. **Don't investigate before the user does.** Template first; hypotheses are theirs to form.
2. **Engage every hypothesis with evidence** — confirming/refuting their guesses is the teaching; bypassing them wastes the ritual.
3. **Not for incidents.** Production fire → incident-response, not this.
4. **Evidence over assertion** — `file:line` / test / trace for every claim; library facts via context7/web.
5. **Close the loop when you can** — root-cause-vs-hypothesis is where the calibration happens.
