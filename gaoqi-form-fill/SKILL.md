---
name: gaoqi-form-fill
description: >-
  高企申报系统表单填写助手。覆盖多张核心表单：费用明细表、活动情况表、知识产权汇总表、产品（服务）情况表、科技成果转化情况等。
  
  人机协作填表：用户提供数据，AI 匹配到表单字段，用户处理导航/点击等操作，建立信任后 AI 全权操作。
  
  **工作模式**：人机协作渐进自动化。第一阶段：你操控页面，我填数据；第二阶段（信任建立后）：放手交给我全自动操作。
  
  **触发场景**：用户在高企认定管理工作网（gqqy.chinatorch.org.cn）的申报书中逐项修改表单数据，且用户提供了包含准确数据的数据源（Excel、表格文本、JSON、结构化数据等任意格式）。
---

# 高企申报表单填写助手

本技能覆盖高企申报系统核心表单。底层的操作逻辑所有表单一致：

```
列表页（找到目标条目）→ 编辑页（填入数据）→ 保存 → 回到列表 → 下一条
```

目前已掌握的表单：

| # | 表单名 | 类型 | 掌握程度 |
|---|-------|------|---------|
| 1 | 企业年度研究开发费用结构明细表 | 数值填写 + 自动计算校验 | ✅ 已覆盖 |
| 2 | 企业研究开发活动情况表 | 字段混合（结构化 + 三级领域 + 经费 + 三段文本） | ✅ 已覆盖 |
| 3 | 知识产权汇总表 | 字段填写 + 附件管理 | ✅ 已覆盖 |
| 4 | 上年度高新技术产品（服务）情况表 | 字段 + 三段文本 + 领域三级下拉 | ✅ 已覆盖 |
| 5 | 企业创新能力—科技成果转化情况 | 汇总文本区 + 逐条成果管理（关联IP/RD/PS） | ✅ 已覆盖 |
| ... | 人力资源情况表等 | 待分析 | ⬜ 遇到时学习 |

> **对新表单的处理方式**：遇到未覆盖的表单时，先让用户带我看一眼页面结构，我分析字段映射关系和交互逻辑，补充到技能知识库中，然后正常开始自动填写。第一次可能慢点，但下次就认识了。

---

## 工作模式：手动 → 自动渐进

本技能采用**渐进式自动化**策略：先手动协作建立信任，再主动问用户要不要切自动挡。

### 第一阶段：手动协作（默认）

前几轮让用户控制导航，AI 只负责填数，让用户建立对数据准确性的信任：

| 谁做 | 做什么 |
|------|--------|
| **你（用户）** | 登录系统 → 进入编辑页 → 审核数据 → 点「保存」/「返回」→ 开下一个 |
| **AI（我）** | 解析用户提供的数据 → 匹配到表单字段 → 填入内容 → 校验结果 |

**手动协作流程：**
```
你: 打开第N条编辑页 → 告诉我编号
我: 填数/校验 → 报结果
你: 审核 → 保存/返回 → 开下一个 → 告诉我编号
↻ 循环
```

### 第二阶段：询问切换自动挡

当手动协作顺利进行了 3-5 次后（用户已看到数据填得准确），主动询问：
> "数据都准确吧？要不要切到**自动挡**？接下来我帮你自动导航、填数、校验、保存，一步到位，你看着就行。"

用口语化的方式问，不要搞成正式确认弹窗的感觉。

### 第三阶段：自动挡

用户同意后，AI 全权操作：
1. 在列表页找到下一个要修改的 RD 项目 → 点击「修改」 → 进入编辑页
2. 填入数据 → 触发计算（费用表）或校验文本（活动表）
3. 点击「保存」 → 等页面回到列表 → 自动开始下一个
4. 中途如果遇到翻页、年份切换等操作，一并自动处理
5. 每个项目完成后简要汇报进度

