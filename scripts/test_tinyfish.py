import requests, json, re, os

API_KEY = 'sk-tinyfish-6JgE2jSpgIiwPrHdXjMvrclc5638kcAx'
PROXY = 'http://127.0.0.1:7897'
BASE = r'E:\ai\program\google seo web\ai-video-tools-comparison'

def tf_search(query, num=5):
    url = f'https://api.search.tinyfish.ai?query={requests.utils.quote(query)}&language=en&numResults={num}'
    r = requests.get(url, headers={'X-API-Key': API_KEY}, proxies={'http': PROXY, 'https': PROXY}, timeout=15)
    return r.json().get('results', [])

for tool in ['HeyGen', 'Synthesia', 'Runway', 'Pika', 'Kling']:
    results = tf_search(f'{tool} G2 rating')
    found = False
    for res in results:
        snip = res.get('snippet', '')
        m = re.search(r'rated ([d.]+) stars? by ([d,]+)', snip)
        if m:
            print(f'{tool}: {m.group(1)}/5 ({m.group(2)} reviews)')
            found = True
            break
    if not found:
        print(f'{tool}: not found in search snippets')

print('\n--- Reddit ---')
for tool in ['HeyGen', 'Synthesia']:
    results = tf_search(f'site:reddit.com {tool} review 2026', 3)
    print(f'\n{tool} Reddit:')
    for r2 in results[:3]:
        print(f'  [{r2.get("date","")}] {r2.get("title","")[:60]}')
        print(f'  {r2.get("snippet","")[:80]}')
