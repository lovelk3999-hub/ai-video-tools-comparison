import asyncio, re, json, urllib.request
from playwright.async_api import async_playwright

async def extract_heygen():
    req = urllib.request.Request("https://www.heygen.com/pricing", 
        headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    prices = re.findall(r"\$[\d,]+(?:\.\d+)?\s*/\s*(?:month|mo)", html)
    plans = re.findall(r"(?i)(Free|Creator|Pro|Enterprise|Business)\s*[^<]{0,40}", html)
    return {"name": "HeyGen", "prices": prices[:10], "plans": list(set(p.strip() for p in plans if len(p.strip()) > 3))[:10]}

async def extract_runway():
    req = urllib.request.Request("https://runwayml.com/pricing",
        headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    prices = re.findall(r"\$[\d,]+(?:\.\d+)?\s*/?\s*(?:month|mo)", html)
    plans = re.findall(r"(?i)(Free|Standard|Pro|Max|Enterprise)\s*[^<]{0,40}", html)
    return {"name": "Runway", "prices": prices[:10], "plans": list(set(p.strip() for p in plans if len(p.strip()) > 3))[:10]}

async def extract_pika():
    req = urllib.request.Request("https://pika.art/pricing",
        headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    prices = re.findall(r"\$[\d,]+(?:\.\d+)?\s*/?\s*(?:month|mo)", html)
    plans = re.findall(r"(?i)(Free|Basic|Pro|Enterprise)\s*[^<]{0,40}", html)
    return {"name": "Pika", "prices": prices[:10], "plans": list(set(p.strip() for p in plans if len(p.strip()) > 3))[:10]}

async def extract_synthesia():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.synthesia.io/pricing", wait_until="domcontentloaded", timeout=30000)
        text = await page.inner_text("body")
        await browser.close()
        prices = re.findall(r"\$[\d,]+(?:\.\d+)?(?:\s*/\s*(?:month|mo|yr|year))?", text)
        plans = re.findall(r"(?i)(Free|Starter|Creator|Pro|Enterprise|Personal|Business)\s*\b", text)
        return {"name": "Synthesia", "prices": prices[:10], "plans": list(set(plans))[:10]}

async def extract_kling():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://klingai.com", wait_until="domcontentloaded", timeout=30000)
        text = await page.inner_text("body")
        await browser.close()
        prices = re.findall(r"(?:\$|¥)[\d,]+(?:\.\d+)?(?:\s*/?\s*(?:month|mo|yr|year|月))?", text)
        plans_en = re.findall(r"(?i)(Free|Basic|Plus|Pro|Enterprise|Standard|Premium)\s*\b", text)
        return {"name": "Kling", "prices": prices[:10], "plans": list(set(plans_en))[:10]}

async def main():
    results = await asyncio.gather(
        extract_heygen(), extract_runway(), extract_pika(),
        extract_synthesia(), extract_kling()
    )
    for r in results:
        print(f"\n=== {r['name']} ===")
        print(f"  Prices: {r['prices']}")
        print(f"  Plans: {r['plans']}")

asyncio.run(main())
