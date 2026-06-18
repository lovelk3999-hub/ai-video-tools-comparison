import asyncio, re, json, urllib.request
from playwright.async_api import async_playwright

results = {}

def fetch_page(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="ignore")

# Runway
try:
    html = fetch_page("https://runwayml.com/pricing")
    prices = re.findall(r"\$([\d,]+(?:\.\d+)?)\s*/?\s*(?:month|mo)", html, re.I)
    plans = re.findall(r"(?i)(Free|Standard|Pro|Max|Enterprise)\s*[^<]{0,40}", html)
    results["Runway"] = {"prices": [f"${p}/mo" for p in prices[:6]], "plans": list(set(p.strip() for p in plans if len(p) > 3))[:6]}
except Exception as e:
    results["Runway"] = {"error": str(e)}

# HeyGen
try:
    html = fetch_page("https://www.heygen.com/pricing")
    prices = re.findall(r"\$([\d,]+(?:\.\d+)?)\s*/?\s*(?:month|mo)", html, re.I)
    plans = re.findall(r"(?i)(Free|Creator|Business|Enterprise)\s*[^<]{0,40}", html)
    results["HeyGen"] = {"prices": [f"${p}/mo" for p in prices[:10]], "plans": list(set(p.strip() for p in plans if len(p) > 3))[:6]}
except Exception as e:
    results["HeyGen"] = {"error": str(e)}

# Pika
try:
    html = fetch_page("https://pika.art/pricing")
    prices = re.findall(r"\$([\d,]+(?:\.\d+)?)", html)
    plans = re.findall(r"(?i)(Free|Basic|Pro|Enterprise)\s*[^<]{0,40}", html)
    results["Pika"] = {"prices": [f"${p}" for p in prices[:8]], "plans": list(set(p.strip() for p in plans if len(p) > 3))[:6]}
except Exception as e:
    results["Pika"] = {"error": str(e)}

async def fetch_all():
    async with async_playwright() as p:
        # Synthesia
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.synthesia.io/pricing", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        text = await page.inner_text("body")
        prices = re.findall(r"\$([\d,]+(?:\.\d+)?)\s*/?\s*(?:month|mo)", text, re.I)
        plans = re.findall(r"(?i)(Free|Starter|Creator|Enterprise|Personal|Business)\s*\b", text)
        results["Synthesia"] = {"prices": [f"${p}/mo" for p in prices[:8]], "plans": list(set(plans))[:6]}
        await browser.close()
        
        # Kling
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://klingai.com", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        text = await page.inner_text("body")
        prices = re.findall(r"(?:\$|¥)([\d,]+(?:\.\d+)?)", text)
        plans = re.findall(r"(?i)(Free|Basic|Plus|Pro|Enterprise|Standard|Premium)\s*\b", text)
        results["Kling"] = {"prices": [f"${p}" for p in prices[:8]], "plans": list(set(plans))[:6]}
        await browser.close()
        
        # Sora
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://openai.com/sora/", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        text = await page.inner_text("body")
        prices = re.findall(r"\$([\d,]+(?:\.\d+)?)", text)
        plans = re.findall(r"(?i)(Plus|Pro|Enterprise|Free)\s*\b", text)
        results["Sora"] = {"prices": [f"${p}" for p in prices[:8]], "plans": list(set(plans))[:6]}
        await browser.close()

asyncio.run(fetch_all())

for name, data in results.items():
    print(f"\n=== {name} ===")
    if "error" in data:
        print(f"  ERROR: {data['error']}")
    else:
        print(f"  Prices: {data.get('prices', [])}")
        print(f"  Plans: {data.get('plans', [])}")

with open("E:\\ai\\program\\google seo web\\ai-video-tools-comparison\\data\\pricing_refresh.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
