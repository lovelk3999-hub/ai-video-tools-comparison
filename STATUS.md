# STATUS - AI Video Tools Comparison

> Last updated: 2026-06-19
> Current task: Category pages added + pricing updated

---

## Recent Progress (This Session)

| Task | Status | Notes |
|------|--------|-------|
| PixVerse/Adobe Firefly pricing fixed | ? | Used TinyFish for accurate data, no more estimates |
| Adobe Firefly G2 added | ? | 4.4/5 (335 reviews) from G2 via TinyFish |
| Category pages generated | ? | best-avatar-tools, best-text-to-video-tools, best-video-gen-tools (3 new pages) |
| generate.py fixes | ? | Category function call, video-gen mapping, sitemap, summary |

---

## Overall Completion

| Module | Status | Notes |
|--------|--------|-------|
| Site Architecture | ? | Cloudflare Pages + Python static gen + GitHub Actions |
| 17 tools | ? | heygen, synthesia, runway, pika, sora, kling, invideo, capcut, colossyan, seedance, hailuoai, luma, vidu, did, pixverse, veo, adobe-firefly |
| 159 pages | ? | 1 index + 17 tool + 136 compare + 3 category + sitemap + robots |
| FAQ 30 + JSON-LD | ? | Schema.org structured data |
| SEO basics | ? | OG tags / sitemap.xml / robots.txt / canonical |
| Official videos | ? | All 17 tools have YouTube embed |
| CI/CD auto-deploy | ? | GitHub Actions push -> Cloudflare Pages |
| G2 ratings | ? | TinyFish API, 15/17 tools have data |
| Reddit discussions | ? | TinyFish search, 3 posts per tool |
| Pricing auto-collection | ? | Playwright monthly cron |
| Google Search Console | ?? | Verified + sitemap submitted, waiting 1-2 days |
| Google Analytics 4 | ? | G-B8SKQ9HHPZ installed |

---

## Key Files

| File | Purpose |
|------|---------|
| scripts/generate.py | Static site generator |
| scripts/collect_social_proxy.py | TinyFish proxy for G2 + Reddit |
| data/tools.json | All tool data |

## Next Actions (Priority Order)

1. **Check Search Console** (after 1-2 days, ~June 20-21) - verify indexing started
2. **Build backlinks** - submit to AI tools directories, write guest posts
3. **Monitor pricing updates** - next Playwright run in 1 month
4. **Content expansion** - add more FAQ, comparison highlights

## Known Issues

1. G2 has DataDome CAPTCHA -> TinyFish API proxy workaround
2. Seedance/HailuoAI no G2 data -> no alternative source yet
3. Reddit anti-scrape strict -> TinyFish search
4. Windows GBK encoding -> file I/O must encoding=utf-8
5. Sora pricing opaque -> need manual monitoring

## Key Decisions

See DECISIONS.md
