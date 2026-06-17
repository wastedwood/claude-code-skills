# 知识产权汇总表（type=4）

## 重要特性

**专利号自动校验：系统连接国家知识产权局数据库。**

- **专利**（发明/实用新型/外观）：输入正确专利号后，名称/获得方式/授权日自动回填
- **软著**：完全手填
- 专利号格式：`ZL` + 申请号（去掉 CN 前缀），例如 `ZL202520850832.6`
- 附件（专利证书PDF）为可选项，不强制上传

## 依赖

无（但需要有真实专利/软著数据，不能填假数据）

## URL

| 用途 | URL |
|------|-----|
| 列表页 | `initDataInnocom.do?type=4&dataInnocomId=xxx` |
| 新增页 | `addDataEprIntellectualPropert.do?dataInnocomId=xxx` |
| 编辑页 | `updateaddDataEprIntellectualPropert.do?id=xxx` |

## 操作流程

```
列表页 → 点「添加」→ 填数据 → 点「保存」→ 回到列表
```

## 字段映射

| 字段 ID | name 属性 | 标签 | 类型 |
|---------|----------|------|------|
| `propertyNo` | `dataEprIntellectualPropert.Pzscqbh` | 知识产权编号 | 文本输入，手填（如"01"） |
| `propertyCategory` | `dataEprIntellectualPropert.Plb` | 类别 | 下拉选择 |
| `propertyAccredit` | `dataEprIntellectualPropert.Psqh` | 专利号/著作权号 | 文本输入 |
| `propertyName` | `dataEprIntellectualPropert.Psqxmmc` | 知识产权名称 | 文本输入（专利自动回填） |
| `propertyWay` | `dataEprIntellectualPropert.Phdfs` | 获得方式 | 下拉选择（专利自动回填） |
| `txtDate` | `dataEprIntellectualPropert.Psqrq` | 授权日期 | 日期选择器（专利自动回填） |

## 类别选项

| value | 文本 |
|-------|------|
| 2 | 实用新型专利 |
| 3 | 外观设计专利 |
| 4 | 软件著作权 |
| 12 | 发明专利（非国防专利） |
| 6 | 发明专利（国防专利） |
| 7 | 植物新品种 |
| 8 | 国家级农作物品种 |
| 9 | 国家新药 |
| 10 | 国家一级中药保护品种 |
| 11 | 集成电路布图设计专有权 |

## 获得方式选项

| value | 文本 |
|-------|------|
| 1 | 其他 |
| 2 | 自主研发 |
| 3 | 受让 |
| 4 | 受赠 |
| 5 | 并购 |

## 填写步骤（关键！必须按顺序）

```
Step 1: propertyNo = "01"              # 手填编号
Step 2: propertyCategory = "2"          # 先选类别
Step 3: propertyAccredit = "ZL2025..."  # 输专利号 → 自动触发数据库查询
Step 4: 等待 3-5 秒 → propertyName/propertyWay/txtDate 自动填充
Step 5: 点「保存」(id="addsave")
```

## 保存

```javascript
document.querySelector("#addsave").click();
// 或：document.getElementById("addForm").submit();
```

## 返回列表

```javascript
document.querySelector("button.btn-default").click();
// 或导航：initDataInnocom.do?type=4&dataInnocomId=xxx
```

## 已知要点

- 新增 IP 编号是手填的纯数字（如"01"），不包含"IP"前缀
- 专利输入框自动大写 + 全角转换
- 系统会联网校验专利号真实性，不存在的专利号无法保存
- 附件（专利证书PDF）为可选项，不强制上传
- 已用II类知识产权表格：不参与创新能力评价，仅可作为关联
