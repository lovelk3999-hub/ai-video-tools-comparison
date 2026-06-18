#!/usr/bin/env python3
"""Static site generator for AI Video Tools Comparison"""
import json, os, shutil, itertools
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "tools.json")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

tools = data["tools"]
tool_map = {t["id"]: t for t in tools}

def render_nav():
    items = "".join(f'<option value="/{t["id"]}/">{t["name"]}</option>' for t in tools)
    return f"""
<header>
  <div class="container">
    <a href="/" style="display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit;">
      <span style="font-size:24px;">🎬</span>
      <h1 style="font-size:18px;">AI Video Tools Comparison</h1>
    </a>
    <nav>
      <a href="/">Home</a>
      <select onchange="if(this.value)window.location=this.value" style="background:rgba(255,255,255,0.15);color:white;border:1px solid rgba(255,255,255,0.3);padding:6px 12px;border-radius:6px;font-size:13px;">
        <option value="">Compare Tools...</option>
        {items}
      </select>
    </nav>
  </div>
</header>"""

def price_display(p):
    if p is None: return "Custom"
    return f"${p}"

price_display_lambda = staticmethod(price_display)

def generate_index():
    overview_rows = ""
    for t in tools:
        min_price = float("inf")
        for plan in t["plans"]:
            if plan["price_monthly"] is not None and plan["price_monthly"] > 0:
                min_price = min(min_price, plan["price_monthly"])
        start_price = f"${min_price:.0f}/mo" if min_price < float("inf") else "Custom"
        has_free = any(p["price_monthly"] == 0 for p in t["plans"])
        
        overview_rows += f"""
        <tr>
            <td><a href="/{t['id']}/" style="font-weight:600;color:#1e40af;">{t['name']}</a></td>
            <td><span class="price" style="font-size:18px;">{start_price}</span></td>
            <td>{'✅ Yes' if has_free else '❌ No'}</td>
            <td>{'Avatar / Digital Human' if t['category'] == 'avatar' else 'Text-to-Video Generation'}</td>
            <td><a href="/{t['id']}/" class="btn" style="padding:6px 16px;font-size:13px;">Details</a></td>
        </tr>"""
    # Add comparison links
    compare_links = ""
    pairs = list(itertools.combinations(tools, 2))
    for a, b in pairs[:6]:
        compare_links += f'<p><a href="/compare/{a["id"]}-{b["id"]}/" style="color:#1e40af;">{a["name"]} vs {b["name"]}</a></p>'
    
    # Tool cards
    tool_cards = ""
    for t in tools:
        min_price = float("inf")
        for plan in t["plans"]:
            if plan["price_monthly"] is not None and plan["price_monthly"] > 0:
                min_price = min(min_price, plan["price_monthly"])
        start_price = f"${min_price:.0f}/mo" if min_price < float("inf") else "Custom"
        tool_cards += f"""
        <div class="tool-card">
            <h2><a href="/{t['id']}/">{t['name']}</a></h2>
            <p class="desc">{t['description'][:120]}...</p>
            <p><span class="price">{start_price}</span> <span class="price-label">starting</span></p>
            <p style="margin-top:8px;"><span style="color:#f59e0b;">*</span> {t.get('g2_rating', 'N/A')} ({t.get('g2_reviews', 'N/A')} reviews)</p>
            <a href="/{t['id']}/" class="btn" style="padding:6px 16px;font-size:13px;">View Plans -></a>
        </div>"""
    
    faq_section = ""
    for faq in data.get("faqs", []):
        faq_section += f"""
        <div class="faq-item" style="background:white;border-radius:8px;padding:16px 20px;margin-bottom:8px;box-shadow:0 1px 2px rgba(0,0,0,0.05);">
            <h3 style="font-size:15px;cursor:pointer;" onclick="this.nextElementSibling.classList.toggle('hidden')">{faq['q']}</h3>
            <p style="font-size:14px;color:#475569;margin-top:8px;">{faq['a']}</p>
        </div>"""
    
    content = f"""
<section class="hero">
    <div class="container">
        <h1>AI Video Tool Pricing Comparison</h1>
        <p>Compare pricing, features, and capabilities of the top 6 AI video creation platforms. Find the perfect tool for your content creation needs.</p>
        <p style="font-size:13px;color:#94a3b8;margin-top:8px;">Updated June 2026 • Independent comparison</p>
    </div>
</section>
<div class="container">
    <h2 style="margin-top:32px;">📊 Quick Overview</h2>
    <div class="table-container"><table><thead><tr><th>Tool</th><th>Starting Price</th><th>Free Plan</th><th>Category</th><th></th></tr></thead><tbody>{overview_rows}</tbody></table></div>
    <h2 style="margin-top:40px;">🔧 Tool Details</h2>
    <div class="tool-grid">{tool_cards}</div>
    <h2 style="margin-top:40px;">⚖️ Popular Comparisons</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:16px 0;">{compare_links}</div>
    <h2 style="margin-top:40px;">❓ Frequently Asked Questions</h2>
    {faq_section}
</div>"""
    return render_page("AI Video Tool Pricing Comparison 2026 - Independent Guide", content)

