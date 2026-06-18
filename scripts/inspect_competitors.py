import asyncio
from playwright.async_api import async_playwright

async def inspect_site(url, name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(3000)  # Wait for JS to render
            
            title = await page.title()
            print(f"\n=== {name} ({url}) ===")
            print(f"  Title: {title}")
            
            # Get headings structure
            headings = await page.evaluate("""
                () => {
                    const hs = [];
                    for (let h of document.querySelectorAll('h1, h2, h3')) {
                        if (h.innerText.trim()) hs.push(h.tagName + ': ' + h.innerText.trim().slice(0, 80));
                    }
                    return hs.slice(0, 25);
                }
            """)
            print(f"  Page structure:")
            for h in headings:
                print(f"    {h}")
            
            # Count pricing/price mentions
            body_text = await page.inner_text("body")
            price_count = body_text.lower().count("$")
            plan_count = len([x for x in ["free", "pro", "enterprise", "starter", "creator", "standard", "basic"] if x in body_text.lower()])
            print(f"  Price markers: ${price_count}, Plan names: {plan_count}")
            print(f"  Body length: {len(body_text)} chars")
            
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            await browser.close()

async def main():
    sites = [
        ("https://artificialanalysis.ai/models", "artificialanalysis.ai"),
        ("https://costgoat.com/compare/llm-api", "CostGoat"),
        ("https://pricepertoken.com/", "PricePerToken"),
        ("https://automios.com/openai-vs-deepseek-vs-gemini-api-pricing-comparison/", "Automios"),
    ]
    for url, name in sites:
        await inspect_site(url, name)

asyncio.run(main())
