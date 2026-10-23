"""Build the upstream Minimal Light HTML edition using only Python's standard library."""
import html
import json
import shutil
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"


def escape(value):
    return html.escape(str(value), quote=True)


def link(url, label, css=""):
    return f'<a href="{escape(url)}"{f" class={chr(34)}{css}{chr(34)}" if css else ""}>{escape(label)}</a>'


def news(items):
    if not items:
        return ""
    rows = []
    for item in sorted(items, key=lambda item: item["date"], reverse=True):
        date = escape(item["date"])
        label = date.replace("-", ".")
        rows.append(f'<li><time datetime="{date}">{label}</time><span>{escape(item["text"])}</span></li>')
    return f'<h2 id="news">News</h2><ul class="news-list">{"".join(rows)}</ul>'


def research_interests(profile, papers):
    papers_by_id = {paper["id"]: paper for paper in papers}
    groups = []
    for group in profile["research_groups"]:
        badges = []
        for paper_id in group["papers"]:
            paper = papers_by_id[paper_id]
            label = paper["research_label"]
            if paper.get("url"):
                badges.append(f'<a class="research-badge" href="#pub-{escape(paper_id)}" aria-label="{escape(label + ": " + paper["title"])}" title="{escape(paper["title"])}">{escape(label)}</a>')
            else:
                badges.append(f'<span class="research-badge research-badge-static" title="{escape(paper["title"])}">{escape(label)}</span>')
        heading_id = "interest-" + group["id"]
        groups.append(f'<article class="research-card" aria-labelledby="{escape(heading_id)}"><h3 id="{escape(heading_id)}">{escape(group["title"])}</h3><div class="research-papers">{"".join(badges)}</div></article>')
    return "\n".join(groups)


def publication(paper, name):
    authors = ", ".join(f"<strong>{escape(a)}</strong>" if a == name else escape(a) for a in paper["authors"])
    buttons = " ".join(link(paper[key], label, "btn") for key, label in [("pdf", "PDF"), ("code", "Code"), ("page", "Project Page"), ("bibtex", "BibTeX")] if paper.get(key))
    if paper.get("notes"):
        buttons += f' <span class="pub-note">{escape(paper["notes"])}</span>'
    title = escape(paper["title"])
    image = f'<img class="teaser" src="{escape(paper["image"])}" alt="" width="680" height="456" loading="lazy">'
    if paper.get("url"):
        title = link(paper["url"], paper["title"])
        image = f'<a href="{escape(paper["url"])}" tabindex="-1" aria-hidden="true">{image}</a>'
    return f'''<li><article id="pub-{escape(paper['id'])}" class="pub-row" aria-label="{escape(paper['title'])}">
      <div class="abbr">{image}<abbr class="badge" title="{escape(paper['venue'])}">{escape(paper['badge'])}</abbr></div>
      <div class="pub-details"><div class="title">{title}</div><div class="author">{authors}</div><div class="periodical"><em>{escape(paper['venue'])}, {escape(paper['year'])}.</em></div><div class="links">{buttons}</div></div>
    </article></li>'''


def main():
    profile = json.loads((ROOT / "data/profile.json").read_text())
    papers = json.loads((ROOT / "data/publications.json").read_text())
    fields = {key: escape(value or "") for key, value in profile.items() if isinstance(value, (str, type(None)))}
    fields["interests"] = research_interests(profile, papers)
    fields["publications"] = "\n".join(publication(p, profile["name"]) for p in papers)
    fields["canonical"] = f'<link rel="canonical" href="{escape(profile["canonical_url"])}">' if profile.get("canonical_url") else ""
    fields["contact"] = f'<p>{link("mailto:" + profile["email"], profile["email"])}</p>' if profile.get("email") else ""
    fields["news"] = news(profile.get("news", []))
    document = Template((ROOT / "templates/index.html").read_text()).substitute(fields)
    DIST.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    (DIST / "index.html").write_text(document)
    for paper in papers:
        for key in ("image", "bibtex"):
            if paper.get(key) and not paper[key].startswith("https://") and not (DIST / paper[key]).is_file():
                raise FileNotFoundError(paper[key])
    print(f"Built {len(papers)} selected publications: {DIST / 'index.html'}")


if __name__ == "__main__":
    main()
