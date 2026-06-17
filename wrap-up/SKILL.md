---
name: wrap-up
description: >
  项目收尾工作流——先同步文档与记忆（内置知识审查流程），再扫 git 变更、生成
  conventional commits 格式的 changelog、用户确认后 commit、打语义版本 tag、
  询问后 push 到 GitHub。触发词：收尾、提交、wrap up、准备推送、打版、整理提交、
  我要提交了、准备合并、commit、push、版本发布、整理一下准备提交。收尾、同步一下、
  整理文档、梳理一下。
---

# wrap-up — 项目收尾工作流

你正在帮助用户完成一次项目收尾。严格按以下 7 个阶段执行，**每阶段完成后才进下一阶段**。

## 红线（必须遵守）

- **git push 必须先问用户**，得到确认后才执行。这是用户的硬性要求。
- **不要擅自改用户没碰过的文件**。Phase 1（知识同步）只更新文档/记忆，不动业务代码。
- **commit message 用英文写**（conventional commits 格式），CHANGELOG.md 用中文。

---

## Phase 1：知识同步（文档与记忆审查）

**目标**：在提交代码前，确保项目文档和 agent 记忆与本次变更一致。这个阶段内置了知识同步流程（原 neat-freak 技能的核心逻辑），不需要外部技能。

**注意**：此阶段只更新文档/记忆，不动业务代码。

### 1.1 盘点现状

列出当前项目中所有需要审查的文件：
- Agent 记忆文件：`~/.claude/projects/` 下对应项目的 `memory/` 目录
- 项目根文档：`CLAUDE.md`、`README.md`、`AGENTS.md`（若存在）
- 项目 `docs/` 下所有 `*.md` 文件
- 当前工作目录下其他 `*.md`（排除 `node_modules/`、`.git/`、`产出/` 等非文档目录）

### 1.2 识别变更

审查本次对话产生的变更，对照 **[references/sync-matrix.md](references/sync-matrix.md)** 判断需要同步哪些文档层：

| 变更类型 | 需要同步的目标 |
|---|---|
| 新增/修改 API、路由 | CLAUDE.md 路由清单 · docs/integration-guide.md · docs/architecture.md |
| 新增/改名 环境变量 | CLAUDE.md 环境变量表 · docs/operator-runbook.md |
| 新增 数据库表/字段 | CLAUDE.md 数据模型 · docs/architecture.md Data Model |
| 新增大特性 | 以上全部 + docs/architecture.md 新增章节 + docs/handoff.md |
| 新增/修改 用户流程 | CLAUDE.md · README 相关示例 · docs/handoff.md |
| 新增术语/改命名 | docs/integration-guide.md 术语表 · 全局搜索旧术语替换 |
| 过期事实/相对时间 | 记忆文件中的相对时间→绝对日期 |
| 已完成待办/推翻决策 | 记忆文件中删除或替换 |

### 1.3 执行修改

**顺序**：先改 docs/（外部读者可见）→ 再改 CLAUDE.md（下次会话的自己）→ 最后改 agent 记忆（跨会话复用）。即使被打断，读者看到的也是最新状态。

**编辑原则**：
- **合并**优于追加：改旧条目，不加新一条
- **删除**优于保留：已完成待办、推翻的决策、过期上下文，删掉
- **精确**优于冗长：一条记一件事，不塞三件
- **绝对时间**：永远写 `2026-05-29`，不写"今天"、"最近"
- **面向读者**：docs/ 的读者是第一次接触项目的外部人，写的时候想象对方只有 5 分钟

### 1.4 自检清单

改完后逐条过：
- [ ] 盘点出的每个文件都标了"不用改"或"已改"
- [ ] 记忆索引里的链接指向存在的文件，description 与内容一致
- [ ] CLAUDE.md 提到的路径/命令/环境变量在代码中真实存在
- [ ] README 安装/运行步骤跟实际一致
- [ ] 无相对时间遗留（`今天|昨天|最近|上周|today|yesterday|recently` 清零）
- [ ] 跨项目影响：下游项目的 docs 也对齐了

### 1.5 变更摘要

记录本次修改了什么文件，后续提交用：

```
## 文档同步
- 更新/新增/删除：CLAUDE.md（原因）
- 更新/新增/删除：docs/xxx.md（原因）
- 更新/新增/删除：agent 记忆（原因）
```

---

## Phase 2：扫描变更

**目标**：全面了解工作目录的变更情况。

