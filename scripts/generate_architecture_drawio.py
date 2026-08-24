#!/usr/bin/env python3
"""Generate draw.io architecture diagrams for the resume appendix."""

from __future__ import annotations

from pathlib import Path

from drawpyo.diagram import Edge, Object
from drawpyo.diagram.objects import object_from_library
from drawpyo.diagram.text_format import TextFormat
from drawpyo.file import File
from drawpyo.page import Page

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "architecture" / "drawio"

PAGE_W, PAGE_H = 1600, 900

COLORS = {
    "blue": ("#dae8fc", "#6c8ebf"),
    "green": ("#d5e8d4", "#82b366"),
    "yellow": ("#fff2cc", "#d6b656"),
    "orange": ("#ffe6cc", "#d79b00"),
    "purple": ("#e1d5e7", "#9673a6"),
    "red": ("#f8cecc", "#b85450"),
    "gray": ("#f5f5f5", "#666666"),
    "cyan": ("#b1ddf0", "#10739e"),
    "white": ("#ffffff", "#666666"),
}


def tf(size: int = 11, bold: bool = False, align: str = "center") -> TextFormat:
    return TextFormat(
        formattedText=True,
        fontSize=size,
        fontFamily="Helvetica",
        align=align,
        verticalAlign="middle",
        bold=bold,
    )


def box(
    page: Page,
    value: str,
    x: int,
    y: int,
    w: int,
    h: int,
    color: str = "blue",
    parent: Object | None = None,
    size: int = 11,
    bold: bool = False,
) -> Object:
    fill, stroke = COLORS[color]
    kwargs = dict(
        page=page,
        value=value,
        position=(x, y),
        width=w,
        height=h,
        rounded=1,
        fillColor=fill,
        strokeColor=stroke,
        text_format=tf(size, bold),
    )
    if parent is not None:
        kwargs["parent"] = parent
    return Object(**kwargs)


def lane(page: Page, title: str, x: int, y: int, w: int, h: int, color: str = "gray") -> Object:
    fill, stroke = COLORS[color]
    return object_from_library(
        "general",
        "labeled_container",
        page=page,
        value=title,
        position=(x, y),
        width=w,
        height=h,
        fillColor=fill,
        strokeColor=stroke,
        text_format=tf(12, True, "left"),
    )


def header(page: Page, title: str, subtitle: str) -> None:
    box(page, f"<b>{title}</b>", 30, 14, 1540, 38, "blue", size=20, bold=True)
    box(page, subtitle, 30, 56, 1540, 26, "white", size=11)


def footer(page: Page, text: str) -> None:
    box(page, text, 30, 854, 1540, 32, "white", size=11)


def arrow(page: Page, src: Object, dst: Object, label: str = "") -> Edge:
    return Edge(
        source=src,
        target=dst,
        page=page,
        waypoints="orthogonal",
        rounded=1,
        line_end_target="classic",
        endFill_target=True,
        label=label,
        strokeWidth=1.4,
    )


def new_file(name: str) -> tuple[File, Page]:
    file = File(file_name=f"{name}.drawio", file_path=str(OUT_DIR))
    page = Page(file=file, name=name, width=PAGE_W, height=PAGE_H)
    return file, page


def place_row(page: Page, parent: Object, items: list[tuple[str, str]], y: int, h: int, gap: int = 16) -> list[Object]:
    n = len(items)
    inner = parent.width - 24
    w = (inner - gap * (n - 1)) // n
    objs = []
    x = 12
    for value, color in items:
        objs.append(box(page, value, x, y, w, h, color, parent=parent))
        x += w + gap
    return objs


def write_file(file: File) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = Path(file.write())
    print(f"Wrote {path}")
    return path


