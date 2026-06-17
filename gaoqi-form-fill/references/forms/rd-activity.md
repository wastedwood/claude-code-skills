# 企业研究开发活动情况表（type=2）

## 依赖

- 可选关联 IP（需先有知识产权数据）

## URL

| 用途 | URL |
|------|-----|
| 列表页 | `initDataInnocom.do?type=2&dataInnocomId=xxx` |
| 新增页 | `addDataEprProject.do?dataInnocomId=xxx` |
| 编辑页 | `updateaddDataEprProject.do?id=xxx` |

## 字段映射

### 基本信息

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `hcod` | `dataEprProject.Pxmbh` | 研发活动编号 RD* | 文本（纯数字） |
| `yproductName` | `dataEprProject.Pxmmc` | 研发活动名称* | 文本 |
| `dataEprPQzsj` | `dataEprProject.Pqzsj` | 开始日期* | 日期（只读） |
| `dataEprPJssj` | `dataEprProject.Pjssj` | 结束日期* | 日期（只读） |

### 技术领域（三级级联）

| 字段 ID | name | 标签 |
|---------|------|------|
| `onemain` | `dataEprProject.Pjsly1` | 技术领域一级* |
| `scdmain` | `dataEprProject.Pjsly2` | 技术领域二级* |
| `thdmain` | `dataEprProject.Pjsly3` | 技术领域三级* |

> 级联操作见 [operations.md](../operations.md)

### 技术来源与 IP

| 字段 ID | name | 标签 | 类型 |
|---------|------|------|------|
| `jslyList` | `dataEprProject.Pjslya` | 技术来源* | 下拉 |
| `PZscqbha` | `dataEprProject.Pzscqbha` | 知识产权编号 | 多选下拉（Ctrl+左键） |

### 经费

| 字段 ID | name | 标签 | 说明 |
|---------|------|------|------|
| `spending` | `dataEprProject.Pyfjfzys` | 研发经费总预算* | 手填 |
| `yfjfzzc` | `dataEprProject.Pyfjfzzc` | 近三年总支出-总计 | 只读自动合计 |
| `zc1` | `dataEprProject.Pyfzc3` | 其中（2023） | 年份对应当前申报年度 |
| `zc2` | `dataEprProject.Pyfzc2` | 其中（2024） | 年份对应当前申报年度 |
| `zc3` | `dataEprProject.Pyfzc1` | 其中（2025） | 年份对应当前申报年度 |

> **注意**：三个年份字段名后缀是倒序的（Pyfzc3→zc1=2023, Pyfzc2→zc2=2024, Pyfzc1→zc3=2025）。实际操作时从页面 label 确认年份映射。

### 文本段落（各限400字）

| 字段 ID | name | 标签 |
|---------|------|------|
| `PLxmd` | `dataEprProject.Plxmd` | 目的及组织实施方式* |
| `PHxjs` | `dataEprProject.Phxjs` | 核心技术及创新点* |
| `PQdcg` | `dataEprProject.Pqdcg` | 取得的阶段性成果* |

### 技术来源选项

| value | 文本 |
|-------|------|
| 1 | 大专院校 |
| 2 | 地方属科研院所 |
| 3 | 其他企业技术 |
| 4 | 引进技术本企业消化创新 |
| 5 | 国外技术 |
| 6 | 企业自有技术 |
| 7 | 中央属科研院所 |

### 技术领域一级选项

| value | 文本 |
|-------|------|
| 1 | 电子信息 |
| 2 | 高技术服务 |
| 3 | 先进制造与自动化 |
| 4 | 航空航天 |
| 6 | 生物与新医药 |
| 7 | 新材料 |
| 8 | 新能源与节能 |
| 9 | 资源与环境 |

## 保存

```javascript
document.querySelector("#dataEprsave").click();
```
