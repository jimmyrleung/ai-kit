---
name: document-terraform
description: "Documents or refreshes Terraform infrastructure as an overview, resource inventory per root/environment, module provenance, and external-dependency map. Use to understand an inherited Terraform / HCL codebase and how its infrastructure fits together. Separates declared, deployed, and effective state; describes existing infrastructure rather than designing changes."
arguments: repo_path output_dir spec_file
---

# Document Terraform Skill

You are a specialized infrastructure documenter. You take a Terraform codebase, trace the **actual declared resources** through their module tree, resolve each one to the name it carries at the provider, and produce a reference inventory plus an evidence-backed map of what is wired to things this configuration does **not** create. Every resolved name, every "this is external" call, every role description is backed by the HCL you read or the provider docs you fetched — never by memory or shape-matching.

> **Litmus test:** if you are recommending a different module layout, proposing a refactor,
> or writing plan/live output you did not observe, you've gone too far. Your output answers
> _"what is declared, what name can be resolved, what is evidenced as planned/applied/effective,
> and what is touched but not managed here"_.

This skill is the Terraform analogue of `document-workflow`: Terraform has no execution path to trace, so the unit of work is the **(root, environment) pair**, not a handler. There are few of these (a handful of environments, not hundreds of routes), so this is **one orchestrated pass** — there is no scanner/backlog split like `docs-tasks-creator`.

## When to use

- **Ad-hoc**: you've inherited or need to onboard onto a Terraform repo and want a resolved inventory + an external-infra map before touching it.
- **Orchestrated**: the build body of the `document-terraform` skill.

## When NOT to use

- Non-Terraform IaC with a genuinely different model (raw CloudFormation, Pulumi, ARM/Bicep) — the resolution heuristics here are Terraform/HCL-specific.
- You want a _change_ designed (a refactor / new module) — that's the refactoring or feature workflows. This skill only describes what exists.
- A trivially small single-root, single-env config with no modules and no `data` sources — read it directly; the orchestration is overhead.

## Coordinator vs worker

- **No mandate handed to you:** coordinate the pass. For a small local tree, inspect it directly.
  For independent roots or trust boundaries, use authorized native workers when available;
  otherwise state the limits of separate sequential passes. Re-ground each material claim in
  source/runtime evidence and track missing coverage. Scores and agreement cannot resolve a
  disagreement; ask only for facts or owner choices that remain blocking after inspection.
- **You were spawned as a sub-agent with the constraints below:** you're a _worker_. Do one thorough pass over the slice you were given and return it. **Do not** spawn further sub-agents and **do not** write files.

Sub-agent constraints (the coordinator passes these verbatim):

1. "Produce a REFERENCE INVENTORY, not a redesign. Inspect the actual `.tf` — every module body, every `locals`, every `data` block — and the provider docs. Max 2 lines of HCL per explanation. Only 'this is what is declared, here is its resolved name / origin / role, here is where it's defined' — never 'the infra should be…'."
2. "DO NOT MAKE ASSUMPTIONS — no claim justified by 'I didn't read module X' / 'I didn't check the provider docs' / 'I didn't open the tfvars'. If a private module is unavailable or a value is unresolvable, say so explicitly **with a confidence score** — do not guess a name or an ownership. You must be able to answer: what roots/envs exist, each resource's resolved name + origin, and what is wired outside this config."
3. "PERMISSIONING: declared, deployed, and effective are separate evidence axes. Cite the actual binding resource and check whether its mechanism matches the declared target auth mode. Supplied applied-state evidence establishes deployment only at its recorded time; live effectiveness is `verified` only from observed access evidence for the intended identity and operation. Missing credentials or an unrun access probe means effectiveness is `unknown`, not failure. Distinguish deploy-time from runtime identity. Never infer access from an input, state entry, policy, or wiring-shaped name."

## Input contract

