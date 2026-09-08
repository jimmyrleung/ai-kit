# Astra review walkthrough backlog — 2026-09-07

Status: conceptual walkthrough complete; **WB01–WB03 execution authorized on 2026-09-07**.
Owner instruction: “agree, let's consolidate all of that in the walkthrough backlog and
start a new goal to address all of them”. This supersedes the earlier execution deferral.
Preserve existing uncommitted work and historical evidence. Do not commit or publish.

| Item | Outcome | Status |
|---|---|---|
| WB01 | Self-contained skill folders generated from maintained shared rules | Done; ready for owner review |
| WB02 | Concise descriptions with preserved selection boundaries | Done; ready for owner review |
| WB03 | Explicit, self-contained confidence scoring and gate guidance | Done; ready for owner review |

Execution order: capture the current baseline; design the packaging and confidence contracts;
implement WB01/WB03 together where references overlap; revise descriptions under WB02;
run focused behavior checks, repository validation, independent review, and final QA.
Completion means all items have recorded acceptance evidence or an explicit owner-accepted
limitation, and the uncommitted result is ready for owner review. Existing deferred hosted CI
and unavailable provider checks retain their recorded scope; they cannot become fabricated PASS.

This document records decisions and follow-ups from the walkthrough of the
[Astra implementation](20260906_astra_review_execution.md). The
[original backlog](20260906_astra_review_backlog.md) and its review evidence retain their
historical scope. Append further walkthrough items here with stable `WB` identifiers.

## WB01 — Make distributed skills self-contained

Status: **Done — locally verified and independently reviewed; owner GO pending.**

### Owner decision and rationale

The owner prefers each skill to contain its supporting instructions, so installing an
individual skill does not require manually copying shared documents from elsewhere in
the ai-kit repository.

The proposed direction was: maintain shared source rules, generate the needed copies
inside each skill's `references/` directory, and check that those copies remain current.
The owner accepted that direction: “agree with your preference”. The owner then requested
this backlog “to act on after the walkthrough, do not dispatch it yet”.

### Pre-execution behavior to change

