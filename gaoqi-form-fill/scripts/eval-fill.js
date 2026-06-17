// ========================================
// 通用填值工具函数
// 每次操作前先 inPage 到对应 iframe context
// ========================================

/**
 * 填单值字段（input/textarea），触发 input/change/blur 事件
 * @param {Document} doc - 目标页面的 document
 * @param {string} id - 字段 ID
 * @param {string} val - 要填的值
 */
function setVal(doc, id, val) {
  var el = doc.getElementById(id);
  if (!el) return { id: id, ok: false, reason: "not found" };
  el.value = val;
  ["input", "change", "blur"].forEach(function(evt) {
    el.dispatchEvent(new Event(evt, { bubbles: true }));
  });
  return { id: id, ok: true, value: el.value };
}

/**
 * 设置下拉选择框（按 value）
 * @param {Document} doc - 目标页面的 document
 * @param {string} id - select 元素 ID
 * @param {string} val - 要选中的 value
 */
function setSelectByValue(doc, id, val) {
  var el = doc.getElementById(id);
  if (!el) return { id: id, ok: false, reason: "not found or not select" };
  if (el.tagName !== "SELECT") return { id: id, ok: false, reason: "not a SELECT" };
  el.value = val;
  el.dispatchEvent(new Event("change", { bubbles: true }));
  return { id: id, ok: true, value: el.value };
}

/**
 * 多选下拉框按文本匹配选中
 * @param {Document} doc - 目标页面的 document
 * @param {string} id - select-multiple 元素 ID
 * @param {string} text - 要匹配的文本片段
 */
function selectMultiContains(doc, id, text) {
  var el = doc.getElementById(id);
  if (!el) return { id: id, ok: false, reason: "not found" };
  if (el.tagName !== "SELECT") return { id: id, ok: false, reason: "not a SELECT" };
  var chosen = [];
  for (var i = 0; i < el.options.length; i++) {
    var t = (el.options[i].text || "").trim();
    el.options[i].selected = t.indexOf(text) >= 0;
    if (el.options[i].selected) chosen.push(t);
  }
  el.dispatchEvent(new Event("change", { bubbles: true }));
  return { id: id, ok: chosen.length > 0, chosen: chosen };
}

/**
 * 选中 radio 按钮
 * @param {Document} doc - 目标页面的 document
 * @param {string} name - radio 组 name 属性
 * @param {string} val - 要选中的值
 */
function clickRadio(doc, name, val) {
  var radios = doc.querySelectorAll("input[name='" + name + "']");
  var found = 0;
  radios.forEach(function(r) {
    if (r.value === val) {
      r.checked = true;
      r.dispatchEvent(new Event("change", { bubbles: true }));
      found++;
    }
  });
  return { name: name, value: val, found: found };
}

/**
 * 读取字段值（调试用）
 */
function getVal(doc, id) {
  var el = doc.getElementById(id);
  return el ? el.value : null;
}

/**
 * 穿透 iframe 获取 innocomFrame 的 document
 * 适用于从主页面穿透两层 iframe 的场景
 */
function getInnocomDoc() {
  var mf = document.getElementById("mainFrame");
  if (!mf) return null;
  var md = mf.contentDocument || mf.contentWindow.document;
  if (!md) return null;
  var inf = md.getElementById("innocomFrame");
  if (!inf) return null;
  var idoc = inf.contentDocument || inf.contentWindow.document;
  return idoc;
}
