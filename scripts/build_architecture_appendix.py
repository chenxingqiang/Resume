#!/usr/bin/env python3
"""Convert architecture SVGs to PDF and merge with resume PDFs."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import cairosvg
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "docs" / "architecture" / "svg"
PDF_DIR = ROOT / "docs" / "architecture" / "pdf"
APPENDIX_PDF = ROOT / "docs" / "architecture" / "architecture-appendix.pdf"

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

RESUME_PDFS = [
    ROOT / "xingqiangchen-en.pdf",
    ROOT / "xingqiangchen-zn.pdf",
    ROOT / "xingqiangchen-zn-adjust.pdf",
]


def ensure_deps() -> None:
    try:
        import cairosvg  # noqa: F401
        import pypdf  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "cairosvg", "pypdf"]
        )


def svg_to_pdf(svg_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2pdf(url=str(svg_path), write_to=str(pdf_path))
    print(f"Converted {svg_path.name} -> {pdf_path.name}")


def build_appendix() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    diagram_pdfs: list[Path] = []
    for slug, _ in PROJECTS:
        svg = SVG_DIR / f"{slug}.svg"
        pdf = PDF_DIR / f"{slug}.pdf"
        if not svg.exists():
            raise FileNotFoundError(f"Missing SVG: {svg}")
        svg_to_pdf(svg, pdf)
        diagram_pdfs.append(pdf)

    writer = PdfWriter()
    for pdf in diagram_pdfs:
        reader = PdfReader(str(pdf))
        for page in reader.pages:
            writer.add_page(page)

    APPENDIX_PDF.parent.mkdir(parents=True, exist_ok=True)
    with APPENDIX_PDF.open("wb") as f:
        writer.write(f)
    print(f"Built appendix: {APPENDIX_PDF} ({len(diagram_pdfs)} pages)")


def merge_resumes() -> None:
    if not APPENDIX_PDF.exists():
        raise FileNotFoundError(f"Appendix missing: {APPENDIX_PDF}")

    appendix_reader = PdfReader(str(APPENDIX_PDF))
    for resume_pdf in RESUME_PDFS:
        if not resume_pdf.exists():
            print(f"Skip missing resume: {resume_pdf}")
            continue
        writer = PdfWriter()
        resume_reader = PdfReader(str(resume_pdf))
        for page in resume_reader.pages:
            writer.add_page(page)
        for page in appendix_reader.pages:
            writer.add_page(page)
        with resume_pdf.open("wb") as f:
            writer.write(f)
        print(f"Merged appendix into {resume_pdf.name} ({len(resume_reader.pages)} + {len(appendix_reader.pages)} pages)")


def main() -> None:
    ensure_deps()
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "generate_architecture_svgs.py")])
    build_appendix()
    merge_resumes()


if __name__ == "__main__":
    main()
