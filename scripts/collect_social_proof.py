#!/usr/bin/env python3
import requests, json, re, os, time, sys
from datetime import datetime

API_KEY = 'sk-tinyfish-6JgE2jSpgIiwPrHdXjMvrclc5638kcAx'
PROXY = 'http://127.0.0.1:7897'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'tools.json')

# G2 tool IDs mapped to search-friendly names
G2_QUERIES = {
    "heygen": "HeyGen", "synthesia": "Synthesia", "runway": "RunwayML",
    "pika": "Pika AI", "sora": "Sora OpenAI",
    "kling": "Kling AI", "invideo": "Invideo AI",
    "capcut": "CapCut", "colossyan": "Colossyan",
    "seedance": "Seedance", "hailuoai": "Hailuo AI",
    "luma": "Luma Dream Machine", "vidu": "Vidu AI", "did": "D-ID"
}

def tf_search(query, num=5):
    url = f'https://api.search.tinyfish.ai?query={requests.utils.quote(query)}&language=en&numResults={num}'
    r = requests.get(url, headers={'X-API-Key': API_KEY},
                     proxies={'http': PROXY, 'https': PROXY}, timeout=15)
    return r.json().get('results', [])

def get_g2_rating(tool_id):
    name = G2_QUERIES.get(tool_id, tool_id)
    results = tf_search(f'G2.com {name} reviews', 5)
    for res in results:
        snip = res.get('snippet', '')
        m = re.search(r'([\d.]+) stars by ([\d,]+)', snip)
        if m:
            return float(m.group(1)), m.group(2)
    return None, None

def get_reddit_posts(tool_id, max_posts=3):
    name = G2_QUERIES.get(tool_id, tool_id)
    results = tf_search(f'site:reddit.com {name} review 2026', max_posts+2)
    posts = []
    for res in results[:max_posts]:
        posts.append({
            'title': res.get('title', ''),
            'snippet': res.get('snippet', '')[:150],
            'url': res.get('url', ''),
            'date': res.get('date', '')
        })
    return posts

def main():
    print('Loading tools.json...')
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for tool in data['tools']:
        tid = tool['id']
        print(f'\n[{tid}] {tool["name"]}')
        
        # Get G2 rating
        if not tool.get('g2_rating'):
            rating, reviews = get_g2_rating(tid)
            if rating:
                tool['g2_rating'] = rating
                tool['g2_reviews'] = reviews
                print(f'  G2: {rating}/5 ({reviews} reviews)')
            else:
                print('  G2: not found')
        
        # Get Reddit posts
        if not tool.get('reddit_posts'):
            posts = get_reddit_posts(tid)
            if posts:
                tool['reddit_posts'] = posts
                print(f'  Reddit: {len(posts)} posts')
                for p in posts:
                    print(f'    - {p["title"][:50]}')
            else:
                print('  Reddit: not found')
        
        time.sleep(0.5)  # Rate limit
    
    data['updated'] = datetime.now().strftime('%Y-%m-%d')
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'\nUpdated {len(data["tools"])} tools in tools.json')

if __name__ == '__main__':
    main()
