#!/usr/bin/env python3
"""Look up CNIPA publication candidates by application number.

This helper is optional. It requires Playwright in the current Python
environment and never installs dependencies by itself.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Any


OUTPUT_PREFIX = "CNIPA_LOOKUP_JSON:"
CNIPA_URL = "http://epub.cnipa.gov.cn/"
PUBLICATION_RE = re.compile(r"\bCN\d{8,13}[A-Z]\d?\b", re.IGNORECASE)


def normalize_application_number(value: object) -> str:
    text = str(value).strip().upper()
    if text.startswith("CN"):
        text = text[2:]
    return text.replace(".", "").replace('"', "").replace("'", "")


@dataclass
class Candidate:
    publication_no: str
    title: str
    application_no: str
    raw_text: str
    detail_url: str

    def as_dict(self) -> dict[str, str]:
        return {
            "publication_no": self.publication_no,
            "title": self.title,
            "application_no": self.application_no,
            "raw_text": self.raw_text,
            "detail_url": self.detail_url,
        }


def make_report(
    application_no: str,
    *,
    verified: bool,
    publication_no: str = "",
    title: str = "",
    candidates: list[Candidate] | None = None,
    error: str = "",
) -> dict[str, Any]:
    return {
        "source": "cnipa_epub",
        "application_no": application_no,
        "publication_no": publication_no,
        "title": title,
        "verified": verified,
        "candidates": [candidate.as_dict() for candidate in candidates or []],
        "error": error,
    }


def emit(report: dict[str, Any]) -> None:
    print(OUTPUT_PREFIX + json.dumps(report, ensure_ascii=False, separators=(",", ":")))


def compact_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def infer_title(text: str, publication_no: str) -> str:
    compact = compact_text(text)
    if not compact:
        return ""
    if publication_no and publication_no in compact:
        before = compact.split(publication_no, 1)[0].strip(" -:：|")
        if 2 <= len(before) <= 120:
            return before
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        if publication_no not in line and 2 <= len(line) <= 120:
            return line
    return ""


def collect_candidates(page: Any, application_no: str) -> list[Candidate]:
    rows: list[dict[str, str]] = page.evaluate(
        """() => {
            const nodes = Array.from(document.querySelectorAll(
                "tr, .result, .result-item, .search-result, .patent, li, article, div"
            ));
            const seen = new Set();
            const rows = [];
            for (const node of nodes) {
                const text = (node.innerText || "").trim();
                if (!text || text.length < 20 || seen.has(text)) continue;
                seen.add(text);
                const link = node.querySelector("a[href]");
                rows.push({
                    text,
                    href: link ? new URL(link.getAttribute("href"), location.href).href : ""
                });
            }
            return rows;
        }"""
    )

    normalized = normalize_application_number(application_no)
    candidates: list[Candidate] = []
    for row in rows:
        text = row.get("text", "")
        if normalized not in normalize_application_number(text):
            continue
        matches = PUBLICATION_RE.findall(text)
        if not matches:
            continue
        publication_no = matches[0].upper()
        candidates.append(
            Candidate(
                publication_no=publication_no,
                title=infer_title(text, publication_no),
                application_no=application_no,
                raw_text=compact_text(text),
                detail_url=row.get("href", ""),
            )
        )

    unique: dict[str, Candidate] = {}
    for candidate in candidates:
        unique.setdefault(candidate.publication_no, candidate)
    return list(unique.values())


def lookup(application_no: str, *, headless: bool, timeout_ms: int) -> dict[str, Any]:
    normalized = normalize_application_number(application_no)
    if not re.fullmatch(r"\d{5,}[A-Z0-9]", normalized):
        raise ValueError(f"Invalid application number: {application_no!r}")

    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "Playwright is not available in this Python environment; "
            "install or enable Playwright before using CNIPA browser lookup"
        ) from exc

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        try:
            page = browser.new_page(
                locale="zh-CN",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page.set_default_timeout(timeout_ms)
            page.goto(CNIPA_URL, wait_until="domcontentloaded")

            # CNIPA may run JavaScript checks before the search form is usable.
            page.wait_for_load_state("networkidle", timeout=timeout_ms)
            search_box = page.locator("#searchStr")
            search_box.wait_for(state="visible", timeout=timeout_ms)
            page.wait_for_timeout(800)

            search_box.fill(normalized)
            form = page.locator("#indexForm")
            try:
                with page.expect_navigation(wait_until="domcontentloaded", timeout=timeout_ms):
                    form.evaluate("form => form.submit()")
            except PlaywrightTimeoutError:
                form.evaluate("form => form.submit()")

            try:
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
            except PlaywrightTimeoutError:
                pass
            page.wait_for_timeout(1200)

            candidates = collect_candidates(page, normalized)
        finally:
            browser.close()

    verified = len(candidates) == 1
    return make_report(
        normalized,
        verified=verified,
        publication_no=candidates[0].publication_no if verified else "",
        title=candidates[0].title if verified else "",
        candidates=candidates,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("application_no", help="CN application number, with or without CN/dot")
    parser.add_argument("--headed", action="store_true", help="Show the browser window")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    args = parser.parse_args()

    normalized = normalize_application_number(args.application_no)
    try:
        report = lookup(
            normalized,
            headless=not args.headed,
            timeout_ms=args.timeout_ms,
        )
    except Exception as exc:
        emit(make_report(normalized, verified=False, error=str(exc)))
        return 1

    emit(report)
    return 0 if report["verified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
