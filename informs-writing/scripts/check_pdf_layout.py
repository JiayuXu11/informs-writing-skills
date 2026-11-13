#!/usr/bin/env python3
"""Compiled-PDF visual layout, glyph integrity, and typography auditor.

Inspects compiled LaTeX PDFs (and companion .log files) using PyMuPDF (fitz)
with a pypdf text-only fallback when PyMuPDF is absent. Flags:
  - Garbled replacement/control/PUA/mojibake characters (GarbledText)
  - Unresolved LaTeX references/citations: ?? or [?] (UnresolvedRef)
  - Overlapping text lines or horizontal column collisions (TextOverlap)
  - Blank pages and large mid-page whitespace bands (BlankPage, MidPageGap)
  - Underfilled interior pages with large bottom voids (UnderfilledPage)
  - Margin protrusions past safe reading margins (MarginProtrusion)
  - Companion .log errors: Missing character, Overfull \\hbox, Underfull \\vbox
Optionally renders PNG snapshots of flagged pages (`--render-flagged <dir>`)
for direct visual inspection.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class PdfFinding(NamedTuple):
    severity: str  # ERROR | WARN
    category: str
    page: int  # 1-based page number, or 0 for global .log findings
    message: str


MOJIBAKE_RE = re.compile(r"(?:Ã©|Ã¨|Ã¼|Ã¶|Ã¤|â€”|â€“|â€œ|â€\x9d|â€™|â€˜|Â\xa0)")
UNRESOLVED_REF_RE = re.compile(
    r"(?<![A-Za-z0-9_?])\?\?(?![A-Za-z0-9_?])|\[\s*\?\s*\]|\(\s*\?\s*\)"
)
MAJOR_TRANSITION_RE = re.compile(
    r"^\s*(?:Online\s+Appendix|Electronic\s+Companion|E-Companion|EC\.\d|"
    r"References|Bibliography)\b",
    re.IGNORECASE | re.MULTILINE,
)

LOG_MISSING_CHAR_RE = re.compile(r"^Missing character:\s*(.+)$", re.MULTILINE)
LOG_OVERFULL_HBOX_RE = re.compile(
    r"Overfull \\hbox \((\d+(?:\.\d+)?)pt too wide\).*?(?:lines?\s+(\d+(?:--\d+)?))?",
    re.IGNORECASE,
)
LOG_UNDERFULL_VBOX_RE = re.compile(
    r"Underfull \\vbox \(badness 10000\).*?(?:lines?\s+(\d+(?:--\d+)?))?",
    re.IGNORECASE,
)
LOG_UNDEF_REF_RE = re.compile(
    r"LaTeX Warning:\s*(?:Reference|Citation)\s+`([^']+)'\s+(?:on page (\d+)\s+)?undefined",
    re.IGNORECASE,
)
LOG_OVERSIZED_FLOAT_RE = re.compile(
    r"LaTeX Warning:\s*Float too large for page by (\d+(?:\.\d+)?)pt",
    re.IGNORECASE,
)


def parse_tex_log(log_path: Path) -> list[PdfFinding]:
    """Extract critical typography and glyph warnings from a LaTeX .log file."""
    findings: list[PdfFinding] = []
    if not log_path.is_file():
        return findings

    text = log_path.read_text(encoding="utf-8", errors="replace")

    seen_missing: set[str] = set()
    for m in LOG_MISSING_CHAR_RE.finditer(text):
        msg = m.group(1).strip()
        if msg not in seen_missing:
            seen_missing.add(msg)
            findings.append(
                PdfFinding("ERROR", "MissingGlyph", 0, f".log: Missing character: {msg}")
            )

    for m in LOG_UNDEF_REF_RE.finditer(text):
        key = m.group(1)
        pg = int(m.group(2)) if m.group(2) else 0
        findings.append(
            PdfFinding("ERROR", "UnresolvedRef", pg, f".log: Undefined reference/citation '{key}'.")
        )

    for m in LOG_OVERFULL_HBOX_RE.finditer(text):
        pts = float(m.group(1))
        ln = f" (lines {m.group(2)})" if m.group(2) else ""
        if pts >= 15.0:
            findings.append(
                PdfFinding(
                    "ERROR",
                    "OverfullHbox",
                    0,
                    f".log: Severe Overfull \\hbox ({pts:.1f}pt too wide){ln}; split equation/table or load microtype.",
                )
            )
        elif pts >= 3.0:
            findings.append(
                PdfFinding(
                    "WARN",
                    "OverfullHbox",
                    0,
                    f".log: Overfull \\hbox ({pts:.1f}pt too wide){ln}.",
                )
            )

    underfull_hits = list(LOG_UNDERFULL_VBOX_RE.finditer(text))
    if underfull_hits:
        findings.append(
            PdfFinding(
                "WARN",
                "UnderfullVbox",
                0,
                f".log: {len(underfull_hits)} 'Underfull \\vbox (badness 10000)' warning(s); check for stretched page gaps.",
            )
        )

    for m in LOG_OVERSIZED_FLOAT_RE.finditer(text):
        findings.append(
            PdfFinding(
                "WARN",
                "OversizedFloat",
                0,
                f".log: Float too large for page by {m.group(1)}pt; trim figure height or table padding.",
            )
        )
    return findings


def _check_text_anomalies(page_text: str, page_num: int) -> list[PdfFinding]:
    findings: list[PdfFinding] = []
    if "\ufffd" in page_text:
        cnt = page_text.count("\ufffd")
        findings.append(
            PdfFinding(
                "ERROR",
                "GarbledText",
                page_num,
                f"Detected {cnt} Unicode replacement character(s) (U+FFFD).",
            )
        )
    ctrl_matches = re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", page_text)
    if ctrl_matches:
        findings.append(
            PdfFinding(
                "ERROR",
                "GarbledText",
                page_num,
                f"Detected {len(ctrl_matches)} unexpected control character(s) in extracted text.",
            )
        )
    pua_matches = re.findall(r"[\ue000-\uf8ff]", page_text)
    if len(pua_matches) >= 3:
        findings.append(
            PdfFinding(
                "ERROR",
                "GarbledText",
                page_num,
                f"Detected {len(pua_matches)} Private-Use-Area glyph(s) (possible missing font encoding).",
            )
        )
    if MOJIBAKE_RE.search(page_text):
        findings.append(
            PdfFinding(
                "ERROR",
                "GarbledText",
                page_num,
                "Detected UTF-8/Latin-1 mojibake sequences; check fontenc/input encoding.",
            )
        )
    for m in UNRESOLVED_REF_RE.finditer(page_text):
        findings.append(
            PdfFinding(
                "ERROR",
                "UnresolvedRef",
                page_num,
                f"Unresolved LaTeX reference/citation marker '{m.group(0)}' rendered on page.",
            )
        )
    return findings


def _intersect_box(b1: tuple[float, float, float, float], b2: tuple[float, float, float, float]) -> tuple[float, float]:
    iw = min(b1[2], b2[2]) - max(b1[0], b2[0])
    ih = min(b1[3], b2[3]) - max(b1[1], b2[1])
    return iw, ih


def _check_fitz_overlaps_and_margins(
    page: object,
    page_num: int,
) -> list[PdfFinding]:
    findings: list[PdfFinding] = []
    page_w = float(page.rect.width)
    page_h = float(page.rect.height)
    tdict = page.get_text("dict")

    # Collect readable prose/table line boxes (ignore tiny 1-2 char math sub/superscripts)
    lines_info: list[tuple[tuple[float, float, float, float], str, float]] = []
    span_items: list[tuple[tuple[float, float, float, float], str, float, int]] = []

    line_uid = 0
    for block in tdict.get("blocks", []):
        if block.get("type") != 0:
            continue
        for ln in block.get("lines", []):
            line_uid += 1
            valid_spans = []
            max_size = 0.0
            texts = []
            for sp in ln.get("spans", []):
                stxt = sp.get("text", "")
                clean = stxt.strip()
                sz = float(sp.get("size", 0.0))
                sb = tuple(float(v) for v in sp.get("bbox", (0, 0, 0, 0)))
                if not clean:
                    continue
                texts.append(stxt)
                if sz > max_size:
                    max_size = sz
                if len(clean) >= 3 and sz >= 7.5 and (sb[2] - sb[0]) > 2.0 and (sb[3] - sb[1]) > 2.0:
                    valid_spans.append((sb, clean, sz, line_uid))

            joined = re.sub(r"\s+", " ", "".join(texts)).strip()
            lb = tuple(float(v) for v in ln.get("bbox", (0, 0, 0, 0)))
            if len(joined) >= 3 and max_size >= 7.5 and (lb[2] - lb[0]) > 4.0:
                lines_info.append((lb, joined, max_size))
            span_items.extend(valid_spans)

    # 1. Vertical/bounding-box line collision check
    overlap_reported = False
    for i in range(len(lines_info)):
        b1, t1, _ = lines_info[i]
        h1 = b1[3] - b1[1]
        for j in range(i + 1, len(lines_info)):
            b2, t2, _ = lines_info[j]
            if b2[1] >= b1[3] and b1[3] <= b2[1]:
                continue
            iw, ih = _intersect_box(b1, b2)
            h2 = b2[3] - b2[1]
            if iw > 8.0 and ih > max(3.5, 0.35 * min(h1, h2)):
                findings.append(
                    PdfFinding(
                        "ERROR",
                        "TextOverlap",
                        page_num,
                        f"Overlapping lines detected ('{t1[:28]}' vs '{t2[:28]}').",
                    )
                )
                overlap_reported = True
                break
        if overlap_reported:
            break

    # 2. Same-line horizontal span collision (e.g., cramped table cells)
    if not overlap_reported:
        for i in range(len(span_items)):
            sb1, st1, _, lid1 = span_items[i]
            for j in range(i + 1, len(span_items)):
                sb2, st2, _, lid2 = span_items[j]
                if lid1 != lid2:
                    continue
                if abs(sb1[1] - sb2[1]) < 3.0:
                    iw, ih = _intersect_box(sb1, sb2)
                    if iw > 6.0 and ih > 3.0:
                        findings.append(
                            PdfFinding(
                                "ERROR",
                                "TextOverlap",
                                page_num,
                                f"Horizontal text collision on line ('{st1[:24]}' vs '{st2[:24]}').",
                            )
                        )
                        overlap_reported = True
                        break
            if overlap_reported:
                break

    # 3. Left / right margin protrusion check (portrait body region)
    min_left = page_w
    min_right_gap = page_w
    worst_text = ""
    for lb, txt, _ in lines_info:
        if lb[1] <= 0.09 * page_h or lb[3] >= 0.90 * page_h:
            continue
        left_gap = lb[0]
        right_gap = page_w - lb[2]
        if left_gap < min_left:
            min_left = left_gap
            worst_text = txt[:28]
        if right_gap < min_right_gap:
            min_right_gap = right_gap
            worst_text = txt[:28]

    min_edge_gap = min(min_left, min_right_gap)
    if lines_info:
        if min_edge_gap < 16.0:
            findings.append(
                PdfFinding(
                    "ERROR",
                    "MarginProtrusion",
                    page_num,
                    f"Content within {min_edge_gap:.1f}pt of page edge ('{worst_text}'); severe margin overflow.",
                )
            )
        elif min_edge_gap < 26.0:
            findings.append(
                PdfFinding(
                    "WARN",
                    "MarginProtrusion",
                    page_num,
                    f"Content only {min_edge_gap:.1f}pt from page edge ('{worst_text}'); check narrow margin.",
                )
            )

    return findings


def _check_fitz_whitespace(
    page: object,
    page_num: int,
    total_pages: int,
    next_page_text: str,
) -> list[PdfFinding]:
    """Scan 72 DPI grayscale raster rows to catch blank pages & large voids."""
    findings: list[PdfFinding] = []
    import fitz

    pix = page.get_pixmap(dpi=72, colorspace=fitz.csGRAY, alpha=False)
    w = int(pix.width)
    h = int(pix.height)
    if w <= 0 or h <= 0:
        return findings

    samples = pix.samples
    row_start = int(0.10 * h)
    row_end = int(0.88 * h)
    col_start = int(0.08 * w)
    col_end = int(0.92 * w)
    body_rows = max(1, row_end - row_start)

    inked_rows: list[int] = []
    for y in range(row_start, row_end):
        off = y * w
        row_slice = samples[off + col_start : off + col_end]
        if min(row_slice) >= 242:
            continue
        if sum(1 for px in row_slice if px < 242) >= 2:
            inked_rows.append(y)

    if len(inked_rows) / body_rows < 0.01:
        findings.append(
            PdfFinding(
                "ERROR",
                "BlankPage",
                page_num,
                "Rendered page body has < 1% vertical ink coverage (blank or near-blank page).",
            )
        )
        return findings

    first_y = inked_rows[0]
    last_y = inked_rows[-1]

    # Contiguous internal blank bands strictly between first and last inked rows
    max_gap = 0
    for i in range(len(inked_rows) - 1):
        gap = inked_rows[i + 1] - inked_rows[i] - 1
        if gap > max_gap:
            max_gap = gap

    gap_ratio = max_gap / h
    if gap_ratio > 0.32:
        findings.append(
            PdfFinding(
                "ERROR",
                "MidPageGap",
                page_num,
                f"Giant mid-page whitespace gap ({gap_ratio * 100:.0f}% of page height); inspect float placement or display breaks.",
            )
        )
    elif gap_ratio > 0.22:
        findings.append(
            PdfFinding(
                "WARN",
                "MidPageGap",
                page_num,
                f"Large mid-page whitespace gap ({gap_ratio * 100:.0f}% of page height).",
            )
        )

    # Interior underfilled page check (exclude final page and pages right before Appendix/Refs)
    if 1 < page_num < total_pages and not MAJOR_TRANSITION_RE.search(next_page_text or ""):
        bottom_blank_ratio = (row_end - last_y) / h
        if first_y < int(0.35 * h) and bottom_blank_ratio > 0.40:
            findings.append(
                PdfFinding(
                    "WARN",
                    "UnderfilledPage",
                    page_num,
                    f"Interior page ends early with {bottom_blank_ratio * 100:.0f}% trailing blank body space (check restrictive [h]/[H] float or \\clearpage).",
                )
            )

    return findings


INTRO_HEAD_RE = re.compile(r"^\s*(?:1\.?\s+)?Introduction\s*$", re.IGNORECASE)
SEC2_HEAD_RE = re.compile(r"^\s*2\.?\s+[A-Z][A-Za-z0-9\s,&:-]{2,60}$")


def _check_intro_page_span(doc: object) -> list[PdfFinding]:
    """Warn if compiled Introduction spans more than 3 pages."""
    findings: list[PdfFinding] = []
    sec1_pos: tuple[int, float] | None = None
    sec2_pos: tuple[int, float] | None = None

    for idx in range(len(doc)):
        page = doc[idx]
        ph = max(1.0, float(page.rect.height))
        tdict = page.get_text("dict")
        for block in tdict.get("blocks", []):
            if block.get("type") != 0:
                continue
            for ln in block.get("lines", []):
                txt = re.sub(r"\s+", " ", "".join(sp.get("text", "") for sp in ln.get("spans", []))).strip()
                if not txt:
                    continue
                y_rel = float(ln.get("bbox", (0, 0, 0, 0))[1]) / ph
                if sec1_pos is None and INTRO_HEAD_RE.match(txt):
                    sec1_pos = (idx, y_rel)
                elif sec1_pos is not None and SEC2_HEAD_RE.match(txt):
                    if idx > sec1_pos[0] or y_rel > sec1_pos[1]:
                        sec2_pos = (idx, y_rel)
                        break
            if sec2_pos is not None:
                break
        if sec2_pos is not None:
            break

    if sec1_pos is not None and sec2_pos is not None:
        span_pages = (sec2_pos[0] - sec1_pos[0]) + (sec2_pos[1] - sec1_pos[1])
        if span_pages > 3.05:
            findings.append(
                PdfFinding(
                    "WARN",
                    "IntroPageCap",
                    sec2_pos[0] + 1,
                    f"Compiled Introduction spans {span_pages:.1f} pages (keep Introduction <= 3.0 pages).",
                )
            )
    return findings


def audit_pdf(
    pdf_path: Path,
    log_path: Path | None = None,
    render_dir: Path | None = None,
    auto_log: bool = True,
) -> tuple[list[PdfFinding], list[Path]]:
    """Audit a compiled PDF (and optional .log) and optionally render flagged pages."""
    findings: list[PdfFinding] = []
    rendered_paths: list[Path] = []

    if log_path is None and auto_log:
        candidate = pdf_path.with_suffix(".log")
        if candidate.is_file():
            log_path = candidate
    if log_path is not None:
        findings.extend(parse_tex_log(log_path))

    try:
        import fitz  # PyMuPDF

        has_fitz = True
    except ImportError:
        has_fitz = False

    if has_fitz:
        doc = fitz.open(str(pdf_path))
        try:
            total = len(doc)
            page_texts = [doc[i].get_text("text") for i in range(total)]
            for idx in range(total):
                pnum = idx + 1
                findings.extend(_check_text_anomalies(page_texts[idx], pnum))
                findings.extend(_check_fitz_overlaps_and_margins(doc[idx], pnum))
                next_txt = page_texts[idx + 1] if idx + 1 < total else ""
                findings.extend(_check_fitz_whitespace(doc[idx], pnum, total, next_txt))
            findings.extend(_check_intro_page_span(doc))

            if render_dir is not None:
                flagged_pages = sorted({f.page for f in findings if f.page >= 1})
                if flagged_pages:
                    render_dir.mkdir(parents=True, exist_ok=True)
                    for pnum in flagged_pages:
                        pix = doc[pnum - 1].get_pixmap(dpi=150)
                        out_png = render_dir / f"page_{pnum:03d}.png"
                        pix.save(str(out_png))
                        rendered_paths.append(out_png)
        finally:
            doc.close()
    else:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        for idx, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            findings.extend(_check_text_anomalies(txt, idx + 1))
        findings.append(
            PdfFinding(
                "WARN",
                "EngineFallback",
                0,
                "PyMuPDF (fitz) unavailable; skipped visual whitespace, overlap, and PNG rendering checks.",
            )
        )

    findings.sort(key=lambda f: (0 if f.severity == "ERROR" else 1, f.page, f.category))
    return findings, rendered_paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit compiled LaTeX PDF for garbled glyphs, overlaps, blank gaps, and margin overflows."
    )
    parser.add_argument("pdf_file", type=Path, help="Path to compiled .pdf")
    parser.add_argument(
        "--tex-log",
        type=Path,
        default=None,
        help="Optional path to LaTeX .log file (auto-detected alongside PDF by default)",
    )
    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Skip auto-detecting companion .log file",
    )
    parser.add_argument(
        "--render-flagged",
        type=Path,
        default=None,
        help="Directory to save 150-DPI PNG snapshots of flagged pages for read_file inspection",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on WARN findings as well as ERROR findings",
    )
    parser.add_argument(
        "--advisory",
        action="store_true",
        help="Always exit 0 (report findings without blocking)",
    )
    args = parser.parse_args()

    if not args.pdf_file.is_file():
        print(f"ERROR: file not found: {args.pdf_file}", file=sys.stderr)
        return 2

    findings, rendered = audit_pdf(
        args.pdf_file,
        log_path=args.tex_log,
        render_dir=args.render_flagged,
        auto_log=not args.no_log,
    )

    if not findings:
        print(f"PASS: 0 PDF layout/glyph issues found ({args.pdf_file.name}).")
        return 0

    errs = sum(1 for f in findings if f.severity == "ERROR")
    warns = sum(1 for f in findings if f.severity == "WARN")
    print(f"PDF AUDIT ({args.pdf_file.name}): {errs} ERROR(s), {warns} WARN(s)")
    for f in findings:
        loc = f"P{f.page}" if f.page > 0 else "LOG"
        print(f"  [{f.severity}][{f.category}] {loc}: {f.message}")

    if rendered:
        print("Flagged page snapshots (inspect with read_file):")
        for rp in rendered:
            print(f"  {rp}")

    if args.advisory:
        return 0
    if errs > 0 or (args.strict and warns > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