def title_page() -> None:
    file, page = new_file("00-title")
    box(page, "<b>Open Source Architecture Appendix</b>", 120, 180, 1360, 70, "blue", size=28, bold=True)
    box(page, "Chen Xingqiang  ·  github.com/chenxingqiang  ·  draw.io source in docs/architecture/drawio/", 120, 260, 1360, 40, "white", size=14)
    cards = [
        ("TraceSmith", "GPU Profiling & Replay<br>CUPTI / ROCm / Metal / MACA / Ascend", "orange"),
        ("YiRage YPK", "LLM megakernel compiler<br>12 backends + RuntimeFusion", "purple"),
        ("JAX-sklearn", "sklearn API + JAX proxy<br>CPU / GPU / TPU fallback", "cyan"),
        ("Secret-Learn", "191 algos × FL / SL / SS<br>JAX + SecretFlow", "green"),
        ("YouTube-DNN", "Two-tower recall<br>TensorFlow + Spark", "yellow"),
        ("Research CLI", "AI CLI + academic tools<br>multi-provider / MCP", "blue"),
        ("Questions-Gen", "Qwen3-14B contest problems<br>Pretrain → GRPO → Distill", "red"),
    ]
    y = 360
    w, h, gap = 196, 160, 18
    x = 80
    for title, desc, color in cards:
        box(page, f"<b>{title}</b><br><br>{desc}", x, y, w, h, color, size=12)
        x += w + gap
    box(page, "Each following page is a draw.io diagram exported to SVG, then appended to the resume PDF.", 120, 580, 1360, 40, "gray", size=12)
    write_file(file)


def tracesmith() -> None:
    file, page = new_file("tracesmith")
    header(page, "TraceSmith — Cross-platform GPU Profiling & Replay", "github.com/chenxingqiang/TraceSmith  ·  C++ core + pybind11  ·  PyPI: tracesmith")

    l1 = lane(page, "1. Workloads / producers", 30, 94, 1540, 118)
    w1 = place_row(
        page,
        l1,
        [
            ("<b>PyTorch / Kineto</b><br>kernel + runtime traces", "blue"),
            ("<b>TensorFlow / XLA</b><br>graph + device events", "blue"),
            ("<b>Custom CUDA / HIP</b><br>driver / runtime APIs", "blue"),
            ("<b>Multi-GPU cluster</b><br>NCCL collectives", "cyan"),
        ],
        y=38,
        h=68,
    )

    l2 = lane(page, "2. User interface", 30, 224, 1540, 118)
    w2 = place_row(
        page,
        l2,
        [
            ("<b>CLI</b><br>profile / record / view<br>export / analyze / replay", "green"),
            ("<b>Python API</b><br>pybind11 bindings<br>in-process capture", "green"),
            ("<b>Distribution</b><br>pip install tracesmith<br>Apache-2.0", "green"),
        ],
        y=38,
        h=68,
    )

    l3 = lane(page, "3. Capture backends  (platform-specific, lock-free ingest)", 30, 354, 1540, 140)
    w3 = place_row(
        page,
        l3,
        [
            ("<b>NVIDIA CUPTI</b><br>nsys / kernel / memcpy", "orange"),
            ("<b>AMD ROCm</b><br>rocprof / HIP events", "orange"),
            ("<b>Apple Metal</b><br>xctrace / Instruments", "orange"),
            ("<b>MetaX MACA</b><br>MCPTI", "orange"),
            ("<b>Huawei Ascend</b><br>CANN / msprof", "orange"),
            ("<b>Linux eBPF</b><br>host syscall / driver", "orange"),
        ],
        y=38,
        h=86,
    )

    l4 = lane(page, "4. Core pipeline", 30, 506, 1540, 150)
    w4 = place_row(
        page,
        l4,
        [
            ("<b>SPSC ring buffer</b><br>lock-free ingest<br>&lt;1% overhead", "yellow"),
            ("<b>Common / stacks</b><br>event types<br>XRay / host stacks", "yellow"),
            ("<b>SBT format</b><br>string interning<br>delta timestamps", "yellow"),
            ("<b>State / timeline</b><br>GPU state machine<br>stream reconstruction", "yellow"),
        ],
        y=38,
        h=96,
    )

    l5 = lane(page, "5. Replay, export, debug", 30, 668, 1540, 170)
    w5 = place_row(
        page,
        l5,
        [
            ("<b>Replay engine</b><br>full / partial / dry-run<br>stream scheduler<br>determinism checker", "purple"),
            ("<b>Perfetto</b><br>protobuf export<br>~85% smaller than JSON", "purple"),
            ("<b>Tracy profiler</b><br>live timeline view", "purple"),
            ("<b>GDB RSP</b><br>GPU breakpoints<br>trace-driven debug", "purple"),
            ("<b>Cluster sync</b><br>NTP / PTP / CUDA<br>NCCL tracking", "purple"),
        ],
        y=38,
        h=116,
    )

    arrow(page, w1[0], w2[1], "hooks")
    arrow(page, w2[0], w3[0])
    arrow(page, w3[0], w4[0], "events")
    arrow(page, w4[0], w4[1])
    arrow(page, w4[1], w4[2])
    arrow(page, w4[2], w4[3])
    arrow(page, w4[3], w5[0], "timeline")
    arrow(page, w4[3], w5[1], "export")
    footer(page, "Flow: workload → CLI/Python → platform backend → lock-free ring → SBT/timeline → replay or Perfetto/Tracy/GDB.")
    write_file(file)