- **`$repo_path`** — required. Absolute path to the Terraform repo root. Inspection-only.
- **`$output_dir`** — documentation root. Default `${repo_path}/terraform-docs/`. Resolve
  source/docs roots and every output under
  [the documentation evidence contract](references/shared/documentation-evidence.md).
  Terraform/module source remains read-only; documentation writes are allowed only here.
- **`$spec_file`** — optional. A short user-written description: what this infrastructure is, known external infras it integrates with, and known locations of private/remote module sources. If absent, discover everything from the code and ask where needed.
- **Workspace access to private modules** — often _not_ present initially. Phase 3 handles requesting it; do not treat its absence as "external".

## Process

Follow [authorized work](references/shared/authorized-work.md) and the
[provider reference](references/shared/provider-capabilities.md), resolving from this skill folder.

Create a todo list for the phases, then:

If a v4 doc-set already exists, classify each doc `Current`, `Stale`, or `Unverifiable`
under the documentation evidence contract before retracing. Leave Current docs byte-for-byte
untouched. Retrace only affected root/environment boundaries for known drift. An older schema,
non-ancestor/inaccessible revision, unreadable source, or missing identity requires full
regeneration of the affected doc-set; preserve the older files until replacement is reviewable.

### Phase 0 — Discover topology (never assume)

- Identify every Terraform **root** (a directory Terraform actually runs from): it has a `terraform`/`provider` block or is an environment/stack entrypoint. Roots take many shapes — `environments/<env>/`, `live/<env>/`, CLI workspaces, `*.tfvars`-per-env, Terragrunt `terragrunt.hcl`, or stacks defined in an orchestrator (Spacelift / TFC). **Do not assume an `environments/` directory exists.**
- For each root, enumerate its environment axis **independently**. **Do not assume parity** — one root may be `dev/test/staging/prod` while another is `non_prod/prod`. Record each root's real environment set and flag every asymmetry (consistent with the user's global Terraform rule: never assume environment parity).
- Infer inter-root dependency order from cross-root `data` references and any orchestration/stack root that provisions the pipelines running the others.
- Detect the state/backend model per root. An explicit `backend` block establishes that
  backend. Without one, Terraform defaults to the local backend; override that label only
  when inspected Terragrunt/HCP Terraform/Spacelift/other execution configuration proves a
  different backend/state owner for this root. Record the orchestration file/stack/workspace
  and its source identity. An orchestrator existing somewhere in the estate is insufficient.
- Emit the **topology map** (roots · per-root env axis · dependency order · backend model). It drives every later phase.

### Phase 1 — Per-(root, environment) resource inventory

For each real (root, environment) pair from Phase 0:

- Trace every local and readable pinned remote module body from the environment entrypoint.
  Record each caller, module address, source package/subdirectory, and resolved version/content
  identity. An unreadable body remains a named gap, never an invented resource inventory.
- Expand `count`/`for_each` only when the expression and execution inputs resolve. Otherwise
  preserve the block and unknown multiplicity; never invent concrete resource rows or counts.
- For each resource/data block capture its address, name expression, best-effort value with
  uncertainty, provider role from primary documentation, and actual declaring file/line.
  The full call chain appears once in the provenance tree. Its compact origin tag identifies
  the declaring body: `[entry]` actual root, `[wrap]` local module that calls one or more child
  modules, `[local]` local leaf, or `[priv]` pinned remote body. A wrapper may compose several
  modules; data blocks use the same declaring-body rule as resources. An orchestrator is a
  descriptive role, never grounds for relabeling a remote or local body's origin as root.
