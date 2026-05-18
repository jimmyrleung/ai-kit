# document-terraform — Resolution heuristics & worked examples

Progressive-disclosure reference for `SKILL.md`. The SKILL body owns the methodology; this file owns the gnarly detail and the worked examples. **The worked examples use a single synthetic landing-zone repo (an anonymized 3-layer Spacelift/Azure estate) purely to illustrate the heuristics — the skill must NOT be coupled to any layout.** A Terragrunt / TFC / flat-single-root repo exercises the same heuristics with different surface shapes.

---

## Name resolution

Goal: for each resource, emit **both** the raw name template and a best-effort resolved value, each with a confidence score. Never present a guess as a fact; never invent a value you couldn't derive.

### Evaluation order (per environment)

Resolve `var.*` and `local.*` referenced in a `name =` expression by walking, in priority:

1. **Literal arguments at the environment entrypoint.** Thin env wrappers usually pass naming inputs as literals — e.g. `environment = "dev"`, `regions = ["centralus"]` in `environments/dev/main.tf`. These are the highest-confidence source.
2. **`*.tfvars` / `*.auto.tfvars`** for that environment.
3. **Variable `default`s** in the consuming module's `variables.tf`.
4. **`locals`** — evaluate maps and interpolations using the values resolved above. Lookup maps (`local.environment_map[var.environment]`) resolve fully once their key resolves.

A segment you cannot resolve at any tier (orchestrator-injected at runtime, sensitive, computed from an unavailable module) is rendered verbatim as `<var.NAME>` / `<unresolved>` in the resolved value, and the confidence drops accordingly. **Do not** substitute a plausible-looking value.

### Confidence bands for a resolved name

- **90–100%** — every segment resolved from literals / tfvars / defaults + provider-doc-confirmed naming rules. (Typical for structural resources in a thin-env-wrapper repo: env + region are literals.)
- **70–89%** — resolved, but ≥ 1 segment came from a `default` that an env _could_ override, or a provider name-mangling rule (truncation, lowercasing, no-hyphens) you applied from docs but couldn't observe applied.
- **< 70%** — ≥ 1 segment is `<unresolved>`; show the template and the partial value, list exactly which segment is unknown and why.

### Provider name-mangling

Many provider resources mutate the requested name (lowercase, strip hyphens, length cap, append a generated suffix). Confirm the rule from provider docs (context7 → websearch) and apply it to the resolved value; note in the row that the mangling was doc-derived, not observed. Example: an Azure Container Registry name `acme${env}${region}containers1cg` is already lowercased/hyphen-free _by design_ because the author knew the ACR rule — surface that.

### `count` / `for_each` expansion

One logical block → N rows. Record the expansion factor and index basis:

- `count = length(var.regions)` with `regions = ["centralus","eastus2"]` → emit `[0] centralus`, `[1] eastus2` as separate resolved rows.
- `for_each = var.kv_entries` → one row per key; the **key** is in scope for naming (`each.key`), the **value** is a secret (see _Secrets_).

---

## Secrets

Hard rule: record **key names + value-source class only. Never resolve, read, or print a value.**

For secret-bearing constructs (secret-store entries, `*_secret` resources, secret maps fed via `for_each`):

| Capture                                                                 | Don't capture               |
| ----------------------------------------------------------------------- | --------------------------- |
| Secret key name (`ExternalAcmeApi--Key`)                                | The secret value            |
| Value-source class: `from var` / `from resource output` / `hardcoded ⚠` | The resolved variable value |
| The store it lands in (resolved name + confidence)                      | —                           |

