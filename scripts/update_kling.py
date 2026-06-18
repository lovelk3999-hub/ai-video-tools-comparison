"""
Kling Pricing Scraper - persistent browser login (douyin-index pattern)
"""
import asyncio, json, re, os, sys
from datetime import datetime
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_DIR = os.path.join(BASE_DIR, ".kling_browser")
TOOLS_JSON = os.path.normpath(os.path.join(BASE_DIR, "..", "data", "tools.json"))
MEMBERSHIP_URL = "https://klingai.com/app/membership/membership-plan?r=33&f=1"
FX = 7.2

def load():
    with open(TOOLS_JSON, encoding="utf-8") as f:
        return json.load(f)

def save(data):
    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(TOOLS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse(text):
    """Extract monthly prices from Kling membership page."""
    # Gold/Platinum/Diamond: "后续每月 58元"
    regular_prices = [int(m.group(1)) for m in re.finditer(r"后续每月\s*(\d+)\s*元", text)]
    # Black Gold: "续费金额：1149元" or "续费金额: 1149元"
    bg_prices = [int(m.group(1)) for m in re.finditer(r"续费金额[：:]\s*(\d+)\s*元", text)]
    
    print(f"  Regular monthly prices: {regular_prices}")
    print(f"  Black Gold prices: {bg_prices}")
    
    result = {"Free": {"price_monthly": 0}}
    
    plan_order = [("Gold", 660), ("Platinum", 3000), ("Diamond", 8000)]
    for i, (name, credits) in enumerate(plan_order):
        if i < len(regular_prices):
            usd = int(regular_prices[i] / FX + 0.5)
            print(f"    {name}: {regular_prices[i]} CNY -> ${usd}/mo")
            result[name] = {"price_monthly": usd, "credits": f"{credits} pts/mo"}
    
    if bg_prices:
        usd = int(bg_prices[0] / FX + 0.5)
        print(f"    Black Gold: {bg_prices[0]} CNY -> ${usd}/mo")
        result["Black Gold"] = {"price_monthly": usd, "credits": "26000 pts/mo"}
    
    return result


async def main():
    print("=== Kling Pricing Scraper ===")
    first = not os.path.exists(USER_DATA_DIR)
    
    async with async_playwright() as pw:
        browser = await pw.chromium.launch_persistent_context(
            USER_DATA_DIR, headless=not first,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        if first:
            print("\nFIRST RUN: Log in manually (120s)\n")
            await page.goto("https://klingai.com/app", timeout=60000)
            for i in range(120):
                await page.wait_for_timeout(1000)
                if "login" not in page.url.lower() and "auth" not in page.url.lower():
                    print("Logged in!")
                    break
                if i % 10 == 0: print(f"  Waiting {i+1}s")
            else:
                print("Timeout")
                await browser.close()
                return
        
        await page.goto(MEMBERSHIP_URL, wait_until="load", timeout=30000)
        await page.wait_for_timeout(3000)
        text = await page.inner_text("body")
        parsed = parse(text)
        
        data = load()
        tool = next((t for t in data["tools"] if t["id"] == "kling"), None)
        if tool:
            changes = 0
            for pn, pd in parsed.items():
                for ep in tool["plans"]:
                    if ep["name"].lower().startswith(pn.lower()):
                        old = ep.get("price_monthly")
                        new = pd.get("price_monthly")
                        if old != new and new is not None:
                            ep["price_monthly"] = new
                            changes += 1
                            print(f"  {pn}: ${old} -> ${new}")
                        break
            if changes:
                save(data)
                print(f"\n{changes} change(s)")
            else:
                print("\nNo changes")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