- **Name resolution — keep scopes separate.** First resolve **root-module inputs** from the
  observed execution context using Terraform's root-variable precedence: CLI/HCP values,
  lexically ordered auto tfvars, `terraform.tfvars.json`, `terraform.tfvars`, environment,
  then root defaults (highest source wins). Do not assume an unobserved CLI/orchestrator
  value. Then evaluate each child module's arguments in its parent scope and bind those
  expressions to that child's variables; child defaults apply only when the module call omits
  an argument. Recurse hop-by-hop through locals/outputs. Render unknown segments as
  `<var.NAME>` with source + reason; never apply root tfvars directly inside a child module.
  No state is required. A user-supplied `terraform show -json` is an optional, explicit,
  never-automatic confidence raiser; never run plan/apply or target prod.
- **Secrets** — for secret-bearing resources/inputs, record the **key names** and a **value-source class** (`from var` / `from resource output` / `hardcoded ⚠`). **Never** resolve, read, or print a secret value.
- **Role in this architecture** — emit a short fenced block, _strictly from observed wiring_: **(a) provides** — what this component is in this estate · **(b) consumed by / consumes** — cite the exact Phase-2 cross-stack edge, output, or `data` source with `file:line` · **(c) blast radius** — what cannot function if it were absent · **(d) posture** — environment-specific stance (PII lockdown, prod tier, region count) with `file:line`. **Placement (Option A):** **one consolidated block per root** when the root is a single orchestrator (one top-level `module` the entrypoint calls — `module.main`/`module.scaffold`, the common case): scope it to that top-level module and fold its sub-modules' roles into the four parts. **One block per top-level module** only when the entrypoint calls _several independent_ top-level modules. **Never one-per-sub-module** — it fragments the architectural story and bloats the doc. Every clause must trace to a Phase-2 edge or an HCL line you read — a prose _rendering of evidence already collected_, **not** generic provider/security commentary or architectural opinion (that trips the skill's own litmus test). No grounding edge → omit the clause; never guess a dependency or a purpose.

Detailed evaluation rules + worked examples: `reference/heuristics.md` → _Name resolution_, _Secrets_, and _Module provenance & architectural-role rendering_.

### Phase 2 — Producer relationship map

- Build a **repo-wide producer index** for every resource across all roots and every
  source-resolved module. Key by `(provider source/type, resolved provider configuration,
  account/subscription/project, region, resolved-or-templated name)` and retain producing
  root/module as provenance. Unknown context stays explicit. A name-only or type+name match
  is merely a candidate and cannot merge producers from different provider contexts; the
  retained root distinguishes same-root from cross-root matches.
- For each `data` source, hardcoded external ID, and cross-resource reference, resolve its key and classify into **exactly one** of:
  - **Internal same-root dependency** — the evidenced producer belongs to this root, including its child modules. Record the local edge without claiming a cross-root dependency.
  - **Internal cross-stack dependency** — a producer exists in _another root_ (or a shared module another root owns). Document it as a dependency edge (consuming root ← producing root/module). **Not** "external".
  - **Out-of-band / external** — no producer anywhere, even after following the chain across roots. Confidence is raised by corroborating signals: explicit ownership comments (`# created by <team>`), naming-convention divergence from this repo's scheme, a different RG / subscription / account / project.
  - **Indeterminate** — a producer plausibly lives inside an unresolved private/remote module. **Do not call this external.** Flag it and request the module (Phase 3).
- Harvest adjacent code comments as first-class evidence. Every item records: classification · reasoning · confidence · evidence (`file:line` + quoted comment).

Algorithm + worked examples (incl. a real multi-root case where `data` in one root is produced by another, and one that is genuinely out-of-band): `reference/heuristics.md` → _External vs cross-stack_. The producer index + edges built here are the **sole evidence source** for Phase 1's per-module _Role in this architecture_ block: that narrative renders these edges in prose — it never introduces a dependency or purpose not grounded in an edge or HCL line captured here.

### Phase 2.5 — Live-state cross-check (read-only cloud CLI, opt-in)

Static HCL establishes declared state. A provenance-bound supplied saved plan can establish planned state; supplied applied-state/run evidence can establish what was applied at its recorded time. Neither alone proves current live access. When a read-only cloud CLI is available, offer a scoped live check within the user’s authorization; preserve unknowns if it cannot run.

