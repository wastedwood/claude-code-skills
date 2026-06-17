# 高企填表内部数据结构

## 设计原则

用户不需要手写 JSON，也不需要知道系统字段名。

本文件定义的是填表前的中间数据格式，不是要求用户按这个格式准备材料。

第一版支持的用户输入：

- Excel 表格：用于结构化数据，例如知识产权、研发项目、人员、费用、产品。
- Word 文档：用于半结构化文字和 Word 表格，例如研发项目说明、创新能力说明、已有申报材料草稿。

第一版明确不支持：

- PDF
- 图片 / OCR
- 扫描件
- 附件材料自动识别

附件材料只作为用户线下准备和上传的对象，不进入本数据解析层。

助手负责把这些材料整理成统一的内部数据结构，再用于校验、补缺、填表和保存后回读。

工作流程：

```text
用户 Excel / Word 原始资料
  → AI 阅读并整理
  → 中文表格展示给用户确认
  → 生成内部标准 JSON
  → 脚本预检
  → 按表单顺序填写系统
  → 保存后回读校验
```

## 顶层结构

```json
{
  "meta": {},
  "intellectualProperties": [],
  "humanResources": {},
  "rdProjects": [],
  "rdFees": [],
  "products": [],
  "innovation": {},
  "standards": [],
  "businessSummary": {}
}
```

## meta：申报基础信息

```json
{
  "companyName": "测试企业有限公司",
  "reportYear": 2026,
  "dataInnocomId": "",
  "sourceFiles": [],
  "notes": ""
}
```

说明：

- `dataInnocomId` 是系统申报书 ID，通常从当前页面识别，不要求用户提供。
- `sourceFiles` 记录用户提供的数据文件名，不记录敏感原文内容。

## intellectualProperties：知识产权

```json
[
  {
    "no": "01",
    "code": "IP01",
    "name": "测试知识产权名称",
    "category": "实用新型专利",
    "categoryValue": "2",
    "accreditNo": "ZL202500000000.0",
    "applicationNo": "CN202500000000.0",
    "authorizedDate": "2025-03-28",
    "acquireMethod": "自主研发",
    "acquireMethodValue": "2",
    "source": "用户提供",
    "usableForSystemValidation": false,
    "notes": "示例专利号不可用于真实系统校验"
  }
]
```

字段说明：

| 字段 | 说明 |
|------|------|
| `no` | 系统填写用编号，纯数字，如 `01` |
| `code` | 展示编号，如 `IP01` |
| `categoryValue` | 系统下拉值 |
| `accreditNo` | 系统校验用专利号，专利通常为 `ZL + 申请号主体` |
| `applicationNo` | 原始申请号，可选 |
| `usableForSystemValidation` | 是否可用于真实系统校验 |

注意：

- 真实系统测试时，专利号必须真实有效。
- 脱敏示例中的专利号只能做格式样例，不能用于系统校验。

## humanResources：人力资源

```json
{
  "employeeTotal": 50,
  "techStaffTotal": 15,
  "employment": {
    "onJob": { "employee": 50, "tech": 15 },
    "partTime": { "employee": 0, "tech": 0 },
    "temporary": { "employee": 0, "tech": 0 },
    "foreign": { "employee": 0, "tech": 0 },
    "returnedOverseas": { "employee": 0, "tech": 0 },
    "talentPlan": { "employee": 0, "tech": 0 }
  },
  "education": {
    "doctor": 1,
    "master": 5,
    "bachelor": 24,
    "juniorCollegeOrBelow": 20
  },
  "title": {
    "senior": 2,
    "middle": 8,
    "primary": 15,
    "seniorTechnician": 5
  },
  "age": {
    "under30": 8,
    "age31To40": 22,
    "age41To50": 15,
    "over51": 5
  }
}
```

基础校验：

- 科技人员数不能大于职工总数。
- 学历结构合计建议等于职工总数。
- 年龄结构合计建议等于职工总数。

## rdProjects：研发活动

```json
[
  {
    "code": "RD01",
    "no": "01",
    "name": "测试研发活动",
    "startDate": "2023-01-01",
    "endDate": "2023-12-31",
    "domain": {
      "level1": "资源与环境",
      "level1Value": "9",
      "level2": "大气污染控制技术",
      "level2Value": "229",
      "level3": "工业有害废气控制技术",
      "level3Value": "245"
    },
    "technologySource": "企业自有技术",
    "technologySourceValue": "6",
    "relatedIpCodes": ["IP01"],
    "budgetTotal": 3.0,
    "spendingByYear": {
      "2023": 1.0,
      "2024": 1.0,
      "2025": 1.0
    },
    "purposeAndOrganization": "测试说明",
    "coreTechnologyAndInnovation": "测试说明",
    "achievements": "测试说明",
    "orderNo": 1
  }
]
```

