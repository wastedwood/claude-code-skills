// ========================================
// 三级技术领域级联操作
//
// 技术领域的 onemain→scdmain→thdmain 是 AJAX 异步联动
// 必须分步操作，每步间隔等待选项加载
// ========================================

/**
 * 设置三级技术领域（完整流程）
 *
 * 调用方式：分三步执行，每步间隔 1.5~2 秒
 *
 * 示例：
 *   setDomainLevel1(idoc, "onemain", "9");   // 资源与环境
 *   // 等待 2 秒
 *   setDomainLevel2(idoc, "scdmain", "229");  // 大气污染控制技术
 *   // 等待 2 秒
 *   setDomainLevel3(idoc, "thdmain", "245");  // 工业有害废气控制技术
 */

function setDomainLevel1(doc, selectId, value) {
  var el = doc.getElementById(selectId);
  if (!el) return { ok: false, reason: "level1 not found" };
  el.value = value;
  el.dispatchEvent(new Event("change", { bubbles: true }));
  return { ok: true, level: 1, value: value };
}

function setDomainLevel2(doc, selectId, value) {
  var el = doc.getElementById(selectId);
  if (!el) return { ok: false, reason: "level2 not found" };
  // 等待二级选项加载完成（至少有一个非空选项且不是"--请选择--"之外无选项）
  el.value = value;
  el.dispatchEvent(new Event("change", { bubbles: true }));
  return { ok: true, level: 2, value: value };
}

function setDomainLevel3(doc, selectId, value) {
  var el = doc.getElementById(selectId);
  if (!el) return { ok: false, reason: "level3 not found" };
  el.value = value;
  el.dispatchEvent(new Event("change", { bubbles: true }));
  return { ok: true, level: 3, value: value };
}

/**
 * 读取当前选中的完整领域路径
 * 返回如 "资源与环境/大气污染控制技术/工业有害废气控制技术"
 */
function getDomainPath(doc) {
  function getSelectedText(id) {
    var el = doc.getElementById(id);
    if (!el || !el.selectedOptions || !el.selectedOptions[0]) return "";
    return (el.selectedOptions[0].text || "").trim();
  }
  var l1 = getSelectedText("onemain");
  var l2 = getSelectedText("scdmain");
  var l3 = getSelectedText("thdmain");
  return [l1, l2, l3].filter(Boolean).join("/");
}