def generate_tool_page(t):
    plan_boxes = ""
    for plan in t["plans"]:
        monthly = price_display(plan["price_monthly"])
        yearly = price_display(plan["price_yearly"]) if plan["price_yearly"] != plan["price_monthly"] else ""
        featured = " featured" if plan["name"] == "Pro" or (plan["name"] == "Creator" and t["id"] == "heygen") else ""
        features = "".join(f"<li>{f}</li>" for f in plan["features"])
        plan_boxes += f"""
        <div class="plan-box{featured}">
            <h3>{plan['name']}</h3>
            <div class="price">{monthly}<span class="price-period">/mo</span></div>
            {f'<div class="price-period" style="font-size:12px;">or {yearly}/mo billed yearly</div>' if yearly else ''}
            <p style="font-size:13px;color:#64748b;margin-top:8px;">{plan.get('credits','')}</p>
            <ul>{features}</ul>
        </div>"""
    
    feature_rows = ""
    for k, v in t["features"].items():
        label = k.replace("_", " ").title()
        val = "✅" if v is True else ("❌" if v is False else str(v))
        feature_rows += f"<tr><td>{label}</td><td>{val}</td></tr>"
    
    # Comparisons to other tools
    compare_section = ""
    for other in tools:
        if other["id"] == t["id"]: continue
        compare_section += f'<div class="compare-pair"><h3><a href="/compare/{t["id"]}-{other["id"]}/">{t["name"]} vs {other["name"]}</a></h3></div>'
    
    content = f"""
<section class="hero">
    <div class="container">
        <h1>{t["name"]} Pricing & Plans 2026</h1>
        <p>{t["description"]}</p>
    </div>
</section>
<div class="container">
    <h2 style="margin-top:32px;">💵 Pricing Plans</h2>
    <div class="plan-grid">{plan_boxes}</div>
    <h2 style="margin-top:32px;">✨ Key Features</h2>
    <div class="table-container"><table><thead><tr><th>Feature</th><th>Details</th></tr></thead><tbody>{feature_rows}</tbody></table></div>
    {f'<div style="background:#f8fafc;border-radius:8px;padding:16px;margin:16px 0;"><span style="color:#f59e0b;">*</span> <strong>G2 Rating:</strong> {t.get("g2_rating","N/A")}/5 ({t.get("g2_reviews","N/A")} reviews)</div>' if t.get("g2_rating") else ''}
    <h2 style="margin-top:32px;">⚖️ Compare with Alternatives</h2>
    {compare_section}
    <p style="margin-top:32px;">
        <a href="/" class="btn btn-secondary">← Back to All Tools</a>
        <a href="{t["url"]}" class="btn" target="_blank" rel="nofollow noopener">Visit {t["name"]} -></a>
    </p>
</div>"""
    return render_page(f"{t['name']} Pricing & Plans 2026 - Features, Free Plan & Alternatives", content)

