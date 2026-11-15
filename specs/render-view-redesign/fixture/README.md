# render-view fixture

Synthetic spec folder ("invoice reminders") with a spec view, a decision round of 14 items and a tour of two
fixed commits (`f174a75`..`a3ed724`). Every exhibit type is present. The exhibits are kept in `exhibits/`
because `.views/` ignores itself in git. Run from the repository root:

    cp specs/render-view-redesign/fixture/exhibits/*.json specs/render-view-redesign/fixture/.views/exhibits/
    uv run --no-project python -B skills/render-view/scripts/render_view.py build specs/render-view-redesign/fixture --repo .
    uv run --no-project python -B skills/render-view/scripts/render_view.py check specs/render-view-redesign/fixture
