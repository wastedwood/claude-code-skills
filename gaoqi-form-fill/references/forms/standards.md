# 企业参与国家标准或行业标准制定情况汇总表（type=11）

## 结构

列表 → 新增/编辑页，与 IP/RD 类似。

## URL

| 用途 | URL |
|------|-----|
| 列表页 | `initDataInnocom.do?type=11&dataInnocomId=xxx` |
| 新增页 | `addOrUpdateDataEprTotal.do?dataInnocomId=xxx` |

## 字段

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `bname` | `dataEprTotal.bname` | 标准名称* | 文本 |
| — | `dataEprTotal.blevel` | 标准级别* | radio（国家/行业） |
| `bnumber` | `dataEprTotal.bnumber` | 标准编号* | 文本（**不允许空格**） |
| — | `dataEprTotal.pway` | 参与方式* | radio（主持/参与） |

## 保存

```javascript
document.querySelector("#dataEprTotalsave").click();
```
