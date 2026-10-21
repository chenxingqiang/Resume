"""Witmem experience lists ByteDance as the employer unit."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_english_resume_names_bytedance():
    text = (ROOT / "xingqiangchen-en.tex").read_text(encoding="utf-8")
    assert "Witmem Technology (ByteDance)" in text


def test_chinese_resumes_name_bytedance():
    for name in ("xingqiangchen-zn.tex", "xingqiangchen-zn-adjust.tex"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "知存算力（Witmem / ByteDance）" in text
