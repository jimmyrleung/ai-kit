# Exhibits — the illustrations you draw

An exhibit is one JSON file in `<spec>/.views/exhibits/<id>.json`. The build script renders it with a
fixed component (HTML or inline SVG), places it at its anchor, and stamps it with the hash of its source
sections and, for `code` and `diff`, of the code it shows. You write data, never HTML or SVG.

## Choose what to draw

Draw only where a picture beats the text it sits next to. Typical count: 3–7 per spec, at most one per
section.

| The section has… | Draw | Type |
|---|---|---|
| The whole doc (always worth one) | 3–6 behaviour claims a reader can judge without code | `claims` at `top` |
| Parts that call or contain each other, with new / changed / shared parts | A node graph on a grid | `graph` |
| An ordered exchange between parts (save flow, request, job tick) | A sequence diagram, failure exits in the right column | `sequence` |
| A lifecycle or mode table whose transitions are spread through prose | A drawn state machine | `states` |
| A claim that rests on existing code | The real lines from the repo, with pins | `code` |
| A change that already exists in git, or a proposed edit | A git-style diff | `diff` |
| A High risk, or a decision whose reason is non-obvious | A 3-step concrete failure walk (or a `sequence` with a struck line) | `walk` |
| A short ordered checklist with failure exits beside steps | Steps in a column | `flow` |
| Files or components as a plain hierarchy | An indented tree with marks | `tree` |
| Questions the doc itself lists as open, with options | Decision forms with the doc's recommendation suggested | `decisions` |

Do not:

- restate a table that already reads well, or redraw an ASCII diagram unless the picture adds the
  missing exits, transitions or marks;
- invent decisions, options, numbers or behaviour the sources do not state. If you infer something, say
  "inferred" in a `detail` or the `caption`;
- use `decisions` for questions the doc records as answered;
- add a `diff` for a code block the spec already writes as `// before` … `// after`: the build renders
  those as diffs on its own.

## File shape

```json
{
  "id": "save-flow",
  "doc": "techspec.md",
  "anchor": "data-flow",
  "sources": ["data-flow", "key-decisions"],
  "type": "sequence",
  "title": "Save and continue, step by step",
  "caption": "Any failure stops the save and leaves no saved marker.",
  "data": {}
}
```

- `id`: kebab-case, unique; it is the file name without `.json`.
- `doc`: the doc file in the spec folder. Default: the main doc (`techspec.md` when present).
- `anchor`: the heading anchor the exhibit sits under, exactly as `render_view.py plan` lists it, or `top`
  for the start of the doc.
- `sources`: the anchors whose text the exhibit draws from. Default: `[anchor]` (`top` defaults to the
  whole doc, which goes stale on any edit, so list real sources for `top`).
- `stamp`: written by the build. Leave it out of a new file; delete it when you redraw.
- `title`, `caption`: optional, one line each. Text fields accept inline markdown (code, bold, links).
- `refs` (inside items): IDs defined in the spec set (`RF1`, `UT-57`, `T6`), `#anchor` in the same doc,
  or `file.md#anchor`. Unresolved refs show in the build report.

## Diagrams

Diagrams are laid out on a grid you give: `grid` is a list of rows, each a list of ids or `null` for an
empty cell. Put the main path on the top row and branches below it; ids missing from the grid are placed
after it. Keep labels short (a few words) and diagrams small (about 8 states or 12 nodes).

`states`: `initial` is the start state (default: the first); `final` marks a state with no way out. Each
`detail` shows in a list under the drawing. Hovering a state lights up its outgoing transitions.

```json
{ "initial": "queued", "grid": [["queued", "sending", "sent"], [null, "failed", null]],
  "states": [
    { "id": "queued", "detail": "Picked by the 09:00 run." },
    { "id": "sending" }, { "id": "failed" },
    { "id": "sent", "final": true }
  ],
  "transitions": [
    { "from": "queued", "to": "sending", "label": "still unpaid" },
    { "from": "sending", "to": "sent", "label": "ok" },
    { "from": "sending", "to": "failed", "label": "bounced" },
    { "from": "failed", "to": "sending", "label": "retry once" }
  ] }
```

`graph`: `mark` is `new`, `changed`, `shared` (changed and used elsewhere), `removed`, or `same`; `sub` is a
second line under the label. Edges from a row to a lower row draw as elbows, so a top-down grid reads as a
tree. `dashed: true` for optional or async links.

