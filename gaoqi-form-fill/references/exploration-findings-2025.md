# 2025-06-17 全流程探索发现

> 测试账号：青岛迪格环境科技有限公司（统一代码 91370203MA3CP5P7XQ）
> dataInnocomId: c32e931b6a0d11f1b7d7fa163e43a3ec

## 成功验证的表单链路

按依赖顺序：

1. **人力资源情况表** (type=9) → 单记录表单，直接填字段后保存
2. **研究开发活动情况表** (type=2) → 列表+新增，每条 RD 独立保存
3. **费用结构明细表** (type=5) → 按年份分页，关联 RD 项目
4. **高新技术产品情况表** (type=3) → 列表+新增，每条 PS 独立保存
5. **企业创新能力** (type=10) → 4 个子标签页（subType=0~3）
6. **企业标准制定情况** (type=11) → 列表+新增

## 关键发现

### 1. 中文编码
Shell 传中文给 eval 会被乱码破坏。必须用 `--data-binary @file.js` 从 UTF-8 文件读取 JS 代码再 POST。

### 2. iframe 导航
设置 `innocomFrame.src` 要包在 `setTimeout` 里：
```javascript
setTimeout(function() { inf.src = "URL"; }, 100);
```
直接设置会让当前 eval 上下文被销毁，导致 Uncaught 错误。

### 3. 三级级联下拉（技术领域）
onemain → scdmain → thdmain 是 AJAX 异步联动。不能在一个 eval 里设完三级。
正确做法：
```javascript
// Step 1: 设一级，等二级选项加载
setSelectByValue("onemain", "9");
// 等待 1-2 秒
// Step 2: 设二级，等三级选项加载
setSelectByValue("scdmain", "229");
// 等待 1-2 秒
// Step 3: 设三级
setSelectByValue("thdmain", "245");
```

### 4. 费用表计算
仅设 value + dispatchEvent 不会触发合计计算。必须调用页面自身的函数：
```javascript
nbyjkfhj();  // 内部研发费用合计
nwkfhj();    // 内外总合计
```

### 5. 费用表年份
列表页顶部有年份标签（2025/2024/2023），URL 参数 `&year=2023` 切换。
新增页 URL 也要带 year 参数：`addDataEprRdFee.do?...&year=2023`

### 6. 知识产权外部校验
系统连接国家知识产权局数据库校验专利号/软著号。不能用假数据。需要用户提供真实 IP。

### 7. 企业创新能力结构
- subType=0: 知识产权对企业竞争力的作用 → 文本区 Zscqjz
- subType=1: 科技成果转化情况 → 汇总文本区 Kjcgzh + 逐条成果列表
- subType=2: 研究开发与技术创新组织管理情况 → 文本区 Jscxgl
- subType=3: 管理与科技人员情况 → 文本区 Glykj
- 每个子页独立保存（按钮 dataEprCycxSave）

### 8. 成果转化逐条（subType=1 下的子列表）
- "添加"按钮 form action: editDataEprTrans.do?subType=1
- 关联 IP/RD/PS 是多选下拉（Ctrl+左键）
- 转化形式也是多选

### 9. 标准编号不允许空格

### 10. 主要情况表（type=1）
大多数字段是自动计算的（IP数量、人力、研发费用合计、高新收入）：
- IP 数量：getNumber1（I类）/ getNumber2（II类）→ 从知识产权表自动
- 职工/科技：zgzs / humanScience → 从人力资源表自动
- 研发费用总额：从活动情况表自动
- 高新收入：从产品表自动计算
- 手动填的只有：近三年经营数据（净资产/销售/利润）、境内研发费用、企业总收入
