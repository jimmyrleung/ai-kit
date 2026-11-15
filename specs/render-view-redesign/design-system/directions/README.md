# Visual directions — comparison mockups

Step 4 of the `ui-process`, built 2026-11-15. The owner compared four versions of the same sample page (a
synthetic "invoice reminders" techspec) and chose direction C2. Open each file in a browser; each has a
System / Light / Dark switch at the top right.

| File | Direction | Fonts (embedded subsets) | Size |
|---|---|---|---|
| `c-quiet-studio.html` | Sans text, no rules, hierarchy from space and grey levels, one yellow highlight | Geist, Geist Mono | 75 KB |
| `c2-quiet-studio-signal.html` | Direction C with a signal orange in a few places, replacing the yellow (owner's request, 2026-11-15). **The chosen direction** | Geist, Geist Mono | 76 KB |

Two other directions were compared and are not kept: "Paper and ink" (serif reading text) and "Swiss
ledger" (strong rules, IBM Plex). They embedded font subsets whose licence texts were not shipped with
them, so they were removed before the repository was made public.

What was the same in all four, from [../../research.md](../../research.md): one page surface with no
section panels; a prose column of about 66–70 characters with wider tables, code and figures; a one-line
metadata row; light code blocks with GitHub's syntax and diff colours; diagrams as figures with a caption;
decision cards as full-width rows; "Needs you" as the only coloured tag on a card; a quiet "generated"
line in the footer.

Not final: the page shell is static (no scroll tracking, no working Respond), colours are first values,
and narrow screens are not handled. The final values are in [../tokens.css](../tokens.css).

The two kept files embed Geist and Geist Mono subsets (SIL Open Font License). The licence texts are in
[../fonts/](../fonts/) and in `skills/render-view/assets/`.
