#!/usr/bin/env python3
"""Fetch upstream domain lists declared in upstream.yml into cache/."""
import pathlib
import sys
import urllib.request

import yaml


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    cache = root / "cache"
    cache.mkdir(exist_ok=True)
    cfg = yaml.safe_load((root / "upstream.yml").read_text(encoding="utf-8"))
    ok = True
    for src in cfg["upstreams"]:
        dest = cache / (src["name"].lower().replace(" ", "_") + ".txt")
        try:
            req = urllib.request.Request(src["url"], headers={"User-Agent": "blockads-cn-rules/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp, dest.open("wb") as out:
                out.write(resp.read())
            print(f"fetched {src['name']}: {dest.stat().st_size} B")
        except Exception as exc:  # keep building on partial failures
            print(f"WARN: failed to fetch {src['name']}: {exc}", file=sys.stderr)
            ok = ok and dest.exists()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
