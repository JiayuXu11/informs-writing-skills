#!/usr/bin/env python3
"""Extract embedded annotations (highlights, strikeouts, comments, ink) from a PDF
and optionally render annotated pages as PNG snapshots for visual inspection.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


TEXT_MARKUP_TYPES = {"Highlight", "StrikeOut", "Underline", "Squiggly"}


def extract_quad_text(page: Any, annot: Any) -> str:
    """Extract text covered by multi-line quad vertices, falling back to annot.rect."""
    vertices = getattr(annot, "vertices", None)
    if vertices and len(vertices) >= 4:
        chunks: list[str] = []
        for idx in range(0, len(vertices) - 3, 4):
            quad = vertices[idx:idx + 4]
            xs = [pt[0] for pt in quad]
            ys = [pt[1] for pt in quad]
            rect = (min(xs), min(ys), max(xs), max(ys))
            snippet = page.get_text("text", clip=rect).strip()
            if snippet:
                chunks.append(" ".join(snippet.split()))
        if chunks:
            return " ".join(chunks)

    rect = annot.rect
    fallback = page.get_text("text", clip=rect).strip()
    return " ".join(fallback.split())


def extract_context(page: Any, rect: Any, margin_x: float = 120.0, margin_y: float = 28.0) -> str:
    """Grab nearby surrounding text around the annotation bounding box."""
    p_rect = page.rect
    expanded = (
        max(p_rect.x0, rect.x0 - margin_x),
        max(p_rect.y0, rect.y0 - margin_y),
        min(p_rect.x1, rect.x1 + margin_x),
        min(p_rect.y1, rect.y1 + margin_y),
    )
    txt = page.get_text("text", clip=expanded).strip()
    return " ".join(txt.split())[:240]


def run_fitz_extraction(
    pdf_path: Path,
    render_dir: Path | None,
    dpi: int,
    render_all_if_flat: bool,
) -> tuple[list[dict[str, Any]], int]:
    import fitz  # PyMuPDF

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    records: list[dict[str, Any]] = []
    annotated_pages: set[int] = set()

    for page_idx in range(total_pages):
        page = doc[page_idx]
        annots = list(page.annots() or [])
        if not annots:
            continue
        annotated_pages.add(page_idx)

        for annot in annots:
            atype = annot.type[1] if annot.type and len(annot.type) > 1 else str(annot.type)
            if atype == "Popup":
                # Popup text is already attached to its parent markup's info["content"].
                continue
            info = annot.info or {}
            comment = (info.get("content") or "").strip()
            author = (info.get("title") or "").strip()
            marked_text = extract_quad_text(page, annot) if atype in TEXT_MARKUP_TYPES else ""
            context = extract_context(page, annot.rect)

            records.append({
                "page": page_idx + 1,
                "type": atype,
                "author": author,
                "marked_text": marked_text,
                "comment": comment,
                "context": context,
                "rect": [round(float(v), 1) for v in annot.rect],
            })

    if render_dir is not None:
        render_dir.mkdir(parents=True, exist_ok=True)
        pages_to_render = sorted(annotated_pages)
        if not pages_to_render and render_all_if_flat:
            pages_to_render = list(range(total_pages))
        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)
        for pno in pages_to_render:
            pix = doc[pno].get_pixmap(matrix=matrix, annots=True)
            out_png = render_dir / f"page_{pno + 1:03d}.png"
            pix.save(str(out_png))

    doc.close()
    return records, total_pages


def run_pypdf_fallback(pdf_path: Path) -> tuple[list[dict[str, Any]], int]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    records: list[dict[str, Any]] = []
    for idx, page in enumerate(reader.pages):
        annots = page.get("/Annots") or []
        for ref in annots:
            obj = ref.get_object()
            subtype = str(obj.get("/Subtype", "")).lstrip("/")
            if subtype == "Popup":
                continue
            records.append({
                "page": idx + 1,
                "type": subtype or "Unknown",
                "author": str(obj.get("/T", "")),
                "marked_text": "",
                "comment": str(obj.get("/Contents", "")).strip(),
                "context": "",
                "rect": [float(x) for x in (obj.get("/Rect") or [])],
            })
    return records, len(reader.pages)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract annotations and snapshots from an annotated PDF.")
    parser.add_argument("pdf_path", type=Path, help="Path to the annotated PDF file.")
    parser.add_argument("--render-dir", type=Path, default=None, help="Directory to save PNG snapshots of annotated pages.")
    parser.add_argument("--dpi", type=int, default=180, help="DPI for rendered page snapshots (default: 180).")
    parser.add_argument("--render-all-if-flat", action="store_true", help="Render all pages if zero /Annot objects exist.")
    parser.add_argument("--json", type=Path, default=None, help="Optional path to write structured JSON output.")
    args = parser.parse_args()

    if not args.pdf_path.is_file():
        print(f"[ERROR] PDF not found: {args.pdf_path}", file=sys.stderr)
        return 2

    try:
        records, total_pages = run_fitz_extraction(
            args.pdf_path, args.render_dir, args.dpi, args.render_all_if_flat
        )
    except ImportError:
        records, total_pages = run_pypdf_fallback(args.pdf_path)

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"# PDF Annotation Report: {args.pdf_path.name} ({total_pages} pages)\n")
    if not records:
        print("[NOTICE] No embedded PDF /Annot objects found. User markups may be flattened ink; inspect the PDF or rendered PNG pages visually.")
        return 0

    print(f"Found {len(records)} annotation(s):\n")
    for idx, rec in enumerate(records, start=1):
        print(f"## {idx}. Page {rec['page']} — `{rec['type']}`")
        if rec["author"]:
            print(f"- **Author**: {rec['author']}")
        if rec["marked_text"]:
            print(f"- **Marked Text**: {rec['marked_text']}")
        if rec["comment"]:
            print(f"- **Comment**: {rec['comment']}")
        if rec["context"]:
            print(f"- **Context**: {rec['context']}")
        print()

    if args.render_dir is not None and args.render_dir.exists():
        pngs = sorted(args.render_dir.glob("page_*.png"))
        if pngs:
            print(f"Rendered {len(pngs)} annotated page snapshot(s) in `{args.render_dir}`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