`hardcoded ⚠` is itself a finding worth surfacing (a literal secret in HCL is a smell). `from resource output` (e.g. a connection string assembled from another module's output) is documented as a _dependency_, not a value.

Worked: `kv_entries = merge(var.kv_entries, { "AzureServiceBus--FullyQualifiedDomainName" = "${module.service_bus[count.index].name}.servicebus.windows.net" })` → list key `AzureServiceBus--FullyQualifiedDomainName`, class `from resource output` (depends on `module.service_bus`), plus "+ N keys from `var.kv_entries` (orchestrator-injected, values out of scope)". Never attempt the values.

---

## External vs cross-stack (producer index + 3-state)

Replaces the naive "every `data` source = external". A `data` source frequently points at a resource **another root in the same repo creates**, or at one inside a **private module not yet loaded** — neither is "external".

### Build the producer index

Across **all roots** + **every resolvable private/remote module**, index every `resource` block by `(provider type, resolved-or-templated name)`. Templated keys (where a segment is `<var.x>`) match other templates structurally; resolved keys match exactly. Keep the producing root + module + `file:line` on each index entry.

### Classify each consumer (3-state)

For every `data` source / hardcoded external ID / cross-resource reference, resolve its lookup key and pick exactly one:

1. **Internal cross-stack** — producer found in _another root_ (or a shared module another root owns). Output a dependency edge `consuming-root ← producing-root/module`. This is the most commonly _mis_-classified case — check the index before ever writing "external".
2. **Out-of-band / external** — no producer anywhere, even after following the chain across roots. Raise confidence with corroborating signals (below).
3. **Indeterminate** — a producer plausibly lives inside an unresolved private/remote module. **Not external.** Flag, and trigger Phase 3 (ask the user to add the module). Re-classify once available.

### Corroborating signals (raise/lower confidence on "external")

- **Explicit ownership comment** adjacent to the `data` block — e.g. `# created by cloud engineering team`. Strongest single signal; quote it as evidence.
- **Naming-convention divergence** — the looked-up name uses a prefix/scheme this repo's resources never produce (a different env-abbreviation, a platform prefix).
- **Different RG / subscription / account / project** than anything this repo creates.
- **Chain termination** — follow the producer chain across roots; if even the "closest" root _also_ reads it via `data`, it's external at the platform level (see worked example 3).

### Worked examples (illustrative — do not couple)

**1 — Cross-stack (mis-classified by the naive rule).** `terraform/modules/scaffold/main.tf:119`: `data "azuread_group" "image_pull"` with `display_name = "${acr}-image-pull"`. Producer index hit: `shared/modules/container_registry/main.tf:24` _creates_ a group with display name `"${module.container_registry.name}-image-pull"`. → **cross-stack**, edge `terraform ← shared/container_registry`, confidence 95%. The naive rule would have wrongly called this external.

**2 — Cross-stack via identity.** `terraform/.../scaffold/main.tf:128`: `data "azurerm_user_assigned_identity" "ado"` (`ADO-${principal}-LZ`). Producer: `shared/modules/ado_connections/main.tf:30` creates `name = "ADO-${principal_name_underscored}-LZ"`. → **cross-stack**, confidence 95%.

**3 — Genuinely out-of-band.** `terraform/.../scaffold/main.tf:107`: `data "azurerm_subnet" "cae"` on VNet `acme-${vnet_prefix}-…-1-vnet`. No producer in `terraform/`. Follow the chain: the `shared` root (`shared/modules/scaffold/main.tf:88`) _also_ reads that VNet via `data` — the chain terminates with no producer in any root. Corroborated by `terraform/.../scaffold/main.tf:84` comment `# acme resource groups - created by cloud engineering team`. → **external / out-of-band**, confidence 88% (chain-terminated + ownership comment; not 100% because a platform-team repo we can't see could still be Terraform-managed elsewhere).

**4 — Indeterminate.** A `data "X"` whose only plausible producer is inside `<host>/<ns>/networking/azurerm` (private module, not in workspace). → **indeterminate**, confidence n/a; emit "producer likely in private module `networking` — add it to confirm (Phase 3)". Never label external.

---

## Module source-shape classification (convention-agnostic)

Classify by the `source` string's shape; resolution differs per class. **Never** hardcode a client's `registry-name → local-path` convention — ask.

| Shape            | Example                                                  | Resolution                                                                                                                                        |
| ---------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Local            | `../key_vault`, `./modules/x`                            | Trace directly in-repo.                                                                                                                           |
| Public registry  | `terraform-aws-modules/vpc/aws`                          | Semantics from registry/provider docs (context7 → websearch).                                                                                     |
| Private registry | `<host>/<ns>/<name>/<provider>` (e.g. a `*.io` host)     | May hold real resources + Phase-2 producers. Ask the user to add the source; _propose_ a likely sibling location but never assume the naming map. |
| Git              | `git::https://…//mod?ref=v1`, `github.com/org/repo//mod` | As private registry: request access; respect the `ref` pin.                                                                                       |
| Archive / other  | `https://…/mod.zip`                                      | Request the unpacked source; otherwise mark `unresolved-pending-user`.                                                                            |

Record per distinct source: the string, the version/`ref` pin, and a status — `resolved-local` / `resolved-registry-docs` / `unresolved-pending-user`. Unresolved private modules make their would-be resources `indeterminate` in Phase 2 — surface that linkage explicitly so the user understands _why_ adding the module matters.

---

## Module provenance & architectural-role rendering

Two Schema-`v2` deliverables. Both are _renderings of evidence already gathered_ (the module call graph + the Phase-2 producer index) — neither introduces a new claim, so neither costs confidence. They exist because the `v1` inventory reads well only to someone who already holds the estate's shape in their head; these make it legible to a newcomer.

### A. The module-provenance chain + tree

**Per resource — the chain.** Walking the tree (Phase 1) you already cross every hop `caller → module "x" → source`. Tag each hop by the source-shape table above:

| Tag       | Hop is                                                                                                                | Means for a resource/`data` emitted here                                                                                                                                                                                                                           |
| --------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `[entry]` | the environment entrypoint **or the single top-level orchestrator module it calls** (`module.main`/`module.scaffold`) | declared at the entrypoint or in the orchestrator body — **including every `data.*` lookup** the orchestrator performs (cross-stack/external/provider-internal reads are `[entry]`, never `[wrap]`) and the orchestrator's own `resource`/`role_assignment` blocks |
| `[wrap]`  | a **local** module that wraps **one specific** private/registry module                                                | glue _that_ wrapper adds on top of _its_ private module (an admin group, an extra role assignment, a `random_*`) — **not** in the upstream body, and **not** the top-level orchestrator (that is `[entry]`)                                                        |
| `[priv]`  | a private-registry / git / public-registry module                                                                     | emitted by the upstream module body itself, at its pinned version                                                                                                                                                                                                  |

The originating-hop tag is the **last** hop that actually declares the `resource`/`data` block. **Pinned cases (deterministic — do not shape-guess):** (1) the single top-level module the entrypoint calls (the orchestrator — `module.main`/`module.scaffold`) is **`[entry]`, not `[wrap]`**, even though it is a local module; `[wrap]` is reserved for a local module that wraps _one specific_ private module. (2) **every `data.*` source is `[entry]`** when declared in the entrypoint/orchestrator — a `data` lookup is never `[wrap]` (it is not wrapper-added glue on a private module). A resource a _specific_ local wrapper adds is `[wrap]` even though its parent chain passes through `[priv]`; a resource inside the upstream body is `[priv]`. This is the "what did the wrapper add vs what came from the module" distinction.

**Render rule (protects the resolved-name tables — do not bloat them):**

- **Full chain once**, in the provenance tree (and, _if_ the layout uses per-module sub-sections, also on the section heading: `### module.key_vault[0] — [entry]→[wrap] local ../key_vault → [priv] key-vault/azurerm@4.2.0`). The single-table layout — common — carries the full chain in the tree **only**.
- **Per resource row:** only the one-token tag (`[priv]`/`[wrap]`/`[entry]`) in an `Origin` column. Never repeat the whole chain per row.
- **Once per (root,env) doc:** the **provenance tree** near the top — the call skeleton, the wrapper→private hop on its **own indented line**, `count`/`for_each` multiplicity annotated as `(×N)` or `(count=expr=N)` — **never** `module.x[N]`-as-count: square brackets in the tree mean a Terraform **index** only (matching the resource table), so a multi-instance module is `module.networking.cae_subnet (×2)`, not `…[2]` — and inert (`count=0`) modules marked:

```
environments/dev/main.tf
└─ module.main → local ../../modules/scaffold              [entry] orchestrator: RBAC + wiring
   ├─ module.ad_app_access      → [priv] met-application-security-groups/azuread@2.0.0
   ├─ module.key_vault (×1)     → [wrap] local ../key_vault         (count=len(regions)=1; ×2 in a 2-region root)
   │                              └→ [priv] key-vault/azurerm@4.2.0
   ├─ module.container_app_web   → [wrap] local ../container_app
   │                              ├→ [priv] application-insights/azurerm@4.0.0
   │                              └→ [priv] container-app/azurerm@4.0.0
   └─ module.container_app_pollers → [wrap] local ../container_app_func   ⟂ INERT (count=0)
```

An unresolved `[priv]` hop (private module not in workspace, Phase 3) is rendered `[priv?] <source>@<ver> — unresolved`; its would-be resources stay `indeterminate`, never invented into the tree.

### B. The "Role in this architecture" block

Placement is **Option A** (see Phase 1): **one consolidated block per root** when the root is a single orchestrator (one top-level `module` — `module.main`/`module.scaffold`, the common case), scoped to that top-level module with sub-module roles folded into the four parts; **one block per top-level module** only when a root's entrypoint calls several _independent_ top-level modules; **never one-per-sub-module** (fragments the story, bloats the doc). Fixed four-part shape, every clause carrying a `file:line` or a Phase-2 edge ID — **omit a part rather than guess it**:

> **Role in <estate>** — _Provides:_ <what this component is here>. _Consumed by / Consumes:_ <the exact cross-stack edge / output / `data` source, with `file:line`>. _Blast radius:_ <what cannot function if absent>. _Posture:_ <env-specific stance — PII lockdown / prod tier / region count, with `file:line`>.

The hard fence (this is the failure mode to police — it's the one place this skill flirts with the "redesign/opinion" line its litmus test forbids):

| Allowed (it's evidence)                                                                                 | Banned (it's opinion / recall)                            |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| "Consumed by `module.container_user_web` (`container_user/main.tf:64`)" — a producer-index/Phase-2 edge | "central to the security architecture" — no edge          |
| "web app cannot start without it" — follows from the runtime KV-Secrets-User edge                       | "follows landing-zone best practice" — recommendation     |
| "`default_action=Deny`, Tier-1 PII (`scaffold:147`)" — quoted HCL                                       | "should probably also have a private endpoint" — redesign |

If a component has no consumer edge in the producer index, say so explicitly ("_Consumed by:_ no in-repo consumer found — terminal/told-to-exist") rather than inventing a purpose. The block **renders Phase-2 output**; it never sources a new dependency.

### Worked example (illustrative — do not couple)

`module.key_vault[0]` in `terraform/dev`. Chain: `environments/dev/main.tf` → `module.main` `[entry]` (`../../modules/scaffold`) → `module.key_vault` `[wrap]` (`../key_vault`) → `[priv] key-vault/azurerm@4.2.0` → `azurerm_key_vault.vault`. `azuread_group.admin_group` in the same module is tagged `[wrap]` (the local `../key_vault` body creates it; it is _not_ in the upstream `key-vault/azurerm`), making "what did the wrapper add" answerable at a glance. Role block: `terraform/dev` is a single-orchestrator root (`module.main`), so KV does **not** get its own block — its role folds into the **consolidated `module.main`** block as evidence lines: _Provides_ …KV `acme-d-cus-secrets-1-kv`…; _Consumed by_ the `container_user_web` identity edge (`container_user/main.tf:NN`, a producer-index hit) + Terraform-written `AzureAd--*` secrets; _Blast radius_ web app cannot start without KV/CAE/ACR; _Posture_ `Deny`+RBAC+purge-protection, Tier-1 PII (`scaffold/main.tf:147-149`). Every token traces to HCL or a Phase-2 edge — zero generic commentary.

---

## Whole-estate fact ledger

Some facts are **estate-wide** — they hold across roots/envs and flip _real_ behaviour, so the overview and every per-(root,env) doc must state them **identically**. SKILL rule 8 mandates the ledger; this is the how + the canonical failure.

**What goes in the ledger** (resolve each **once, from HCL, at the `Generated From` SHA**):

- A behavioural `variable` default that gates a whole subtree — an `enable_*`/`create_*` toggle whose default decides whether N resources exist at all.
- The backend / state model, per root.
- Each root's environment axis + per-env region count (the topology rule already forbids _assuming_ parity; the ledger additionally forbids _stating it differently in two docs_).
- Each private/remote module's resolution status (`resolved@tag` / `unresolved-pending` / `tag-absent`) — **and** any "is this materially moot?" claim that _depends_ on a toggle: those two ledger facts must agree (a module is only "moot because `count=0`" if the gating toggle actually resolves off).

**Canonical failure (illustrative — do not couple).** Between two runs the repo's `enable_container_pollers` default flips `false → true` (a `git pull`). The per-env `terraform/dev` worker re-reads `variables.tf` at the new SHA and correctly documents the poller subtree as **active**; the `overview` worker reuses the prior run's "inert / `count=0`" line. Same `Generated From` SHA, two contradictory truths — and it **cascades**: the overview then calls an unresolved `storage@x` pin "materially moot (`count=0`)", while the per-env doc correctly flags it ~55%-unresolved _and now load-bearing_. Root cause: the overview asserted an estate fact **independently, from memory**, instead of deriving it from the per-env source reads.

**The rule.** The overview is a **roll-up**, never an independent source of truth for a ledger fact. Build the ledger from the per-(root,env) source reads, diff every value across workers/docs, and on any divergence **re-read the HCL at the SHA** (never resolve by recency or majority), overwrite all docs, and regenerate the overview _from_ the reconciled facts. An unresolved ledger contradiction is a **correctness STOP**, independent of the numeric confidence score.

---

## Backend / state model

No `backend` block ≠ "no state". Classify per root:

- Explicit `backend "s3|azurerm|gcs|…"` → document the backend resource (bucket/container/key), and whether _it_ is created in-repo or is itself external/cross-stack.
- No `backend` block + an orchestration root / `terragrunt.hcl` / TFC or Spacelift stack definitions → **state is orchestrator-managed**. Document it as such with the orchestrator name and where stacks are defined. This is a first-class answer, not a `[TODO]`.

---

## Common idiosyncrasies to handle (not exhaustive)

State-reconstruction `import` blocks / `imports.tf`; multi-region via `count` + splat (`module.x[*].id`); provider aliasing (`providers = { azurerm.alt = azurerm }`); an orchestration root that provisions the pipelines running the workload roots; hardcoded tenant/subscription/account IDs replicated across providers (flag as config smell + an external-infra anchor); `depends_on` between modules (a dependency edge worth documenting). None of these are special-cased in the SKILL body — they fall out of "read it, resolve it, index it, score it".