**自动挡退出条件**：
- 用户随时说"停"或"我来" → 回到手动模式
- 遇到异常（字段找不到、保存失败等）→ 暂停并告知用户，由用户决定继续手动还是排查问题

---

## 通用工作流（所有表单共通）

无论具体是哪张表单，操作链路都是一套模板：

1. **列表页** → 找到要修改的条目（可能需要翻页）
2. **打开编辑页** → 点击「修改」或对应操作入口
3. **填入数据** → 按字段映射将用户数据填入表单
4. **触发校验** → 调用前端计算函数或手动校验逻辑
5. **保存/返回** → 提交修改，回到列表页
6. **循环** → 取下一条，直至全部完成

每张表单的差异只在于：
- 字段数和类型（纯数值？纯文本？混合？）
- 是否需要触发前端计算
- 特殊交互（下拉选择、日期选择器、附件上传等）
- 字数限制、格式要求等校验规则

下文"页面结构"包含了当前高企系统的通用 DOM 结构，"表单一/二"是已掌握的特定表单知识。

---

## 前置条件

1. 用户已登录目标系统，并已进入目标表单页面
2. CDP/Playwright 代理已连接（遵循 web-access skill 的浏览器连接流程）
3. 用户提供了包含相关数据的源材料（Excel、表格文本、JSON、自然语言描述等任何格式）

---

## 页面结构（通用）

### iframe 嵌套

```
主页面
├── div#left（左侧导航）
└── iframe#mainFrame（内容区）
    ├── 顶部标签栏（填报说明、申请书封皮…）
    └── iframe#innocomFrame（表单内容区）
        ├── 列表页（RD 项目表格）
        └── 编辑页（单个 RD 项目的表单）
```

CDP eval 操作需逐层穿透 iframe：

```javascript
var f = document.getElementById("mainFrame");
var d = f.contentDocument || f.contentWindow.document;
var i = d.getElementById("innocomFrame");
var c = i.contentDocument || i.contentWindow.document;
```

### 列表页结构

列表页以表格展示 RD 项目，每行包含：
- `td[1]` — RD 编号（如 RD01）
- `td[2]` — 项目名称
- `td[9]` — 「修改」链接（`a.btn_grid_link_edit`，文本为"修改"）

**翻页**：通过 `DataEprProject_list` 表单提交：

```javascript
var form = c.getElementById("DataEprProject_list");
form.querySelector("[name=DataEprProject_list_p]").value = "2";  // 目标页码
form.action = "/xonlinereport/inforeport/DataInnocom/getDataEprProjects.do";
form.method = "post";
// 重要：用 setTimeout 让 eval 先返回，避免 Uncaught 错误
setTimeout(function() { form.submit(); }, 100);
```

**获取修改链接**：

```javascript
// 遍历当前页表格
var rows = c.querySelectorAll("table")[1].querySelectorAll("tr");
for (var i = 0; i < rows.length; i++) {
  var tds = rows[i].querySelectorAll("td");
  if (tds.length >= 10) {
    var rd = tds[1].textContent.trim();
    var editLink = tds[9].querySelector("a");
    if (editLink) links[rd] = editLink.href;
  }
}
```

**批量收集+直接导航策略**（推荐，避免反复翻页）：
1. 先遍历所有页面，收集全部 RD 的编辑 URL
2. 然后直接设置 iframe src 逐项导航到编辑页，无需再走列表页

```javascript
i.src = "https://gqqy.chinatorch.org.cn/xonlinereport/.../updateaddDataEprProject.do?id=XXX&";
```

### 保存与返回

两个按钮都在编辑页底部：

| 操作 | 按钮 ID | 选择器 | 行为 |
|------|---------|--------|------|
| 保存 | `dataEprsave`（活动表）/ `dataEprRdfeesave`（费用表） | `button.green` 或 `#dataEprsave` | 提交表单，返回列表第1页 |
| 返回 | 无固定 ID | `button.btn-default`（文本=返回） | 放弃修改，返回列表第1页 |

无论点"保存"还是"返回"，都回列表第1页。

