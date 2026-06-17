# 企业创新能力（type=10）

## 结构

4 个子标签页，通过 `subType` 参数切换，每个独立保存：

| subType | 标签 | 说明 |
|---------|------|------|
| 0 | 知识产权对企业竞争力的作用 | 文本区 + 下方IP列表 |
| 1 | 科技成果转化情况 | 汇总文本 + 逐条成果列表 |
| 2 | 研究开发与技术创新组织管理情况 | 文本区 + 附件上传 |
| 3 | 管理与科技人员情况 | 文本区 |

## URL

```javascript
// 各子页：
initDataInnocom.do?type=10&subType=0&dataInnocomId=xxx
initDataInnocom.do?type=10&subType=1&dataInnocomId=xxx
initDataInnocom.do?type=10&subType=2&dataInnocomId=xxx
initDataInnocom.do?type=10&subType=3&dataInnocomId=xxx

// 成果转化逐条新增：
editDataEprTrans.do?subType=1&dataInnocomId=xxx
```

## subType=0：知识产权对企业竞争力的作用

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `Zscqjz` | `dataEprCycx.Czscqjz` | 知识产权对企业竞争力的作用（限400字）* | 文本区 |

保存：`document.querySelector("#dataEprCycxSave").click();`

## subType=1：科技成果转化情况

### 第一层：汇总文本区

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `Kjcgzh` | `dataEprCycx.Ckjcgzh` | 科技成果转化情况（限400字）* | 文本区 |

保存：`document.querySelector("#dataEprCycxSave").click();`

### 第二层：逐条成果列表

与 IP/RD/PS 表单结构类似：列表页 → 「添加」→ 编辑页 → 保存

**「添加」按钮的 form action：** `editDataEprTrans.do?subType=1`

### 第三层：成果编辑页字段

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `transName` | `dataEprTrans.transName` | 科技成果名称* | 文本 |
| `transTypeList` | `dataEprTrans.transType` | 成果类型* | 下拉 |
| `transSourceList` | `dataEprTrans.transSource` | 成果来源* | 下拉 |
| `transResult` | `dataEprTrans.transResult` | 转化结果* | 下拉 |
| `transDate` | `dataEprTrans.transYear` | 转化时间* | 年份（yyyy） |
| `position` | `dataEprTrans.position` | 排序号* | 文本 |
| `transIp` | `dataEprTrans.transIp` | 关联IP* | 多选下拉 |
| `transRd` | `dataEprTrans.transRd` | 关联RD* | 多选下拉 |
| `transPs` | `dataEprTrans.transPs` | 关联PS* | 多选下拉 |
| `transWay` | `dataEprTrans.transWay` | 转化形式* | 多选下拉 |

成果类型：1=专利, 2=版权, 3=集成电路布图设计, 4=其他
成果来源：1=自主研发, 2=受让/受赠/并购, 3=其他
转化结果：1=新产品, 2=新服务, 3=新设备, 4=新技术应用, 5=样品/样机, 6=其他
转化形式：1=许可他人使用, 2=作为投资折算股份, 3=自行投资实施转化, 4=向他人转让, 5=合作条件, 6=其他

保存：`document.querySelector("#dataEprTransSave").click();`

## subType=2：研究开发与技术创新组织管理情况

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `Jscxgl` | `dataEprCycx.Cjscxgl` | 研发组织管理（限400字）* | 文本区 |

保存：`document.querySelector("#dataEprCycxSave").click();`

## subType=3：管理与科技人员情况

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `Glykj` | `dataEprCycx.Cglykj` | 管理及科技人员（限400字）* | 文本区 |

保存：`document.querySelector("#dataEprCycxSave").click();`

## 导航方式（iframe 内切换）

```javascript
setTimeout(function() {
  var mf = document.getElementById("mainFrame");
  var md = mf.contentDocument || mf.contentWindow.document;
  var inf = md.getElementById("innocomFrame");
  inf.src = "https://gqqy.chinatorch.org.cn/.../initDataInnocom.do?type=10&subType=1&dataInnocomId=xxx";
}, 100);
```