```json
{ "grid": [[null, "job", null], ["store", "mailer", "log"]],
  "nodes": [
    { "id": "job", "label": "ReminderJob", "sub": "daily batch", "mark": "new" },
    { "id": "store", "label": "InvoiceStore", "sub": "dueForReminder()", "mark": "changed" },
    { "id": "mailer", "label": "Mailer", "mark": "same" },
    { "id": "log", "label": "reminder_log", "sub": "new table", "mark": "new" }
  ],
  "edges": [ { "from": "job", "to": "store" }, { "from": "job", "to": "mailer" }, { "from": "job", "to": "log" } ] }
```

`sequence`: a step is a message (`from`, `to`, `text`), a `note` (with `over`: participant ids), or a
`divider`. Message `kind` is `call` (default), `reply` (dashed) or `lost` (ends in ✕). `mark` is `new`
(green) or `removed` (red, struck). `fail` on a message or note writes its failure exit in the right
column.

```json
{ "participants": [ { "id": "job", "label": "ReminderJob" }, { "id": "db", "label": "Invoices" }, { "id": "mail", "label": "Mailer" } ],
  "steps": [
    { "from": "job", "to": "db", "text": "read batch" },
    { "divider": "per invoice" },
    { "from": "job", "to": "db", "text": "re-read status", "mark": "new" },
    { "note": "Paid or Void: skip", "over": ["job"] },
    { "from": "job", "to": "mail", "text": "send reminder", "fail": "bounce: log failed, retry once" }
  ] }
```

## Code

Code exhibits need `build --repo <code root>`. Paths use the spec's own spelling; a `| Prefix | Path |`
table in the docs is applied (`BL/…`). They go stale when the code they show changes.

`code`: real lines from the working tree, or from `ref` (any commit or branch). `highlight` takes line
numbers and ranges (`"112,118-120"`); `pins` attach a note under a line (`tone`: `info`, `ok`, `warn`,
`risk`). At most 60 lines.

```json
{ "path": "BL/invoices/InvoiceStore.ts", "lines": "110-124", "highlight": "118",
  "pins": [ { "line": 118, "tone": "ok", "title": "Re-read", "text": "The status is read again just before each send." } ] }
```

`diff` from git: `base` and optional `head` (default: the working tree), any git ref such as a merge and
its first parent (`abc123^1` → `abc123`). `lines` keeps only the rows around those new-side lines;
`context` is 0–12 (default 3). Use it to show what actually shipped, or how code drifted from the spec.

```json
{ "path": "BL/reminders/ReminderJob.ts", "base": "abc123^1", "head": "abc123", "lines": "40-90" }
```

`diff` from text, for a change that does not exist yet (no repo needed):

```json
{ "lang": "ts", "label": "proposed retry", "before": "send(email)", "after": "await send(email)\nif (bounced) retryOnce(email)" }
```

## Other types

`claims`: each claim is a sentence that can be true or false, 20 words at most.

```json
{ "items": [ { "text": "A customer with an unpaid invoice gets an email on day 7 and day 14.", "refs": ["RF1", "UT-02"] } ] }
```

`walk`: 3 steps; mark the wrong outcome; `outcome` says what the design does about it.

```json
{ "steps": [
  { "when": "09:00:00", "text": "The job reads invoice #1042 as Sent." },
  { "when": "09:00:02", "text": "The customer pays; #1042 is Paid." },
  { "when": "09:00:05", "text": "The job emails \"Your invoice is unpaid\".", "wrong": true }
], "outcome": "The job re-reads the status before each send (D4)." }
```

`flow`: `kind` is `step` (default), `key`, `new`, or `end`; `exit` is the failure branch beside the step.

```json
{ "steps": [ { "label": "Re-read the invoice status", "kind": "key", "exit": "Paid or Void: skip and log", "refs": ["#architecture"] } ] }
```

`tree`: nested `nodes` with `label`, `mark` (as in `graph`), optional `detail`, `refs` and `children`.

`decisions`: exactly one option per item has `"suggested": true` — the doc's recommendation.

```json
{ "items": [
  { "id": "Q2", "question": "Retry a bounced email once, one hour later?", "confidence": 80, "refs": ["R2"],
    "options": [
      { "value": "keep", "label": "Keep", "note": "one extra job path", "suggested": true },
      { "value": "remove", "label": "Remove", "note": "a bounce is logged as failed" }
    ] }
] }
```

The reader's choices come back in the Respond block as `→ **Label** \`value\`` with "kept as suggested",
"changed", or "not touched; default kept". Treat "not touched" as no answer for anything that matters.

## Redraw

`plan`, `build` and `check` mark an exhibit `stale` when a source section or the code it shows changed
since its stamp. Re-read what changed, rewrite the file without `stamp`, and rebuild. Delete exhibits
whose anchor no longer exists (`orphan`) or move them to the new anchor; fix `invalid` ones (a bad path,
ref or type) from the message the build prints.
