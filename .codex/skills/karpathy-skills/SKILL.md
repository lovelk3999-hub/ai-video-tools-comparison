---
name: karpathy-skills
description: Andrej Karpathy 四大编码原则——Think Before Coding(编码前思考) + Simplicity First(简单优先) + Surgical Changes(精准修改) + Goal-Driven Execution(目标驱动执行)。解决LLM编码三大通病：隐藏假设、过度设计、无关修改。触发词："Karpathy"/"编码原则"/"简单优先"/"精准修改"/"目标驱动"/"Karpathy Skills"
argument-hint: [task-description]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Andrej Karpathy Skills — 四大编码原则

> 将 Andrej Karpathy（OpenAI 联合创始人、特斯拉前 AI 负责人）的 LLM 编码洞察蒸馏为可遵循的行为规则。
> **GitHub**: https://github.com/forrestchang/andrej-karpathy-skills（140,000+ ⭐）
> **核心目标**：减少 AI 编码时的隐藏假设、过度设计和无关修改。

---

## LLM 编码的三大通病

| 问题 | 表现 |
|:----|:-----|
| **隐藏假设** | 模型代表你做出错误假设，然后默默执行 |
| **过度设计** | 添加没人要求的抽象、无关的改进、不必要的灵活性 |
| **无关修改** | 顺便修改相邻代码、格式、注释等不相关部分 |

---

## 四大核心原则

### 原则 1: Think Before Coding（编码前思考）

**核心理念**：不要假设，不要隐藏困惑，主动暴露权衡。

**具体要求**：
- 将假设明确化，不要静默决定
- 不确定时必须提问
- 主动暴露权衡，列出可选项
- 对不明确的要求提出担忧

**失败模式示例**：用户说"添加搜索栏"，AI 就发明一整套搜索架构，选一个用户不用的库，写 800 行代码，然后用户才来得及干预。

### 原则 2: Simplicity First（简单优先）

**核心理念**：只写解决当前问题所需的最小代码。

**具体要求**：
- 不要添加超出要求的特性
- 不要为一次性代码创建抽象
- 不要添加不可能场景的错误处理
- 写完代码后自问："能更简单吗？"
- **Karpathy 原话**："If you write 200 lines and it could be 50, rewrite it."

### 原则 3: Surgical Changes（精准修改）

**核心理念**：只修改必须修改的部分。

**具体要求**：
- 只修改需要修改的部分
- 遵循现有代码风格，即使你会用不同方式
- 只删除因你的更改而变得不必要的代码
- **不要修改无关代码**

### 原则 4: Goal-Driven Execution（目标驱动执行）

**核心理念**：将模糊请求转化为可验证的目标。

**具体要求**：
- 将任务转化为可验证的目标
- 制定简略的多步骤计划
- 每个步骤设置验证检查点
- 在实现前而非犯错后进行澄清

**转化示例**：
- ❌ "修复bug" -> ✅ "写一个能复现bug的测试，然后让它通过"
- ❌ "添加功能" -> ✅ "明确功能边界 -> 实现最小路径 -> 验证"

---

## 使用方式

当你需要编码时，说：

- "用 Karpathy 原则改这段代码"
- "按简单优先重构这个函数"
- "用 Surgical Changes 修复这个 bug"
- "按 Karpathy Skills 写这个功能"

AI 会遵循四大原则行动。

---

*文档基于 https://github.com/forrestchang/andrej-karpathy-skills 整理*
*安装时间：2026-06-16*
