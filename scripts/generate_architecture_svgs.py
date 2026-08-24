#!/usr/bin/env python3
"""Generate architecture SVG diagrams for resume appendix."""

from __future__ import annotations

from pathlib import Path
import html

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "architecture" / "svg"

W, H = 920, 560
BG = "#ffffff"
TITLE = "#1a365d"
BOX_FILL = "#f7fafc"
BOX_STROKE = "#2b6cb0"
ACCENT = "#2c5282"
TEXT = "#2d3748"
MUTED = "#718096"
ARROW = "#4a5568"


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def svg_header(title: str, subtitle: str) -> str:
    title = esc(title)
    subtitle = esc(subtitle)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
      <polygon points="0 0, 10 4, 0 8" fill="{ARROW}"/>
    </marker>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#00000022"/>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <text x="{W/2}" y="42" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="{TITLE}">{title}</text>
  <text x="{W/2}" y="68" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="{MUTED}">{subtitle}</text>
"""


def svg_footer() -> str:
    return "</svg>\n"


def box(x: float, y: float, w: float, h: float, title: str, lines: list[str], fill: str = BOX_FILL) -> str:
    title = esc(title)
    lines = [esc(line) for line in lines]
    line_h = 16
    body_y = y + 34
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{BOX_STROKE}" stroke-width="1.6" filter="url(#shadow)"/>',
        f'<text x="{x + w/2}" y="{y + 24}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="700" fill="{ACCENT}">{title}</text>',
    ]
    for i, line in enumerate(lines):
        parts.append(
            f'<text x="{x + 12}" y="{body_y + i * line_h}" font-family="Arial, Helvetica, sans-serif" font-size="11.5" fill="{TEXT}">{line}</text>'
        )
    return "\n  ".join(parts)


def arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ARROW}" stroke-width="1.8" marker-end="url(#arrow)"/>'
    )


def lane(x: float, y: float, w: float, h: float, label: str) -> str:
    label = esc(label)
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#edf2f7" stroke="#cbd5e0" stroke-width="1.2"/>
  <text x="{x + 14}" y="{y + 22}" font-family="Arial, Helvetica, sans-serif" font-size="12" font-weight="700" fill="{MUTED}">{label}</text>
"""


def write(name: str, content: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.svg"
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path}")


def tracesmith() -> None:
    s = svg_header("TraceSmith", "Cross-platform GPU Profiling & Replay · github.com/chenxingqiang/TraceSmith")
    s += lane(36, 92, 848, 430, "Capture → Format → State → Replay / Export")
    s += box(56, 130, 180, 120, "Capture", ["CUPTI / ROCm / Metal", "MACA / Ascend / eBPF", "Lock-free SPSC ring"])
    s += box(268, 130, 180, 120, "Common", ["Core event types", "Stack capture", "XRay import"])
    s += box(480, 130, 180, 120, "Format", ["SBT binary traces", "String interning", "Delta timestamps"])
    s += box(692, 130, 170, 120, "State", ["GPU state machine", "Timeline builder", "Perfetto export"])
    s += box(170, 300, 200, 120, "Replay", ["Stream scheduler", "Determinism check", "Full / partial replay"])
    s += box(410, 300, 200, 120, "Cluster", ["Multi-GPU topology", "Time sync / NCCL", "Distributed profiling"])
    s += box(650, 300, 200, 120, "CLI / Python", ["profile / record / view", "PyPI: tracesmith", "GDB RSP / Tracy"])
    s += arrow(236, 190, 268, 190)
    s += arrow(448, 190, 480, 190)
    s += arrow(660, 190, 692, 190)
    s += arrow(777, 250, 777, 300)
    s += arrow(777, 250, 270, 300)
    s += arrow(777, 250, 510, 300)
    s += f'<text x="{W/2}" y="520" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="{MUTED}">GPU events captured non-intrusively, serialized to SBT/Perfetto, then analyzed or deterministically replayed.</text>'
    s += svg_footer()
    write("tracesmith", s)


def yirage() -> None:
    s = svg_header("YiRage (YPK)", "Multi-backend LLM megakernel compiler & runtime · github.com/chenxingqiang/YiRage")
    s += lane(36, 92, 848, 430, "Python API → Backend Manager → Search / Transpile → Persistent Kernel / RuntimeFusion")
    s += box(56, 130, 240, 110, "Python API", ["HardwareRegistry", "UnifiedCompiler", "PersistentKernel / graph"])
    s += box(330, 130, 250, 110, "Backend Manager (C++)", ["BackendRegistry (12 backends)", "CUDA / ROCm / MPS / Ascend", "MACA / TPU / MLIR / CPU"])
    s += box(610, 130, 250, 110, "Search & Strategy", ["Hardware-aware search", "Kernel fingerprinting", "Perf profile / autotune"])
    s += box(120, 290, 230, 120, "Threadblock Ops", ["MatMul / Attention", "RMSNorm / SwiGLU", "Fused LLM operators"])
    s += box(380, 290, 230, 120, "Transpilers", ["Triton / NKI / MLIR", "CodeGen per backend", "JIT compile path"])
    s += box(640, 290, 220, 120, "Runtime", ["Persistent Kernel launch", "RuntimeFusion w/ vLLM", "FusionCapsule decode path"])
    s += arrow(296, 185, 330, 185)
    s += arrow(580, 185, 610, 185)
    s += arrow(735, 240, 735, 290)
    s += arrow(735, 240, 505, 290)
    s += arrow(735, 240, 235, 290)
    s += f'<text x="{W/2}" y="520" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="{MUTED}">Graph superoptimization selects backend-specific fused kernels; RF embeds optimized capsules into vLLM/SGLang decode loops.</text>'
    s += svg_footer()
    write("yirage", s)


