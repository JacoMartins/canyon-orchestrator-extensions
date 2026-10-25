"""Writes dist/registry.json: every pack in packs.json with, per platform, its library's
download URL, SHA-256 and size. Canyon Orchestrator reads this file to install extensions.

Usage: python scripts/registry.py <tag> <owner/repo>
Expects the built libraries in dist/, named <id>-<platform>.<so|dylib|dll>.
"""

import hashlib
import json
import pathlib
import sys

tag, repo = sys.argv[1], sys.argv[2]
dist = pathlib.Path("dist")
packs = json.loads(pathlib.Path("packs.json").read_text())

extensions = []
for pack in packs["packs"]:
    files = {}
    for lib in sorted(dist.glob(f"{pack['id']}-*.*")):
        platform = lib.stem[len(pack["id"]) + 1 :]
        data = lib.read_bytes()
        files[platform] = {
            "url": f"https://github.com/{repo}/releases/download/{tag}/{lib.name}",
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
        }
    if not files:
        sys.exit(f"no libraries built for {pack['id']}")
    extensions.append(
        {
            "id": pack["id"],
            "name": pack["name"],
            "version": pack["version"],
            "description": pack["description"],
            "file_types": pack["file_types"],
            "files": files,
        }
    )

(dist / "registry.json").write_text(json.dumps({"v": 1, "extensions": extensions}, indent=2) + "\n")
print(f"registry.json: {len(extensions)} extensions")
