# 高企申报系统页面结构

## 双层 iframe 架构

```
主页面（homePage.do）
├── iframe#mainFrame（左侧导航 + 顶部标签栏）
│   └── iframe#innocomFrame（表单内容区）
│       ├── 列表页（表格展示）
│       └── 编辑/新增页（表单字段）
├── 主页面独立按钮（打印、提交）
└── 顶部信息栏
```

## 两种渲染模式

### 模式 A：iframe 嵌套（默认）

从 `homePage.do` → 点击顶部标签 → 在 mainFrame 内层导航。

这种情况下，innocomFrame 装表单内容，**所有操作都要穿透两层 iframe**：

```javascript
var mf = document.getElementById("mainFrame");
var md = mf.contentDocument || mf.contentWindow.document;
var inf = md.getElementById("innocomFrame");
var idoc = inf.contentDocument || inf.contentWindow.document;
// 现在 idoc 就是表单页面的 document
```

### 模式 B：直接渲染

直接导航到 `initDataInnocom.do?type=X` 或 `addDataEprXxx.do` 时，**没有 iframe 嵌套**，表单直接渲染在主页面。

```javascript
// 直接操作 document，不需要穿透 iframe
document.getElementById("fieldId");
```

### 如何选择

- 用户从首页点击顶部标签进入 → 模式 A
- 直接用 `/navigate` 导航到表单 URL → 模式 B
- **推荐用模式 B**（更简单），但要注意：主页的按钮（打印、提交）会消失

## URL 参数约定

| 参数 | 含义 | 示例 |
|------|------|------|
| `type` | 表单类型 | `type=2`（研发活动表） |
| `subType` | 子标签（创新能力专用） | `subType=0`~`3` |
| `dataInnocomId` | 申报书 ID | `dataInnocomId=xxx` |
| `innocomType` | 申报类型 | `innocomType=0`（认定） |
| `year` | 年份（费用表专用） | `year=2023` |
| `id` | 条目 ID（编辑时） | `id=xxx` |

## 表单类型对照

| type | 表单 | 填写依赖 |
|------|------|---------|
| 4 | 知识产权汇总表 | 无（但需要真实专利） |
| 9 | 人力资源情况表 | 无 |
| 2 | 研发活动情况表 | 可选关联 IP |
| 5 | 费用结构明细表 | 需先有 RD 项目 |
| 3 | 高新技术产品情况表 | 可选关联 IP |
| 10 | 企业创新能力 | 依赖 IP/RD/PS |
| 11 | 标准制定情况表 | 无 |
| 1 | 主要情况表 | 自动汇总前面所有表 |
| 7 | 上传附件 | 无 |