def yirage() -> None:
    file, page = new_file("yirage")
    header(page, "YiRage (YPK) — Multi-backend LLM Megakernel Compiler & Runtime", "github.com/chenxingqiang/YiRage  ·  based on Mirage (CMU) + multi-backend / RuntimeFusion extensions")

    l1 = lane(page, "1. Serving / embedding", 30, 94, 1540, 118)
    w1 = place_row(
        page,
        l1,
        [
            ("<b>vLLM</b><br>keeps schedule + KV<br>RF selects capsules", "blue"),
            ("<b>SGLang</b><br>decode-loop embed<br>same FusionPlan cache", "blue"),
            ("<b>Python API</b><br>PersistentKernel<br>HardwareRegistry", "blue"),
            ("<b>UnifiedCompiler</b><br>graph + backend pick<br>Cython CoreBridge", "cyan"),
        ],
        y=38,
        h=68,
    )

    l2 = lane(page, "2. RuntimeFusion", 30, 224, 1540, 118)
    w2 = place_row(
        page,
        l2,
        [
            ("<b>FusionPlan cache</b><br>search / profile results<br>per backend + shape", "purple"),
            ("<b>FusionCapsule</b><br>one decode-step kernel<br>selected each token", "purple"),
            ("<b>Device memory</b><br>persistent workspace<br>KV-friendly layout", "purple"),
        ],
        y=38,
        h=68,
    )

    l3 = lane(page, "3. Compiler / search", 30, 354, 1540, 130)
    w3 = place_row(
        page,
        l3,
        [
            ("<b>Kernel graph IR</b><br>matmul / attn / norm<br>mark inputs / outputs", "yellow"),
            ("<b>Superoptimize</b><br>hardware-aware search<br>15 candidate dims", "yellow"),
            ("<b>Fingerprint</b><br>numeric verify<br>before accept", "yellow"),
            ("<b>Autotune</b><br>grid / tile / pipeline<br>occupancy model", "yellow"),
        ],
        y=38,
        h=78,
    )

    l4 = lane(page, "4. Threadblock operators + transpilers", 30, 496, 1540, 150)
    ops = place_row(
        page,
        l4,
        [
            ("<b>MatMul</b><br>Tensor Core / Cube", "green"),
            ("<b>Attention / GQA</b><br>Flash-style tiles", "green"),
            ("<b>RMSNorm / SwiGLU</b><br>fused decode path", "green"),
            ("<b>Triton codegen</b>", "orange"),
            ("<b>NKI / MLIR</b>", "orange"),
            ("<b>CUDA / HIP JIT</b>", "orange"),
        ],
        y=38,
        h=96,
    )

    l5 = lane(page, "5. Backend registry  (12 targets; factory + thread-safe singleton)", 30, 658, 1540, 180)
    place_row(
        page,
        l5,
        [
            ("<b>CUDA</b><br>Tensor Core<br>bank conflict", "orange"),
            ("<b>ROCm</b><br>HIP / MFMA", "orange"),
            ("<b>MPS</b><br>Apple Metal<br>unified mem", "orange"),
            ("<b>Ascend</b><br>AI Core / Cube<br>BiSheng", "orange"),
            ("<b>MACA</b><br>MetaX", "orange"),
            ("<b>TPU / XPU</b><br>NKI / Intel", "orange"),
            ("<b>MLIR / CPU</b><br>LLVM / SIMD", "orange"),
            ("<b>FPGA</b><br>experimental", "gray"),
        ],
        y=38,
        h=126,
    )

    arrow(page, w1[0], w2[1], "decode")
    arrow(page, w1[3], w3[0])
    arrow(page, w3[0], w3[1])
    arrow(page, w3[1], w2[0], "cache")
    arrow(page, w3[1], ops[0])
    footer(page, "Serving keeps scheduling/KV; compiler searches fused kernels; RuntimeFusion injects FusionCapsules into vLLM/SGLang decode.")
    write_file(file)