def generate_compare_page(tool_a, tool_b):
    a, b = tool_a, tool_b
    compare_rows = ""
    # Compare prices
    compare_rows += f"<tr><td><strong>Starting Price</strong></td><td>{price_display(a['plans'][1]['price_monthly'])}/mo</td><td>{price_display(b['plans'][1]['price_monthly'])}/mo</td></tr>"
    compare_rows += f"<tr><td><strong>Free Plan</strong></td><td>{'✅ Yes' if any(p['price_monthly']==0 for p in a['plans']) else '❌ No'}</td><td>{'✅ Yes' if any(p['price_monthly']==0 for p in b['plans']) else '❌ No'}</td></tr>"
    
    # Compare features
    all_features = set(list(a["features"].keys()) + list(b["features"].keys()))
    for feat in sorted(all_features):
        va = a["features"].get(feat, False)
        vb = b["features"].get(feat, False)
        va_str = "✅" if va is True else ("❌" if va is False else str(va))
        vb_str = "✅" if vb is True else ("❌" if vb is False else str(vb))
        label = feat.replace("_", " ").title()
        compare_rows += f"<tr><td>{label}</td><td>{va_str}</td><td>{vb_str}</td></tr>"
    
    # G2 Rating
    compare_rows += f"<tr><td><strong>G2 Rating</strong></td><td>{'*' if a.get('g2_rating') else ''} {a.get('g2_rating','N/A')}/5</td><td>{'*' if b.get('g2_rating') else ''} {b.get('g2_rating','N/A')}/5</td></tr>"
    
    # Plan boxes
    plans_a = ""
    for plan in a["plans"][:3]:
        monthly = price_display(plan["price_monthly"])
        plans_a += f"""<div class="plan-box"><h3>{plan['name']}</h3><div class="price">{monthly}<span class="price-period">/mo</span></div><p style="font-size:12px;color:#64748b;">{plan.get('credits','')}</p></div>"""
    plans_b = ""
    for plan in b["plans"][:3]:
        monthly = price_display(plan["price_monthly"])
        plans_b += f"""<div class="plan-box"><h3>{plan['name']}</h3><div class="price">{monthly}<span class="price-period">/mo</span></div><p style="font-size:12px;color:#64748b;">{plan.get('credits','')}</p></div>"""
    
    # Simple verdict
    a_avg = sum(p["price_monthly"] for p in a["plans"] if p["price_monthly"] and p["price_monthly"] > 0) / max(1, sum(1 for p in a["plans"] if p["price_monthly"] and p["price_monthly"] > 0))
    b_avg = sum(p["price_monthly"] for p in b["plans"] if p["price_monthly"] and p["price_monthly"] > 0) / max(1, sum(1 for p in b["plans"] if p["price_monthly"] and p["price_monthly"] > 0))
    
    if a_avg < b_avg:
        verdict = f"**{a['name']}** is the more affordable option with average plan pricing of ${a_avg:.0f}/mo compared to ${b_avg:.0f}/mo for {b['name']}. However, pricing is just one factor — consider your specific use case and feature requirements."
    elif a_avg > b_avg:
        verdict = f"**{b['name']}** is the more affordable option with average plan pricing of ${b_avg:.0f}/mo compared to ${a_avg:.0f}/mo for {a['name']}. However, pricing is just one factor — consider your specific use case and feature requirements."
    else:
        verdict = f"Both {a['name']} and {b['name']} offer competitive pricing. The best choice depends on your specific use case and feature requirements."
    
    content = f"""
<section class="hero">
    <div class="container">
        <h1>{a["name"]} vs {b["name"]}: Which is Better in 2026?</h1>
        <p>Comprehensive comparison of {a["name"]} and {b["name"]} — pricing, features, and capabilities to help you decide.</p>
    </div>
</section>
<div class="container">
    <h2 style="margin-top:32px;">📋 Feature Comparison</h2>
    <div class="table-container"><table class="compare-table"><thead><tr><th style="width:25%;">Feature</th><th style="width:35%;">{a["name"]}</th><th style="width:35%;">{b["name"]}</th></tr></thead><tbody>{compare_rows}</tbody></table></div>
    <h2 style="margin-top:32px;">💰 Pricing Comparison</h2>
    <div class="plan-grid">{plans_a}{plans_b}</div>
    <div style="background:#f0fdf4;border-radius:12px;padding:24px;margin:24px 0;border:1px solid #bbf7d0;">
        <h3 style="color:#059669;">🏆 Verdict</h3>
        <p style="margin-top:8px;">{verdict}</p>
        <p style="margin-top:12px;font-size:14px;color:#475569;">
            <a href="/{a['id']}/" style="color:#1e40af;">View {a['name']} Plans -></a> &nbsp;|&nbsp; 
            <a href="/{b['id']}/" style="color:#1e40af;">View {b['name']} Plans -></a>
        </p>
    </div>
    <p style="margin-top:24px;"><a href="/" class="btn btn-secondary">← Back to All Tools</a></p>
</div>"""
    return render_page(f"{a['name']} vs {b['name']} 2026 - Pricing, Features & Verdict", content)