```javascript
// 保存
c.getElementById("dataEprsave").click();  // 活动表
c.getElementById("dataEprRdfeesave").click();  // 费用表

// 返回
c.querySelector("button.btn-default").click();
```

如果保存点击不生效，改用直接提交表单：
```javascript
var form = c.getElementById("dataEprForm");  // 活动表
form.submit();
```

---

## 表单一：企业年度研究开发费用结构明细表

### 数据准备

#### 第一步：识别 Excel 列

**用户 Excel 的表头命名可能和系统字段名不完全一致**，必须先读取第一行（表头），根据语义匹配确定每列对应哪个表单字段。不要假设列的顺序或列名与系统完全一致。

**语义匹配参考**（常见的用户写法）：

| 表单字段 | 常见的用户列名写法 |
|---------|------------------|
| 项目编号 | 项目编号、RD编号、项目号、研发项目编号 |
| 人员人工费用 | 人员人工费用、人工费、人员费、研发人员工资、人工成本 |
| 直接投入费用 | 直接投入费用、直接投入、材料费、直接材料、原材料 |
| 折旧摊销 | 折旧摊销、折旧费用、折旧费、长期待摊费用摊销 |
| 无形资产摊销 | 无形资产摊销、无形资产摊销费、无形资产 |
| 设计费 | 设计费、设计费用 |
| 装备调试费用与试验费用 | 装备调试费、试验费、调试试验费 |
| 其他费用 | 其他费用、其他 |
| 委外研发费用 | 委外研发费用、委托外部研发、外包研发、外部研发费 |
| 境内的外部研发费用 | 境内外部研发、境内委外 |
| 研究开发费用合计 | 合计、研发费用合计、总计、研究开发费用合计 |

**识别流程：**
1. 用 officecli 读取 Excel 第一行（表头）
2. 逐个表头文本与上表做模糊匹配，确定每列对应哪个字段
3. 如果某个字段在 Excel 中找不到对应列，则跳过该字段（不修改）
4. 向用户确认识别结果后再开始填写

#### 第二步：标准字段映射

| # | 内容 | 字段 ID | name 属性 | 表单标签 | 类型 |
|---|------|---------|----------|---------|------|
| A | 项目编号 | `xmbh` | `dataEprRdFee.pxmbh` | 项目编号 * | 下拉选择（RD列表） |
| B | 内部研究开发费 | `nbyjkftr` | `dataEprRdFee.pnbyjtrhj` | 共计（万元） | 只读，自动计算 |
| C | 人员人工费用 | `ryrg` | `dataEprRdFee.pryrghj` | 其中：人员人工费用（万元） | 文本输入 |
| D | 直接投入费用 | `zjtr` | `dataEprRdFee.pzjtrhj` | 直接投入费用（万元） | 文本输入 |
| E | 折旧摊销 | `zjfy` | `dataEprRdFee.pzjftxhj` | 折旧费用与长期待摊费用（万元） | 文本输入 |
| F | 无形资产摊销 | `wxzc` | `dataEprRdFee.pwxzchj` | 无形资产摊销费用（万元） | 文本输入 |
| G | 设计费 | `sjf` | `dataEprRdFee.psjfhj` | 设计费用（万元） | 文本输入 |
| H | 装备调试费用与试验费用 | `sbtsf` | `dataEprRdFee.psbtsfhj` | 装备调试费用与试验费用（万元） | 文本输入 |
| I | 其他费用 | `qtfy` | `dataEprRdFee.pqtfyhj` | 其他费用（万元） | 文本输入 |
| J | 委外研发费用 | `wtwbyjkftr` | `dataEprRdFee.pwtwbtrhj` | 委托外部研究开发费用（万元） | 文本输入 |
| K | 境内的外部研发费用 | `pjnwbtrhj` | `dataEprRdFee.pjnwbtrhj` | 其中：境内的外部研发费用 | 文本输入 |
| L | 研究开发费用合计 | `nwhj` | `dataEprRdFee.pyjkfnwhj` | 研究开发费用（内、外部）小计（万元） | 只读，自动计算 |
| M | 企业填报人 | `fillUser` | `dataEprRdFee.pqytbr` | 企业填报人 | 文本输入 |
| N | 填报人签字日期 | `fillUserDate` | `dataEprRdFee.pqytbrqzrq` | 企业填报人签字日期 | 日期选择器 |
| O | 排序号 | `orderNo` | `dataEprRdFee.position` | 排序号 | 文本输入 |

