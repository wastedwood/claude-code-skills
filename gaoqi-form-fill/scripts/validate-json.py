#!/usr/bin/env python3
"""Validate a Gaoqi internal JSON data package before browser filling."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def number(value: Any) -> float:
    if value is None or value == "":
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return 0.0


def add(issue_list: list[dict[str, str]], level: str, code: str, message: str) -> None:
    issue_list.append({"level": level, "code": code, "message": message})


def duplicate_checks(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    groups = {
        "IP": [item.get("code", "") for item in data.get("intellectualProperties", [])],
        "RD": [item.get("code", "") for item in data.get("rdProjects", [])],
        "PS": [item.get("code", "") for item in data.get("products", [])],
    }
    for name, codes in groups.items():
        counter = Counter(code for code in codes if code)
        for code, count in counter.items():
            if count > 1:
                add(issues, "ERROR", "DUPLICATE_CODE", f"{name} 编号重复: {code} 出现 {count} 次")


def reference_checks(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    ip_codes = {item.get("code") for item in data.get("intellectualProperties", [])}
    rd_codes = {item.get("code") for item in data.get("rdProjects", [])}
    ps_codes = {item.get("code") for item in data.get("products", [])}

    for rd in data.get("rdProjects", []):
        for code in rd.get("relatedIpCodes", []):
            if code not in ip_codes:
                add(issues, "ERROR", "MISSING_IP_REF", f"{rd.get('code')} 引用了不存在的知识产权 {code}")

    for product in data.get("products", []):
        for code in product.get("relatedIpCodes", []):
            if code not in ip_codes:
                add(issues, "ERROR", "MISSING_IP_REF", f"{product.get('code')} 引用了不存在的知识产权 {code}")

    for item in data.get("innovation", {}).get("transformations", []):
        for code in item.get("relatedIpCodes", []):
            if code not in ip_codes:
                add(issues, "ERROR", "MISSING_IP_REF", f"成果转化「{item.get('name')}」引用了不存在的知识产权 {code}")
        for code in item.get("relatedRdCodes", []):
            if code not in rd_codes:
                add(issues, "ERROR", "MISSING_RD_REF", f"成果转化「{item.get('name')}」引用了不存在的 RD {code}")
        for code in item.get("relatedPsCodes", []):
            if code not in ps_codes:
                add(issues, "ERROR", "MISSING_PS_REF", f"成果转化「{item.get('name')}」引用了不存在的 PS {code}")


def fee_checks(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    rd_projects = {item.get("code"): item for item in data.get("rdProjects", [])}
    by_rd_year: dict[tuple[str, int], float] = defaultdict(float)

    for fee in data.get("rdFees", []):
        rd_code = fee.get("rdCode")
        year = int(fee.get("year"))
        if rd_code not in rd_projects:
            add(issues, "ERROR", "MISSING_RD_REF", f"费用表引用了不存在的 RD {rd_code}")
            continue

        internal = fee.get("internal", {})
        external = fee.get("external", {})
        total = (
            number(internal.get("personnel"))
            + number(internal.get("directInput"))
            + number(internal.get("depreciation"))
            + number(internal.get("amortization"))
            + number(internal.get("design"))
            + number(internal.get("equipmentDebugTrial"))
            + number(internal.get("other"))
            + number(external.get("entrusted"))
        )
        by_rd_year[(rd_code, year)] += round(total, 2)

    for rd_code, rd in rd_projects.items():
        spending = rd.get("spendingByYear", {})
        for year_text, expected in spending.items():
            year = int(year_text)
            expected_num = round(number(expected), 2)
            actual_num = round(by_rd_year.get((rd_code, year), 0.0), 2)
            if abs(expected_num - actual_num) > 0.02:
                level = "WARN" if expected_num == 0 or actual_num == 0 else "ERROR"
                add(
                    issues,
                    level,
                    "RD_FEE_MISMATCH",
                    f"{rd_code} {year} 年研发费不一致: RD表 {expected_num:.2f}, 费用明细 {actual_num:.2f}",
                )


def required_text_checks(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    for rd in data.get("rdProjects", []):
        for field, label in [
            ("name", "研发项目名称"),
            ("purposeAndOrganization", "研发目的组织方式"),
            ("coreTechnologyAndInnovation", "核心技术及创新点"),
            ("achievements", "阶段性成果"),
        ]:
            if not str(rd.get(field, "")).strip():
                add(issues, "WARN", "MISSING_TEXT", f"{rd.get('code')} 缺少 {label}")

    for product in data.get("products", []):
        for field, label in [
            ("name", "产品名称"),
            ("keyTechnology", "关键技术"),
            ("competitiveAdvantage", "竞争优势"),
            ("ipSupport", "知识产权支持作用"),
        ]:
            if not str(product.get(field, "")).strip():
                add(issues, "WARN", "MISSING_TEXT", f"{product.get('code')} 缺少 {label}")


def human_resource_checks(data: dict[str, Any], issues: list[dict[str, str]]) -> None:
    hr = data.get("humanResources", {})
    total = number(hr.get("employeeTotal"))
    tech = number(hr.get("techStaffTotal"))
    if total <= 0:
        add(issues, "ERROR", "HR_EMPTY", "人员总数为 0")
    if tech > total:
        add(issues, "ERROR", "HR_INVALID", f"科技人员数 {tech:.0f} 大于职工总数 {total:.0f}")
    if tech <= 0:
        add(issues, "WARN", "HR_NO_TECH_STAFF", "科技人员数为 0，请确认人员表是否标记研发人员")


def validate(data: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    duplicate_checks(data, issues)
    reference_checks(data, issues)
    fee_checks(data, issues)
    required_text_checks(data, issues)
    human_resource_checks(data, issues)
    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python gaoqi-form-fill/scripts/validate-json.py 输入.json", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"找不到输入文件: {input_path}", file=sys.stderr)
        return 2

    data = json.loads(input_path.read_text(encoding="utf-8"))
    issues = validate(data)
    errors = [item for item in issues if item["level"] == "ERROR"]
    warnings = [item for item in issues if item["level"] == "WARN"]

    print(f"预检结果: ERROR {len(errors)} 个, WARN {len(warnings)} 个")
    for item in issues:
        print(f"[{item['level']}] {item['code']}: {item['message']}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

