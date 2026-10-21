"""Architecture diagrams describe system structure, not data flow."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from scripts.generate_architecture_svgs import (
    DIAGRAMS,
    PAGE_H,
    PAGE_W,
    PROJECT_INTRODUCTIONS,
    _text_width,
    build_all,
)


NS = {"svg": "http://www.w3.org/2000/svg"}


def _pages(name: str, locale: str = "zh") -> list[ET.Element]:
    result = DIAGRAMS[name](locale)
    if isinstance(result, str):
        result = [result]
    return [ET.fromstring(xml) for xml in result]


def _root(name: str, locale: str = "zh") -> ET.Element:
    return _pages(name, locale)[0]


def _texts(root: ET.Element) -> str:
    return " ".join((t.text or "") for t in root.findall(".//svg:text", NS))


def _all_texts(name: str, locale: str = "zh") -> str:
    nodes = []
    for page in _pages(name, locale):
        nodes.extend(t.text or "" for t in page.findall(".//svg:text", NS))
    # Wrapped module names are split across text nodes. Keep both the spaced
    # reading order and the concatenated form so those names still match.
    return " ".join(nodes) + "\n" + "".join(nodes)


def test_casemaker_visual_language():
    root = _root("tracesmith")
    assert root.attrib["width"] == "8.5in"
    assert root.attrib["height"] == "11in"
    assert root.attrib["viewBox"] == f"0 0 {PAGE_W} {PAGE_H}"
    assert "sans-serif" in root.attrib.get("font-family", "")
    bg = root.find("svg:rect", NS)
    assert bg is not None and bg.attrib["fill"] == "#ffffff"
    assert root.find("svg:line", NS) is None
    assert root.find("svg:path", NS) is None
    assert "架构分区" in _texts(root)
    zones = [
        r
        for r in root.findall("svg:rect", NS)
        if r.attrib.get("stroke-dasharray") == "7,5"
    ]
    assert len(zones) >= 1
    for text in root.findall(".//svg:text", NS):
        assert float(text.attrib["y"]) < PAGE_H - 4


def test_pages_match_resume_letter_size():
    for name in DIAGRAMS:
        for locale in ("zh", "en"):
            pages = _pages(name, locale)
            assert pages
            for root in pages:
                assert root.attrib["width"] == "8.5in"
                assert root.attrib["height"] == "11in"
                assert root.attrib["viewBox"] == "0 0 816 1056"
                for text in root.findall(".//svg:text", NS):
                    x = float(text.attrib["x"])
                    y = float(text.attrib["y"])
                    size = float(text.attrib.get("font-size", "12"))
                    bold = int(text.attrib.get("font-weight", "400")) >= 600
                    width = _text_width(text.text or "", size, bold)
                    anchor = text.attrib.get("text-anchor", "start")
                    if anchor == "middle":
                        left, right = x - width / 2, x + width / 2
                    elif anchor == "end":
                        left, right = x - width, x
                    else:
                        left, right = x, x + width
                    assert 4 <= y <= PAGE_H - 4
                    assert left >= -1, (name, locale, text.text)
                    assert right <= PAGE_W + 1, (name, locale, text.text)


def test_tracesmith_official_modules():
    text = _all_texts("tracesmith")
    for token in (
        "APPLICATION",
        "BINDINGS",
        "CORE LIBRARY",
        "Capture Module",
        "State Module",
        "Replay Module",
        "Cluster Module",
        "CUPTIProfiler",
        "MCPTIProfiler",
        "AscendProfiler",
        "GPUTopology",
        "InstructionStream",
        "PerfettoProtoExporter",
        "SBTWriter",
        "RingBuffer",
        "ReplayEngine",
        "FrameCapture",
        "RSPHandler",
        "_tracesmith.so",
        "trace.sbt",
        "GPU BACKENDS",
        "架构分区",
    ):
        assert token in text, token


def test_yirage_official_stack():
    text = _all_texts("yirage")
    for token in (
        "INFERENCE ENGINE",
        "RuntimeFusion",
        "RF.step",
        "FusionCapsule",
        "BackendRegistry",
        "yirage.serving",
        "yirage.core",
        "MuGraph",
        "seed_verify",
        "vLLM",
        "superoptimize",
        "CUDA",
        "MACA",
        "Triton",
        "NVIDIA GPU",
    ):
        assert token in text, token


def test_jax_sklearn_five_layers():
    text = _all_texts("jax-sklearn")
    for token in (
        "USER CODE",
        "COMPATIBILITY",
        "JAX ACCELERATION",
        "DATA MANAGEMENT",
        "HARDWARE",
        "EstimatorProxy",
        "AcceleratorRegistry",
        "_universal_jax.py",
        "_data_conversion.py",
        "complexity >= 1e8",
        "_gp.py",
        "_mlp.py",
        "_svm.py",
        "_tree.py",
    ):
        assert token in text, token


def test_secret_learn_privacy_modes():
    text = _all_texts("secret-learn")
    for token in (
        "APPLICATION", "SKLEARN API", "PRIVACY MODES", "FEDERATED",
        "SECRET SHARING", "SPLIT LEARNING", "SPU", "PYU", "HEU", "TEE",
        "federated_learning", "ABY3", "Paillier", "FLLinearRegression",
        "SLMLPClassifier", "Linear Models",
    ):
        assert token in text, token


def test_youtube_two_tower():
    text = _all_texts("youtube-recsys")
    for token in (
        "DATA PROCESSING", "STORAGE", "MODEL TRAINING", "dnn.py", "TFRecords",
        "PREDICTION", "data2tfrecords.py", "MakeDataOne.scala",
        "visit_items_index", "Average Pooling", "Dense 64",
        "PredictUserVector.scala", "feature_column.py",
    ):
        assert token in text, token


def test_research_cli_packages():
    text = _all_texts("research-cli")
    for token in (
        "packages/cli", "packages/core", "modelRouterService", "MCP", "PROVIDERS",
        "defaultStrategy", "bibliography-manager", "latex-manager",
        "journal-matcher", "literature-investigator", "researchChat.ts",
    ):
        assert token in text, token


def test_questions_gen_three_stages():
    text = _all_texts("questions-gen")
    for token in (
        "Stage 1", "SFT", "Stage 2", "GRPO", "Stage 3", "Distill",
        "RewardCalculator", "DeepSeekTeacher", "QuestionDataPreparer",
        "NoveltyConstraint", "model_validator.py", "ollama_manager.py",
        "0.4 difficulty", "8 problems/group",
    ):
        assert token in text, token


def test_diagrams_do_not_narrate_data_flow():
    banned = ("主数据流", "主链", "Primary flow", "Primary path", "Fallback / feedback", "回退 / 反馈", "→")
    for name in DIAGRAMS:
        for locale in ("zh", "en"):
            text = _all_texts(name, locale)
            for token in banned:
                assert token not in text, (name, locale, token)


def test_each_project_has_localized_introduction():
    assert set(PROJECT_INTRODUCTIONS) == set(DIAGRAMS) - {"00-title"}
    for name, localized in PROJECT_INTRODUCTIONS.items():
        assert set(localized) == {"en", "zh"}, name
        assert sum(map(len, localized["en"])) >= 120, name
        assert sum(map(len, localized["zh"])) >= 45, name
        en_text = _all_texts(name, "en")
        zh_text = _all_texts(name, "zh")
        assert localized["en"][0] in en_text
        assert localized["zh"][0] in zh_text
        assert localized["zh"][0] not in en_text


def test_title_page_is_localized():
    assert "Architecture Appendix" in _all_texts("00-title", "en")
    assert "架构附录" in _all_texts("00-title", "zh")


def test_build_all_writes_svgs(tmp_path, monkeypatch):
    import scripts.generate_architecture_svgs as gen

    monkeypatch.setattr(gen, "SVG_DIR", tmp_path)
    written = build_all("zh")
    names = set()
    for path in written:
        stem = path.stem
        if stem in DIAGRAMS:
            names.add(stem)
        else:
            base, _, suffix = stem.rpartition("-")
            assert suffix.isdigit()
            names.add(base)
    assert names == set(DIAGRAMS)
    for path in written:
        ET.parse(path)

    english = build_all("en")
    assert all(path.parent == tmp_path / "en" for path in english)


def test_resume_appendix_language_mapping():
    from scripts.build_architecture_appendix import APPENDIX_PDFS, RESUME_APPENDIX

    assert APPENDIX_PDFS["en"].name == "architecture-appendix-en.pdf"
    assert APPENDIX_PDFS["zh"].name == "architecture-appendix.pdf"
    assert RESUME_APPENDIX["xingqiangchen-en.pdf"] == "en"
    assert RESUME_APPENDIX["xingqiangchen-zn.pdf"] == "zh"
    assert RESUME_APPENDIX["xingqiangchen-zn-adjust.pdf"] == "zh"


def test_svg_pdf_is_us_letter(tmp_path):
    import cairosvg
    from pypdf import PdfReader

    svg = tmp_path / "jax-sklearn.svg"
    svg.write_text(DIAGRAMS["jax-sklearn"]("en")[0], encoding="utf-8")
    pdf = tmp_path / "jax-sklearn.pdf"
    cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))
    page = PdfReader(str(pdf)).pages[0]
    assert abs(float(page.mediabox.width) - 612) < 1.5
    assert abs(float(page.mediabox.height) - 792) < 1.5
