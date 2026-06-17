# Claude Code Skills

Claude Code 的自定义技能集。每个技能是一个独立的工作流，封装了特定场景下的提示词、约束条件和操作流程。

## 这是什么

Claude Code 支持通过 `SKILL.md` 定义**自定义技能**——相当于给 AI 配一份岗位说明书。当你在对话中输入 `/<skill-name>` 时，Claude 会按照对应的技能定义来工作，而不是通用对话模式。

这个仓库收集了我日常使用的各种技能，覆盖申报填表、文书写作、代码审查、研究分析等场景。

## Skill 的两种运行模式

### 1. 通过 SKILL.md 热加载（推荐）

在项目根目录下放 `.claude/skills.json`，把技能路径注册进去：

```json
{
  "skills": ["gaoqi-form-fill/SKILL.md"]
}
```

然后在对话中输入 `/gaoqi-form-fill` 即可触发。

### 2. 直接引用

不注册也可以，对话中告诉 Claude：
> "读一下 gaoqi-form-fill/SKILL.md，然后按这个技能工作"

Claude 会读取文件并按其中的指令执行。

### 编写自己的 Skill

参考 [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code/skills)，一个 `SKILL.md` 包含：

- **Frontmatter**（YAML 头）：`name`、`description`（描述决定触发匹配）、`metadata.type`
- **正文**：用 Markdown 写行为规则、约束条件、工作流程、输出格式

> 先创建 `.claude/settings.json` 设置 permissions，再写 SKILL.md。详情见[官方文档](https://docs.anthropic.com/en/docs/claude-code/skills)。

## 技能列表

| 技能 | 描述 |
|------|------|
| [gaoqi-form-fill](gaoqi-form-fill/SKILL.md) | 高企申报系统表单填写助手。覆盖费用明细表、活动情况表、知识产权汇总表、产品（服务）情况表、科技成果转化情况等 5 张核心表单。人机协作渐近自动化，用户提供数据，AI 匹配字段并填入，信任建立后可全自动操作。 |
| [enterprise-writing](enterprise-writing/SKILL.md) | 企业文书写作助手。覆盖 7 类企业政府文书：科技项目申报书、资质认定申请（小巨人/单项冠军）、工程研究中心/平台申请、人才申报书、绩效评价报告、典型案例、发言稿。内置各类文书知识库。 |
| [vision](vision/SKILL.md) | 图片分析技能。使用阿里云百炼视觉模型（通义千问 VL）识别图片中的文字、物体、场景等，支持 OCR、截图分析、图片内容理解。 |
| [wrap-up](wrap-up/SKILL.md) | 项目收尾工作流。自动同步文档与记忆，扫描 git 变更生成 changelog，用户确认后按 conventional commits 格式提交、打版、推送。 |

## 开发计划（欢迎 PR）

- [x] 更多企业申报类技能（专精特新、小巨人等）
- [x] 文书写作技能（材料撰写、润色、格式化）
- [ ] 代码审查与分析技能（进行中）
- [ ] 通用研究分析技能（进行中）

## 使用前提

- 已安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
- 按各技能 `SKILL.md` 中的前置条件准备环境

## License

MIT