#### 填写策略

哪些字段需要修改取决于 Excel 数据，**不是固定的 5 个**。原则是：

1. Excel 中值不为 0 的字段 → 必须填入
2. Excel 中值为 0 且页面也为 0 的字段 → 不动
3. 页面已有值但与 Excel 不一致的字段 → 用 Excel 值覆盖

#### 触发自动计算

填入字段后，需调用页面的计算函数才能得到合计：
```javascript
c.defaultView.nbyjkfhj();
```

#### 读取合计值校验

```javascript
var total = c.getElementById("nwhj").value;
```

#### 修改链接定位

该表单的「修改」链接格式：
```html
<a href="/xonlinereport/inforeport/DataInnocom/addDataEprRdFee.do?id=XXX&year=2023&">修改</a>
```

批量获取：
```javascript
var els = c.querySelectorAll("[href*=\"RdFee\"]");
```

#### 保存

```javascript
c.getElementById("dataEprRdfeesave").click();
```

---

## 表单二：企业研究开发活动情况表

### 编辑页

该表单字段较丰富，分为几组：

#### 基本信息（结构化）

| 字段 ID | name 属性 | 表单标签 | 类型 |
|---------|----------|---------|------|
| `hcod` | `dataEprProject.Pxmbh` | 研发活动编号：RD * | 文本输入，纯数字 |
| `yproductName` | `dataEprProject.Pxmmc` | 研发活动名称 * | 文本输入 |
| `dataEprPQzsj` | `dataEprProject.Pqzsj` | 开始日期 * | 日期选择器（只读）YYYY-MM-DD |
| `dataEprPJssj` | `dataEprProject.Pjssj` | 结束日期 * | 日期选择器（只读）YYYY-MM-DD |

#### 技术领域（三级级联）

与「上年度高新技术产品（服务）情况表」的级联完全一致：

| 字段 ID | name 属性 | 标签 | 说明 |
|---------|----------|------|------|
| `onemain` | `dataEprProject.Pjsly1` | 技术领域（一级）* | 下拉选择（八大领域） |
| `scdmain` | `dataEprProject.Pjsly2` | 技术领域（二级）* | 下拉选择，随一级联动 |
| `thdmain` | `dataEprProject.Pjsly3` | 技术领域（三级）* | 下拉选择，随二级联动 |

领域选项值同表单四（参见上文「技术领域一级选项」表）。

#### 技术来源与知识产权关联

| 字段 ID | name 属性 | 表单标签 | 类型 |
|---------|----------|---------|------|
| `jslyList` | `dataEprProject.Pjslya` | 技术来源 * | 下拉选择（同表单四选项表） |
| `PZscqbha` | `dataEprProject.Pzscqbha` | 知识产权编号 | 多选下拉（Ctrl+左键） |

#### 经费

| 字段 ID | name 属性 | 表单标签 | 类型 | 说明 |
|---------|----------|---------|------|------|
| `spending` | `dataEprProject.Pyfjfzys` | 研发经费总预算（万元）* | 文本输入 | |
| `yfjfzzc` | `dataEprProject.Pyfjfzzc` | 研发经费近三年总支出—总计 | 文本输入（只读） | 自动合计 |
| `zc1` | `dataEprProject.Pyfzc3` | 其中（2023） | 文本输入 | 年份与该 RD 条目所在申报年度对应 |
| `zc2` | `dataEprProject.Pyfzc2` | 其中（2024） | 文本输入 | |
| `zc3` | `dataEprProject.Pyfzc1` | 其中（2025） | 文本输入 | |

