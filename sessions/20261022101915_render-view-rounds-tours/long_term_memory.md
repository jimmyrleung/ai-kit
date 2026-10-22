# Long-term memory candidates

Proposals for `AGENTS.md` or `rules/`. The owner decides what goes in.

1. **Test skill handoffs with the writer's real output.** When one skill writes an artifact another skill parses
   (a round file, a tour doc, a tasks doc), test the parser against an artifact the writing skill produced, not only
   fixtures. A round numbered `1..N` did not parse because every fixture used `D4`-style IDs.
2. **A mode offer gets its own turn.** A skill that offers another cadence or medium (a page instead of chat, a batch
   instead of one item) ends that turn with the single question and presents no work in it. Folded into item 1, the
   offer read as chat.
3. **Check bundled scripts on their oldest claimed Python.** Skills claim 3.10+ while CI runs 3.12; before a commit,
   run `uv run --no-project --python 3.10 python -m py_compile <script>` (f-string rules differ).
4. **Commit identity on this machine.** No git identity is configured; reuse the previous commits' author
   (`git log -1 --format='%an <%ae>'`) inline with `-c user.name=… -c user.email=…`, never by changing global config.
