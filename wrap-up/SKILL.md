---
name: wrap-up
description: >
  项目正式收尾与发布工作流。用于 /wrap-up、收尾、整理提交、准备提交、
  准备推送、commit、push、tag、打版、发布等场景。默认目标是整理本次
  change，更新必要文档和 changelog，推断版本号，生成提交/打 tag/推送预览；
  用户确认后再执行 commit、tag 和 push。
---

# wrap-up

## 定位

用户调用 `/wrap-up` 时，通常已经希望完成正式收尾：整理 change、提交、打 tag、推到 GitHub。

不要让用户选择 quick / push / release 模式。默认按正式发布收尾处理。

正确节奏：

```text
整理 change
  → 检查敏感文件
  → 同步必要文档和 CHANGELOG
  → 推断版本号
  → 生成 commit/tag/push 预览
  → 询问用户确认
  → 用户确认后执行 commit、tag、push
```

## 红线

以下动作必须在执行前明确告知用户并获得确认：

- `git commit`
- `git tag`
- `git push`
- 删除文件、目录或 git 历史
- 修改 `.env`、密钥、token、CI/CD 配置
- 发布到任何远端或公共平台

确认问题只需要问一次。预览中必须明确写出将执行哪些动作，例如：

```text
确认执行 commit + tag v0.6.0 + push 到 origin/master 吗？
```

用户确认后，可以连续执行预览中列出的动作，不需要再分多轮询问。

## 工作流程

### 1. 读取必要上下文

优先看：

- 项目根 `AGENTS.md`、`CLAUDE.md`、README。
- 本次变更涉及目录下的 `SKILL.md`、README、references 文档。
- `CHANGELOG.md`。

不要全仓库无差别审查所有文档。

本技能的参考文件只在需要时读取：

- `references/agent-paths.md`：仅在需要处理 agent 记忆时读取。
- `references/sync-matrix.md`：仅在不确定文档同步范围时读取。

如果 Claude/Codex 记忆目录只有 `.jsonl` 会话日志，没有明确 `memory/` 索引，跳过记忆同步。

### 2. 扫描 git 变更

执行：

```bash
git status --short
git diff --stat
git diff --staged --stat
git log --oneline -5
git describe --tags --abbrev=0
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

### 4. 同步必要文档

只同步和本次变更直接相关的文档。

通常需要：

- 变更目录下的 `SKILL.md` / references 文档。
- 项目根 README。
- `CHANGELOG.md`。

原则：

- 合并旧内容，不机械追加。
- 删除过期说法。
- 使用绝对日期，例如 `2026-06-17`。
- 不扩大范围改无关文档。

### 5. 推断版本号

从最新 tag 推断下一版本：

- breaking change：major。
- 新功能：minor。
- 修复、文档、重构、工具调整：patch。

如果没有 tag，从 `v0.1.0` 开始。

如果 tag 已存在，停止并让用户指定处理方式。

### 6. 生成提交预览

预览必须包含：

- 版本号。
- 变更文件清单。
- 敏感文件检查结果。
- commit message，英文 conventional commits 格式。
- CHANGELOG 摘要。
- 将执行的动作：`commit + tag + push`。

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

预览后询问：

```text
确认执行 commit + tag vX.Y.Z + push 到 GitHub 吗？
```

用户确认后再执行。

用户要求修改时，调整预览后重新确认。

用户取消时，不清理变更。

### 8. 执行

确认后执行：

```bash
git add <本次确认的文件>
git commit -m "<message>"
git tag vX.Y.Z
git push
git push --tags
```

如果 commit、tag 或 push 失败，展示错误并停止，不要强行绕过。

## 最终输出

保持简短，固定包含：

```text
wrap-up 完成

- commit: <hash> <message>
- tag: vX.Y.Z
- push: 已推送 / 未推送
- 工作区: 干净 / 仍有未提交变更
```
