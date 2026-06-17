---
name: wrap-up
description: >
  项目收尾工作流。用于 /wrap-up、收尾、整理提交、准备提交、准备推送、
  commit、push、打版、发布等场景。自动判断 quick / push / release 模式：
  默认 quick，只整理变更并生成提交预览；明确需要推送时进入 push；明确需要
  发布、打版或 tag 时进入 release。执行 commit、tag、push 前必须让用户确认。
---

# wrap-up

## 核心原则

用户通常只会输入 `/wrap-up`。不要让用户先选择模式，由 agent 根据上下文自动判断。

默认行为要轻：只做必要整理、敏感文件检查、相关文档同步和提交预览。

不要主动跑验证。只记录本轮对话中已经执行过的验证结果；如果没有验证记录，摘要中写明“未记录验证”。

## 红线

以下动作必须在执行前明确告知用户并获得确认：

- `git commit`
- `git tag`
- `git push`
- 删除文件、目录或 git 历史
- 修改 `.env`、密钥、token、CI/CD 配置
- 发布到任何远端或公共平台

如果用户已经在同一请求中明确说“提交并推到 GitHub”“commit and push”等，可以把 commit 与 push 放进同一个确认预览里。确认后可以连续执行，不需要再次询问模式。

## 自动模式判断

### quick 模式

默认模式。

适用场景：

- 用户只说 `/wrap-up`、收尾、整理一下、准备提交。
- 本次只是文档、小脚本、小修。
- 没有明确远端推送或发布意图。
- 没有必要 bump 版本或 tag。

执行范围：

- 扫描 git 变更。
- 检查敏感文件风险。
- 同步必要文档。
- 生成 commit message 和提交预览。
- 等用户确认后 commit。
- 不 tag、不 push。

### push 模式

适用场景：

- 用户明确说 push、推送、GitHub、提交并推送。
- 用户在当前上下文刚要求把结果推到远端。

执行范围：

- quick 全部步骤。
- 等用户确认后 commit。
- 推送当前分支。
- 不自动 tag，除非同时命中 release 模式。

### release 模式

适用场景：

- 用户明确说 release、发布、打版、tag、版本。
- 本次变更已经更新 CHANGELOG 的版本条目。
- 本次是对外可用的新能力，并且项目已有 tag 体系，agent 判断应该发布新版本。

执行范围：

- quick 全部步骤。
- 更新或确认 CHANGELOG。
- 推断版本号。
- 等用户确认后 commit。
- 创建 tag。
- 如用户表达了推送意图，推送代码和 tag。

## 工作流程

### 1. 读取上下文

先看项目规范：

- 项目根 `AGENTS.md`、`CLAUDE.md`、README。
- 当前技能或模块自己的说明文件。
- 本技能的 `references/agent-paths.md` 仅在需要处理 agent 记忆时读取。
- 本技能的 `references/sync-matrix.md` 仅在不确定文档同步范围时读取。

不要全仓库无差别审查所有文档。优先看本次变更涉及的目录和根文档。

### 2. 扫描变更

执行：

```bash
git status --short
git diff --stat
git diff --staged --stat
git log --oneline -5
```

按类型分组：

- 修改文件
- 新增文件
- 删除文件
- 未跟踪文件

### 3. 敏感文件检查

提交前必须检查新增和修改文件名，重点关注：

- `.env`
- 密钥、token、credential、secret
- 真实客户或公司数据
- 未脱敏 Excel / Word / PDF
- 私人账号、密码、cookie
- 大体积二进制文件

如果疑似敏感文件将被提交，停下来说明风险，让用户决定。不要擅自删除。

### 4. 必要文档同步

只同步和本次变更直接相关的文档。

优先级：

1. 变更目录下的 `SKILL.md` / README / references 文档。
2. 项目根 README。
3. CHANGELOG，仅 release 模式或用户要求打版时更新。
4. Agent 记忆，仅当存在明确 `memory/` 目录和索引文件时处理；如果只有 `.jsonl` 会话日志，跳过。

原则：

- 合并旧内容，不机械追加。
- 删除过期说法。
- 使用绝对日期，例如 `2026-06-17`。
- 不扩大范围改无关文档。

### 5. 记录验证状态

不要主动运行测试、构建或预检。

只记录本轮已经发生的验证，例如：

- `python -m py_compile` 已通过。
- 业务预检 `ERROR 0 / WARN 0`。
- 未记录验证。

如果用户明确要求 wrap-up 时顺便验证，才执行对应验证。

### 6. 生成提交预览

根据变更生成：

- 自动判断的模式：quick / push / release。
- 版本号：仅 release 模式需要。
- 变更文件清单。
- 验证状态。
- commit message，英文 conventional commits 格式。
- CHANGELOG 摘要，若本次更新了 CHANGELOG。
- 将要执行的动作：commit / tag / push。

提交信息格式：

```text
<type>(<scope>): <summary>
```

常用 type：

- `feat`
- `fix`
- `docs`
- `refactor`
- `chore`
- `test`

### 7. 用户确认

预览后只问一次：

```text
确认执行以上操作吗？
```

如果是 quick，说明将执行 commit。

如果是 push，说明将执行 commit + push。

如果是 release，说明将执行 commit + tag，以及是否 push。

用户确认后再执行。用户要求修改时，调整预览后再确认。用户取消时，不清理变更。

### 8. 执行

按确认内容执行：

```bash
git add <本次确认的文件>
git commit -m "<message>"
```

push 模式：

```bash
git push
```

release 模式：

```bash
git tag vX.Y.Z
git push
git push --tags
```

如果 tag 已存在，停止并让用户指定处理方式。

## 最终输出

保持简短，固定包含：

```text
wrap-up 完成

- 模式：quick / push / release
- commit: <hash> <message>
- tag: vX.Y.Z / 无
- push: 已推送 / 未推送
- 验证: 已记录 xxx / 未记录验证
- 工作区: 干净 / 仍有未提交变更
```

