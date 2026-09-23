"""Architecture diagrams describe system structure, not data flow."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from scripts.generate_architecture_svgs import (
    DIAGRAMS,
    PROJECT_INTRODUCTIONS,
    build_all,
)


NS = {"svg": "http://www.w3.org/2000/svg"}


def _root(name: str, locale: str = "zh") -> ET.Element:
    xml = DIAGRAMS[name](locale)
    return ET.fromstring(xml)


def _texts(root: ET.Element) -> str:
    return " ".join((t.text or "") for t in root.findall(".//svg:text", NS))


def test_casemaker_visual_language():
    root = _root("tracesmith")
    width, height = root.attrib["viewBox"].split()[2:]
    assert width == "1720"
    assert int(height) >= 1100
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
    assert len(zones) >= 5
    for text in root.findall(".//svg:text", NS):
        assert float(text.attrib["y"]) < int(height) - 4


def test_tracesmith_official_modules():
    text = _texts(_root("tracesmith"))
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
    text = _texts(_root("yirage"))
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
    text = _texts(_root("jax-sklearn"))
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
    text = _texts(_root("secret-learn"))
    for token in (
        "APPLICATION", "SKLEARN API", "PRIVACY MODES", "FEDERATED",
        "SECRET SHARING", "SPLIT LEARNING", "SPU", "PYU", "HEU", "TEE",
        "federated_learning", "ABY3", "Paillier", "FLLinearRegression",
        "SLMLPClassifier", "Linear Models",
    ):
        assert token in text, token


def test_youtube_two_tower():
    text = _texts(_root("youtube-recsys"))
    for token in (
        "DATA PROCESSING", "STORAGE", "MODEL TRAINING", "dnn.py", "TFRecords",
        "PREDICTION", "data2tfrecords.py", "MakeDataOne.scala",
        "visit_items_index", "Average Pooling", "Dense 64",
        "PredictUserVector.scala", "feature_column.py",
    ):
        assert token in text, token


def test_research_cli_packages():
    text = _texts(_root("research-cli"))
    for token in (
        "packages/cli", "packages/core", "modelRouterService", "MCP", "PROVIDERS",
        "defaultStrategy", "bibliography-manager", "latex-manager",
        "journal-matcher", "literature-investigator", "researchChat.ts",
    ):
        assert token in text, token


def test_questions_gen_three_stages():
    text = _texts(_root("questions-gen"))
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
            text = _texts(_root(name, locale))
            for token in banned:
                assert token not in text, (name, locale, token)


def test_each_project_has_localized_introduction():
    assert set(PROJECT_INTRODUCTIONS) == set(DIAGRAMS) - {"00-title"}
    for name, localized in PROJECT_INTRODUCTIONS.items():
        assert set(localized) == {"en", "zh"}, name
        assert sum(map(len, localized["en"])) >= 120, name
        assert sum(map(len, localized["zh"])) >= 45, name
        en_text = _texts(_root(name, "en"))
        zh_text = _texts(_root(name, "zh"))
        assert localized["en"][0] in en_text
        assert localized["zh"][0] in zh_text
        assert localized["zh"][0] not in en_text


def test_title_page_is_localized():
    assert "Architecture Appendix" in _texts(_root("00-title", "en"))
    assert "架构附录" in _texts(_root("00-title", "zh"))


def test_build_all_writes_svgs(tmp_path, monkeypatch):
    import scripts.generate_architecture_svgs as gen

    monkeypatch.setattr(gen, "SVG_DIR", tmp_path)
    written = build_all("zh")
    assert set(p.stem for p in written) == set(DIAGRAMS)
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
