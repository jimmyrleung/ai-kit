# Skill draft — check a local HTML page at several widths

Draft from the 2026-11-15 session. For the owner to review; not a live skill.

**Use when:** a generated or hand-written HTML file must be seen in a browser, in both themes and at
desktop, tablet and phone widths.

## Steps

1. Serve the folder on the loopback address only, in the background:
   `python -m http.server <port> --bind 127.0.0.1` from the folder that holds the page.
2. Open `http://127.0.0.1:<port>/<page>` in a new tab. The Chrome extension cannot open `file://`.
3. Desktop: take a screenshot; scroll to the parts that matter with `element.scrollIntoView()`.
4. Themes: set `document.documentElement.dataset.theme = 'dark'` (or the page's own switch) and look again.
5. Narrow widths: replace the tab's body with iframes of the widths to test, for example 1000px and 420px,
   each loading the same page. Compare `documentElement.scrollWidth` with the iframe width to find
   sideways overflow.
6. Read the console for errors.
7. Stop the server and close the tab.

## Notes

- A window resize may not change the viewport; the iframe method does not depend on it.
- Private pages stay local: copy them to a scratch folder and serve that folder, never a hosted page.
- Say which widths, themes and modes were looked at, and which were not.
