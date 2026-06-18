import json
with open("E:\\ai\\program\\google seo web\\ai-video-tools-comparison\\data\\tools.json", "r", encoding="utf-8-sig") as f:
    d = json.load(f)
m = {t["id"]: t for t in d["tools"]}

k = m["kling"]
k["plans"] = [
    {"name": "Free", "price_monthly": 0, "price_yearly": 0, "credits": "128 inspiration pts/mo (login)", "resolution": "480p", "video_length": "5 sec", "features": ["128 free pts/mo", "480p export", "30 creations limit", "Watermark", "No commercial use"]},
    {"name": "Gold", "price_monthly": 8, "price_yearly": None, "credits": "660 inspiration pts/mo", "resolution": "1080p", "video_length": "30 sec", "features": ["660 pts/mo (~$8)", "1080p export", "No watermark", "Fast queue", "Commercial use"]},
    {"name": "Platinum", "price_monthly": 33, "price_yearly": None, "credits": "3000 inspiration pts/mo", "resolution": "1080p", "video_length": "3 min", "features": ["3000 pts/mo (~$33)", "1080p export (4K available)", "Fastest queue", "Video extension", "Image enhance"]},
    {"name": "Diamond", "price_monthly": 81, "price_yearly": None, "credits": "8000 inspiration pts/mo", "resolution": "1080p", "video_length": "3 min", "features": ["8000 pts/mo (~$81)", "Priority queue", "New features first", "All perks"]},
    {"name": "Black Gold", "price_monthly": 160, "price_yearly": None, "credits": "26000 inspiration pts/mo", "resolution": "1080p+", "video_length": "3 min", "features": ["26000 pts/mo (~$160)", "All features", "Limited beta access", "Highest priority"]}
]
k["description"] = "Kuaishou's state-of-the-art AI video generation platform with powerful text-to-video and image-to-video capabilities. One of the leading AI video platforms with competitive per-use pricing model."

with open("E:\\ai\\program\\google seo web\\ai-video-tools-comparison\\data\\tools.json", "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("Kling pricing updated based on actual subscription page!")
for p in k["plans"]:
    print(f"  {p['name']}: ${p['price_monthly']}/mo - {p['credits']}")
