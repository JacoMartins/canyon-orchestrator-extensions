"""Writes dist/registry.json: every pack in packs.json with, per platform, its library's
download URL, SHA-256 and size, and its query files (the same on every platform). Canyon
Orchestrator reads this file to install extensions.

Usage: python scripts/registry.py <tag> <owner/repo>
Expects the built libraries in dist/, named <id>-<platform>.<so|dylib|dll>, and the query
files beside them, named <id>-<name>.scm (copied from packs/<id>/queries/<name>.scm).
"""

import hashlib
import json
import pathlib
import sys

tag, repo = sys.argv[1], sys.argv[2]
dist = pathlib.Path("dist")
packs = json.loads(pathlib.Path("packs.json").read_text())



def asset(path):
    data = path.read_bytes()
    return {
        "url": f"https://github.com/{repo}/releases/download/{tag}/{path.name}",
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


extensions = []
for pack in packs["packs"]:
    files, queries = {}, {}
    for f in sorted(dist.glob(f"{pack['id']}-*.*")):
        name = f.stem[len(pack["id"]) + 1 :]
        if f.suffix == ".scm":
            queries[name] = asset(f)
        else:
            files[name] = asset(f)
    if not files:
        sys.exit(f"no libraries built for {pack['id']}")
    if "highlights" not in queries:
        sys.exit(f"no highlights.scm for {pack['id']}")
    extensions.append(
        {
            "id": pack["id"],
            "name": pack["name"],
            "version": pack["version"],
            "description": pack["description"],
            "file_types": pack["file_types"],
            "files": files,
            "queries": queries,
            # What it asks for beyond its grammar (files, commands, network, a program of its
            # own), shown to the person before it installs. Grammar packs ask for none.
            **({"needs": pack["needs"]} if pack.get("needs") else {}),
        }
    )

(dist / "registry.json").write_text(json.dumps({"v": 1, "extensions": extensions}, indent=2) + "\n")
print(f"registry.json: {len(extensions)} extensions")
