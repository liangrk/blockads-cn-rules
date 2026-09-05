#!/usr/bin/env python3
"""Merge rules/ + upstream cache/ into dist/, enforcing the allowlist.

Output: dist/cn-ads.txt (domains, sorted) + dist/cn-ads.allowlist.txt.
"""
import pathlib
import re
import sys

DOMAIN_RE = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$")


def extract_domain(line):
    line = line.strip().lower()
    if not line or line.startswith(("#", "!")):
        return None
    if line.startswith("0.0.0.0 ") or line.startswith("127.0.0.1 "):
        line = line.split()[1]
    line = line.split("#")[0].strip()
    if not line:
        return None
    return line if DOMAIN_RE.match(line) else None


def load(path):
    domains = set()
    if not path.exists():
        return domains
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        d = extract_domain(raw)
        if d:
            domains.add(d)
    return domains


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    rules_dir = root / "rules"
    cache_dir = root / "cache"
    dist_dir = root / "dist"
    dist_dir.mkdir(exist_ok=True)

    allow = load(rules_dir / "allowlist.txt")
    if not allow:
        print("FATAL: rules/allowlist.txt empty or missing", file=sys.stderr)
        return 1

    hand = set()
    for f in sorted(rules_dir.glob("*.txt")):
        if f.name == "allowlist.txt":
            continue
        hand |= load(f)

    upstream = set()
    for f in sorted(cache_dir.glob("*.txt")):
        upstream |= load(f)

    blocked = hand | upstream

    def protected(domain):
        return any(domain == a or domain.endswith("." + a) for a in allow)

    # Hand-curated vendor rules survive allowlist suffix protection:
    # they are verified ad-only domains (e.g. gdt.qq.com under qq.com).
    stripped = {d for d in blocked if protected(d) and d not in hand}
    final = sorted(d for d in blocked if not protected(d) or d in hand)

    (dist_dir / "cn-ads.txt").write_text(
        "# blockads-cn-rules - merged CN ad domains (ads only).\n"
        "# Core business domains are protected via rules/allowlist.txt.\n"
        + "\n".join(final) + "\n",
        encoding="utf-8",
    )
    (dist_dir / "cn-ads.allowlist.txt").write_text(
        "\n".join(sorted(allow)) + "\n", encoding="utf-8"
    )
    print(f"dist/cn-ads.txt: {len(final)} domains; allowlist: {len(allow)}")
    if stripped:
        print(f"stripped {len(stripped)} protected domains, e.g. {sorted(stripped)[:5]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
