# Upstream ad-domain sources merged daily into dist/cn-ads.txt.
# Only ads-only sources are accepted; core business domains are stripped
# by rules/allowlist.txt during merge.

## Repo structure

```
rules/          # hand-curated vendor modules (one file per ad SDK / app)
  douyin.txt    # Douyin/ByteDance ad-only subdomains (NEVER core domains)
  pangle.txt    # Pangle (穿山甲) ad SDK
  kuaishou.txt  # Kuaishou ad SDK
  jd.txt        # JD splash/ads
  zhihu.txt     # Zhihu splash/ads
  amap.txt      # Amap splash/ads
  gdt.txt       # Tencent GDT (优量汇) ad SDK
  baidu.txt     # Baidu ad SDK (百青藤)
  allowlist.txt # core business domains — never blocked
scripts/        # fetch_upstream.py + merge.py
cache/          # downloaded upstream snapshot (gitignored)
dist/           # published artifacts (consumed by the BlockAds app)
  cn-ads.txt            # merged blocklist (one domain per line)
  cn-ads.allowlist.txt  # protection list (stripped from cn-ads.txt)
```

## Ads only, by contract

`merge.py` enforces: every domain in the final artifact that matches an
allowlist entry or its subdomains is **removed**. The app also loads the
allowlist into its whitelist channel as a second layer of protection.

## Maintenance

- New domains from packet captures → add to the matching `rules/*.txt`.
- Upstream refresh: daily GitHub Action (`.github/workflows/update.yml`).

## License

- Code: MIT
- Domain lists: CC0 1.0