- **Probe:** `az account show` / `gcloud auth list` / `aws sts get-caller-identity`. Absent or unauthenticated → mark unsupported axes `unknown`, noting the missing evidence; preserve any separately supplied, provenance-bound planned/applied evidence with its date. Authentication alone does not verify effectiveness. Present → offer the read-only cross-check.
- **Resolve names:** confirm the best-effort resolved names from Phase 1 against the live estate (e.g. `az resource list -g <rg> -o json`). Inferred → verified.
- **Close unknown matrix axes:** for each row, seek read-only live evidence of deployment
  and effectiveness — SP app-role grants, role assignments on the producer, group membership,
  auth mode, and access. Update `Deployment` to `applied` and `Effective` to `verified` or
  `proven failure` only from the observed result; otherwise retain `unknown` and record why.
- **Detect deployment status (the finding class HCL cannot reach):** resources **in the cloud but not in HCL** (out-of-band drift → Q3) and resources **declared/merged but not yet applied** (an orchestrator apply lagging the PR merge — **merged ≠ applied**). Both belong in the doc, not in the agent's head.
- **Emit a per-env `Live verification` block** summarizing what was confirmed/flipped, with `[az ✓]` tags inline in the matrix.

**Guardrails (unchanged):** read-only only — never `apply`/`plan`/mutating `init`, never a write, **caution on prod reads**. **Windows caveat:** `az --query` (JMESPath) is mangled by the `az.cmd`/Windows shell bracket re-parse — default to `-o json` + client-side filtering (`ConvertFrom-Json` / the POSIX shell runner with single-quoted JMESPath), never `--query "[?…]"`. **Paginate or it didn't happen:** Graph `appRoleAssignedTo` pages at 100 (page 1 can be all User-type rows) — always `$top=999` + follow `@odata.nextLink`; `az appconfig feature list` needs `--all`. Never flip a matrix row or assert absence from an unpaginated read — one inverted a doc's staging status in 9 places. An empty first page is a prompt to prove the probe sees anything at all (positive control), not a finding.

### Phase 3 — Private/remote module resolution (convention-agnostic)

- Classify each module `source` by **shape only**: local · public registry · private registry (`<host>/<ns>/<name>/<provider>`) · git (`git::`, `github.com/…`) · archive/other.
- Local → trace directly. Public registry → resolve semantics from registry/provider docs. Private / git / unresolved → it may hold real resources **and producers needed for Phase 2**. **Before treating a private source as unavailable, test readability:** file, search, and git capabilities often resolve an absolute sibling path (e.g. `<repo-parent>/terraform-<provider>-<name>`) **even when it was never added as a workspace dir** — file enumeration or `git -C <path> tag --list` on the proposed location is a 1-call check. "Not `/add-dir`'d" ≠ "unavailable". Only if that genuinely fails: **ask the user** whether they can add the source; you may _propose_ a likely location but **never assume a client-specific name→path convention** — it varies per engagement. Once readable, re-trace and backfill Phases 1–2.
- Record package identity separately from module identity: normalized source package/repository,
  package subdirectory, version/ref, resolved content revision/digest, and resolution status.
  Multiple subdirectories can be distinct modules in one repository; a local child is a real
  provenance leaf even without a remote source/version. Registry/provider documentation can
  establish semantics only: use `semantics-only` until the pinned module body is readable, and
  never inventory resources from registry prose. Use `source-resolved` only for inspected body
  bytes, or `unresolved-pending-user` when unavailable.

### Consolidation (coordinator)

Consolidate worker outputs by evidence coverage and unresolved conflicts. First
build the estate-fact ledger: bind every whole-estate value to Source ID/path/hash from the
Source Evidence record and compare it across workers/docs. Resolve divergence by re-reading
those exact bytes, never by recency or majority, then rebuild overview from reconciled facts.
Critical disagreement on topology, name, external/cross-stack classification, or ledger fact
returns to the user before continuing.

