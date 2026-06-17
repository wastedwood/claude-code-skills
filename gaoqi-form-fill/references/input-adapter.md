# 填表前数据中转流程

## 定位

这里不是一个复杂的数据整理平台。

第一版只做一件事：在网页填表前，把用户资料整理成一份稳定的标准 JSON，并做基础预检。

推荐流程：

```text
用户提供 Excel / Word
  → AI 阅读和判断字段含义
  → AI 或脚本生成标准 JSON
  → 脚本做基础预检
  → AI 根据 JSON 填网页
```

## 为什么需要中间 JSON

不是因为模型看不懂用户材料，而是因为网页填表阶段需要稳定、可重复、可检查的数据。

中间 JSON 的作用：

- 固定字段名，避免填表时临时猜字段。
- 固定编号关系，例如 IP、RD、PS 之间的引用。
- 在进入网页前发现明显错误。
- 让 Codex、Claude Code、便宜模型都能按同一份数据执行。

## 第一版支持范围

支持：

- Excel：结构化数据的主要来源。
- Word：作为 AI 阅读参考，主要用于补充长文本。

不支持：

- PDF
- 图片 / OCR
- 扫描件
- 附件材料识别
- 历史映射记忆
- 自动理解任意乱格式 Excel
- 用户确认界面

## Excel 的处理方式

第一版优先支持推荐模板：

```text
gaoqi-form-fill/examples/test-data/gaoqi-sample-data.xlsx
```

脚本入口：

```powershell
python gaoqi-form-fill/scripts/excel-to-json.py `
  gaoqi-form-fill/examples/test-data/gaoqi-sample-data.xlsx `
  gaoqi-form-fill/examples/test-data/gaoqi-sample-data.json
```

Excel 可以有多余列，但核心表和核心字段应尽量接近示例模板。

如果用户给的 Excel 很乱，第一版不要求脚本完全自动识别。正确做法是：

1. AI 先看 Excel 内容。
2. AI 判断哪些列对应标准字段。
3. 必要时手动整理或生成标准 JSON。
4. 再运行预检。

## Word 的处理方式

Word 暂不做确定性自动解析。

Word 的定位是参考材料：

- AI 读取 Word。
- 抽取研发目的、核心技术、阶段性成果、产品说明、创新能力说明等长文本。
- 把文本补进标准 JSON。

人员花名册、研发费用、知识产权明细这类大表，优先要求用户提供 Excel。

## 预检边界

预检脚本只检查明显问题：

- 编号重复。
- IP / RD / PS 引用断链。
- 研发费用和 RD 年度费用不一致。
- 关键文本缺失。
- 人员数量异常。

预检不是申报规则审查，也不是专家评审。它只负责在自动填网页前拦住低级错误。

脚本入口：

```powershell
python gaoqi-form-fill/scripts/validate-json.py `
  gaoqi-form-fill/examples/test-data/gaoqi-sample-data.json
```

判断标准：

- 有 `ERROR`：不要继续自动填表。
- 只有 `WARN`：先让用户确认。
- `ERROR 0 / WARN 0`：可以进入填表流程。

## Claude Code 兼容要求

为了让 Claude Code 和其他模型能接手：

- 文档使用普通 Markdown。
- 脚本使用普通命令行入口。
- 不依赖 Codex 专有工具。
- 不依赖浏览器环境。
- 不要求模型记住隐藏规则，关键流程写在文档里。