def jax_sklearn() -> None:
    file, page = new_file("jax-sklearn")
    header(page, "JAX-sklearn (xlearn) — Drop-in sklearn with automatic JAX acceleration", "github.com/chenxingqiang/jax-sklearn  ·  13,058 tests passed  ·  pip install jax-sklearn")

    l1 = lane(page, "1. User code  (zero API change)", 30, 94, 1540, 110)
    place_row(
        page,
        l1,
        [
            ("<b>import xlearn as sklearn</b><br>LinearRegression().fit(X, y)", "blue"),
            ("<b>Same estimators</b><br>cluster / decompose / preprocess", "blue"),
            ("<b>config_context()</b><br>force GPU / disable JAX", "cyan"),
        ],
        y=38,
        h=60,
    )

    l2 = lane(page, "2. sklearn-compatible surface", 30, 216, 1540, 130)
    place_row(
        page,
        l2,
        [
            ("<b>Linear</b><br>LR / Ridge / Lasso<br>ElasticNet", "green"),
            ("<b>Cluster</b><br>KMeans<br>282 tests", "green"),
            ("<b>Decompose</b><br>PCA / TruncatedSVD<br>528 tests", "green"),
            ("<b>Preprocess</b><br>Standard / MinMax", "green"),
            ("<b>Others</b><br>native sklearn<br>via fallback", "gray"),
        ],
        y=38,
        h=78,
    )

    l3 = lane(page, "3. Runtime injection / proxy", 30, 358, 1540, 150)
    w3 = place_row(
        page,
        l3,
        [
            ("<b>__getattr__ lazy import</b><br>xlearn.linear_model …", "yellow"),
            ("<b>_auto_jax_accelerate</b><br>replace estimator classes", "yellow"),
            ("<b>EstimatorProxy</b><br>create JAX or original impl", "yellow"),
            ("<b>Heuristics</b><br>LR &gt; 1e8  ·  KMeans &gt; 1e6<br>PCA &gt; 1e7 complexity", "yellow"),
        ],
        y=38,
        h=96,
    )

    l4 = lane(page, "4. Acceleration + data", 30, 520, 1540, 140)
    w4 = place_row(
        page,
        l4,
        [
            ("<b>JAX kernels</b><br>JIT / vmap<br>universal mixins", "purple"),
            ("<b>Algo kernels</b><br>GP / MLP / SVM / tree", "purple"),
            ("<b>NumPy ↔ JAX</b><br>dtype / shape guards", "purple"),
            ("<b>Fallback</b><br>small data or error<br>→ original sklearn", "red"),
        ],
        y=38,
        h=86,
    )

    l5 = lane(page, "5. Hardware abstraction  (auto-select by problem size)", 30, 672, 1540, 160)
    place_row(
        page,
        l5,
        [
            ("<b>CPU</b><br>&lt;10K samples<br>1.0–2.5×", "cyan"),
            ("<b>NVIDIA GPU</b><br>10K–100K<br>5.5–8×", "cyan"),
            ("<b>Google TPU</b><br>&gt;100K<br>9.5–15×", "cyan"),
            ("<b>Apple Metal</b><br>M1/M2/M3 beta<br>2–4×", "gray"),
        ],
        y=38,
        h=106,
    )

    arrow(page, w3[0], w3[1])
    arrow(page, w3[1], w3[2])
    arrow(page, w3[2], w4[0], "JAX")
    arrow(page, w3[2], w4[3], "fallback")
    footer(page, "Proxy decides JAX vs sklearn from dataset size, algorithm family, and configured platform; errors fall back silently.")
    write_file(file)