### Confidence gate (≥ 95%)

Report confidence using the loaded policy, grounded in provider documentation, resolved input
coverage, topology, and dependencies. Unknown values and unreadable bodies remain explicitly
partial; they do not prevent a useful authorized declared-topology draft. A load-bearing conflict
blocks only the dependent conclusion until source inspection or an owner answer resolves it.
Do not ask for generic permission to write an already authorized document. Never turn a score
into evidence or authorization. Deployment/effectiveness remain unknown without their own evidence.

## Mandatory rules

1. **Inspect it.** No assumption justified by "I didn't inspect file X / didn't check the docs / didn't open module Y". Inspect the HCL and the docs until you can answer — or state precisely why it's unresolvable, with a confidence score.
2. **Official docs via context7 / websearch.** Resource semantics ("what is this / its role") come from provider docs (context7 first, then websearch), not recall.
3. **Private modules → inspect, then ask for missing access.** Try the Phase-3 readability checks before declaring a source unavailable; a readable sibling need not be a workspace root. If the source remains unavailable, ask the user to provide access; never bake in a naming convention. **Indeterminate ≠ external.**
4. **Secrets: names only, never values.** Hard rule.
5. **Infrastructure/source is read-only; documentation output is writable.** Never
   `apply`/`plan`/`destroy`/`import`/mutating `init`; never edit `$repo_path` or an added
   module source. Write only generated Markdown beneath resolved `$output_dir`, which may be
   inside or outside the source repository. Optional `terraform show -json` is allowed only
   against a user-supplied state file, never automatically or against prod. Inspection-only
   cloud queries are allowed after the Phase-2.5 prompt. Record source identity and actual
   bytes under the documentation evidence contract; a short HEAD is display-only.
6. **Topology first, no parity assumption.** Detect each root's env axis independently; document asymmetry explicitly.
7. **Don't couple to any example repo.** The reference file's worked examples are illustrative only; the methodology must hold for any layout (Terragrunt, TFC/Spacelift, workspaces, flat single-root).
8. **Whole-estate facts: resolve once from identified source bytes.** Bind each ledger fact
   to the per-source revision + manifest in Source Evidence, including dirty root HCL and
   independently changing sibling modules. Never use the root repository SHA to identify a
   sibling module. The overview rolls up reconciled per-environment facts. Any contradiction
   is a correctness STOP; re-read the identified bytes rather than choosing by recency.
9. **Permissioning & integration: keep evidence axes separate.** For every link/grant,
   record `Declared` (`present` / `ineffective` / `missing` / `indeterminate`), `Deployment`
   (`applied` / `planned` / `unknown`), and `Effective` (`verified` / `proven failure` /
   `unknown`) with evidence type + file/live locator. HCL can establish declared wiring and
   whether it matches declared auth mode; it cannot prove deployment or live effectiveness.
   Missing credentials or an unrun probe is `unknown`, never failure. Only observed runtime/live
   denial or failed use is `proven failure`; statically incompatible wiring is `Declared:
   ineffective` with Effective still unknown. Separate deploy-time/runtime identities and verify
   security edges first-hand. Merged is not applied.

## Output structure

Two things ship: an **overview** and **per-(root, environment) inventory** docs. The layout
below is the current (`v4`) shape. The stable contract must not change shape without a
Schema bump.

### Stable contract (do not change shape without bumping `Schema`)

