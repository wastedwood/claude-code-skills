#!/usr/bin/env python3
"""Download patent PDFs from a JSON manifest and validate the deliverable."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


REQUIRED_FIELDS = {
    "patent_no",
    "application_no",
    "publication_no",
    "title",
    "pdf_url",
}


def normalize_application_number(value: object) -> str:
    text = str(value).strip().upper()
    if text.startswith("CN"):
        text = text[2:]
    return text.replace(".", "")


def format_application_number(value: object) -> str:
    normalized = normalize_application_number(value)
    if len(normalized) < 2:
        raise ValueError(f"Invalid application number: {value!r}")
    return f"CN{normalized[:-1]}.{normalized[-1]}"


def load_manifest(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list) or not data:
        raise ValueError("Manifest must be a non-empty JSON array")

    rows: list[dict[str, str]] = []
    for index, raw in enumerate(data, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"Manifest row {index} is not an object")
        missing = REQUIRED_FIELDS - raw.keys()
        if missing:
            raise ValueError(
                f"Manifest row {index} is missing: {', '.join(sorted(missing))}"
            )
        row = {key: str(raw[key]).strip() for key in REQUIRED_FIELDS}
        if any(not row[key] for key in REQUIRED_FIELDS):
            raise ValueError(f"Manifest row {index} contains an empty required field")

        publication = row["publication_no"].upper()
        if not re.fullmatch(r"CN\d{9}[A-Z]", publication):
            raise ValueError(
                f"Manifest row {index} has invalid publication number: {publication}"
            )
        if publication not in row["pdf_url"].upper():
            raise ValueError(
                f"Manifest row {index}: PDF URL does not contain {publication}"
            )
        if normalize_application_number(
            row["application_no"]
        ) != normalize_application_number(row["patent_no"]):
            raise ValueError(
                f"Manifest row {index}: patent_no and application_no do not match"
            )
        row["publication_no"] = publication
        rows.append(row)

    names = [row["patent_no"] for row in rows]
    publications = [row["publication_no"] for row in rows]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate patent_no values in manifest")
    if len(publications) != len(set(publications)):
        raise ValueError("Duplicate publication_no values in manifest")
    return rows


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 patent-pdf-batch-download"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        content_type = response.headers.get("Content-Type", "")
        data = response.read()
    if not data.startswith(b"%PDF-"):
        raise ValueError(
            f"Downloaded content is not a PDF ({content_type or 'unknown type'})"
        )
    destination.write_bytes(data)


def page_count(path: Path) -> int:
    try:
        from pypdf import PdfReader
    except ImportError:
        pdfinfo = shutil.which("pdfinfo")
        if not pdfinfo:
            raise RuntimeError(
                "Page-count validation requires pypdf or the pdfinfo executable; "
                "neither is available"
            )
        completed = subprocess.run(
            [pdfinfo, str(path)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        match = re.search(r"^Pages:\s+(\d+)\s*$", completed.stdout, re.MULTILINE)
        if not match:
            raise RuntimeError(f"pdfinfo did not report a page count for {path.name}")
        return int(match.group(1))
    return len(PdfReader(str(path)).pages)


def run(manifest_path: Path, output_dir: Path) -> dict[str, object]:
    rows = load_manifest(manifest_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    expected = {f"{row['patent_no']}.pdf" for row in rows}
    existing = {path.name for path in output_dir.glob("*.pdf")}
    unexpected = sorted(existing - expected)
    if unexpected:
        raise ValueError(
            "Output directory already contains unrelated PDFs: "
            + ", ".join(unexpected)
        )

    results: list[dict[str, object]] = []
    for row in rows:
        destination = output_dir / f"{row['patent_no']}.pdf"
        if destination.exists():
            if destination.read_bytes()[:5] != b"%PDF-":
                raise ValueError(f"Existing file is not a PDF: {destination.name}")
        else:
            download(row["pdf_url"], destination)

        pages = page_count(destination)
        if pages < 1:
            raise ValueError(f"PDF has no pages: {destination.name}")
        results.append(
            {
                "file": destination.name,
                "publication_no": row["publication_no"],
                "bytes": destination.stat().st_size,
                "pages": pages,
            }
        )

    actual = {path.name for path in output_dir.glob("*.pdf")}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise ValueError(f"Filename mismatch; missing={missing}, extra={extra}")

    return {
        "output_dir": str(output_dir.resolve()),
        "count": len(results),
        "total_pages": sum(int(row["pages"]) for row in results),
        "min_pages": min(int(row["pages"]) for row in results),
        "max_pages": max(int(row["pages"]) for row in results),
        "files": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument("output_dir", nargs="?", type=Path)
    parser.add_argument(
        "--format-application",
        help="Print a normalized CN application number and exit",
    )
    args = parser.parse_args()

    if args.format_application:
        print(format_application_number(args.format_application))
        return 0
    if args.manifest is None or args.output_dir is None:
        parser.error("manifest and output_dir are required")

    try:
        report = run(args.manifest, args.output_dir)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
