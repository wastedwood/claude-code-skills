# 上年度高新技术产品（服务）情况表（type=3）

## 依赖

- 可选关联 IP（IP 从知识产权表读取）

## URL

| 用途 | URL |
|------|-----|
| 列表页 | `initDataInnocom.do?type=3&dataInnocomId=xxx` |
| 新增/编辑页 | `addOrUpdateDataEprProduct.do?dataInnocomId=xxx` |

## 字段映射

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `cod` | `dataEprProduct.Pbh` | 编号 | 文本（纯数字） |
| `productName` | `dataEprProduct.Pcpmc` | 产品（服务）名称* | 文本 |
| `onemain` | `dataEprProduct.MainDomain1` | 技术领域一级* | 下拉 |
| `scdmain` | `dataEprProduct.MainDomain2` | 技术领域二级* | 下拉 |
| `thdmain` | `dataEprProduct.MainDomain3` | 技术领域三级* | 下拉 |
| `technologyS` | `dataEprProduct.PjslyQk` | 技术来源* | 下拉 |
| `shr` | `dataEprProduct.Psnxssr` | 上年度销售收入* | 文本 |
| `checkbox_yes` / `checkbox_no` | `dataEprProduct.Psfzycpstatus` | 是否主要产品* | radio |
| `Zscqbh` | `dataEprProduct.Pzscqbh` | 知识产权编号 | 多选下拉 |
| `yxZscqbh` | — | 已选知识产权 | 只读显示 |
| `PGjjszb` | `dataEprProduct.Pgjjszb` | 关键技术及主要技术指标*（限400字） | 文本区 |
| `PJzys` | `dataEprProduct.Pjzys` | 与同类产品竞争优势*（限400字） | 文本区 |
| `PZscqqk` | `dataEprProduct.Pzscqqk` | 知识产权获得情况及支持作用*（限400字） | 文本区 |

> 三级级联操作见 [operations.md](../operations.md)

## 技术来源选项

| value | 文本 |
|-------|------|
| 1 | 大专院校 |
| 2 | 地方属科研院所 |
| 3 | 其他企业技术 |
| 4 | 引进技术本企业消化创新 |
| 5 | 国外技术 |
| 6 | 企业自有技术 |
| 7 | 中央属科研院所 |

## 保存

```javascript
document.querySelector("#eprproductsave").click();
```