The [installation instructions](README.md#install-and-synchronize) require the full checkout
because skills reference shared `docs/contracts/` files. The
[skill policy](docs/contracts/skill-policy.md#semantic-guidance) likewise requires detached
copies to bundle dependencies. The current symlink installation exposes checkout edits
directly, but does not package those external dependencies into individual skill folders.

### Intended outcome

- Keep one maintained source for common rules.
- Generate the supporting rule documents inside each affected skill folder and make its
  references resolve locally, including dependencies referenced by those documents.
- Keep the generation/check mechanism small and consistent with the existing repository
  tooling. Generated copies must be clearly identified so edits go to the maintained source.
- Explain the update process for maintainers and individual-skill users, including when
  generation is needed and how it relates to the existing symlink installation.

### Acceptance to verify after implementation

- An affected skill copied to an isolated location can resolve its required supporting
  documents without the original checkout or manual dependency copying. Verify both file
  resolution and a representative agent task; distinguish those results.
- Changing a maintained shared rule updates every affected generated copy; an unchanged
  generation run leaves the output unchanged.
- The normal validation path detects stale or missing generated dependencies.
- Existing whole-checkout installation remains supported, and installation/authoring
  guidance describes the resulting packaging and update workflow consistently.

### Design questions recorded before execution

At execution time, inspect the actual dependency graph, choose the generation trigger and
output mapping, and resolve transitive references. The shared-source location and command
interface are not yet designed. This item does not authorize unrelated changes to skill
behavior or a new general-purpose packaging framework.

Confidence: 97% in the recorded direction and current installation behavior. Remaining
uncertainty concerns the dependency mapping and generation design, to resolve during execution.

## WB02 — Tighten skill descriptions without losing selection boundaries

Status: **Done — locally verified and independently reviewed; owner GO pending.**

Owner rationale: expected a substantial cut in frontmatter/descriptions and asked whether
the current result was sufficiently concise. The owner accepted a focused conciseness pass
after reviewing the measured results; no arbitrary percentage reduction was requested.

Baseline measured during this session against `aeec06b` using directory enumeration and
parsed YAML descriptions across the same 31 skills: descriptions 17,663 → 16,694 characters
(−5.49%); complete frontmatter 19,201 → 18,232 (−5.05%); bodies excluding frontmatter
364,106 → 401,713 (+10.33%, excluding external references). Fifteen descriptions were
unchanged and ten exceeded the maintained policy's 600-character review target. These are
character counts, not token usage or proof of discovery quality. Recapture before editing.

### Intended outcome and acceptance

- Prioritize purpose, user trigger phrases, relevant inputs, and distinctions from neighboring
  skills. Move procedural plumbing and historical explanations out of descriptions while
  preserving necessary behavior in the body or appropriate local reference.
- Inspect all canonical descriptions; justify retained length where useful selection context
  requires it. Preserve valid provider metadata and explicit-invocation settings.
- Record before/after description and frontmatter measurements. Keep body/reference size
  separate; do not report relocated text as eliminated runtime context or measured cost savings.
- Check representative positive, neighboring, and non-trigger requests using fresh reviewers
  with the competing descriptions. Record prompts, expected selections, actual results, and
  limitations; roster simulation is not native discovery.
- Run the shipping metadata/portability checks. No broad analyzer rewrite or unproven
  simplification adoption is included in this item.

## WB03 — Restore explicit, portable confidence assessment

Status: **Done — locally verified and independently reviewed; owner GO pending.**

Owner rationale: confidence scores are useful, and merely saying “report confidence” may
not reproduce the desired assessment. The owner accepted restoring explicit guidance while
retaining the evidence and authorization safeguards discussed in the walkthrough.

### Intended outcome and acceptance

- The main spec-driven skills provide an explicit 0–100 confidence assessment, a suitable
  factor rubric, evidence supporting the score, remaining uncertainty, consequences, and
  the next check. Do not depend on the owner's private instructions for the default format.
- Restore workflow-appropriate calculation guidance (analysis previously used requirements,
  codebase/constraint understanding, and change-path clarity; techspec used docs, patterns,
  data flow, complexity, and cross-system impact). Reconcile shared defaults and caller
  overrides explicitly; retain stricter applicable user requirements.
- Define threshold behavior and carry the effective policy into workers and downstream gates.
  A high score cannot waive missing required evidence, failed checks, or authorization.
  Explain what a low score blocks and what independent work remains permitted.
- Keep severity, certainty, and causal evidence distinct. Do not use numerical worker
  agreement as proof or present heuristic scores as calibrated success probabilities.
- Bundle required scoring references under WB01. Check representative analysis/spec/task
  outputs without private confidence instructions, plus an explicit stricter override and
  an unresolved critical-evidence case. Record results and reconcile affected skill guidance.

### Owner acceptance scope

The latest “agree” accepts WB02 and WB03 as follow-ups and authorizes execution of all three
items. It does not grant final approval of their eventual implementation or permission to commit.

## Walkthrough agreements — 2026-09-07

The entries below preserve the original discussion and deferral history. The current
execution authorization at the top supersedes their earlier scheduling constraints.

### Step 2 — Review, verification, and completion

Owner response: “agree with all these”. Accepted conceptual direction:

- Review all intended change layers within an explicit scope.
- Bind review and verification evidence to the actual content and relevant dependencies.
- Verify exact task criteria and reuse executed checks only when their relevant inputs match.
- Scale independent review to risk and distinguish severity from certainty.
- Separate repository completion, operational completion, and accepted limitations.

No new implementation follow-up was requested for this step. This agreement concerns the
explained approach; it is not aggregate implementation GO, a commit instruction, or permission
to start WB01. All walkthrough implementation work remains deferred.

### Step 3 — Authorization and discussion cadence

Owner response: “yep agree with this one too”. Accepted conceptual direction:

- Continue work within existing authorization without repeated routine permission questions.
- Ask for missing consequential facts, scope boundaries, and decisions reserved for the owner.
- Preserve recommendation-only requests, deferred execution, and the requested discussion pace.
- Do not infer authorization from confidence scores or agreement between agents.

No new implementation follow-up was requested. Final implementation approval and all deferred
walkthrough work retain their existing boundaries.

### Step 4 — Documentation locations, freshness, and infrastructure evidence

Owner response: “agree”. Accepted conceptual direction:

- Carry explicit source, workspace, and documentation output locations through handoffs.
- Classify freshness as Current, Stale, or Unverifiable using actual sources and controlling
  inputs; preserve Current documents and retrace where the evidence is insufficient.
- Separate declared infrastructure, deployment evidence, and observed effective access.
- Perform these checks when the documentation skills run; no automatic background refresh
  was introduced.

No new implementation follow-up was requested. Agreement covers the explained approach;
deferred execution and final implementation approval remain unchanged.

### Step 5 — Feedback, memory, and improvement continuity

Owner response: “agree”. Accepted conceptual direction:

- Resolve configurable recording while supporting the existing store and preserving explicit
  user-required recording gates.
- Treat observations as selected feedback, separate from measured invocation counts.
- Identify sessions/runs, deduplicate nested observations, and distinguish started from completed
  recording so close and harvest can resume or repeat safely.
- Keep unresolved improvements and predictions reachable independently of the discovery watermark.
- Preserve decision authorship and supersession history; stage improvements for owner review.

No new implementation follow-up was requested. Agreement covers the explained approach;
deferred execution and final implementation approval remain unchanged.

### Step 6 — Provider compatibility, tooling, and evaluation

Owner response: “sounds good”. Accepted conceptual direction:

- Resolve capabilities from the active host/tools and disclose unavailable or weaker alternatives.
- Strengthen inventory, metadata, link, sync-diagnostic, and copied-instruction drift checks.
- Distinguish structural validation, native discovery, agent task outcomes, and owner judgment.
- Preserve failed/confounded trials; retain the original analyzer structure without claiming
  unproven simplification or efficiency benefits.

The planned conceptual tour is complete. No additional implementation follow-up was requested
for this step. Existing provider/platform limits and final implementation approval remain separate.

## Walkthrough closeout

| Step | Topic | Disposition |
|---|---|---|
| 1 | Skills, shared docs, and tests | Packaging direction revised; WB01 agreed and deferred |
| 2 | Review, verification, and completion | Conceptual direction agreed |
| 3 | Authorization and discussion cadence | Conceptual direction agreed |
| 4 | Documentation locations and freshness | Conceptual direction agreed |
| 5 | Feedback and memory continuity | Conceptual direction agreed |
| 6 | Provider compatibility, tooling, and evaluation | Conceptual direction agreed |

Next implementation item: WB01, after an owner instruction to begin. No code changes,
implementation delegation, or commits were performed during this walkthrough; only this
backlog and its agreement records were written. Earlier execution evidence retains its scope.

## Execution handoff — 2026-09-07

WB01–WB03 implementation and current verification are recorded in
[the walkthrough execution record](20260907_astra_review_walkthrough_execution.md).
The closeout paragraph above describes the earlier walkthrough stopping point, not current
authorization or implementation status. The original Astra records remain historical.

### Fresh review correction — 2026-09-07

F1 is fixed and independently rechecked: Markdown title syntax and next-line destinations no
longer cause required bundled dependencies to be overlooked. Regression and repository checks
pass. The original multiline fixture's trailing-period mistake is explicitly corrected in
the evidence; the valid single-title finding is closed. See the
[correction record](20260907_astra_review_walkthrough_execution.md#fresh-review-correction--2026-09-07)
for current source/check identities and routing-provenance limits. WB01–WB03 acceptance criteria
are unchanged; owner GO and existing provider/platform boundaries remain pending as recorded.
