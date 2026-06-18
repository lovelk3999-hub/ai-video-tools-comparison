# AI Video Tools Comparison — Agent 工作规范

## 项目概述

AI 视频工具定价对比网站。静态站点生成器（Python）→ Cloudflare Pages 部署。
GitHub: https://github.com/lovelk3999-hub/ai-video-tools-comparison
网站: https://ai-video-tools-comparison.pages.dev

---

## 一、系统环境

| 项目 | 版本 |
|------|------|
| Shell | **PowerShell 5.1**（Windows 10） |
| Python | 3.12.10 |
| Node.js | 22.14.0 |
| Git | 2.51.0.windows.2 |
| 编码 | Windows GBK（控制台输出时 emoji 会崩溃！） |

### 编码注意事项 ⚠️

Windows 控制台默认 GBK 编码，Python 的 `print()` 输出 emoji 或中文会崩溃。
**解决方法：**

1. **Python 脚本文件** — 写入文件的 Python 代码使用 `encoding="utf-8"` 读写文件
2. **调试输出** — 避免 emoji 在 `print()` 中出现，用 ASCII 符号代替（`>>` 替代 ✅）
3. **PowerShell heredoc** — 用 `@`...`@` 包裹多行 Python 代码传给 stdin
4. **复杂 Python 代码编辑** — 写到临时 .py 文件再执行，不要用单行 `-c`
5. **CSS/模板代码** — 包含 `{}` 或 `:;` 的内容会被 PowerShell 解释，必须用 Node.js 或 Python 脚本编辑

### 常用命令语法

```powershell
# Python 脚本执行
python scripts/generate.py

# 多行 Python 传递给 python (用 @".."@)
@"...代码..."@ | python

# 验证语法
python -c "import py_compile; py_compile.compile('scripts/generate.py', doraise=True); print('OK')"

# 读取 UTF-8 文件
Get-Content file.py -Encoding UTF8

# 写入 UTF-8 文件 (无 BOM)
$c | Set-Content file.py -Encoding UTF8
```

---

## 二、编码原则（Karpathy Skills）

本项目的所有编码工作遵循 Andrej Karpathy 四大原则：

### 原则 1: Think Before Coding（编码前思考）
- 不要假设，不确定时必须提问
- 主动暴露权衡，列出可选项
- 对不明确的要求提出担忧

### 原则 2: Simplicity First（简单优先）
- 只写解决当前问题所需的最小代码
- 不要添加超出要求的特性
- 不要为一次性代码创建抽象
- 写完代码后自问："能更简单吗？"

### 原则 3: Surgical Changes（精准修改）
- 只修改必须修改的部分
- 遵循现有代码风格
- 不要修改无关代码
- 一次只改一个功能，验证通过后再改下一个

### 原则 4: Goal-Driven Execution（目标驱动执行）
- 将任务转化为可验证的目标
- 制定简略的多步骤计划
- 每个步骤设置验证检查点
- 验证通过才算完成

---

## 三、工作流程（Superpowers）

### 7阶段工作流

1. **Brainstorming** — 先讨论方案，暴露权衡
2. **Git Worktrees** — 隔离分支开发（暂不使用，直接 main 分支）
3. **Writing Plans** — 小粒度实施计划
4. **Sub-Agent Driven** — 复杂任务拆分子代理
5. **Test-Driven Development** — 先写验证，再写代码
6. **Code Review** — 每次提交前自审查
7. **Finishing** — 提交/推送/部署

### 验证优先
- 代码改完后必须运行验证
- `python scripts/generate.py` 必须无错误退出
- 验证 sitemap、OG 标签等输出

---

## 四、项目约定

### 目录结构
```
ai-video-tools-comparison/
├── .codex/skills/       # 项目级技能
├── data/
│   └── tools.json       # 工具数据（定价、特性、视频等）
├── scripts/
│   └── generate.py      # 静态站点生成器
├── templates/            # 模板文件（未使用，模板在 generate.py 内）
└── output/              # 生成输出（部署到 Cloudflare Pages）
```

### 数据文件（tools.json）字段
- `id` / `name` / `description` / `category` / `url`
- `plans[]` — 定价计划（`name`, `price_monthly`, `price_yearly`, `credits`, `features[]`）
- `features{}` — 特性键值对
- `youtube_official[]` / `youtube_reviews[]` — 视频嵌入数据
- `g2_rating` / `g2_reviews`

### Git 规范
- 分支前缀: `codex/`
- 提交信息格式: `type: description`
- 提交后自动触发 Cloudflare Pages 部署

### 部署
- Cloudflare Pages 自动从 GitHub main 分支部署
- GitHub Actions: 每月定时执行定价爬虫

---

## 五、已知问题与解决

| 问题 | 解决 |
|------|------|
| Windows GBK 编码 | 所有 Python 文件读写用 `encoding="utf-8"`，避免 print(emoji) |
| PowerShell 转义 `{}` | 有 CSS/模板代码时用 Node.js 或 Python 脚本文件编辑 |
| Python heredoc 传 stdin | 用 `@"...@"` 语法 |
| Node REPL 变量冲突 | `js_reset` 后重新声明变量，避免 `const` 重复 |
