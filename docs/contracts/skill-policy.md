# Skill policy ownership

For work on ai-kit, the shipping authority for executable metadata rules is the target
checkout's `scripts/check-skill-portability.mjs`.
Authoring, audit, and improvement workflows use its findings instead of copying a
field allowlist. The checker enforces the standard profile and the explicitly
reviewed provider overlays. An overlay is not permission to add arbitrary fields.

From that target repository's root, validate the final proposed tree with:

```sh
npm ci
npm test
npm run check:portability
```

Structural mode isolates schema fixtures; transitional mode reports coupling as
warnings. Neither replaces final mode for shipping. The sync engine separately
checks safe directory names and readable source envelopes using the standard
library; it does not parse YAML or certify schema or runtime behavior. Run the
checker before syncing. The inventory check compares names, duplicates, and the
derived population, so an unchanged count cannot conceal a wrong member.

These commands operate on the repository being maintained; they are not supporting files
loaded from the installed skill. In another repository, inspect its documented validation
commands and the applicable skill standard. Record unavailable executable validation as
unavailable, never PASS. The semantic guidance below is bundled with individual skills.

## Semantic guidance

- Give each skill one coherent purpose and a clear trigger boundary. A description
  identifies when to select it; the body supplies the actual procedure.
- Aim for descriptions of 600 characters or less. Longer descriptions are a review
  lead when they contain procedure detail; preserve useful trigger distinctions.
  The checker owns the standard's binding bounds. There is no separate host cap in
  this policy.
- Prefer a short core with evidence requirements, conditional decisions, checks,
  and handoff. Lines, words, repeated headings, and trigger overlap are inspection
  signals, never automatic failures or grounds to merge distinct workflows.
- Load substantial conditional references when their condition applies, including
  error and negative cases. Keep the required contract discoverable from the body.
  Resolve bundled references relative to the installed skill folder. Maintain shared rules
  centrally and generate local copies, including transitive references, before distribution.
  Copy the complete skill folder; no separate ai-kit checkout is needed to read these rules.
- Report description size separately from the effective catalog shown by a host.
  A host can budget, shorten, filter, or omit entries. Neither aggregate size nor a
  description-only routing simulation proves actual discovery or task quality.

## Three separate checks

1. **Routing:** positive, neighboring, and non-trigger requests against the observed
   catalog. Record host/version/model/settings and distinguish a simulation from
   native discovery.
2. **Procedure and outcome:** execute representative tasks, preserve source state,
   traces and artifacts, and grade missed obligations, errors, and coverage. Use
   repeated trials and owner review for subjective quality. Compare no-skill,
   baseline, and candidate where meaningful; unavailable runs remain unavailable.
3. **Final tree:** strict schema, coupling, inventory membership, local references,
   and relevant executable regression checks. A passing routing trial cannot waive
   these checks, and structural conformance cannot certify runtime quality.

Use this policy from `write-skills`, `audit-skills`, and `improve`. Existing staged
tree, observation-tag, and completion-dependency validations remain required.
The [Agent Skills specification](https://agentskills.io/specification) was checked
2026-09-07 for metadata boundaries; its guidance on body organization is distinct
from required metadata validation. Vercel's
[repository-instruction evaluation](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
is evidence about its tested Next.js tasks and configurations, not universal proof
that always-loaded instructions outperform skills.
