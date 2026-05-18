# Terraform documentation SKILL

## Reasoning for this skill

I want to create a documentation skill focused on Terraform `document-terraform`. We already have the `document-workflow` command but it is really focused on front-end to back-end flows.

My reasoning for a separate skill is that for terraform, we don't really need to trace a sequence of steps or heavy business rules as we usually do for "standard" coding apps.

My idea is to generate a documentation that helps me with the following:

1. Overview of shipped infrastructure (what environments exist, high-level structure, list of external infras it interacts with, count of components, etc.).

2. Inventory of resources per environment: I'd say this would be the most used part of the documentation, something that would tell me:
   - Provisioned resources with resolved name (so if needed I can search on the provider where it is deployed that exact resource)
   - If it is originated from a shared/private module or not, and if yes, which shared module it uses
   - What is that specific resource
   - What's the role/importance of each specific resource
   - Is it associated with an external infra? if yes, which one
   - Where I can find the source for that specific component

3. If possible, map what might be handled out of terraform: there are specific permissions or links that might have been done outside of terraform due to company security and privacy policies, so would be nice to have these flagged (I understand sometimes it is not really possible to be sure if something is handled or not outside terraform, and that's okay, we should add at least reasoning and confidence score for each one)

## Drafting the skill

### SKILL.md

I want to test a couple things I read, so for this SKILL I want:

1. SKILL.md with concise instructions and output guidance
2. Additional reference files if content exceeds 500 lines

We would provide a high-level description or a small spec file describing what repos/projects are involved.

### document-workflow - any valuable parts?

Also, I'd like you to fully read the `document-workflow` command and see if anything there would be valuable here. I stated what I want with the benefits, but there might be something else that would really help and I'm not seeing

> We should probably get from document-workflow all the "audit" stuff (createdAt/lastupdatedAt + commit hash) so we can easily track updates instead of re-generating it every time

### Real world reference

For building this SKILL I'd like you not to suppose things, I'd like you to use a real client Azure landing-zone repo (anonymized throughout this archive as `<repo-root>/landing-zone`) to have a real-world example of where this SKILL would be used.

**IMPORTANT**: It doesn't mean EVERY repo I apply this SKILL will have that structure, this is one example, so you should not couple the SKILL with this repo, but you should be able to validate the effectiveness of the SKILL by enhancing your drafting process with a real-world scenario.

## Must be included on the SKILL

On the documentation process, there are a couple rules I want stated on the SKILL for the agents to follow:

- Try to use websearch or context7 to retrieve information directly from official docs.
- Really try to explore and find answers on the terraform code or on the docs - no assumptions with justifications like "I didn't read the file {xyz}", "I didn't look the docs to confirm {abc}" or "I didn't check the module {fgh} files"
- If it is a shared/private module, there's a chance we might have access to the source of that module, so go back to the user and ask if they have access to it and if they could add that to the workspace so you can fully trace it.

---

## v1 — what got built & decisions locked (2026-05-18)

Files created:

- `skills/document-terraform/SKILL.md` — concise methodology (Phases 0–3, coordinator/worker, ≥95% gate, output contract, mandatory rules).
- `skills/document-terraform/reference/heuristics.md` — the verbose detail + worked (anonymized) examples (the progressive-disclosure "reference file if >500 lines" pattern you wanted to test).
- `commands/document-terraform.md` — thin shim, mirroring `investigate-bug.md` → `bug-investigation`.

Decisions locked into v1 (from the assessment dialogue):

- **Topology-first.** Phase 0 discovers roots / per-root env axes / dependency order / backend model. No flat or symmetric-environment assumption; asymmetry is documented, never synthesized away.
- **Name resolution = static + confidence.** Evaluate locals/vars from entrypoint literals → tfvars → defaults; unresolved segments rendered `<var.x>` with lowered confidence, never invented. State/`terraform show -json` is an optional, never-automatic, never-prod confidence-raiser only.
- **Secrets = key names + value-source class only. Never values.** Hard rule + table in the reference.
- **External detection = producer-index + 3-state** (`cross-stack` / `out-of-band` / `indeterminate`), replacing the naive "every `data` = external". Driven by a repo-wide producer index across all roots + resolvable private modules, with ownership-comment / naming-divergence / chain-termination corroboration. Your correction #3 is encoded as worked examples 1–4.
- **Module resolution = convention-agnostic.** Classify source by shape; ask the user to add private/remote sources; propose but never hardcode a client's `registry-name → local-path` map. `indeterminate ≠ external`.
- **Output = stable contract + iterating layout.** The audit/staleness header (`Created` / `Last Updated` / `Generated From` SHA / `Schema`), the Source-Files table, the Change Log, and the three questions every doc-set must answer are **fixed**; the file layout is explicitly v1 and expected to iterate. Lifted wholesale from `document-workflow`.
- **One orchestrated pass, no scanner split** (Terraform has ~handfuls of envs, not hundreds of handlers — `docs-tasks-creator`'s backlog model doesn't apply).

Open / iterate:

- Output **layout** (`overview.md` + `<root>/<env>.md`) is a v1 guess — validate against a real generation and reshape; the contract stays fixed so staleness tracking survives layout churn.
- Private-module-resolution UX only gets validated once run against a real unresolved module.

Deliberately NOT done in this scope (flagged, not silent) — confirm before I touch any:

- `INVENTORY/skills.md` + `INVENTORY/commands.md` entries; `README.md` cross-workflow/family mentions.
- Codex adapter note: a plain skill is auto-junctioned by `adapters/codex/sync.ps1`; the thin command has no Codex form (same as other shims) — no generation needed, but worth a line in the adapter README if we mainstream this.
- Optional dedicated `terraform-documentation-agent` (v1 uses generic `Explore` workers, matching the kit's fallback).
- The dogfood validation run against the real landing-zone repo (the natural next iterate step).

---

## What we ended up building — 2026-05-18

**Shipped as the `document-terraform` skill** (SKILL.md + `reference/heuristics.md` progressive-disclosure reference + thin-shim `/document-terraform` command). Built v1 from this draft, then hardened it across **5 dogfood → assess → refine cycles** against a real (now-anonymized) 3-layer Spacelift/Azure landing zone.

- **Positioning:** the Terraform analogue of `document-workflow`. Terraform has no execution path to trace, so the unit of work is the **(root, environment) pair**, not a handler; one orchestrated pass, no scanner/backlog split (handfuls of envs, not hundreds of routes). Separate skill — rejected extending `document-workflow`.
- **The iteration arc (each cycle = regenerate real docs → honest assessment → refine the skill):**
  1. **v1** — topology-first discovery; static name-resolution + confidence (`<var.x>` for the unresolvable, never invented); secrets = key-names + value-source-class only; external detection = repo-wide producer-index **3-state** (cross-stack / out-of-band / indeterminate); convention-agnostic module resolution; audit/staleness header lifted from `document-workflow`.
  2. **Provenance + role** — per-resource module-provenance chain (entrypoint → local wrapper → private module@version → resource) + a per-component "role in the architecture" narrative **grounded only in observed wiring** + a newcomer on-ramp. Schema bumped v1 → v2.
  3. **Option A + notation + counts** — role block consolidated per single-orchestrator root (not per-sub-module); `(×N)` / `(count=…)` multiplicity notation, square brackets reserved for real Terraform indices; count-integrity rule.
  4. **Tag taxonomy + doc-wide counts** — `[entry]`/`[wrap]`/`[priv]` pinned deterministically (the top-level orchestrator **and every `data.*` lookup** are `[entry]`; `[wrap]` only for a local module wrapping one specific private module); count-integrity widened doc-wide (sources vs source@version pairs vs sibling repos kept distinct).
  5. **Whole-estate-fact reconciliation guard** (the decisive cycle) — a real `git pull` flipped a behavioural toggle's default between two runs; the per-env worker re-read it correctly while the overview carried the **stale prior-SHA value** → a split-brain doc-set, cascading into a wrong "this module is moot" claim. Added a 4-touchpoint guard: a mandatory rule + a consolidation ledger-diff + a confidence-gate hard-stop + a worked example. Estate-wide facts are resolved **once from source at the generation SHA**, stated identically everywhere; the overview is a **roll-up**, never an independent source of truth. Verified fixed on the next regen.
- **Disposition of this draft's asks:** (1) overview / per-env inventory / external map — delivered and exceeded (provenance chains + role narrative + on-ramp went beyond the original ask). (2) "concise SKILL.md + reference file if >500 lines" — applied: methodology in SKILL.md, gnarly detail + worked examples in `reference/heuristics.md`. (3) the three must-include rules (official docs via context7/websearch; no lazy assumptions; ask before treating a private module as external) — all encoded as mandatory rules, and the skill **held the discipline** every cycle (unresolved module pins were flagged at low confidence, never invented).
- **On the "do not couple" IMPORTANT block:** verified followed — the *methodology* is generic with explicit anti-coupling guardrails (mandatory rule "Don't couple to any example repo"; "never bake in a naming convention"; every worked example tagged "illustrative — do not couple"). The real repo was used to *validate the drafting* (as instructed); the worked examples were then **anonymized to a synthetic `acme` estate** so nothing client-identifying ships in this public repo — paths, project name and IDs masked, the generic Terraform/Azure architecture shape kept (that's the pedagogical value). "Coupled" and "contains client strings" were two different problems; only the second was real, and it was a public-repo confidentiality fix, not a coupling fix.
- **Files:** `skills/document-terraform/SKILL.md`, `skills/document-terraform/reference/heuristics.md`, `commands/document-terraform.md`. Schema at **v2**.
- **Deferred (not done this session):** `INVENTORY/{skills,commands}.md` + `README.md` family mentions; codex-adapter note (plain skill auto-junctioned by `adapters/codex/sync.ps1`; thin command needs no Codex form); optional dedicated `terraform-documentation-agent` (v1 uses generic `Explore` workers); a `/audit-skills` structural pass over the new skill.
