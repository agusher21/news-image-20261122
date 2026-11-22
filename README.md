# news-image-20261122

**Sum up 22 November 2026 world news in one image** — make.fun bounty entry.

A dense newspaper front page packing 35 stories across 6 regions into a single 1024×1024 PNG. Features the unique "THE DAY IN UTC" timeline spine marking the day's seven biggest moments from 03:00 to 22:00 UTC.

[![make.fun badge](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank badge](https://make.fun/badge/news-image-20261122/agusher21/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward badge](https://make.fun/badge/news-image-20261122/agusher21/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

## Competition Details

- **Pool:** 100 USDC
- **Top 50 paid**
- **Entries close:** 24 Nov 2026 07:00 WIB
- **Wallet:** `7FxQ7pkQeEixkjnk6zeKPFix3KsiZWjp88VMEpTbHS8G`

## Build

```bash
# Generate the image (already committed as out/entry.png)
python3 tools/generate.py

# Verify entry program
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

The entry program (`main.ts`) only copies the pre-rendered `out/entry.png` to `MAKEFUN_OUTPUT_DIR` — no generation at grading time.