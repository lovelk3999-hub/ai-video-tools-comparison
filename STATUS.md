# STATUS - AI Video Tools Comparison

> Last updated: 2026-06-19
> Current task: Category pages added + pricing updated

---

## Recent Progress (This Session)

| Task | Status | Notes |
|------|--------|-------|
| PixVerse/Adobe Firefly pricing | DONE | Used TinyFish to get accurate data |
| Adobe Firefly G2 added | DONE | 4.4/5 (335 reviews) via TinyFish |
| Category pages generated | DONE | best-avatar-tools, best-text-to-video-tools, best-video-gen-tools (3 pages) |
| generate.py fixes | DONE | Category function call, video-gen mapping, sitemap, summary |
| Meta description fix | DONE | Dynamic desc parameter instead of hardcoded |
| collect_social_proof.py update | DONE | Added pixverse, veo, adobe-firefly queries |
| ROADMAP updated | DONE | Reflected actual progress state |

---

## Overall Completion

| Module | Status | Notes |
|--------|--------|-------|
| Site Architecture | DONE | Cloudflare Pages + Python static gen + GitHub Actions |
| 17 tools | DONE | All major AI video generation tools |
| 159 pages | DONE | 1 index + 17 tool + 136 compare + 3 category + sitemap + robots |
| FAQ 30 + JSON-LD | DONE | Schema.org structured data |
| SEO basics | DONE | OG tags / sitemap.xml / robots.txt / canonical / meta desc |
| Official videos | DONE | All 17 tools have YouTube embed |
| CI/CD auto-deploy | DONE | GitHub Actions push -> Cloudflare Pages |
| G2 ratings | DONE | TinyFish API, 15/17 tools have data |
| Reddit discussions | DONE | TinyFish search, 3 posts per tool |
| Pricing auto-collection | DONE | Playwright monthly cron |
| Google Search Console | PENDING | Verified + sitemap submitted, waiting 1-2 days |
| Google Analytics 4 | DONE | G-B8SKQ9HHPZ installed |

---

## Key Files

| File | Purpose |
|------|---------|
| scripts/generate.py | Static site generator (17 tools, 159 pages) |
| scripts/collect_social_proof.py | TinyFish proxy for G2 + Reddit |
| data/tools.json | All tool data (pricing, plans, features) |

## Next Actions (Priority Order)

1. **Check Search Console** (after 1-2 days, ~June 20-21) - verify indexing started
2. **Monitor site traffic** via GA4 after indexing begins
3. **Build backlinks** - submit to AI tools directories
4. **Monitor pricing updates** - next Playwright run in 1 month
5. **Content expansion** - add more FAQ, comparison highlights

## Known Issues

1. G2 has DataDome CAPTCHA -> TinyFish API proxy workaround
2. Seedance/HailuoAI no G2 data -> no alternative source yet
3. Reddit anti-scrape strict -> TinyFish search
4. Windows GBK encoding -> file I/O must encoding=utf-8
5. Sora pricing opaque -> need manual monitoring

## Key Decisions

See DECISIONS.md