> **注意：** 三个「其中」年份字段（zc1/zc2/zc3）的 name 后缀是倒序的（zc3→Pyfzc1），但 name 中的年份数字（Pyfzc_N_）和 id 中的数字**不对应年份**。实际操作时应从页面读取 label（"其中（2023）"等）确认各字段映射到哪一年，不要硬编码字段与年份的关系。

#### 文本段落（各限400字）

| 字段 ID | name 属性 | 表单标签 | 说明 |
|---------|----------|---------|------|
| `PLxmd` | `dataEprProject.Plxmd` | 目的及组织实施方式（限400字）* | 研发目的 + 组织方式 |
| `PHxjs` | `dataEprProject.Phxjs` | 核心技术及创新点（限400字）* | 技术/创新点 |
| `PQdcg` | `dataEprProject.Pqdcg` | 取得的阶段性成果（限400字）* | 成果描述 |

#### 附件

PDF 上传区，提示语："请上传科研项目立项证明（已验收或结题项目需附验收或结题报告）相关材料。"

### 保存与返回

```javascript
c.getElementById("dataEprsave").click();   // 保存
c.querySelector("button.btn-default").click();  // 返回
```

### 数据识别

用户数据通常是结构化表格，包含：项目编号、名称、起止日期、技术领域（完整路径）、技术来源、关联IP、总预算、分年度经费、三段文本等。按语义匹配识别各列对应关系。

### 预算校验（以往版本遗留，作为参考）

通过 `charCodeAt` 匹配中文字符来定位文本区中的预算数字（因 Shell 传中文给 eval 会乱码）：

```javascript
var v = c.getElementById("PLxmd").value;
for (var i = 0; i < v.length - 1; i++) {
  if (v.charCodeAt(i) === 39044 && v.charCodeAt(i+1) === 31639) {  // "预算"
    // 提取后续数字
  }
}
```

---

## 表单三：知识产权汇总表

### 列表页

顶部有汇总统计表（按 I 类/II 类分专利类型统计数量），下方是 IP 详细列表，每行包含：
- checkbox（多选）
- 知识产权编号（如 IP01）
- 知识产权名称
- 类别（发明专利、实用新型等）
- 专利号/著作权号
- 证明材料（「查看」链接下载文件）
- 操作（「修改」链接）
- 知识产权（预留）

**修改链接：**
```javascript
var links = c.querySelectorAll("a[href*=\"updateaddDataEprIntellectualPropert\"]");
// links[0].href = "https://.../updateaddDataEprIntellectualPropert.do?id=XXX&"
```

### 编辑页

字段映射：

| 字段 ID | name 属性 | 表单标签 | 类型 | 说明 |
|---------|----------|---------|------|------|
| `propertyNo` | `dataEprIntellectualPropert.Pzscqbh` | 知识产权编号 | 文本输入 | 纯数字，如"01"（不包含IP前缀） |
| `propertyCategory` | `dataEprIntellectualPropert.Plb` | 类别 | 下拉选择 | 见下方选项列表 |
| `propertyAccredit` | `dataEprIntellectualPropert.Psqh` | 专利号/著作权号 | 文本输入（只读） | 自动大写+全角转换 |
| `propertyName` | `dataEprIntellectualPropert.Psqxmmc` | 知识产权名称 | 文本输入 | |
| `propertyWay` | `dataEprIntellectualPropert.Phdfs` | 获得方式 | 下拉选择 | 自主研发/受让/受赠/并购/其他 |
| `txtDate` | `dataEprIntellectualPropert.Psqrq` | 授权日期 | 日期选择器（只读） | YYYY-MM-DD |

**类别下拉：**

| value | 显示文本 |
|-------|---------|
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

**获得方式下拉：**

