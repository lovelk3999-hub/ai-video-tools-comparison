# scripts/update_pricing.py
"""
AI Video Tools - Automated Pricing Scraper
Usage: python scripts/update_pricing.py [--dry-run]
"""
import asyncio, json, re, os, sys
from datetime import datetime

TOOLS_JSON = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tools.json")
DRY_RUN = "--dry-run" in sys.argv

def load_tools():
    with open(TOOLS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tools(data):
    if DRY_RUN:
        print("[DRY-RUN] Would save")
        return
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(TOOLS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved to tools.json")

PRICE_RE = re.compile(r'\$([0-9,]+(?:\.[0-9]+)?)\s*')

def extract_prices(text):
    prices = set()
    for m in PRICE_RE.finditer(text):
        try:
            p = int(m.group(1).replace(",", ""))
            if 1 < p < 500:
                prices.add(p)
        except:
            pass
    return prices

async def scrape_one(page, url, detect_fn, timeout_ms=30000):
    await page.goto(url, wait_until="load", timeout=timeout_ms)
    await page.wait_for_timeout(3000)
    text = await page.inner_text("body")
    prices = extract_prices(text)
    result = detect_fn(text, prices) if detect_fn else {}
    print(f"    Prices: {sorted(prices)} -> Plans: {list(result.keys())}")
    return result if result else None

def detect_heygen(text, prices):
    r = {}
    if "3 videos per month" in text: r["Free"] = {"price_monthly": 0}
    if 29 in prices: r["Creator"] = {"price_monthly": 29}
    if 49 in prices: r["Pro"] = {"price_monthly": 49}
    if 149 in prices: r["Business"] = {"price_monthly": 149}
    return r

def detect_synthesia(text, prices):
    r = {}
    if 19 in prices: r["Starter"] = {"price_monthly": 19}
    if 89 in prices: r["Creator"] = {"price_monthly": 89}
    if "enterprise" in text.lower(): r["Enterprise"] = {"price_monthly": None}
    if "free" in text.lower(): r["Free"] = {"price_monthly": 0}
    return r

def detect_runway(text, prices):
    r = {}
    if "free" in text.lower(): r["Free"] = {"price_monthly": 0}
    if 12 in prices: r["Standard"] = {"price_monthly": 12}
    if 28 in prices: r["Pro"] = {"price_monthly": 28}
    if 76 in prices: r["Max"] = {"price_monthly": 76}
    if "enterprise" in text.lower(): r["Enterprise"] = {"price_monthly": None}
    return r

def detect_pika(text, prices):
    r = {}
    for p in sorted(prices):
        if 8 <= p <= 10: r["Basic"] = {"price_monthly": 10}
        elif 25 <= p <= 35: r["Standard"] = {"price_monthly": 35}
        elif 70 <= p <= 95: r["Pro"] = {"price_monthly": 95}
    if "fancy" in text.lower(): r["Fancy"] = {"price_monthly": None}
    if "free" in text.lower() or "$0" in text: r["Free"] = {"price_monthly": 0}
    return r

def detect_kling_parse(text):
    """Parse Kling pricing (CNY -> USD conversion)."""
    result = {"Free": {"price_monthly": 0}}
    regular = [int(m.group(1)) for m in re.finditer(r"后续每月\s*(\d+)\s*元", text)]
    bg = [int(m.group(1)) for m in re.finditer(r"续费金额[：:]\s*(\d+)\s*元", text)]
    print(f"    Kling CNY prices: {regular}, Black Gold: {bg}")
    plans_w_credits = [("Gold", 660), ("Platinum", 3000), ("Diamond", 8000)]
    for i, (name, creds) in enumerate(plans_w_credits):
        if i < len(regular):
            usd = int(regular[i] / 7.2 + 0.5)
            result[name] = {"price_monthly": usd, "credits": f"{creds} pts/mo"}
    if bg:
        usd = int(bg[0] / 7.2 + 0.5)
        result["Black Gold"] = {"price_monthly": usd, "credits": "26000 pts/mo"}
    return result


async def scrape_kling(pw, data):
    """Scrape Kling using persistent login profile."""
    kling_dir = os.path.join(os.path.dirname(__file__), ".kling_browser")
    tool = next((t for t in data["tools"] if t["id"] == "kling"), None)
    if not tool or not os.path.exists(kling_dir):
        return 0
    
    print("\n  [5/5] Kling...", end=" ")
    changes = 0
    try:
        kb = await pw.chromium.launch_persistent_context(
            kling_dir, headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        kp = kb.pages[0] if kb.pages else await kb.new_page()
        # Build URL without &
        url = "https://klingai.com/app/membership/membership-plan"
        url += "?r=33"
        url += "&f=1"
        await kp.goto(url, wait_until="load", timeout=30000)
        await kp.wait_for_timeout(3000)
        text = await kp.inner_text("body")
        parsed = detect_kling_parse(text)
        for pn, pd in parsed.items():
            for ep in tool["plans"]:
                if ep["name"].lower().startswith(pn.lower()):
                    old = ep.get("price_monthly")
                    new = pd.get("price_monthly")
                    if old != new and new is not None:
                        ep["price_monthly"] = new
                        changes += 1
                        print(f"{pn}: ${old} -> ${new}", end="; ")
                    break
        await kb.close()
        print("OK" if not changes else "")
    except Exception as e:
        print(f"Error: {e}")
    return changes


async def main():
    print(f"=== Pricing Auto-Update: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    if DRY_RUN: print("[DRY-RUN mode]\n")

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("ERROR: pip install playwright && playwright install chromium")
        sys.exit(1)

    data = load_tools()
    changes = 0

    scrapers = [
        ("heygen", "https://www.heygen.com/pricing", detect_heygen, 30000),
        ("synthesia", "https://www.synthesia.io/pricing", detect_synthesia, 60000),
        ("runway", "https://runwayml.com/pricing", detect_runway, 60000),
        ("pika", "https://pika.art/pricing", detect_pika, 30000),
    ]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        pg = await ctx.new_page()

        for idx, (tid, url, det, to) in enumerate(scrapers, 1):
            tool = next((t for t in data["tools"] if t["id"] == tid), None)
            if not tool or tool.get("status") == "discontinued":
                print(f"  [{idx}/5] {tid}: skipped")
                continue
            print(f"\n  [{idx}/5] {tool['name']}...", end=" ")
            try:
                result = await scrape_one(pg, url, det, to)
                if not result:
                    print("skipped")
                    continue
                for pname, pdata in result.items():
                    for ep in tool["plans"]:
                        if ep["name"].lower().startswith(pname.lower()):
                            old = ep.get("price_monthly")
                            new = pdata.get("price_monthly")
                            if old != new and new is not None:
                                ep["price_monthly"] = new
                                changes += 1
                                print(f"{pname}: ${old} -> ${new}", end="; ")
                            break
                print("OK")
            except Exception as e:
                print(f"Error: {e}")

        await browser.close()

        # Kling (uses persistent login, separate PW context)
        changes += await scrape_kling(pw, data)

    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    save_tools(data)
    print(f"\n{'Changed' if changes else 'No changes'} - {changes} pricing update(s)")
    print("=== Done ===")

if __name__ == "__main__":
    asyncio.run(main())
