# 企业年度研究开发费用结构明细表（type=5）

## 重要特性

**填完明细必须调用页面内置 JavaScript 计算函数，只设 value 不够。**

## 依赖

- 必须先有 RD 项目（项目编号下拉从 RD 表读取）
- URL 必须指定年份参数 `&year=2023`
- 年份由 RD 项目的起止日期决定

## URL

| 用途 | URL |
|------|-----|
| 列表页 | `initDataInnocom.do?type=5&dataInnocomId=xxx&year=2023` |
| 新增页 | `addDataEprRdFee.do?dataInnocomId=xxx&year=2023` |
| 编辑页 | `addDataEprRdFee.do?id=xxx&year=2023` |

## 字段映射

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `xmbh` | `dataEprRdFee.pxmbh` | 项目编号* | 下拉（RD列表） |
| `nbyjkftr` | `dataEprRdFee.pnbyjtrhj` | 共计（万元） | **只读自动计算** |
| `ryrg` | `dataEprRdFee.pryrghj` | 人员人工费用 | 文本 |
| `zjtr` | `dataEprRdFee.pzjtrhj` | 直接投入费用 | 文本 |
| `zjfy` | `dataEprRdFee.pzjftxhj` | 折旧费用与长期待摊费用 | 文本 |
| `wxzc` | `dataEprRdFee.pwxzchj` | 无形资产摊销费用 | 文本 |
| `sjf` | `dataEprRdFee.psjfhj` | 设计费用 | 文本 |
| `sbtsf` | `dataEprRdFee.psbtsfhj` | 装备调试费用与试验费用 | 文本 |
| `qtfy` | `dataEprRdFee.pqtfyhj` | 其他费用 | 文本 |
| `wtwbyjkftr` | `dataEprRdFee.pwtwbtrhj` | 委托外部研究开发费用 | 文本 |
| `pjnwbtrhj` | `dataEprRdFee.pjnwbtrhj` | 境内的外部研发费用 | 文本 |
| `nwhj` | `dataEprRdFee.pyjkfnwhj` | 研究开发费用小计 | **只读自动计算** |
| `fillUser` | `dataEprRdFee.pqytbr` | 企业填报人 | 文本 |
| `fillUserDate` | `dataEprRdFee.pqytbrqzrq` | 填报人签字日期 | 日期 |
| `orderNo` | `dataEprRdFee.position` | 排序号 | 文本 |

## 核心操作流程

```
1. 选择项目编号（从 RD 列表下拉选）
2. 填入各项费用明细
3. 调用 nbyjkfhj()   → 内部费用合计
4. 填入委外研发费用
5. 调用 nwkfhj()     → 内外总合计
6. 填入填报人、日期
7. 点保存
```

### 计算函数调用

```javascript
// 在填完所有数值字段后调用：
nbyjkfhj();  // 计算内部研究开发费用合计（ryrg+zjtr+zjfy+wxzc+sjf+sbtsf+qtfy）
// 读取内部合计：
var internalTotal = document.getElementById("nbyjkftr").value;

// 填完委外费用后调用：
nwkfhj();    // 计算内外总合计（内部 + 委外）
// 读取总合计：
var grandTotal = document.getElementById("nwhj").value;
```

## 保存

```javascript
document.querySelector("#dataEprRdfeesave").click();
```

## 已知要点

- 费用表年份由 RD 项目起止日期决定（如 RD01 为 2023-2025，则费用表有 2023/2024/2025 三页）
- 年份标签（2025/2024/2023）通过 URL 参数 `&year=2023` 切换
- 填完明细不调计算函数，合计不会自动刷新
- 0.01 以内的尾差是浮点精度问题，如实告知用户即可
- 费用字段可能出现负数（如冲减前期费用），正常填入即可