| value | 显示文本 |
|-------|---------|
| 1 | 其他 |
| 2 | 自主研发 |
| 3 | 受让 |
| 4 | 受赠 |
| 5 | 并购 |

### 操作

**保存：**
```javascript
c.getElementById("addsave").click();
```

**返回：**
```javascript
c.querySelector("button.btn-default").click();
// 等价导航：/xonlinereport/inforeport/DataInnocom/initDataInnocom.do?type=4&dataInnocomId=XXX
```

### 数据识别

知识产权数据通常是结构化表格，包含：编号、名称、类别、专利号、获得方式、授权日期等字段。按语义匹配识别各列对应关系。

---

## 表单四：上年度高新技术产品（服务）情况表

### 列表页

表格列：
- checkbox（多选）
- 产品编号（如 PS01）
- 产品（服务）名称
- 技术领域（三级级联，如"先进制造与自动化/先进制造工艺与装备/智能装备驱动控制技术"）
- 技术来源
- 上年度销售收入（万元）
- 是否主要产品（服务）
- 知识产权（关联的 IP 编号列表）
- 证明材料（「查看」下载链接）
- 操作（「修改」链接）

**修改链接定位：**
```javascript
var links = c.querySelectorAll("a[href*=\"addOrUpdateDataEprProduct\"]");
// links[0].href = "https://.../addOrUpdateDataEprProduct.do?id=XXX&"
```

### 编辑页

字段映射：

| 字段 ID | name 属性 | 表单标签 | 类型 | 说明 |
|---------|----------|---------|------|------|
| `cod` | `dataEprProduct.Pbh` | 编号 | 文本输入 | 纯数字，如"01"（不含PS前缀） |
| `productName` | `dataEprProduct.Pcpmc` | 产品（服务）名称 | 文本输入 | |
| `onemain` | `dataEprProduct.MainDomain1` | 技术领域（一级） | 下拉选择 | 八大领域，见下方 |
| `scdmain` | `dataEprProduct.MainDomain2` | 技术领域（二级） | 下拉选择 | 随一级联动变化 |
| `thdmain` | `dataEprProduct.MainDomain3` | 技术领域（三级） | 下拉选择 | 随二级联动变化 |
| `technologyS` | `dataEprProduct.PjslyQk` | 技术来源 | 下拉选择 | 见下方选项 |
| `shr` | `dataEprProduct.Psnxssr` | 上年度销售收入（万元） | 文本输入 | 数值 |
| `checkbox_yes`/`checkbox_no` | `dataEprProduct.Psfzycpstatus` | 是否主要产品（服务） | radio | 是(1)/否(0) |
| `Zscqbh` | `dataEprProduct.Pzscqbh` | 知识产权编号 | 多选下拉 | Ctrl+左键多选 |
| `yxZscqbh` | —（只读文本区） | 已选知识产权 | 只读 | 自动显示已选IP列表 |
| `PGjjszb` | `dataEprProduct.Pgjjszb` | 关键技术及主要技术指标（限400字）* | 文本区 | |
| `PJzys` | `dataEprProduct.Pjzys` | 与同类产品（服务）的竞争优势（限400字）* | 文本区 | |
| `PZscqqk` | `dataEprProduct.Pzscqqk` | 知识产权获得情况及其对产品（服务）在技术上发挥的支持作用（限400字）* | 文本区 | |

**技术领域一级选项：**

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

**技术来源选项：**

| value | 文本 |
|-------|------|
| 1 | 大专院校 |
| 2 | 地方属科研院所 |
| 3 | 其他企业技术 |
| 4 | 引进技术本企业消化创新 |
| 5 | 国外技术 |
| 6 | 企业自有技术 |
| 7 | 中央属科研院所 |

**注意：** 二级/三级领域是级联下拉，选择一级后二级自动加载可用选项。如果用户提供的数据中包含完整领域路径（如"先进制造与自动化/先进制造工艺与装备/智能装备驱动控制技术"），需要拆分后逐级设置。