def secret_learn() -> None:
    file, page = new_file("secret-learn")
    header(page, "Secret-Learn — Privacy-preserving ML (191 algorithms × FL / SL / SS)", "github.com/chenxingqiang/Secret-Learn  ·  sklearn API  ·  JAX acceleration  ·  SecretFlow devices")

    l1 = lane(page, "1. Applications", 30, 94, 1540, 110)
    place_row(
        page,
        l1,
        [
            ("<b>Healthcare</b><br>hospitals keep records local", "blue"),
            ("<b>Finance</b><br>cross-bank fraud / risk", "blue"),
            ("<b>IoT / edge</b><br>federated sensors", "blue"),
            ("<b>Research</b><br>multi-institution studies", "blue"),
        ],
        y=38,
        h=60,
    )

    l2 = lane(page, "2. sklearn-compatible API  (191 estimators, 30+ categories)", 30, 216, 1540, 120)
    place_row(
        page,
        l2,
        [
            ("Linear / GLM", "green"),
            ("Ensemble / trees", "green"),
            ("SVM / neighbors", "green"),
            ("Cluster / PCA", "green"),
            ("NN / Naive Bayes", "green"),
            ("Preprocess / select", "green"),
        ],
        y=38,
        h=68,
    )

    l3 = lane(page, "3. Privacy mode router", 30, 348, 1540, 160)
    w3 = place_row(
        page,
        l3,
        [
            ("<b>FL — Federated</b><br>data stays on PYU<br>local JAX train<br>HEU secure aggregate<br>best: horizontal FL", "yellow"),
            ("<b>SL — Split learning</b><br>model split by party<br>encrypted activations<br>vertical / deep models", "yellow"),
            ("<b>SS — Secret sharing</b><br>SPU MPC encrypt<br>maximum privacy<br>multi-party runtime", "yellow"),
        ],
        y=38,
        h=108,
    )

    l4 = lane(page, "4. Intelligent generation + acceleration", 30, 520, 1540, 140)
    w4 = place_row(
        page,
        l4,
        [
            ("<b>Algorithm classifier</b><br>supervised? partial_fit?<br>fit(x) vs fit(x,y)", "purple"),
            ("<b>Template migrator</b><br>auto-generate FL/SL/SS<br>adapter from sklearn", "purple"),
            ("<b>JAX-sklearn core</b><br>local 5×+ speedup<br>CPU / GPU / TPU", "cyan"),
            ("<b>573 examples</b><br>one per algo × mode<br>batch runners", "gray"),
        ],
        y=38,
        h=86,
    )

    l5 = lane(page, "5. SecretFlow device plane", 30, 672, 1540, 160)
    place_row(
        page,
        l5,
        [
            ("<b>PYU</b><br>plaintext local<br>party compute", "orange"),
            ("<b>HEU</b><br>homomorphic<br>secure aggregate", "orange"),
            ("<b>SPU</b><br>MPC / secret share", "orange"),
            ("<b>TEE</b><br>trusted execution", "orange"),
            ("<b>DP hooks</b><br>optional noise", "gray"),
        ],
        y=38,
        h=106,
    )

    arrow(page, w3[0], w4[2], "local JAX")
    arrow(page, w3[2], w4[0])
    footer(page, "Same estimator call; mode picks FL/SL/SS. FL keeps data local, SL splits the net, SS runs under MPC on SPU.")
    write_file(file)


