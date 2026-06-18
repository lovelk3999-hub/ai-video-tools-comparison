# STATUS - AI Video Tools Comparison

> 上次更新: 2026-06-19
> 当前任务: 09-more-tools-research.md (Phase 2 - 更多新工具)

---

## 最新进展

G2评分 + Reddit讨论已集成完毕 | Google Search Console已验证 & sitemap已提交 | 正在补官方视频

---

## 完成状态

| 模块 | 状态 | 说明 |
|------|------|------|
| 网站架构 | ✅ 完成 | Cloudflare Pages + Python静态生成 + GitHub Actions |
| 14个工具收录 | ✅ 完成 | HeyGen, Synthesia, Runway, Pika, Sora, Kling, Invideo AI, CapCut, Colossyan, Seedance, HailuoAI, Luma, Vidu, D-ID |
| 108个页面生成 | ✅ 完成 | 首页 + 14详情页 + 80+对比页 + sitemap + robots |
| FAQ 17条+JSON-LD | ✅ 完成 | 基础问答 + Schema.org结构化数据 |
| SEO基础 | ✅ 完成 | OG标签 / sitemap.xml / robots.txt / canonical |
| 官方视频 | ✅ 14/14 | 全部工具已有YouTube官方视频嵌入 |
| CI/CD自动部署 | ✅ 完成 | GitHub Actions push触发 -> Cloudflare Pages |
| G2评分采集 | ✅ 完成 | TinyFish API代理采集，12/14工具有数据 |
| Reddit讨论采集 | ✅ 完成 | TinyFish搜索，每个工具3条Reddit帖子 |
| G2+Reddit前端展示 | ✅ 完成 | 详情页显示G2评分 + Reddit讨论卡片 |
| 定价数据自动采集 | ✅ 完成 | Playwright每月定时采集 |
| Google Search Console | ✅ 已验证 | meta tag验证 + sitemap已提交 |
| Pika官方视频 | ✅ 完成 | Pika 2.0 Scene Ingredients |
| Vidu官方视频 | ✅ 完成 | Vidu Q3 Suite Upgraded |
| FAQ扩充到30+条 | ✅ 完成 | 已从17条扩充到30条 |
| 新增工具(PixVerse) | ✅ 完成 | PixVerse已收录，15个工具，123页 |

---

## 核心文件

| 文件/脚本 | 说明 |
|-----------|------|
| scripts/generate.py | 静态站点生成器，含G2评分 + Reddit展示 |
| scripts/collect_social_proxy.py | TinyFish代理采集G2+Reddit |
| data/tools.json | 所有工具数据，含G2评分 |

## 关键决策

见 DECISIONS.md

## 已知问题

1. G2有DataDome CAPTCHA强反爬 -> 走TinyFish API代理
2. Seedance/HailuoAI没有G2数据 -> 暂无替代数据源
3. Reddit反爬严格 -> 走TinyFish搜索
4. Windows GBK编码 -> print()不能用emoji，文件I/O必须encoding=utf-8
5. Sora定价不透明 -> 需要人工关注更新
