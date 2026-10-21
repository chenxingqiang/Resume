#!/usr/bin/env python3
"""Generate architecture SVGs, convert them to PDF, and merge onto resumes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "docs" / "architecture" / "pdf"
APPENDIX_PDFS = {
    "en": ROOT / "docs" / "architecture" / "architecture-appendix-en.pdf",
    "zh": ROOT / "docs" / "architecture" / "architecture-appendix.pdf",
}

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


def generate_svg() -> dict[str, list[Path]]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from scripts.generate_architecture_svgs import build_all

    return {"zh": build_all("zh"), "en": build_all("en")}


def _assert_letter(pdf: Path) -> None:
    from pypdf import PdfReader

    page = PdfReader(str(pdf)).pages[0]
    width, height = float(page.mediabox.width), float(page.mediabox.height)
    if abs(width - 612) > 1.5 or abs(height - 792) > 1.5:
        raise SystemExit(
            f"{pdf.name} is {width:.1f} x {height:.1f} pt; expected US Letter 612 x 792"
        )


def convert_svg_to_pdf(pages: dict[str, list[Path]]) -> dict[str, list[Path]]:
    import cairosvg

    pdfs: dict[str, list[Path]] = {}
    for locale, svgs in pages.items():
        pdf_dir = PDF_DIR if locale == "zh" else PDF_DIR / locale
        pdf_dir.mkdir(parents=True, exist_ok=True)
        for stale in pdf_dir.glob("*.pdf"):
            stale.unlink()
        converted: list[Path] = []
        for svg in svgs:
            pdf = pdf_dir / f"{svg.stem}.pdf"
            cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))
            _assert_letter(pdf)
            converted.append(pdf)
            print(f"Converted [{locale}] {svg.name} -> {pdf.name}")
        pdfs[locale] = converted
    return pdfs


def build_appendices(pdfs: dict[str, list[Path]]) -> None:
    from pypdf import PdfReader, PdfWriter

    for locale, diagram_pdfs in pdfs.items():
        writer = PdfWriter()
        for pdf in diagram_pdfs:
            reader = PdfReader(str(pdf))
            for page in reader.pages:
                writer.add_page(page)

        appendix_pdf = APPENDIX_PDFS[locale]
        appendix_pdf.parent.mkdir(parents=True, exist_ok=True)
        with appendix_pdf.open("wb") as handle:
            writer.write(handle)
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
    pages = generate_svg()
    pdfs = convert_svg_to_pdf(pages)
    build_appendices(pdfs)
    merge_resumes()


if __name__ == "__main__":
    main()
