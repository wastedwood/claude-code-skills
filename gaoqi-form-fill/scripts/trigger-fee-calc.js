// ========================================
// 费用表计算函数
// 必须在费用表编辑页的页面上下文中执行
// ========================================

/**
 * 填写费用明细并触发计算
 *
 * @param {Document} doc - 页面 document（直接渲染时用 document，iframe 内用 idoc）
 * @param {Object} fields - 费用字段对象
 * @param {string} fields.ryrg - 人员人工费用
 * @param {string} fields.zjtr - 直接投入费用
 * @param {string} fields.zjfy - 折旧摊销
 * @param {string} fields.wxzc - 无形资产摊销
 * @param {string} fields.sjf - 设计费
 * @param {string} fields.sbtsf - 装备调试费
 * @param {string} fields.qtfy - 其他费用
 * @param {string} fields.wtwb - 委外研发费用（可选）
 * @param {string} fields.pjnwb - 境内委外费用（可选）
 * @returns {Object} { internalTotal, grandTotal }
 */
function fillFeeAndCalc(doc, fields) {
  var r = {};

  // 1. 填入各项费用
  if (fields.ryrg) setVal(doc, "ryrg", fields.ryrg);
  if (fields.zjtr) setVal(doc, "zjtr", fields.zjtr);
  if (fields.zjfy) setVal(doc, "zjfy", fields.zjfy);
  if (fields.wxzc) setVal(doc, "wxzc", fields.wxzc);
  if (fields.sjf)  setVal(doc, "sjf", fields.sjf);
  if (fields.sbtsf) setVal(doc, "sbtsf", fields.sbtsf);
  if (fields.qtfy) setVal(doc, "qtfy", fields.qtfy);

  // 2. 触发内部合计计算
  if (typeof nbyjkfhj === "function") {
    nbyjkfhj();
    r.internalCalc = "nbyjkfhj called";
  } else {
    r.internalCalc = "nbyjkfhj not found";
  }

  // 3. 读取内部合计
  var internalEl = doc.getElementById("nbyjkftr");
  r.internalTotal = internalEl ? internalEl.value : "N/A";

  // 4. 填入委外费用
  if (fields.wtwb) setVal(doc, "wtwbyjkftr", fields.wtwb);
  if (fields.pjnwb) setVal(doc, "pjnwbtrhj", fields.pjnwb);

  // 5. 触发内外总合计
  if (typeof nwkfhj === "function") {
    nwkfhj();
    r.grandCalc = "nwkfhj called";
  }

  // 6. 读取总合计
  var grandEl = doc.getElementById("nwhj");
  r.grandTotal = grandEl ? grandEl.value : "N/A";

  return r;
}

/**
 * 读取费用表合计值（不填数据，只校验）
 */
function readFeeTotals(doc) {
  return {
    internal: (doc.getElementById("nbyjkftr") || {}).value || "N/A",
    grand: (doc.getElementById("nwhj") || {}).value || "N/A"
  };
}

// ----- 依赖的通用函数 -----
function setVal(doc, id, val) {
  var el = doc.getElementById(id);
  if (!el) return;
  el.value = val;
  ["input", "change", "blur"].forEach(function(evt) {
    el.dispatchEvent(new Event(evt, { bubbles: true }));
  });
}
