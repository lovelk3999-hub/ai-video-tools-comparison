import urllib.request, re, json

def fetch_page(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def extract_prices(html, pattern):
    return list(set(re.findall(pattern, html)))

results = {}

# 1. HeyGen
html = fetch_page("https://www.heygen.com/pricing")
prices = re.findall(r"\$([\d,]+(?:\.\d+)?)\s*/\s*(?:month|mo)", html, re.I)
print(f"HeyGen prices: {[f'${p}/mo' for p in prices[:8]]}")

# 2. Runway
html = fetch_page("https://runwayml.com/pricing")
prices = re.findall(r"\$([\d,]+(?:\.\d+)?)\s*/?\s*(?:month|mo)", html, re.I)
print(f"Runway prices: {[f'${p}/mo' for p in prices[:8]]}")
plans = re.findall(r"(?i)(Free|Standard|Pro|Max|Enterprise)\s*[^<]{0,30}", html)
print(f"Runway plans: {list(set(p.strip() for p in plans if len(p) > 3))[:6]}")

# 3. Pika
html = fetch_page("https://pika.art/pricing")
prices = re.findall(r"\$([\d,]+(?:\.\d+)?)\s*/?\s*(?:month|mo)", html, re.I)
print(f"Pika prices: {[f'${p}/mo' for p in prices[:8]]}")

# 4. Sora - check OpenAI pricing page for Sora
html = fetch_page("https://openai.com/api/pricing/")
if "sora" in html.lower():
    sora_info = re.findall(r"(?i)(sora[^<]{0,100})", html)[:3]
    print(f"Sora found in OpenAI pricing: {sora_info}")
else:
    print("Sora not in pricing page - likely ChatGPT Plus/Pro inclusion")