def youtube_recsys() -> None:
    file, page = new_file("youtube-recsys")
    header(page, "YouTube-DNN-RecSys — Two-tower recall (Covington et al.) in TF + Spark", "github.com/chenxingqiang/YouTube-DNN-RecSys  ·  Python TensorFlow  ·  Scala Spark  ·  60 GitHub stars")

    l1 = lane(page, "1. Event / feature sources", 30, 94, 1540, 118)
    w1 = place_row(
        page,
        l1,
        [
            ("<b>Watch history</b><br>video / search ids", "blue"),
            ("<b>Context</b><br>device / geo / time", "blue"),
            ("<b>Continuous feats</b><br>age / counts", "blue"),
            ("<b>Candidate items</b><br>catalog embeddings", "blue"),
        ],
        y=38,
        h=68,
    )

    l2 = lane(page, "2. Dual implementation stacks", 30, 224, 1540, 200)
    py = box(
        page,
        "<b>Python / TensorFlow</b><br>data2tfrecords.py<br>models/dnn.py (Estimator)<br>custom layers / TensorBoard<br>SavedModel export",
        20,
        40,
        740,
        144,
        "green",
        parent=l2,
        size=12,
    )
    sc = box(
        page,
        "<b>Scala / Spark</b><br>FeatureBuilder.scala<br>BaseSparkLocal<br>PredictUserVector<br>ItemEmbeddingPredictor",
        780,
        40,
        740,
        144,
        "cyan",
        parent=l2,
        size=12,
    )

    l3 = lane(page, "3. Two-tower model", 30, 436, 1540, 190)
    user = box(page, "<b>User tower</b><br>item-id embeddings<br>average watch history<br>concat continuous feats<br>MLP → user vector u", 20, 40, 480, 134, "yellow", parent=l3, size=12)
    match = box(page, "<b>Matching</b><br>dot(u, v_i)<br>sampled softmax<br>next-watch objective", 530, 40, 480, 134, "orange", parent=l3, size=12)
    item = box(page, "<b>Item tower</b><br>shared item embedding<br>table v_i<br>optional side features", 1040, 40, 480, 134, "yellow", parent=l3, size=12)

    l4 = lane(page, "4. Train / serve", 30, 638, 1540, 196)
    place_row(
        page,
        l4,
        [
            ("<b>Train</b><br>TF Estimator<br>optional PS / workers<br>checkpoints", "purple"),
            ("<b>Eval</b><br>hold-out next-item<br>TensorBoard curves", "purple"),
            ("<b>Online recall</b><br>ANN / softmax top-k<br>user vec × item table", "purple"),
            ("<b>Artifacts</b><br>TFRecords<br>SavedModel / Spark vecs", "gray"),
        ],
        y=38,
        h=142,
    )

    arrow(page, w1[0], py)
    arrow(page, w1[0], sc)
    arrow(page, py, user)
    arrow(page, sc, item)
    arrow(page, user, match)
    arrow(page, item, match)
    footer(page, "History embeddings are mean-pooled into a user vector and scored against the item table — the paper's candidate-generation stage.")
    write_file(file)


def research_cli() -> None:
    file, page = new_file("research-cli")
    header(page, "Research CLI — Command-line AI workflow with academic research tools", "github.com/iechor-research/research-cli  ·  TypeScript monorepo  ·  Gemini CLI lineage + multi-provider + research modules")

    l1 = lane(page, "1. Interaction", 30, 94, 1540, 118)
    w1 = place_row(
        page,
        l1,
        [
            ("<b>packages/cli</b><br>Ink TUI  ·  research.tsx", "blue"),
            ("<b>Slash commands</b><br>/research /paper /submit<br>/model config|select", "blue"),
            ("<b>Non-interactive</b><br>npx / CI scripts", "blue"),
            ("<b>VS Code companion</b><br>packages/vscode-ide", "cyan"),
        ],
        y=38,
        h=68,
    )

    l2 = lane(page, "2. packages/core — orchestration", 30, 224, 1540, 150)
    w2 = place_row(
        page,
        l2,
        [
            ("<b>Prompt + context</b><br>GEMINI.md<br>file discovery", "yellow"),
            ("<b>Session state</b><br>history / compress<br>1M-token window", "yellow"),
            ("<b>Policy / sandbox</b><br>tool permission<br>workspace isolation", "yellow"),
            ("<b>Routing</b><br>provider + model<br>fallback chain", "yellow"),
        ],
        y=38,
        h=96,
    )

    l3 = lane(page, "3. Multi-model providers", 30, 386, 1540, 130)
    place_row(
        page,
        l3,
        [
            ("Gemini / Vertex", "orange"),
            ("OpenAI", "orange"),
            ("Anthropic", "orange"),
            ("Baidu ERNIE", "orange"),
            ("DeepSeek", "orange"),
            ("Qwen / Groq / Kimi", "orange"),
        ],
        y=38,
        h=78,
    )

    l4 = lane(page, "4. Tools + MCP", 30, 528, 1540, 140)
    w4 = place_row(
        page,
        l4,
        [
            ("<b>Workspace tools</b><br>fs / shell / git", "green"),
            ("<b>MCP servers</b><br>external capabilities", "green"),
            ("<b>Search grounding</b><br>iEchor / web", "green"),
            ("<b>SDK / a2a-server</b><br>programmatic embed", "green"),
        ],
        y=38,
        h=86,
    )

    l5 = lane(page, "5. Academic research modules  (packages/core/src/tools/research)", 30, 680, 1540, 154)
    place_row(
        page,
        l5,
        [
            ("<b>Bibliography</b><br>arXiv / PubMed / IEEE<br>BibTeX export", "purple"),
            ("<b>Writing</b><br>outline / grammar<br>LaTeX manager", "purple"),
            ("<b>Analysis</b><br>stats / citation net<br>experiment codegen", "purple"),
            ("<b>Submission</b><br>journal matcher<br>template / package", "purple"),
        ],
        y=38,
        h=100,
    )

    arrow(page, w1[0], w2[0])
    arrow(page, w2[3], w4[0], "tool calls")
    footer(page, "Prompt → core context → selected provider → tools/MCP/research modules → streamed terminal result.")
    write_file(file)


