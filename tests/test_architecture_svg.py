"""Architecture diagrams must follow the casemaker zone-flow drawing style."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from scripts.generate_architecture_svgs import DIAGRAMS, build_all


NS = {"svg": "http://www.w3.org/2000/svg"}


def _root(name: str) -> ET.Element:
    xml = DIAGRAMS[name]()
    return ET.fromstring(xml)


def _texts(root: ET.Element) -> str:
    return " ".join((t.text or "") for t in root.findall(".//svg:text", NS))


def test_casemaker_visual_language():
    root = _root("tracesmith")
    assert root.attrib["viewBox"] == "0 0 1440 1230"
    assert "sans-serif" in root.attrib.get("font-family", "")
    bg = root.find("svg:rect", NS)
    assert bg is not None and bg.attrib["fill"] == "#ffffff"
    assert root.find("svg:defs/svg:marker[@id='arr']", NS) is not None
    assert root.find("svg:defs/svg:marker[@id='arrP']", NS) is not None
    zones = [
        r
        for r in root.findall("svg:rect", NS)
        if r.attrib.get("stroke-dasharray") == "7,5"
    ]
    assert len(zones) >= 5


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
        "ReplayEngine",
        "_tracesmith.so",
        "trace.sbt",
        "GPU BACKENDS",
        "主数据流",
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
        "vLLM",
        "superoptimize",
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
    ):
        assert token in text, token


def test_secret_learn_privacy_modes():
    text = _texts(_root("secret-learn"))
    for token in ("APPLICATION", "SKLEARN API", "PRIVACY MODES", "FEDERATED", "SECRET SHARING", "SPLIT LEARNING", "SPU", "PYU"):
        assert token in text, token


def test_youtube_two_tower():
    text = _texts(_root("youtube-recsys"))
    for token in ("DATA PROCESSING", "STORAGE", "MODEL TRAINING", "dnn.py", "TFRecords", "PREDICTION"):
        assert token in text, token


def test_research_cli_packages():
    text = _texts(_root("research-cli"))
    for token in ("packages/cli", "packages/core", "modelRouterService", "MCP", "PROVIDERS"):
        assert token in text, token


def test_questions_gen_three_stages():
    text = _texts(_root("questions-gen"))
    for token in ("Stage 1  SFT", "Stage 2  GRPO", "Stage 3  Distill", "RewardCalculator", "DeepSeekTeacher"):
        assert token in text, token


def test_build_all_writes_svgs(tmp_path, monkeypatch):
    import scripts.generate_architecture_svgs as gen

    monkeypatch.setattr(gen, "SVG_DIR", tmp_path)
    written = build_all()
    assert set(p.stem for p in written) == set(DIAGRAMS)
    for path in written:
        ET.parse(path)
