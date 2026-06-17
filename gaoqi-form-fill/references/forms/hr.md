# 人力资源情况表（type=9）

## 特性

- 单记录表单（每个申报书只有一条 HR 记录）
- 分两大区块：总体情况（职工 vs 科技人员对比） + 人员结构（学历/职称/年龄）

## 字段映射

### 总体情况

| 字段 ID | 标签 | 说明 |
|---------|------|------|
| `entHrTotal` | 职工总数 |  |
| `satHrTotal` | 科技人员数 | **必须 ≤ 职工总数** |
| `entHrOnJob` | 在职人员-职工 | |
| `satHrOnJob` | 在职人员-科技 | **必须 ≤ 在职人员-职工** |
| `entHrPart` | 兼职人员-职工 | |
| `satHrPart` | 兼职人员-科技 | **必须 ≤ 兼职人员-职工** |
| `entHrExt` | 临时聘用人员-职工 | |
| `satHrExt` | 临时聘用人员-科技 | **必须 ≤ 临时聘用人员-职工** |
| `entHrForg` | 外籍人员-职工 | |
| `satHrForg` | 外籍人员-科技 | |
| `entHrAbroed` | 留学归国人员-职工 | |
| `satHrAbroed` | 留学归国人员-科技 | |
| `entHrTsdplan` | 干人计划人员-职工 | |
| `satHrTsdplan` | 干人计划人员-科技 | |

### 学历结构

| 字段 ID | 标签 |
|---------|------|
| `entHrDoctor` | 博士 |
| `entHrMaster` | 硕士 |
| `entHrBachelor` | 本科 |
| `entHrJunior` | 大专及以下 |

### 职称结构

| 字段 ID | 标签 |
|---------|------|
| `entHrSenior` | 高级职称 |
| `entHrMiddle` | 中级职称 |
| `entHrPrimary` | 初级职称 |
| `entHrMechanic` | 高级技工 |

### 年龄结构

| 字段 ID | 标签 |
|---------|------|
| `entHrAge1` | 30及以下 |
| `entHrAge2` | 31-40 |
| `entHrAge3` | 41-50 |
| `entHrAge4` | 51及以上 |

## 校验规则

- **科技人员各子项 ≤ 职工对应子项**（如 satHrOnJob ≤ entHrOnJob）
- 学历合计理论上应 = 职工总数（系统可能校验）
- 年龄合计理论上应 = 职工总数（系统可能校验）

## 保存

```javascript
document.querySelector("#dataEnmanressave").click();
```
