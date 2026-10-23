# Josh Qixuan Sun — academic homepage

Personal academic website: **https://realjoshqsun.github.io/**

Based on the [Minimal Light](https://github.com/yaoyao-liu/minimal-light) HTML theme. The upstream stylesheets and CC0 license are retained, with custom styles for the profile, research interests, news, and publications.

## Update content

- `data/profile.json`: profile information, research themes, and news. News dates use `YYYY-MM` and are displayed as `YYYY.MM`, newest first.
- `data/publications.json`: selected papers, author lists, venues, figures, and public resource links. The array controls publication order.
- `templates/index.html`: page structure and About Me text.
- `assets/css/custom.css`: visual adjustments and responsive layout.
- `assets/img/avatar-linkedin.jpg`: the current profile photo.
- `assets/img/publications/` and `assets/bib/`: paper figures and BibTeX files.

## Preview locally

Python 3.8 or later is required; no external Python packages are needed.

```sh
python3 build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4173/.

## Publish

Push changes to `main`. The GitHub Actions workflow builds the website with `python3 build.py` and publishes only `dist/` to GitHub Pages. The repository's Pages publishing source is **GitHub Actions**.

The site follows the visitor's light/dark system preference. Fonts are loaded from Google Fonts with a serif fallback. No analytics are configured.
