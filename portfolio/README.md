# GO BEYOND — ゴー・ビヨンド

A bilingual personal archive and technical showcase under construction.

## Local preview

From the repository root (Python 3.10+; no third-party packages):

```sh
python3 portfolio/build.py
python3 -m http.server 8000 --directory portfolio/dist
```

Open http://localhost:8000/ (Portuguese) or http://localhost:8000/en/ (English).

- `content/catalog.json`: owner-confirmed content seed; not all content is rendered yet.
- `src/style.css`: provisional foundation styling, not the final design.
- `build.py`: static build and structural checks.
- `ROADMAP.md`: scope, requirements, architecture decision and release gates.
- `dist/`: generated output, ignored by Git.

The workflow builds on main pushes. Publishing is intentionally manual: set Settings → Pages → Source to GitHub Actions, then run GO BEYOND from main with publish enabled when the site is ready. Expected project URL: https://kayo-willian.github.io/kayo-willian/.

The profile README and existing assets are not modified by the website build.
