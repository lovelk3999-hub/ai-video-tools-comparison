import json
with open("E:\\ai\\program\\google seo web\\ai-video-tools-comparison\\data\\tools.json", "r", encoding="utf-8-sig") as f:
    d = json.load(f)
m = {t["id"]: t for t in d["tools"]}

p = m["pika"]
p["plans"] = [
    {"name": "Free", "price_monthly": 0, "price_yearly": 0, "credits": "80 credits/mo", "resolution": "480p", "video_length": "5 sec", "features": ["80 credits/mo", "480p only", "Watermark", "Basic generation"]},
    {"name": "Basic", "price_monthly": 10, "price_yearly": 8, "credits": "700 credits/mo", "resolution": "1080p", "video_length": "5 sec", "features": ["700 credits/mo", "1080p", "No watermark", "Commercial use", "Pika 2.5"]},
    {"name": "Standard", "price_monthly": 35, "price_yearly": 28, "credits": "2300 credits/mo", "resolution": "1080p", "video_length": "10 sec", "features": ["2300/mo", "1080p", "Fast gen", "All effects"]},
    {"name": "Pro", "price_monthly": 95, "price_yearly": 76, "credits": "6000 credits/mo", "resolution": "4K", "video_length": "10 sec", "features": ["6000/mo", "4K", "Fastest", "Priority"]}
]

s = m["synthesia"]
s["plans"][1]["price_monthly"] = 19
s["plans"][1]["price_yearly"] = 14
s["plans"][2]["price_monthly"] = 89
s["plans"][2]["price_yearly"] = 59

with open("E:\\ai\\program\\google seo web\\ai-video-tools-comparison\\data\\tools.json", "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

for t in d["tools"]:
    ps = ", ".join([f'{p["name"]}: ${p["price_monthly"]}/mo' if p["price_monthly"] else f'{p["name"]}: Custom' for p in t["plans"]])
    print(f'{t["name"]}: {ps}')
