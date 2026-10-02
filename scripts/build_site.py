#!/usr/bin/env python3
"""Build the served skills tree and its discovery index.

Writes <out>/.well-known/agent-skills/index.json plus one payload per skill,
hashing each payload in the same pass that writes it. Also writes human docs:
<out>/index.html (the catalog) and <out>/agent-skills/<name>/index.html (each
skill's README.md, rendered).

  pip install markdown
  python3 scripts/build_site.py <base-url> [out-dir]

A skill whose folder holds only SKILL.md (README.md is repo docs, not shipped)
is served as SKILL.md; any other skill is served as a flat, reproducible tarball.
"""
import gzip
import hashlib
import html
import io
import json
import os
import re
import shutil
import sys
import tarfile
import unicodedata
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NOT_SHIPPED = {"README.md"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REPO = "https://github.com/" + os.environ.get("GITHUB_REPOSITORY", "a-laughlin/agentic-resources")

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<style>
:root {{ --bg: #fff; --fg: #1f2328; --muted: #59636e; --line: #d1d9e0; --code: #f6f8fa; --link: #0969da; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #0d1117; --fg: #e6edf3; --muted: #9198a1; --line: #3d444d; --code: #151b23; --link: #4493f8; }}
}}
body {{ margin: 0; background: var(--bg); color: var(--fg);
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
main {{ max-width: 52rem; margin: 0 auto; padding: 2rem 16px 4rem; }}
nav {{ font-size: .9rem; color: var(--muted); }}
a {{ color: var(--link); }}
code, pre {{ font: .875em/1.45 ui-monospace, SFMono-Regular, Menlo, monospace; background: var(--code); border-radius: 6px; }}
code {{ padding: .15em .35em; }}
pre {{ padding: 1rem; overflow-x: auto; }}
pre code {{ padding: 0; background: none; font-size: 1em; }}
table {{ border-collapse: collapse; display: block; overflow-x: auto; }}
th, td {{ border: 1px solid var(--line); padding: .4rem .75rem; text-align: left; }}
h1, h2 {{ border-bottom: 1px solid var(--line); padding-bottom: .3em; }}
dt {{ font-weight: 600; margin-top: 1rem; }}
dd {{ margin-left: 0; color: var(--muted); }}
</style>
</head>
<body>
<main>
<nav>{nav}</nav>
{body}
</main>
</body>
</html>
"""


def front_matter(skill_md):
    m = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(), re.S)
    if not m:
        sys.exit(f"{skill_md}: missing front matter")
    fields = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            fields[key.strip()] = value
    return fields


def github_slug(value, separator):
    # Match GitHub's heading anchors so README links like #challenges resolve on the site too.
    kept = "".join(c for c in value.lower()
                   if c in " -_" or unicodedata.category(c)[0] in "LMN")
    return kept.replace(" ", separator)


def render_page(path, title, description, nav, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PAGE.format(title=html.escape(title), description=html.escape(description),
                                nav=nav, body=body))


def render_readme(readme):
    # GitHub reads a trailing backslash as a line break; Python-Markdown wants two trailing spaces.
    # Odd parts are fenced code, where a trailing backslash is literal (e.g. shell continuations).
    parts = re.split(r"(^```.*?^```)", readme.read_text(), flags=re.M | re.S)
    text = "".join(p if i % 2 else re.sub(r"\\$", "  ", p, flags=re.M) for i, p in enumerate(parts))
    return markdown.markdown(text, extensions=["fenced_code", "tables", "toc"],
                             extension_configs={"toc": {"slugify": github_slug}})


def flat_tarball(files, skill_dir):
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for f in sorted(files):
            data = f.read_bytes()
            info = tarfile.TarInfo(f.relative_to(skill_dir).as_posix())
            info.size = len(data)
            info.mode = 0o755 if f.stat().st_mode & 0o111 else 0o644
            info.mtime = 1577836800  # 2020-01-01 UTC
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(data))
    return gzip.compress(raw.getvalue(), mtime=0)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    base = sys.argv[1].rstrip("/")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else ROOT / "_site")
    shutil.rmtree(out, ignore_errors=True)

    entries = []
    for skill_dir in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()):
        meta = front_matter(skill_dir / "SKILL.md")
        name, description = meta.get("name"), meta.get("description")
        if name != skill_dir.name or not NAME_RE.match(name or ""):
            sys.exit(f"{skill_dir}: name {name!r} must match folder and [a-z0-9-]")
        if not description:
            sys.exit(f"{skill_dir}: missing description")
        if any(e["name"] == name for e in entries):
            sys.exit(f"duplicate skill name {name!r}")

        shipped = [f for f in skill_dir.rglob("*") if f.is_file() and f.name not in NOT_SHIPPED]
        if len(shipped) == 1:
            kind, rel, payload = "skill-md", f"agent-skills/{name}/SKILL.md", shipped[0].read_bytes()
        else:
            kind, rel, payload = "archive", f"agent-skills/{name}.tar.gz", flat_tarball(shipped, skill_dir)

        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)

        readme = skill_dir / "README.md"
        if readme.is_file():
            render_page(out / f"agent-skills/{name}/index.html", name, description,
                        f'<a href="{base}/">Agent skills</a> · <a href="{REPO}/tree/main/skills/{name}">Source</a>',
                        render_readme(readme))
        entries.append({
            "name": name,
            "description": description,
            "type": kind,
            "url": f"{base}/{rel}",
            "digest": "sha256:" + hashlib.sha256(payload).hexdigest(),
        })

    index = out / ".well-known/agent-skills/index.json"
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(json.dumps({
        "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
        "skills": entries,
    }, indent=2) + "\n")

    items = "\n".join(
        f'<dt><a href="{base}/agent-skills/{e["name"]}/">{e["name"]}</a></dt>\n'
        f'<dd>{html.escape(e["description"])}</dd>'
        for e in entries)
    render_page(out / "index.html", "Agent skills", "Agent skills by Adam Laughlin.",
                f'<a href="{REPO}">Source</a> · <a href="{base}/.well-known/agent-skills/index.json">Discovery index</a>',
                f"<h1>Agent skills</h1>\n<dl>\n{items}\n</dl>\n"
                f"<h2>Install</h2>\n<pre><code>npx skills add {base}</code></pre>\n"
                f"<p>Each skill's page lists more install options.</p>")
    print(index.read_text())


if __name__ == "__main__":
    main()