def questions_gen() -> None:
    file, page = new_file("questions-gen")
    header(page, "Questions-Gen — Math competition problem generator (Qwen3-14B)", "github.com/chenxingqiang/GenQuestion  ·  Unsloth training  ·  Hugging Face: xingqiang/*  ·  pip install questions-gen")

    l1 = lane(page, "1. Training mixture", 30, 94, 1540, 118)
    w1 = place_row(
        page,
        l1,
        [
            ("<b>Historical contests</b><br>50%  ·  CUMCM / olympiad", "blue"),
            ("<b>Conditional variants</b><br>30%  ·  rewrite constraints", "blue"),
            ("<b>Innovative types</b><br>20%  ·  new stems", "blue"),
            ("<b>data_preparer.py</b><br>tokenize / pack", "cyan"),
        ],
        y=38,
        h=68,
    )

    l2 = lane(page, "2. Three-stage pipeline", 30, 224, 1540, 200)
    s1 = box(page, "<b>Stage 1 — Pretrain</b><br>Qwen3-14B SFT<br>HF: stage1-fp-merged<br>base generation", 20, 40, 360, 144, "yellow", parent=l2, size=12)
    s2 = box(page, "<b>Stage 2 — GRPO</b><br>8 problems / group<br>novelty constraint<br>policy optimization", 400, 40, 360, 144, "orange", parent=l2, size=12)
    reward = box(page, "<b>Reward</b><br>0.4 difficulty<br>0.3 novelty<br>0.2 rigor<br>0.1 diversity", 780, 40, 360, 144, "red", parent=l2, size=12)
    s3 = box(page, "<b>Stage 3 — Distill</b><br>DeepSeek-R1 teacher<br>difficulty / logic / edu<br>final merged FP16", 1160, 40, 360, 144, "purple", parent=l2, size=12)

    l3 = lane(page, "3. Validation  (questions_gen/validation)", 30, 436, 1540, 160)
    w3 = place_row(
        page,
        l3,
        [
            ("<b>ModelValidator</b><br>single-model n tests", "green"),
            ("<b>BatchValidator</b><br>algebra / calculus<br>geometry / number theory", "green"),
            ("<b>QualityEvaluator</b><br>content / clarity<br>difficulty / originality", "green"),
            ("<b>Scores</b><br>Final 0.847<br>teacher 4.2 / 5", "cyan"),
        ],
        y=38,
        h=108,
    )

    l4 = lane(page, "4. Package / deploy", 30, 608, 1540, 226)
    place_row(
        page,
        l4,
        [
            ("<b>CLI</b><br>questions-gen<br>validate / batch<br>quality / compare", "blue"),
            ("<b>Python API</b><br>QuestionsGenTrainer<br>OllamaManager<br>HuggingFaceUtils", "blue"),
            ("<b>Hugging Face</b><br>stage1 / stage2 / final<br>xingqiang/*", "purple"),
            ("<b>Ollama</b><br>push-all<br>local generate API", "purple"),
        ],
        y=38,
        h=172,
    )

    arrow(page, w1[3], s1)
    arrow(page, s1, s2)
    arrow(page, s2, reward, "score")
    arrow(page, s2, s3)
    arrow(page, s3, w3[0], "eval")
    footer(page, "Pretrain → GRPO with multi-dimensional rewards → R1 distillation → validate by category → publish HF weights and Ollama models.")
    write_file(file)


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