1. 运行 `git status` 看整体状态
2. 运行 `git diff --staged`（如果已有 staged 变更）和 `git diff` 看 unstaged 变更
3. 运行 `git log --oneline -5` 看最近提交记录（了解当前在哪个提交之上工作）
4. 列出变更文件清单，按类型分组：
   - 新文件（untracked）
   - 修改（modified）
   - 删除（deleted）
   - 重命名（renamed）

---

## Phase 3：生成 Changelog 与 Commit Message

**目标**：根据变更内容自动生成 CHANGELOG.md 条目和 conventional commits 格式的提交信息。

### 确定版本号

按 commit 类型自动推断版本 bump：
- **major**（不兼容变更）：存在 breaking change（如删除/重命名 API、改接口签名、删路由、改数据库 schema）
- **minor**（新功能）：存在 `feat` 类型变更，无 breaking change
- **patch**（修复/杂项）：只有 `fix`、`chore`、`refactor`、`docs`、`style`、`test` 等

从当前最新 tag 读取当前版本（`git describe --tags --abbrev=0`），如果还没有 tag 则从 `v0.1.0` 开始。

### 生成 Commit Message（conventional commits 格式）

分析 diff，提取变更要点，格式：
```
<type>(<scope>): <简短描述>

<详细说明（可选）>

<footer（可选，BREAKING CHANGE 放这里）>
```

type 取值：
- `feat` — 新功能
- `fix` — 修 bug
- `docs` — 文档
- `refactor` — 重构
- `chore` — 杂项（构建、工具、配置）
- `test` — 测试
- `style` — 格式调整

scope 从变更涉及的主要模块/目录推断。

### 更新 CHANGELOG.md

如果项目根目录没有 `CHANGELOG.md`，创建一个。格式：

```markdown
# Changelog

## [v1.2.0] - 2026-05-07

### Added（新增）
- 用户认证 OAuth 支持（#15）
- 仪表盘数据导出功能

### Changed（变更）
- 重构数据库查询层，提升响应速度

### Fixed（修复）
- 修复 Session 超时后页面崩溃的问题

### Breaking Changes
- 移除 v1 版本 API `/api/v1/process`，迁移至 `/api/v2/process`
```

如果有已有 CHANGELOG.md，在顶部插入新版本条目。

**CHANGELOG.md 用中文写**，让用户（非程序员）也能看懂。

---

## Phase 4：用户确认

**目标**：让用户了解即将提交的内容，并获得明确确认。

展示以下摘要：

```
## 提交预览

### 版本：v1.2.0（patch）

### 变更文件（N 个）
  M  src/controller.py
  A  src/utils.py
  D  src/old.py

### Commit Message
fix(controller): 修复 xx 场景下的空指针异常

### Changelog
[Fixed]
- 修复 xx 场景下的空指针异常
```

然后问用户：
```
确认提交以上内容？(y/n)
```

- 如果用户说 y / 确认 / 好 / 可以 → 进入 Phase 5
- 如果用户表示要修改 → 让用户修改 commit message 或选择跳过某些文件，然后回到此阶段开头
- 如果用户说 n / 取消 → 终止流程，不清除任何变更

---

## Phase 5：执行提交

1. `git add` 所有变更（包括 Phase 1 中改的文档/记忆文件）
2. 用 Phase 3 生成的 commit message 执行 `git commit`
3. 如果 commit 失败（如 hook 拦截），显示错误信息，让用户决定怎么处理

---

## Phase 6：打 Tag

1. 用 Phase 3 确定的版本号执行 `git tag vX.Y.Z`
2. 如果 tag 已存在，报错并让用户指定新版本号

---

## Phase 7：推送（先问后推）

**这是用户的红线，必须问。**

```
准备好推送到 GitHub？（当前版本 v1.2.0，含 N 个提交和 tag）
[1] 推送（git push && git push --tags）
[2] 只推代码，不推 tag
[3] 暂不推送
```

- 选 1 → `git push` 然后 `git push --tags`
- 选 2 → 只 `git push`
- 选 3 → 结束流程，告知用户本地已提交

---

## 最终输出

完成后输出摘要：

```
## wrap-up 完成

### 文档同步
- CLAUDE.md 更新了 xxx
- docs/architecture.md 更新了 xxx

### 提交
v1.2.0 — fix(controller): 修复 xx 场景下的空指针异常

### 文件变更
N 个文件变更，+M / -D

### 推送状态
✅ 已推送到 GitHub
```
