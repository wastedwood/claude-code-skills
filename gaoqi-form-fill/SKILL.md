---
name: gaoqi-form-fill
description: >-
  高企申报系统表单填写助手。覆盖 7 张核心表单：人力资源情况表、研发活动情况表、费用结构明细表、
  知识产权汇总表、产品（服务）情况表、科技成果转化情况、标准制定情况表。

  人机协作填表：用户提供数据，AI 匹配到表单字段，用户处理导航/点击等操作，建立信任后 AI 全权操作。

  **工作模式**：人机协作渐进自动化。第一阶段：你操控页面，我填数据；第二阶段（信任建立后）：放手交给我全自动操作。

  **触发场景**：用户在高企认定管理工作网（gqqy.chinatorch.org.cn）的申报书中逐项修改表单数据，
  且用户提供了包含准确数据的数据源。第一版优先支持 Excel，Word 作为长文本参考材料。
---

# 高企申报表单填写助手

## 前置条件

1. 用户已登录 [gqqy.chinatorch.org.cn](https://gqqy.chinatorch.org.cn) 并已打开申报书
2. CDP 代理已启动（通过 `web-access` 技能）
3. 用户提供了数据来源（第一版支持 Excel / Word；浏览器填表前应先转换为标准 JSON）

## 操作须知

```text
温馨提示：部分站点对浏览器自动化操作检测严格，存在账号封禁风险。
已内置防护措施但无法完全避免，Agent 继续操作即视为接受。
```

---

## 工作模式

### 第一阶段：手动协作（默认）

| 你（用户） | AI（我） |
|-----------|---------|
| 登录进入编辑页 → 告诉我编号 | 解析数据 → 匹配字段 → 填入 → 校验 |
| 审核 → 保存/返回 → 开下一页 | 等待下一步指令 |

### 第二阶段：询问切换自动挡

手动协作 3-5 次顺利后，主动问用户要不要切自动挡。用户同意后：

### 第三阶段：自动挡

AI 全权操作：导航 → 填数 → 校验 → 保存 → 下一条，循环直到完成。

---

## 通用工作流（所有表单共通）

```
列表页 → 找到目标条目（需翻页时遍历所有页）
  → 点击「修改」或「添加」
  → 编辑页填入数据 → 触发校验/计算
  → 点「保存」 → 回到列表页 → 下一条
```

每张表单的差异见对应的 [references/forms/](./references/forms/) 文件。

---

## 表单填写顺序

按依赖关系依次处理：

| # | 表单 | 参考文件 | 依赖 |
|---|------|---------|------|
| 1 | [知识产权汇总表](./references/forms/ip.md) | `ip.md` | 需真实专利 |
| 2 | [人力资源情况表](./references/forms/hr.md) | `hr.md` | 无 |
| 3 | [研发活动情况表](./references/forms/rd-activity.md) | `rd-activity.md` | 可选 IP |
| 4 | [费用结构明细表](./references/forms/rd-fee.md) | `rd-fee.md` | 需 RD 项目 |
| 5 | [产品情况表](./references/forms/ps.md) | `ps.md` | 可选 IP |
| 6 | [企业创新能力](./references/forms/innovation.md) | `innovation.md` | 需 IP/RD/PS |
| 7 | [标准制定情况表](./references/forms/standards.md) | `standards.md` | 无 |
| 8 | 主要情况表 | 自动汇总 | 前面表填完后核对 |
| 9 | 上传附件 | — | 最后统一处理 |

---

## 页面结构

两种渲染模式（详见 [`references/structure.md`](./references/structure.md)）：

- **iframe 嵌套模式**：`homePage.do` → `mainFrame` → `innocomFrame`，需穿透两层 iframe
- **直接渲染模式**：`initDataInnocom.do?type=X`，无 iframe，直接操作 `document`

---

## 浏览器操作要点

详见 [`references/operations.md`](./references/operations.md)：

1. **中文编码**：必须用 `--data-binary @file.js`
2. **iframe 导航**：必须用 `setTimeout`
3. **三级级联下拉**：必须分步操作，不能一次设完
4. **费用表计算**：必须调用 `nbyjkfhj()` / `nwkfhj()`
5. **费用表年份**：URL 参数 `&year=2023`
6. **IP 专利号格式**：ZL+申请号（去CN前缀）
7. **标准编号**：不允许空格

---

## 填表前数据中转与预检

浏览器填表前，先把用户 Excel 整理为标准 JSON，并运行预检。

Word 暂不做确定性自动解析，只作为 AI 阅读参考，用来补充研发说明、产品说明、创新能力说明等长文本。

第一版已实现 Excel 入口：

```powershell
python scripts/excel-to-json.py `
  examples/test-data/gaoqi-sample-data.xlsx `
  examples/test-data/gaoqi-sample-data.json

python scripts/validate-json.py `
  examples/test-data/gaoqi-sample-data.json
```

预检出现 `ERROR` 时，不应继续自动填表。预检只有 `WARN` 时，应先让用户确认。

相关文档：

- [`references/data-schema.md`](./references/data-schema.md)
- [`references/input-adapter.md`](./references/input-adapter.md)

## 脚本工具

每次操作时从对应文件复制使用：

| 文件 | 用途 |
|------|------|
| [`scripts/excel-to-json.py`](./scripts/excel-to-json.py) | Excel 转标准 JSON |
| [`scripts/validate-json.py`](./scripts/validate-json.py) | 标准 JSON 预检 |
| [`scripts/eval-fill.js`](./scripts/eval-fill.js) | 通用填值工具函数 |
| [`scripts/trigger-fee-calc.js`](./scripts/trigger-fee-calc.js) | 费用表计算 |
| [`scripts/cascade-domain.js`](./scripts/cascade-domain.js) | 三级级联 |

---

## 相关技能

- **`web-access`**：本技能依赖 web-access 的 CDP 浏览器连接能力。
- **`officecli`**：用于读取 Excel 数据源。

---

## 已知陷阱

完整清单见各表单的 reference 文件 + `operations.md`。核心陷阱：

- 中文通过 Shell 传 eval 会乱码（必须 `--data-binary @file`）
- iframe 内直接设 src 导致 Uncaught（必须 `setTimeout`）
- 三级下拉联动需要等待（不能一次 eval）
- 费用表不调计算函数，合计不会刷新
- IP 专利号格式必须是 ZL+申请号，且要先选类别
- IP 表附件（专利证书PDF）为可选项，不强制上传
- 保存/返回都回到列表第 1 页
- 系统对自动化操作敏感，批量时注意节奏
