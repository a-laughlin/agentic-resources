#!/usr/bin/env python3
"""Build the served skills tree and its discovery index.

Writes <out>/.well-known/agent-skills/index.json plus one payload per skill,
hashing each payload in the same pass that writes it. Human-facing pages
(<out>/index.html and <out>/agent-skills/<name>/index.html) just redirect to
the GitHub repo.

  python3 scripts/build_site.py <base-url> [out-dir]

A skill whose folder holds only SKILL.md (README.md is repo docs, not shipped)
is served as SKILL.md; any other skill is served as a flat, reproducible tarball.
"""
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NOT_SHIPPED = {"README.md"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REPO = "https://github.com/" + os.environ.get("GITHUB_REPOSITORY", "a-laughlin/agentic-resources")

REDIRECT = """<!doctype html>
<meta charset="utf-8">
<title>Agent skills</title>
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<a href="{url}">{url}</a>
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


def redirect(path, url):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(REDIRECT.format(url=url))


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

        redirect(out / f"agent-skills/{name}/index.html", f"{REPO}/tree/main/skills/{name}")
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

    redirect(out / "index.html", REPO)
    print(index.read_text())


if __name__ == "__main__":
    main()
