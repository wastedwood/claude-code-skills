# Personal Agent Skills

个人使用的 AI 助手技能库，兼容 Codex、Claude Code 等支持 `SKILL.md` 的工具。每个技能是一个独立工作流，封装特定场景下的规则、约束和操作流程。

## 这是什么

`SKILL.md` 相当于给 AI 助手准备一份可复用的岗位说明书。支持技能机制的工具读取对应文件后，会按照其中定义的工作流程执行任务。

这个仓库收集了我日常使用的各种技能，覆盖申报填表、文书写作、代码审查、研究分析等场景。

## 版本管理原则

- GitHub 仓库 [`wastedwood/personal-agent-skills`](https://github.com/wastedwood/personal-agent-skills) 是唯一正式版本。
- 技能修改先在本仓库完成并验证，再同步到 GitHub。
- Codex、Claude Code 等工具中的技能目录仅作为安装副本，不直接在安装副本中维护。
- 后续安装或更新技能时，以 GitHub 仓库中的版本为准。

## 使用方式

将需要的技能目录安装到所用 AI 工具的个人技能目录。不同工具的安装位置和触发方式不同，具体规则见各工具文档以及 [`wrap-up/references/agent-paths.md`](wrap-up/references/agent-paths.md)。

也可以让 AI 助手直接读取某个技能的 `SKILL.md`，例如：“读取 `gaoqi-form-fill/SKILL.md`，然后按这个技能工作。”

## 技能列表

| 技能 | 描述 |
|------|------|
| [gaoqi-form-fill](gaoqi-form-fill/SKILL.md) | 高企申报系统表单填写助手。覆盖 7 张核心表单（人力资源、研发活动、费用明细、知识产权、产品情况、成果转化、标准制定），含 references/ 知识库和 scripts/ 工具脚本。新增 Excel → 标准 JSON → 基础预检的数据中转流程，网页填表前先检查编号关联和研发费用一致性。 |
| [enterprise-writing](enterprise-writing/SKILL.md) | 企业文书写作助手。覆盖 7 类企业政府文书：科技项目申报书、资质认定申请（小巨人/单项冠军）、工程研究中心/平台申请、人才申报书、绩效评价报告、典型案例、发言稿。内置各类文书知识库。 |
| [vision](vision/SKILL.md) | 图片分析技能。使用阿里云百炼视觉模型（通义千问 VL）识别图片中的文字、物体、场景等，支持 OCR、截图分析、图片内容理解。 |
| [wrap-up](wrap-up/SKILL.md) | 项目收尾工作流。自动同步文档与记忆，扫描 git 变更生成 changelog，用户确认后按 conventional commits 格式提交、打版、推送。 |
| [patent-pdf-batch-download](patent-pdf-batch-download/SKILL.md) | 专利 PDF 批量下载技能。优先通过 Google Patents 将中国专利申请号匹配为公开号，必要时用 CNIPA 公布公告系统补查公告号，批量下载全文，按原专利号命名，并校验文件数量、名称和 PDF 完整性。 |

## 开发计划（欢迎 PR）

- [x] 更多企业申报类技能（专精特新、小巨人等）
- [x] 文书写作技能（材料撰写、润色、格式化）
- [ ] 代码审查与分析技能（进行中）
- [ ] 通用研究分析技能（进行中）

## 使用前提

- 已安装支持相应技能机制的 AI 助手，例如 Codex 或 Claude Code
- 按各技能 `SKILL.md` 中的前置条件准备环境

## License

MIT