说明：

- `spendingByYear` 决定费用表按哪个年度填写。
- 费用表下拉是否能选到某个 RD，取决于 RD 起止日期和当前费用年度。

## rdFees：研发费用

```json
[
  {
    "rdCode": "RD01",
    "year": 2023,
    "internal": {
      "personnel": 1.0,
      "directInput": 0,
      "depreciation": 0,
      "amortization": 0,
      "design": 0,
      "equipmentDebugTrial": 0,
      "other": 0
    },
    "external": {
      "entrusted": 0,
      "domesticEntrusted": 0
    },
    "fillUser": "测试填报人",
    "fillDate": "2026-06-17",
    "orderNo": 1
  }
]
```

校验规则：

- 同一 `rdCode + year` 的费用合计应等于 `rdProjects[].spendingByYear[year]`。
- 填完费用明细后必须调用系统计算函数 `nbyjkfhj()` 和 `nwkfhj()`，再保存。

## products：高新技术产品（服务）

```json
[
  {
    "code": "PS01",
    "no": "01",
    "name": "测试产品",
    "domain": {
      "level1": "电子信息",
      "level1Value": "1",
      "level2": "软件",
      "level2Value": "",
      "level3": "基础软件",
      "level3Value": ""
    },
    "technologySource": "企业自有技术",
    "technologySourceValue": "6",
    "salesRevenue": 1.23,
    "isMainProduct": false,
    "relatedIpCodes": ["IP01"],
    "keyTechnology": "测试说明",
    "competitiveAdvantage": "测试说明",
    "ipSupport": "测试说明",
    "orderNo": 1
  }
]
```

说明：

- `salesRevenue` 会参与主要情况表的高新收入汇总。
- 技术领域仍需走三级级联。

## innovation：企业创新能力

```json
{
  "ipCompetitiveness": "测试说明",
  "transformationSummary": "测试说明",
  "transformations": [
    {
      "name": "测试科技成果",
      "type": "专利",
      "typeValue": "1",
      "source": "自主研发",
      "sourceValue": "1",
      "result": "新产品",
      "resultValue": "1",
      "year": "2023",
      "relatedIpCodes": ["IP01"],
      "relatedRdCodes": ["RD01"],
      "relatedPsCodes": ["PS01"],
      "ways": ["自行投资实施转化"],
      "wayValues": ["3"],
      "orderNo": 1
    }
  ],
  "rdOrganizationManagement": "测试说明",
  "managementAndTechStaff": "测试说明"
}
```

说明：

- 成果转化逐条记录依赖 IP/RD/PS 已存在。
- 多选字段要同时确认页面显示值和隐藏提交值。

## standards：标准制定

```json
[
  {
    "name": "测试标准",
    "level": "行业",
    "number": "T/TEST-0001-2026",
    "participation": "参与",
    "orderNo": 1
  }
]
```

说明：

- 标准编号建议避免空格，必要时自动替换为短横线或删除空格。

## businessSummary：主要情况表

```json
{
  "netAssets": {
    "2023": 0,
    "2024": 0,
    "2025": 0
  },
  "salesRevenue": {
    "2023": 0,
    "2024": 0,
    "2025": 0
  },
  "profit": {
    "2023": 0,
    "2024": 0,
    "2025": 0
  },
  "domesticRdExpense": {
    "2023": 0,
    "2024": 0,
    "2025": 0
  },
  "totalRevenue": 0
}
```

说明：

- 主要情况表中很多字段由前面表单自动汇总。
- 手动字段主要是近三年经营数据、境内研发费用、企业总收入等。

## 脱敏规则

生成示例数据时：

- 企业名、人名、客户名、项目名替换为测试名称。
- 财务金额保持量级和逻辑关系，可做小幅扰动。
- 日期可平移或替换，但应保持申报周期逻辑。
- 专利号、统一社会信用代码、电话、地址替换为格式正确的假值。
- 不保存真实值到假值的映射表。
- 示例 IP 标注 `usableForSystemValidation: false`。

## 用户确认视图

内部 JSON 不直接给用户填。需要用户确认时，转换为中文表格即可，例如：

```text
研发活动整理结果

| 编号 | 名称 | 起止时间 | 领域 | 关联IP | 2023费用 | 2024费用 | 2025费用 |
|------|------|----------|------|--------|----------|----------|----------|
| RD01 | 测试研发活动 | 2023-01-01 至 2025-12-31 | 资源与环境/... | IP01 | 1.00 | 1.00 | 1.00 |
```

用户确认后，再执行填表。
