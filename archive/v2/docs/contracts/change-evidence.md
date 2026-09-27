# Change scope and evidence identity

Use this contract for implementation review, task verification, QA, and artifact review.
Repository SHA and dirty status are context, never proof that content is unchanged.

## Resolve scope before inspection

Record repository identity/root, explicit base revision, prefix, task IDs (or named artifact
sections), intended paths, and exclusions with reasons. Resolve a supplied base to a full
revision; otherwise inspect history to identify the work boundary. A merge-base is only a
candidate: confirm it does not silently include unrelated earlier work. Never infer a task
from a fixed history window. An ambiguous base or mixed task ownership needs clarification.
An unborn repository uses the empty tree as base (`git hash-object -t tree --stdin`
with an empty input stream; do not depend on a platform-specific null-device path);
record HEAD as absent. A one-commit repository does not require a parent commit.

Inventory with `git status --short` and a filename-safe untracked enumeration such as
`git ls-files --others --exclude-standard -z`. Inspect content, not only status/stat:

- committed: `git diff --find-renames <base> HEAD` (omit when HEAD is absent);
- staged: `git diff --cached --find-renames HEAD` (use empty-tree base if HEAD is absent);
- unstaged: `git diff --find-renames`;
- untracked: read each in-scope file, including relevant binary/asset content with a suitable
  viewer or decoder; unreadable content is an explicit coverage gap.

Apply the explicit task boundary to each layer. Inspect each intended layer transition once,
including staged content later changed again in the worktree; do not duplicate it by also
reviewing a cumulative diff as new work. Record rename old/new paths and type/mode changes.
Read the resulting files and necessary callers for context. Record out-of-scope changes as
exclusions, not task failures by default; unresolved ownership is a scope gap. A relevant
unexpected file joins scope explicitly. Ignored files are included when named dependencies
or generated artifacts affect the claim; status cannot establish their absence.

## Minimal evidence record (version 1)

Append a uniquely identified run with:

- `record_id`, timestamp, kind (artifact-review/code-review/verification), and verdict;
- repository/source identity and resolved base; exact prefix/task/section/path scope and
  exclusions, including rename mapping and inspected layers;
- a sorted manifest of path, kind/mode, and SHA-256 of actual reviewed bytes (or an explicit
  missing/deleted sentinel); for layered review include each inspected layer's snapshot;
- relevant dependency identities: requirements/AC sections, source/configuration inputs,
  test commands and environment/build identity when results depend on them;
- coverage, command/output references, unresolved gaps, accepted reasons, and follow-ups.

For a section-scoped dependency name its exact stable heading/ID boundaries and hash those
bytes. Use whole-file identity when a safe boundary is unavailable; a relevant change then
requires rechecking. Repository identity must distinguish different repositories even when
paths match; use a public-safe repo identifier, never credentials from a remote URL.

Keep evidence outside hashed subject bytes. When stored inline, place only evidence inside
explicit `<!-- evidence:begin <record_id> -->` / `<!-- evidence:end <record_id> -->` markers
and exclude those exact regions from the subject digest. Log the exclusion rule in the
record. Never exclude requirements, task status/AC definitions, fixes, or arbitrary prose
merely because they sit under a Review/QA heading. Existing unmarked records remain readable
but unverified; do not retroactively manufacture identity for them.

Exclusions depend on the claim's subject. Exclude a review/verification record from the code
or AC bytes that it assesses, but include that record's complete bytes when a later workflow
consumes its verdict, findings, or provenance. A feedback harvest hashes the Verify/QA/review
evidence it consumes and excludes only its own harvest/receipt markers. Record the exact IDs
and kinds excluded; a blanket strip of every evidence block would hide changed findings.

Before reuse, recompute and compare the actual scoped bytes, scope/base, and relevant
dependencies. Compare snapshot bytes across representations: committing identical reviewed
work changes its layer location, not its content. A final-state check may retain coverage
across that commit if its final content, boundary and dependencies match; changed intermediate
content needs a new layer review. A change at unchanged HEAD still invalidates affected
review. Unrelated paths outside the recorded scope/dependencies do not. Adding only delimited
evidence does not invalidate its own subject. A changed reviewed spec invalidates dependent
design/implementation evidence. Missing identity/dependencies or an inaccessible baseline
means unverified; mismatch means stale. Never advance on stale, rejected, Needs revision,
or incomplete evidence. A task-only review covers only its named tasks; prefix review needs
coverage of every repository task and shared integration changes. New runs preserve old
records and identify which earlier record they supersede.

## Reusing executed checks

A passing check may be reused across implementation, verification and QA only when its record
names the actually executed command, exit/result, full required suite/tier scope and output
locator, plus matching source, test, configuration, environment and build identities. Compare
these inputs immediately before reuse and cite the original run; do not claim a new execution.
A subset only covers that subset. Blocked, unrun, incomplete, inaccessible or identity-free
results cannot become PASS. A relevant change reruns the affected check; an unrelated scoped-out
change does not force rerunning everything. Unknown environment/build identity means no reuse.

Choose checks from the actual changed contract, repository instructions and CI, with each
required behavior mapped to execution evidence. Record inapplicable gates with a concrete reason;
missing toolchain or required environment is BLOCKED, not inapplicable. Environment differences
are evaluated against requirements and consumed configuration: a missing required key fails;
a deliberate unrelated difference is documented in the established artifact, with no magic
comment syntax. Observable UI ACs may use actual browser evidence tied to the current build;
subjective acceptance or an owner decision still requires the user.

## Task and lifecycle handoff

Resolve `scope_kind: task|prefix`, `task_id`, `task_locator`, `ac_source` and exact AC list,
`declared_files`, `observed_changes`, `base`, `budgets`, `test_commands`, `dependencies`, and
`record_id` before invoking gates. Task ACs come only from the designated Acceptance criteria
section (or an explicitly resolved legacy AC range), never test checkboxes, prior evidence,
or neighboring tasks. Heading tasks end at the next same-or-higher heading; numbered tasks
end at the next peer item. For ambiguous legacy boundaries, resolve once with the owner and
record the locator. No heuristic fallback to all prefix ACs.

A tasks-doc-less fix uses the bug ID, investigation path, proposed-fix locator, and an explicit
AC mapping from expected behavior plus the fix techspec's designated ACs when a techspec
exists. For a reviewed small fix that legitimately skips a techspec, use its explicit
testable expected outcomes without inventing a missing document. Retain source
locators and deduplicate identical obligations. For example, expected behavior "returns 2"
and a designated fix AC "returns 2" become one obligation with both source locators, not
two checks; retain a distinct negative-input AC separately. Resolve missing testable outcomes
before verification. The investigation need not pretend to contain a Task heading.

Use a Verify heading one level below its task heading, or a delimited evidence block beneath
a numbered task item (no escaping `##` heading). Fix evidence can be a top-level delimited
Verify section. Append every re-run; reuse the original AC source, not generated gate lines.
A composed QA call consumes these authoritative inputs without independently widening them;
it may flag missing relevant coverage for explicit resolution. Prefix QA separately derives
prefix ACs and scope, and cannot inherit a task-only boundary accidentally.

Keep task Status values unchanged. Add lifecycle boundary `pre-merge` (default for existing
repository-only docs), `deploy`, or `live`, plus each operational task's required evidence.
Repository review/QA waits for repository tasks only; deploy/live tasks depend on repository
GO and their actual operational producers. Pending operations remain Not Started/In Progress
with their evidence unmet. Report repository completion and operational completion separately;
repository GO never claims deployment, rehearsal, or authorization to perform them.
