# 决策日志 DECISIONS.md

> 追加式写入，不覆盖。格式：日期 | 决策 | 理由 | 来源

| 日期 | 决策 | 理由 | 来源 |
|------|------|------|------|
| 2026-06-19 | 确定对比网站定位：AI视频工具定价对比，不自己做评测 | 信息聚合，降低运营成本 | 项目启动 |
| 2026-06-19 | 技术栈：Cloudflare Pages + Python静态生成 + GitHub Actions | 零成本，自动部署 | 项目启动 |
| 2026-06-19 | Playwright采集定价数据，每月更新 | 无需API，官网直采 | 方案设计 |
| 2026-06-19 | 视频素材从测评博主/官网采集，不自己生成 | 降低内容制作成本 | 方案设计 |
| 2026-06-19 | 只做对比表+定价，不做主观评测 | 避免争议，保持中立定位 | 方案设计 |
| 2026-06-19 | 站点SEO：OG标签 + sitemap + robots.txt + FAQ结构化数据 | Google搜索排名优化 | SEO优化 |
2026-06-19 | CI/CD Secrets配置 | CF_API_TOKEN + CF_ACCOUNT_ID 添加到GitHub Secrets | 部署流水线
2026-06-19 | GitHub Actions权限修复 | 添加 contents: write 权限和工作流自动提交 | 自动部署修复
2026-06-19 | DataDome反爬对策 | G2用浏览器采集（非headless），Reddit用Playwright方案 | G2有强反爬
