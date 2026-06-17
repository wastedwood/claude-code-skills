# 浏览器操作通用知识

> 基于 2025-06-17 全流程探索验证

## 1. 中文编码（必须注意！）

**Shell 传中文给 eval 会被乱码破坏。**

```bash
# ❌ 错误：中文会乱码
curl -s -X POST "http://localhost:3456/eval?target=ID" -d 'setVal("name", "测试数据")'

# ✅ 正确：写 UTF-8 文件后用 --data-binary
curl -s -X POST --data-binary @file.js "http://localhost:3456/eval?target=ID"
```

每次填包含中文的数据时，把 JavaScript 写成文件再用 `--data-binary` 传。

## 2. iframe 导航

**直接设置 `inf.src` 会让当前 eval 上下文被销毁（Uncaught 错误）。**

```javascript
// ❌ 错误：eval 会崩溃
inf.src = "https://...";

// ✅ 正确：用 setTimeout 让 eval 先返回
setTimeout(function() {
  var mf = document.getElementById("mainFrame");
  var md = mf.contentDocument || mf.contentWindow.document;
  var inf = md.getElementById("innocomFrame");
  inf.src = "https://...";
}, 100);
```

或分开两步：
```bash
curl -s -X POST ... -d 'setTimeout(function() { inf.src = "URL"; }, 100); "ok"'
sleep 4   # 等待页面加载
curl -s -X POST ... -d '...后续操作...'
```

## 3. 三级技术领域级联

技术领域的 `onemain→scdmain→thdmain` 是 AJAX 异步联动，**不能在一个 eval 里设完三级**。

```javascript
// Step 1: 设一级
el = idoc.getElementById("onemain");
el.value = "9";  // 资源与环境
el.dispatchEvent(new Event("change", {bubbles:true}));
// 等待 1-2 秒让二级选项加载

// Step 2: 设二级
el = idoc.getElementById("scdmain");
el.value = "229";  // 大气污染控制技术
el.dispatchEvent(new Event("change", {bubbles:true}));
// 等待 1-2 秒让三级选项加载

// Step 3: 设三级
el = idoc.getElementById("thdmain");
el.value = "245";  // 工业有害废气控制技术
el.dispatchEvent(new Event("change", {bubbles:true}));
```

## 4. 费用表自动计算

**仅设 value + dispatchEvent 不会触发费用表的合计计算。**

必须调用页面本身的 JavaScript 函数：
```javascript
// 填写完所有费用明细后：
nbyjkfhj();  // 内部研究开发费用合计（人员+材料+折旧+...）
nwkfhj();    // 内外总合计（内部 + 委外）
```

这两个函数存在于费用表编辑页的全局作用域中。

## 5. 费用表年份

费用表按年份分页，通过 URL 参数 `&year=2023` 切换。

列表页顶部有年份标签（如"2025 2024 2023"），点击后 URL 变成：
```
initDataInnocom.do?type=5&dataInnocomId=xxx&year=2023
```

**新增/编辑页也必须在 URL 中指定 year 参数**，否则项目编号下拉为空。

## 6. 保存后等待

点击保存按钮后：
1. 表单提交 → 服务器处理 → 返回列表页
2. 如果还停在编辑页，说明：
   - 有验证弹窗（检查 dialog）
   - 或 JS 验证不通过
   - 或表单已提交但页面未刷新（try `form.submit()` 代替按钮点击）
3. 成功标志：页面回到列表页，看到新增/修改的记录

## 7. web-access CDP Proxy API 速查

```bash
# 列出标签页
curl -s http://localhost:3456/targets

# 创建新标签页
curl -s -X POST --data-raw 'URL' http://localhost:3456/new

# 执行 JS 表达式
curl -s -X POST "http://localhost:3456/eval?target=ID" -d 'JS_CODE'  

# 用文件传 JS（避免中文乱码）
curl -s -X POST --data-binary @file.js "http://localhost:3456/eval?target=ID"

# 导航主页面
curl -s -X POST --data-raw 'URL' "http://localhost:3456/navigate?target=ID"

# 截图
curl -s "http://localhost:3456/screenshot?target=ID&file=/tmp/shot.png"
```
