import asyncio
from playwright.async_api import async_playwright

async def search_google(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 搜 Google
        await page.goto(f"https://www.google.com/search?q={query}&hl=en", wait_until="domcontentloaded", timeout=15000)
        await page.wait_for_timeout(2000)
        
        # 提取搜索结果
        results = await page.evaluate("""
            () => {
                const items = document.querySelectorAll('div.g');
                return Array.from(items).slice(0, 8).map(item => {
                    const h3 = item.querySelector('h3');
                    const link = item.querySelector('a');
                    const snippet = item.querySelector('span.aCOpRe, div[data-sncf]');
                    return {
                        title: h3 ? h3.innerText : '',
                        url: link ? link.href : '',
                        snippet: snippet ? snippet.innerText.slice(0, 150) : ''
                    };
                });
            }
        """)
        
        await browser.close()
        return results

async def main():
    queries = [
        "AI video tools pricing comparison 2026",
        "heygen synthesia runway comparison pricing",
        "AI video generation platform compare",
        "best AI video tool comparison website"
    ]
    
    for q in queries:
        print(f"\n=== {q} ===")
        try:
            results = await search_google(q)
            for r in results:
                if r["title"]:
                    print(f"  {r['title']}")
                    if r["url"]:
                        print(f"    URL: {r['url'][:100]}")
                    if r["snippet"]:
                        print(f"    {r['snippet']}")
        except Exception as e:
            print(f"  Error: {e}")

asyncio.run(main())