def render_page(title, content):
    nav = render_nav()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="Compare AI video tool pricing, plans, and features. Independent comparison of HeyGen, Synthesia, Runway, Pika, Sora, and Kling.">
    <style>
        *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
        body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,sans-serif;background:#f8fafc;color:#1e293b;line-height:1.6;}}
        .container{{max-width:1200px;margin:0 auto;padding:0 20px;}}
        header{{background:linear-gradient(135deg,#1e40af 0%,#3b82f6 100%);color:white;padding:20px 0;}}
        header .container{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;}}
        header h1{{font-size:20px;font-weight:700;}}
        header a{{color:white;text-decoration:none;}}
        nav{{display:flex;align-items:center;gap:16px;}}
        nav a{{font-size:14px;opacity:0.9;transition:opacity 0.2s;}}
        nav a:hover{{opacity:1;text-decoration:underline;}}
        .hero{{background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 100%);padding:48px 0 36px;text-align:center;}}
        .hero h1{{font-size:32px;font-weight:800;margin-bottom:10px;}}
        .hero p{{font-size:16px;color:#475569;max-width:600px;margin:0 auto;}}
        .table-container{{overflow-x:auto;margin:20px 0;border-radius:10px;}}
        table{{width:100%;border-collapse:collapse;background:white;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.08);}}
        th,td{{padding:10px 14px;text-align:left;border-bottom:1px solid #e2e8f0;font-size:14px;}}
        th{{background:#f1f5f9;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:0.05em;color:#475569;}}
        tr:hover{{background:#f8fafc;}}
        .tool-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px;margin:20px 0;}}
        .tool-card{{background:white;border-radius:10px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,0.08);}}
        .tool-card:hover{{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.1);}}
        .tool-card h2{{font-size:18px;margin-bottom:6px;}}
        .tool-card h2 a{{color:#1e40af;text-decoration:none;}}
        .tool-card .desc{{color:#64748b;font-size:13px;margin-bottom:10px;}}
        .price{{font-size:22px;font-weight:700;color:#059669;}}
        .price-label{{font-size:12px;color:#94a3b8;}}
        .plan-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin:20px 0;}}
        .plan-box{{background:white;border-radius:10px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,0.08);border:1px solid #e2e8f0;text-align:center;}}
        .plan-box.featured{{border-color:#3b82f6;box-shadow:0 0 0 2px #bfdbfe;}}
        .plan-box h3{{font-size:15px;color:#475569;margin-bottom:6px;}}
        .plan-box .price{{font-size:26px;font-weight:800;color:#1e293b;}}
        .plan-box .price-period{{font-size:13px;color:#94a3b8;}}
        .plan-box ul{{list-style:none;text-align:left;margin-top:12px;}}
        .plan-box ul li{{padding:3px 0;font-size:12px;color:#475569;}}
        .plan-box ul li::before{{content:\"âœ“ \";color:#059669;font-weight:700;}}
        .compare-pair{{background:white;border-radius:8px;padding:14px 18px;margin-bottom:10px;box-shadow:0 1px 2px rgba(0,0,0,0.05);}}
        .compare-pair h3{{font-size:15px;}}
        .compare-pair h3 a{{color:#1e40af;text-decoration:none;}}
        .btn{{display:inline-block;background:#3b82f6;color:white;padding:8px 20px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;}}
        .btn:hover{{background:#2563eb;}}
        .btn-secondary{{background:#e2e8f0;color:#1e293b;}}
        .btn-secondary:hover{{background:#cbd5e1;}}
        footer{{background:#1e293b;color:#94a3b8;padding:24px 0;text-align:center;font-size:13px;margin-top:48px;}}
        footer a{{color:#94a3b8;text-decoration:underline;}}
        .hidden{{display:none;}}
        @media(max-width:768px){{.hero h1{{font-size:22px;}}.tool-grid{{grid-template-columns:1fr;}}.plan-grid{{grid-template-columns:1fr 1fr;}}}}
    </style>
</head>
<body>
    {nav}
    {content}
    <footer>
        <div class="container">
            <p>© 2026 AI Video Tools Comparison. Independent comparison of AI video creation platforms.</p>
            <p style="margin-top:6px;">Prices and features sourced from official websites. Always verify on the official site. This site uses affiliate links.</p>
        </div>
    </footer>
</body>
</html>"""

def main():
    print(f"Generating site from {len(tools)} tools...")
    
    # Clean output
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    # Generate index
    html = generate_index()
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] index.html ({len(html)} bytes)")
    
    # Generate tool pages
    for t in tools:
        html = generate_tool_page(t)
        tool_dir = os.path.join(OUTPUT_DIR, t["id"])
        os.makedirs(tool_dir, exist_ok=True)
        with open(os.path.join(tool_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [OK] {t['id']}/index.html")
    
    # Generate compare pages
    pairs = list(itertools.combinations(tools, 2))
    for a, b in pairs:
        html = generate_compare_page(a, b)
        comp_dir = os.path.join(OUTPUT_DIR, "compare", f"{a['id']}-{b['id']}")
        os.makedirs(comp_dir, exist_ok=True)
        with open(os.path.join(comp_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [OK] compare/{a['id']}-{b['id']}/index.html")
    
    # Summary
    total = 1 + len(tools) + len(pairs)
    print(f"\n✅ Generated {total} pages:")
    print(f"  - 1 index page")
    print(f"  - {len(tools)} tool pages")
    print(f"  - {len(pairs)} comparison pages")
    print(f"  Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