def jax_sklearn() -> None:
    s = svg_header("JAX-sklearn (xlearn)", "Drop-in sklearn API with automatic JAX acceleration · github.com/chenxingqiang/jax-sklearn")
    s += lane(36, 92, 848, 430, "User API → Proxy → JAX / NumPy fallback → Hardware backends")
    s += box(80, 140, 760, 70, "User Code Layer", ["import xlearn as sklearn  ·  LinearRegression / KMeans / PCA  ·  100% sklearn-compatible API"])
    s += box(110, 240, 220, 110, "Compatibility Layer", ["Lazy module import", "Intelligent proxy", "Runtime class injection"])
    s += box(360, 240, 220, 110, "JAX Acceleration", ["JIT / vmap dispatch", "Algorithm thresholds", "Universal JAX mixins"])
    s += box(610, 240, 220, 110, "Data Management", ["NumPy ↔ JAX arrays", "dtype / shape guards", "Graceful fallback"])
    s += box(235, 390, 450, 70, "Hardware Abstraction", ["CPU (default)  ·  CUDA GPU  ·  Apple Metal  ·  Google TPU"])
    s += arrow(460, 210, 220, 240)
    s += arrow(460, 210, 470, 240)
    s += arrow(460, 210, 720, 240)
    s += arrow(470, 350, 460, 390)
    s += f'<text x="{W/2}" y="520" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="{MUTED}">Proxy decides JAX vs native sklearn by dataset size, algorithm type, and configured hardware.</text>'
    s += svg_footer()
    write("jax-sklearn", s)


def secret_learn() -> None:
    s = svg_header("Secret-Learn", "Privacy-preserving ML · 191 algorithms × FL/SS/SL · github.com/chenxingqiang/Secret-Learn")
    s += lane(36, 92, 848, 430, "sklearn API → Privacy mode router → JAX + SecretFlow devices")
    s += box(80, 130, 760, 60, "Application / sklearn-compatible API", ["191 estimators across linear, ensemble, clustering, neural nets, preprocessing"])
    s += box(90, 220, 230, 100, "FL Mode", ["Local PYU compute", "HEU secure aggregate", "Data stays on device"])
    s += box(345, 220, 230, 100, "SL Mode", ["Split model layers", "Encrypted activations", "Collaborative training"])
    s += box(600, 220, 230, 100, "SS Mode", ["SPU MPC encryption", "Maximum privacy", "Multi-party execution"])
    s += box(170, 360, 250, 90, "JAX Acceleration", ["xlearn / jax-sklearn core", "5×+ local speedup", "CPU / GPU / TPU"])
    s += box(500, 360, 250, 90, "SecretFlow Integration", ["SPU / PYU / HEU / TEE", "Algorithm classifier", "Template generator"])
    s += arrow(460, 190, 205, 220)
    s += arrow(460, 190, 460, 220)
    s += arrow(460, 190, 715, 220)
    s += arrow(205, 320, 295, 360)
    s += arrow(715, 320, 625, 360)
    s += f'<text x="{W/2}" y="520" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="{MUTED}">Same sklearn call surface; privacy mode selects FL/SS/SL execution path with optional JAX-accelerated local work.</text>'
    s += svg_footer()
    write("secret-learn", s)


def youtube_recsys() -> None:
    s = svg_header("YouTube-DNN-RecSys", "Two-tower recall pipeline · TensorFlow + Spark · github.com/chenxingqiang/YouTube-DNN-RecSys")
    s += lane(36, 92, 848, 430, "Data ingest → Feature build → DNN training → User/Item vectors → Serving")
    s += box(60, 140, 180, 100, "Raw Events", ["User watch history", "Continuous features", "Candidate items"])
    s += box(270, 140, 180, 100, "Data Prep", ["Python: TFRecords", "Scala: Spark ETL", "FeatureBuilder"])
    s += box(480, 140, 180, 100, "DNN Model", ["Item embeddings", "History average pool", "Dense tower → user vec"])
    s += box(690, 140, 180, 100, "Training", ["TensorFlow Estimator", "Softmax over items", "Checkpoints / TB"])
    s += box(190, 300, 240, 110, "Python Inference", ["load_dnn_model.py", "User vector export", "TensorFlow SavedModel"])
    s += box(490, 300, 240, 110, "Spark Inference", ["PredictUserVector", "ItemEmbeddingPredictor", "Distributed scoring"])
    s += arrow(240, 190, 270, 190)
    s += arrow(450, 190, 480, 190)
    s += arrow(660, 190, 690, 190)
    s += arrow(570, 240, 570, 300)
    s += arrow(570, 240, 310, 300)
    s += f'<text x="{W/2}" y="520" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="{MUTED}">Watch history embeddings are pooled into a user vector and matched against item embeddings for next-item recommendation.</text>'
    s += svg_footer()
    write("youtube-recsys", s)