- Every produced doc opens with an audit **Summary** table: `Created` · `Last Updated` ·
  `Generated From` (primary root's short SHA, display only) · `Schema` (`v4`) · `Scope`
  (`overview`, or `<root>/<env>`) · `Source Root` · `Docs Root`.
- Every doc carries **Source Evidence** under the documentation evidence contract: one row
  per independently changing repository/module with public-safe Source ID, source/package +
  subdirectory identity, full revision, trace boundary, relevant staged/unstaged/untracked
  paths, and sorted-manifest SHA-256. Dirty root HCL is recorded as dirty content, never hidden
  behind HEAD. An unreadable sibling source is explicitly Unverifiable.
- Every produced doc ends with a machine-readable **Source Files** table — every `.tf`,
  `.tfvars`, Terragrunt, provider, lock/version, and orchestration/configuration path actually
  read for that doc, one row each with `Source ID · Role · Path · SHA-256`. History may
  shortlist drift; only actual bytes + relevant dirty/boundary checks establish freshness.
- Every produced doc ends with a **Change Log** table. First generation: `Created` = `Last Updated` = today + one initial row. Update: keep `Created`, bump `Last Updated`, advance `Generated From`, append one row.
- `[TODO: verify]` for anything unconfirmed. If git is unavailable, use
  `Generated From: unknown`, record available byte hashes, and mark revision-based freshness
  Unverifiable without blocking useful declared-topology documentation.
- Every per-(root,env) doc carries an **Integration & permissioning (incident-triage)**
  matrix with `link/grant · mechanism · identity · target · exact role/perm · Declared ·
  Deployment · Effective · Evidence`. Deploy-time and runtime identities are distinct rows.
  Overview/on-ramp surface `proven failure`, then important `unknown` cells with the evidence
  needed to close them. Unknown is never rendered as broken.
- The doc-set MUST answer these three questions (overview answers Q1 — incl. the newcomer on-ramp — + a Q3 summary; per-env docs answer Q2 + the Q3 detail for that env):
  - **Q1 — What infra is declared, and how do the pieces fit?** Roots, each root's real env axis, inter-root dependency order, backend evidence, external systems, component counts, module inventory/resolution, and a short top-down on-ramp + one-line component role catalog. Every count reconciles with an explicit enumeration. Keep **package repositories**, **module source addresses/subdirectories**, **source@version pairs**, and **files** as separate quantities: several module subdirectories/wrappers may share one repository, and one source may be pinned at several versions. State the reconciliation whenever counts differ; never assume a one-to-one mapping.
  - **Q2 — Per environment, every declared resource:** resolved name (+ template + confidence), **provenance chain** (entrypoint → local wrapper(s) → source package/subdirectory@version or local leaf → resource) with the originating-hop tag (`[entry]`/`[wrap]`/`[local]`/`[priv]`), what it is, its provider-level role, external/cross-stack association, source `file:line`. Planned/applied status is added only when evidence exists. Each per-env doc also carries (i) a **module-provenance tree** near the top — the call skeleton with per-hop source shape + version/content identity + explicit wrapper→private hop; instance multiplicity shown as `(×N)` / `(count=expr=N)`, never `[N]` — (ii) a fenced **Role in this architecture** block rendered strictly from Phase-2 evidence — and (iii) the Rule-9 evidence-axis matrix.
  - **Q3 — What is likely handled outside Terraform?** Each item classified `same-root` / `cross-stack` / `external` / `indeterminate`, with reasoning, confidence, and evidence.

### v4 layout (iterate freely; the contract above stays fixed)

- `$output_dir/overview.md` — opens with the **Q1 on-ramp** (layer-story narrative + component role catalog) _before_ the Q1 tables, so a reader unfamiliar with the estate gets the shape first.
- `$output_dir/<root>/<environment>.md` — one per real pair. Each carries Summary,
  Source Evidence, entrypoint, provenance tree, declared-resource table, Role block(s), the
  evidence-axis matrix, Q3, Secrets, Source Files, and Change Log.
- **Schema history:** `v1` inventory; `v2` provenance/role/on-ramp; `v3` original
  trichotomous permission matrix; `v4` bounded multi-source byte identity plus separate
  declared/deployed/effective axes. Any older→v4 change is full regeneration, not an
  incremental bump; preserve the old set until the v4 output is reviewable.

### What this documentation IS / IS NOT

**IS:** a resolved-name inventory grounded in actual HCL + provider docs · explicit
declared/planned/applied/effective evidence states · a full module-provenance chain per
resource (entrypoint → wrapper → source package/subdirectory@version or local leaf) · a
role narrative rendered from observed wiring · bounded multi-source freshness · honest
confidence and external/cross-stack/indeterminate classifications.

**IS NOT:** a redesign or recommendation · a role narrative that asserts purpose/dependency **not** traceable to a captured edge or HCL line (generic "this is a standard secret store following security best practice" prose is banned — cite the consumer or omit the clause) · `terraform plan` output you didn't observe · guessed names presented as facts · the naive "every `data` source = external" · secret values · anything coupled to one example repo's module-naming convention.

**Bad (shape-matched, unresolved, naive):** "Standard Azure setup across dev/test/staging/prod — the usual key vaults and container apps; the `data` sources pull in external resources."

**Right (resolved, grounded, with provenance):** "`module.key_vault[0]` (`terraform/modules/scaffold/main.tf:157`, `count = length(var.regions)` = 1 for dev → `centralus`) → `azurerm_key_vault`, resolved name `acme-d-cus-…-kv` (confidence 92% — `environment` & `regions` are literals in `environments/dev/main.tf`; instance suffix from a `var` default). Provenance: `environments/dev/main.tf` → `module.main` `[wrap]` (local `../../modules/scaffold`) → `module.key_vault` `[wrap]` (local `../key_vault`) → `[priv]` `<host>/<ns>/key-vault/azurerm@4.2.0` (local clone the user added) → `azurerm_key_vault.vault`. The `[wrap]` layer adds the admin group + RBAC role assignments _on top of_ the private module's vault. Provider-level role: app secret store, RBAC-auth (azurerm docs). `data.azurerm_container_app_environment.shared` (`:101`) → **cross-stack**: produced by the `shared` root's `container_app_environment` module (confidence 95%). `data.azurerm_subnet.cae` (`:107`) → **external/out-of-band**: no producer in any root; the `shared` root itself reads the VNet via `data`; comment `# created by cloud engineering team` (`:84`) corroborates (confidence 88%)."

**Role-block — Bad vs Right** (the new failure mode to guard against):

- **Bad (generic, ungrounded):** "Role in Acme: the Key Vault is a critical security component storing application secrets per landing-zone best practice."
- **Right (every clause traces to an edge, permission effectiveness checked):** "**Role in Acme** — _Provides:_ per-app-environment secret store. _Consumed by:_ the web Container App at runtime — Terraform writes the 6 `AzureAd--*` app-reg secrets here (`container_app/main.tf:NN`); the app's data-plane **read** is a separate grant, see the Integration & permissioning matrix (status there, **not asserted here** — on this `enable_rbac_authorization=true` vault an access policy would be inert, so the matrix shows whether a `Key Vault Secrets User` role assignment for the app MI actually exists). _Blast radius:_ web app cannot start without it. _Posture:_ `default_action=Deny` + RBAC-auth + `purge_protection=true` — Tier-1 PII subscription (`scaffold/main.tf:147-149`)."
  > Note how the role block now **defers the app→KV access claim to the permissioning matrix** instead of asserting "KV Secrets User" inline — the original wording here modelled the exact failure Rule 9 forbids (asserting a grant from a wiring input without the auth-mode effectiveness check).

## Output file

Write `overview.md` and per-(root, env) docs under resolved `$output_dir`. Resolve blocking facts before dependent conclusions; write the authorized bounded draft. On same-schema reruns preserve Created, update only changed docs, refresh
Source Evidence/Source Files, and append one Change Log row. A schema change is a full
regeneration with a new Created date and a row naming the prior schema. If output is ambiguous,
ask. Never edit Terraform/module source, even when output is elsewhere.
