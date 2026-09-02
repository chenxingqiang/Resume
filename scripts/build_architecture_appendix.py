#!/usr/bin/env python3
"""Generate architecture SVGs, convert them to PDF, and merge onto resumes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "docs" / "architecture" / "svg"
PDF_DIR = ROOT / "docs" / "architecture" / "pdf"
APPENDIX_PDFS = {
    "en": ROOT / "docs" / "architecture" / "architecture-appendix-en.pdf",
    "zh": ROOT / "docs" / "architecture" / "architecture-appendix.pdf",
}

PROJECTS = [
    ("00-title", "Appendix Title"),
    ("tracesmith", "TraceSmith"),
    ("yirage", "YiRage (YPK)"),
    ("jax-sklearn", "JAX-sklearn"),
    ("secret-learn", "Secret-Learn"),
    ("youtube-recsys", "YouTube-DNN-RecSys"),
    ("research-cli", "Research CLI"),
    ("questions-gen", "Questions-Gen"),
]

RESUME_APPENDIX = {
    "xingqiangchen-en.pdf": "en",
    "xingqiangchen-zn.pdf": "zh",
    "xingqiangchen-zn-adjust.pdf": "zh",
}

RESUME_BODY_PAGES = 3


def ensure_deps() -> None:
    try:
        import pypdf  # noqa: F401
        import cairosvg  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "pypdf", "cairosvg"]
        )


def generate_svg() -> None:
    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "generate_architecture_svgs.py")]
    )


def convert_svg_to_pdf() -> None:
    import cairosvg

    for locale in ("zh", "en"):
        svg_dir = SVG_DIR if locale == "zh" else SVG_DIR / locale
        pdf_dir = PDF_DIR if locale == "zh" else PDF_DIR / locale
        pdf_dir.mkdir(parents=True, exist_ok=True)
        for slug, _ in PROJECTS:
            svg = svg_dir / f"{slug}.svg"
            pdf = pdf_dir / f"{slug}.pdf"
            if not svg.exists():
                raise FileNotFoundError(f"Missing architecture SVG: {svg}")
            cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))
            print(f"Converted [{locale}] {svg.name} -> {pdf.name}")


def build_appendices() -> None:
    from pypdf import PdfReader, PdfWriter

    for locale in ("zh", "en"):
        pdf_dir = PDF_DIR if locale == "zh" else PDF_DIR / locale
        diagram_pdfs: list[Path] = []
        for slug, _ in PROJECTS:
            pdf = pdf_dir / f"{slug}.pdf"
            if not pdf.exists():
                raise FileNotFoundError(f"Missing architecture PDF: {pdf}")
            diagram_pdfs.append(pdf)

        writer = PdfWriter()
        for pdf in diagram_pdfs:
            reader = PdfReader(str(pdf))
            for page in reader.pages:
                writer.add_page(page)

        appendix_pdf = APPENDIX_PDFS[locale]
        appendix_pdf.parent.mkdir(parents=True, exist_ok=True)
        with appendix_pdf.open("wb") as f:
            writer.write(f)
        print(f"Built [{locale}] appendix: {appendix_pdf} ({len(diagram_pdfs)} pages)")


def merge_resumes() -> None:
    from pypdf import PdfReader, PdfWriter

    for resume_name, locale in RESUME_APPENDIX.items():
        resume_pdf = ROOT / resume_name
        if not resume_pdf.exists():
            print(f"Skip missing resume: {resume_pdf}")
            continue
        appendix_pdf = APPENDIX_PDFS[locale]
        if not appendix_pdf.exists():
            raise FileNotFoundError(f"Appendix missing: {appendix_pdf}")
        appendix_reader = PdfReader(str(appendix_pdf))
        writer = PdfWriter()
        resume_reader = PdfReader(str(resume_pdf))
        body_pages = min(RESUME_BODY_PAGES, len(resume_reader.pages))
        for page in resume_reader.pages[:body_pages]:
            writer.add_page(page)
        for page in appendix_reader.pages:
            writer.add_page(page)
        with resume_pdf.open("wb") as f:
            writer.write(f)
        print(
            f"Merged appendix into {resume_pdf.name} "
            f"({body_pages} + {len(appendix_reader.pages)} pages)"
        )


def main() -> None:
    ensure_deps()
    generate_svg()
    convert_svg_to_pdf()
    build_appendices()
    merge_resumes()


if __name__ == "__main__":
    main()
