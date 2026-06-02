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
| [gaoqi-form-fill](gaoqi-form-fill/SKILL.md) | 高企申报系统「企业年度研究开发费用结构明细表」填写助手。人机协作模式，在 gqqy.chinatorch.org.cn 上自动填入 RD 项目费用数据并校验合计。 |

## 开发计划（欢迎 PR）

- [ ] 更多企业申报类技能（专精特新、小巨人等）
- [ ] 文书写作技能（材料撰写、润色、格式化）
- [ ] 代码审查与分析技能
- [ ] 通用研究分析技能

## 使用前提

- 已安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
- 按各技能 `SKILL.md` 中的前置条件准备环境

## License

MIT
