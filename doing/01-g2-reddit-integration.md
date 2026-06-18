# Current Task: G2 + Reddit Social Proof Integration

## Status
**COMPLETED** - 2026-06-19

## What Was Done
1. Fixed generate.py line 174: replaced star emoji with plain text G2 display
2. Added Reddit discussions section to tool detail pages
3. Updated 10/14 tools with real G2 ratings via TinyFish API
4. Created scripts/collect_social_proof.py for automated collection
5. Committed and pushed to GitHub

## G2 Ratings (TinyFish)
| Tool | Rating | Reviews |
|------|--------|---------|
| HeyGen | 4.8 | 1831 |
| Synthesia | 4.6 | 2759 |
| Runway | 4.8 | 38 |
| Pika | 4.5 | - |
| Sora | 4.6 | 2698 |
| Invideo | 4.4 | 173 |
| CapCut | 4.6 | 41 |
| Colossyan | 4.6 | 492 |
| Kling | 4.0 | hardcoded |
| D-ID | 4.6 | 117 |
| Luma | 5.0 | 1 |
| Vidu | 4.9 | hardcoded |
| Seedance | - | no G2 data |
| HailuoAI | - | no G2 data |

## Next Steps
1. More video embeds (Pika, Vidu etc.)
2. FAQ expansion to 30+
3. New tools (PixVerse etc.)

## Architecture Decisions
- TinyFish API replaces direct G2/Reddit scraping (avoids CAPTCHA)
- G2 displayed as text (no stars) to avoid Windows GBK crash
- Reddit shown as cards on each tool detail page
