# Changelog

## [v0.5.1] - 2026-06-17

### Changed（变更）
- 调整 wrap-up 技能定位：`/wrap-up` 默认按正式收尾发布流程处理，不再让 agent 在 quick / push / release 之间切换。
- 明确 wrap-up 的执行节奏：整理 change、检查敏感文件、同步必要文档和 CHANGELOG、推断版本号、生成 commit/tag/push 预览，用户确认后再执行。
- 移除验证记录要求：验证是进入 wrap-up 前的前置动作，不属于 wrap-up 技能职责。

## [v0.5.0] - 2026-06-17

### Added（新增）
- 新增 gaoqi-form-fill 的填表前数据中转流程：Excel → 标准 JSON → 基础预检 → 网页填表。
- 新增脱敏示例数据：`gaoqi-sample-data.xlsx` 和对应标准 JSON 示例。
- 新增 `excel-to-json.py`，可将推荐 Excel 模板转换为内部标准 JSON。
- 新增 `validate-json.py`，可检查编号重复、IP/RD/PS 引用断链、研发费用不一致、关键文本缺失和人员数据异常。
- 新增 `references/data-schema.md`，定义高企填表内部数据结构。
- 新增 `references/input-adapter.md`，明确第一版只做轻量数据中转，不做 PDF、图片、OCR、附件识别或复杂数据整理平台。

### Changed（变更）
- 更新 gaoqi-form-fill 技能入口，要求浏览器填表前优先使用标准 JSON 和预检结果。
- 更新 README 中 gaoqi-form-fill 的能力描述，补充数据中转和预检能力。
- 更新 `.gitignore`，排除本地 AGENTS、真实数据 Excel 和 Python 缓存文件。

## [v0.4.0] - 2026-06-17

### Changed（变更）
- 重构 gaoqi-form-fill 技能架构：715 行单文件 SKILL.md 拆分为 135 行入口 + references/ 知识库（7 表单文件） + scripts/ 工具脚本（3 个）
- 补充人力资源情况表、标准制定情况表两张新表单的知识覆盖

### Added（新增）
- 新增 IP 自动回填工作流：选类别→输专利号（ZL+申请号）→系统自动从国家数据库同步名称/获得方式/授权日
- 新增费用表自动计算函数调用文档：nbyjkfhj() / nwkfhj()
- 新增中文编码处理方案：必须用 --data-binary @file.js 传 UTF-8 内容
- 新增三级技术领域级联操作脚本

### Fixed（修复）
- 修正 SKILL.md 中知识产权附件"强制上传"的错误描述（附件为可选项）

## [v0.3.0] - 2026-06-17

### Added（新增）
- 新增企业文书写作助手技能（enterprise-writing），覆盖 7 类企业政府文书：科技项目申报书、资质认定申请、平台申请、人才申报书、绩效评价报告、典型案例、发言稿
- 新增图片分析技能（vision），基于阿里云百炼通义千问 VL，支持 OCR、截图分析、图片内容理解
- 新增项目收尾工作流技能（wrap-up），自动同步文档、扫描变更、生成 changelog、提交打版推送

## [v0.2.0] - 2026-06-03

### Added（新增）
- 新增知识产权汇总表表单知识（类别下拉、附件管理）
- 新增上年度高新技术产品（服务）情况表表单知识（三级级联领域、三段文本、关联IP）
- 新增企业创新能力—科技成果转化情况表单知识（三层结构、多表关联IP/RD/PS）

### Changed（变更）
- 重构企业研究开发活动情况表字段映射，补全技术领域、技术来源、关联IP、近三年经费等遗漏字段
- 完善企业年度研究开发费用结构明细表字段映射，补全填报人、签字日期、排序号字段
- 数据来源不再限定 Excel 格式，支持表格文本、JSON、结构化数据等任意格式
- 重构 SKILL.md 结构，增加通用工作流、渐进覆盖表和表单目录