### 操作

**保存：**
```javascript
c.getElementById("eprproductsave").click();
// 或用 form.submit()
```

**返回：**
```javascript
c.querySelector("button.btn-default").click();
// 后台执行 back() 函数
```

### 数据识别

用户数据通常是结构化表格，包含：产品编号、名称、技术领域、技术来源、销售收入、是否主要产品、关联IP、三段文本描述等字段。按语义匹配识别各列。

---

## 表单五：企业创新能力—科技成果转化情况

该表单嵌套在「企业创新能力」大标签下，分 4 个子标签。本表单对应子标签「科技成果转化情况」(subType=1)。

**结构特点：双层设计**

### 第一层：汇总文本区

位于页面上方，一个文本区 + 保存按钮：

| 字段 ID | name 属性 | 标签 | 类型 |
|---------|----------|------|------|
| `Kjcgzh` | `dataEprCycx.Ckjcgzh` | 科技成果转化情况（限400字）* | 文本区 |

保存：
```javascript
c.getElementById("dataEprCycxSave").click();
```

### 第二层：逐条成果列表

下方表格列出所有转化成果条目，每行包含：
- 序号
- 科技成果名称
- 成果类型
- 科技成果来源
- 转化结果
- 转化时间
- 关联 IP
- 关联 RD
- 关联 PS
- 排序号
- 证明材料（查看/下载）
- 操作（修改/删除）

**修改链接：**
```javascript
var links = c.querySelectorAll("a[href*=\"editDataEprTrans\"]");
// links[0].href = "https://.../editDataEprTrans.do?id=XXX&subType=1"
```

### 第三层：单条成果编辑页

点击「添加」或「修改」进入。

字段映射：

| 字段 ID | name 属性 | 表单标签 | 类型 |
|---------|----------|---------|------|
| `transName` | `dataEprTrans.transName` | 科技成果名称 * | 文本输入 |
| `transTypeList` | `dataEprTrans.transType` | 成果类型 * | 下拉选择 |
| `transSourceList` | `dataEprTrans.transSource` | 成果来源 * | 下拉选择 |
| `transResult` | `dataEprTrans.transResult` | 转化结果 * | 下拉选择 |
| `transDate` | `dataEprTrans.transYear` | 转化时间 * | 年份选择（yyyy） |
| `position` | `dataEprTrans.position` | 排序号 * | 文本输入 |
| `transIp` | `dataEprTrans.transIp` | 关联 IP * | 多选下拉（Ctrl+左键） |
| `transRd` | `dataEprTrans.transRd` | 关联 RD * | 多选下拉（Ctrl+左键） |
| `transPs` | `dataEprTrans.transPs` | 关联 PS * | 多选下拉（Ctrl+左键） |
| `transWay` | `dataEprTrans.transWay` | 转化形式 * | 多选下拉（Ctrl+左键） |
| — | — | 附件 | PDF 上传 |

**成果类型选项：**

| value | 文本 |
|-------|------|
| 1 | 专利 |
| 2 | 版权 |
| 3 | 集成电路布图设计 |
| 4 | 其他 |

**成果来源选项：**

| value | 文本 |
|-------|------|
| 1 | 自主研发 |
| 2 | 受让、受赠、并购 |
| 3 | 其他 |

**转化结果选项：**

| value | 文本 |
|-------|------|
| 1 | 新产品 |
| 2 | 新服务 |
| 3 | 新设备 |
| 4 | 新技术应用 |
| 5 | 样品/样机 |
| 6 | 其他 |

**转化形式选项（多选）：**

| value | 文本 |
|-------|------|
| 1 | 许可他人使用该科技成果 |
| 2 | 以该科技成果作为投资，折算股份或出资比例 |
| 3 | 自行投资实施转化 |
| 4 | 向他人转让该科技成果 |
| 5 | 以该科技成果作为合作条件，与他人共同实施转化 |
| 6 | 其他 |