def research_cli() -> None:
    s = svg_header("Research CLI", "CLI AI workflow + academic research tools · github.com/iechor-research/research-cli")
    s += lane(36, 92, 848, 430, "Terminal UI → Core orchestration → Providers / Tools / MCP")
    s += box(80, 140, 760, 70, "CLI Frontend (packages/cli)", ["Interactive TUI / slash commands", "/research /paper /submit", "Session & theme management"])
    s += box(110, 240, 220, 110, "Core Backend", ["Prompt + context build", "File discovery / GEMINI.md", "Chat compression"])
    s += box(360, 240, 220, 110, "Tool Orchestration", ["Filesystem / shell tools", "Policy engine / sandbox", "MCP server adapters"])
    s += box(610, 240, 220, 110, "Multi-Model Router", ["Gemini / OpenAI / Claude", "Baidu / DeepSeek / Qwen", "Provider config & fallback"])
    s += box(170, 390, 580, 70, "Academic Research Modules", ["Bibliography (arXiv/PubMed)  ·  LaTeX manager  ·  Experiment codegen  ·  Journal matcher / submission prep"])
    s += arrow(460, 210, 220, 240)
    s += arrow(460, 210, 470, 240)
    s += arrow(460, 210, 720, 240)
    s += arrow(470, 350, 460, 390)
    s += f'<text x="{W/2}" y="520" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="{MUTED}">User prompts flow through core, selected provider generates plans, tools/MCP execute actions, results stream back to terminal.</text>'
    s += svg_footer()
    write("research-cli", s)


def questions_gen() -> None:
    s = svg_header("Questions-Gen", "Math competition problem generator · Qwen3-14B · github.com/chenxingqiang/GenQuestion")
    s += lane(36, 92, 848, 430, "Data → 3-stage training → Validation → Deployment")
    s += box(60, 140, 190, 110, "Training Data", ["Historical contests", "Conditional variations", "Innovative problem types"])
    s += box(280, 140, 190, 110, "Stage 1", ["Basic pretraining", "Qwen3-14B fine-tune", "HF: stage1-fp-merged"])
    s += box(500, 140, 190, 110, "Stage 2", ["RL GRPO optimization", "8-problem reward groups", "Novelty constraints"])
    s += box(720, 140, 160, 110, "Stage 3", ["DeepSeek-R1 distill", "Quality scoring", "Final merged model"])
    s += box(150, 300, 250, 110, "Validation", ["ModelValidator", "BatchValidator", "QualityEvaluator"])
    s += box(430, 300, 250, 110, "CLI / API", ["questions-gen CLI", "validate / batch / quality", "Category benchmarks"])
    s += box(710, 300, 170, 110, "Deploy", ["HuggingFace weights", "Ollama import", "Local inference"])
    s += arrow(250, 195, 280, 195)
    s += arrow(470, 195, 500, 195)
    s += arrow(690, 195, 720, 195)
    s += arrow(800, 250, 795, 300)
    s += arrow(590, 250, 555, 300)
    s += arrow(370, 250, 275, 300)
    s += f'<text x="{W/2}" y="520" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="{MUTED}">Reward = 0.4·difficulty + 0.3·novelty + 0.2·rigor + 0.1·diversity; staged models validated then published to HF/Ollama.</text>'
    s += svg_footer()
    write("questions-gen", s)


def title_page() -> None:
    s = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <text x="{W/2}" y="220" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700" fill="{TITLE}">Open Source Architecture Appendix</text>
  <text x="{W/2}" y="260" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="{MUTED}">Chen Xingqiang · github.com/chenxingqiang</text>
  <rect x="180" y="300" width="560" height="2" fill="#cbd5e0"/>
  <text x="{W/2}" y="340" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="{TEXT}">TraceSmith · YiRage · JAX-sklearn · Secret-Learn</text>
  <text x="{W/2}" y="368" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="{TEXT}">YouTube-DNN-RecSys · Research CLI · Questions-Gen</text>
</svg>
"""
    write("00-title", s)


def main() -> None:
    title_page()
    tracesmith()
    yirage()
    jax_sklearn()
    secret_learn()
    youtube_recsys()
    research_cli()
    questions_gen()


if __name__ == "__main__":
    main()
