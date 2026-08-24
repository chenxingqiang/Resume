#!/usr/bin/env python3
"""Generate draw.io diagrams, export SVG, convert to PDF, merge onto resumes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAWIO_DIR = ROOT / "docs" / "architecture" / "drawio"
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

RESUME_BODY_PAGES = 3


def ensure_deps() -> None:
    try:
        import pypdf  # noqa: F401
        import drawpyo  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "pypdf", "drawpyo"]
        )


def generate_drawio() -> None:
    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "generate_architecture_drawio.py")]
    )


def export_svg() -> None:
    script = ROOT / "scripts" / "export_drawio_svg.sh"
    script.chmod(script.stat().st_mode | 0o111)
    subprocess.check_call(["bash", str(script)])


def build_appendix() -> None:
    from pypdf import PdfReader, PdfWriter

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    diagram_pdfs: list[Path] = []
    for slug, _ in PROJECTS:
        pdf = PDF_DIR / f"{slug}.pdf"
        if not pdf.exists():
            raise FileNotFoundError(f"Missing draw.io PDF: {pdf}")
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
    from pypdf import PdfReader, PdfWriter

    if not APPENDIX_PDF.exists():
        raise FileNotFoundError(f"Appendix missing: {APPENDIX_PDF}")

    appendix_reader = PdfReader(str(APPENDIX_PDF))
    for resume_pdf in RESUME_PDFS:
        if not resume_pdf.exists():
            print(f"Skip missing resume: {resume_pdf}")
            continue
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
    generate_drawio()
    export_svg()
    build_appendix()
    merge_resumes()


if __name__ == "__main__":
    main()