**保存：**
```javascript
c.getElementById("dataEprTransSave").click();
// 或 form.submit()
```

**返回：**
```javascript
c.querySelector("button.btn-default").click();
```

---

## 协作流程（分步）

### 第一步：理解数据

1. 用户提供数据（可以是 Excel 文件、表格文本、JSON、结构化数据、自然语言描述等任何格式）
2. 根据数据格式用合适的方式读取：
   - Excel (.xlsx) → 使用 `officecli` 读取
   - 网页/动态数据源 → 使用 web-access 获取
   - 结构化文本/JSON → 直接从用户消息中解析
   - 自然语言描述 → 从中提取关键信息
3. 建立各 RD 项目的数据字典，明确每个字段的数据来源和对应关系

### 第二步：确认起点

确认用户已完成哪些项目、从哪个 RD 项目开始。例如：
> "2023年 RD01-RD25 已填好，从 RD26 开始"

### 第三步：循环填表

每轮循环中，AI 需要**主动判断用户已到达编辑页**，而不是等用户报编号。

识别用户已就绪的信号：
- 用户明确报了一个 RD 编号（如 "26"、"34"）
- 用户说了"好了"、"可以了"、"继续"、"下一个"等
- 用户没说任何话，但感知到页面已经切换到编辑页（通过检查 iframe 内容判断）

无论用户以什么方式示意，AI 的响应都是：
1. 如果用户报了编号 → 查找对应数据填入
2. 如果用户没报编号 → 通过页面上项目名称等字段确认是哪个 RD 项目，再匹配数据
3. 逐一将数据填入或校验表单字段
4. 触发自动计算（费用表）或校验文本（活动表）
5. 向用户报告结果
6. 等待用户审核后保存，继续下一个

### 第四步：校验

- **费用表**：确认合计值与数据源一致。0.01 以内的尾差（浮点精度导致），如实告知用户即可。
- **活动表**：确认预算数字与数据源一致。不匹配则修正。

---

## 已知陷阱与经验

1. **分页表单提交（Uncaught 错误）**：直接 `form.submit()` 会触发 iframe 导航，导致 eval 上下文销毁报 Uncaught。解法：用 `setTimeout(function(){form.submit()}, 100)` 让 eval 先返回。
2. **中文文本操作**：Shell 传中文字符给 CDP eval 会被乱码破坏，不能直接 `indexOf('预算')`。必须用 `charCodeAt` 匹配 Unicode 码点定位中文。
3. **年份切换**：列表页顶部有年份标签（如「2025 2024 2023」），点击后加载对应年份数据。程序化点击可能因页面事件绑定方式不同而失败，此时让用户手动点击即可。
4. **负值**：费用字段可能出现负数（如冲减前期费用），属于正常数据，按实际值填入即可。
5. **保存不生效**：点击保存按钮后页面仍停留在编辑页，说明提交未触发。改用 `form.submit()` 直接提交表单。
6. **批量链接收集**：推荐一次性遍历所有分页，收集全部 RD 的编辑 URL，然后直接设置 iframe src 逐项处理，避免每次保存后翻页回原位。
7. **保存/返回都到第1页**：无论点"保存"还是"返回"，列表页都重置到第1页。需要翻页才能继续处理后面的 RD。
8. **字段读取为 null**：编辑页表单字段全部为 null，说明 iframe 内容尚未完成加载。等待后重新设置 iframe 的 src 重试。
9. **页面提示条**：列表页顶部有"是否默认隐藏提示"的开关，不影响数据操作。
10. **政府系统自动挡风险**：高企申报系统对自动化操作敏感，批量操作时注意控制节奏，优先手动→自动渐进策略。

---

## 相关技能

- **web-access**：本技能依赖 web-access 的 CDP 浏览器连接能力。在启动本技能前，确保 CDP 代理已连接。
- **officecli**：用于读取 Excel 等结构化数据源的标准化工具（也支持从用户提供的表格文本、JSON 等直接解析）。

---
