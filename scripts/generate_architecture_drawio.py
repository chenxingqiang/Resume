#!/usr/bin/env python3
"""Generate DS4-style draw.io diagrams strictly from each repo's architecture.

Visual language follows the DS4/BW01 system diagram:
  dark canvas, nested containers, monospace labels, real file/module names.

Content follows official repo diagrams + source trees, not invented boxes:
  TraceSmith  docs/architecture.drawio
  YiRage      docs/yirage-architecture.drawio + include/backend/*.h
  Secret-Learn docs/secret_learn_architecture.drawio + src/secretlearn/
  YouTube     docs/architecture.drawio + src/python|scala
  JAX-sklearn xlearn/_jax/*.py
  Research CLI packages/{cli,core}
  Questions-Gen src/*.py + questions_gen/
"""

from __future__ import annotations

from pathlib import Path

from drawpyo.diagram import Edge, Object
from drawpyo.diagram.objects import object_from_library
from drawpyo.diagram.text_format import TextFormat
from drawpyo.file import File
from drawpyo.page import Page

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "architecture" / "drawio"

W, H = 1720, 1080

BG = "#0b1520"
INK = "#c5dde3"
CYAN = "#3ecfcf"
CYAN2 = "#7ee8f0"
TEAL = "#173445"
NAVY = "#102433"
ORANGE = "#ff8c42"
ORANGE_BG = "#3a2618"
MUTED = "#7a9aa3"
GREEN = "#6ee7b7"
GREEN_BG = "#16352c"
PURPLE = "#c4b5fd"
PURPLE_BG = "#2a2150"


def tf(size: int = 10, bold: bool = False, color: str = INK, align: str = "center") -> TextFormat:
    return TextFormat(
        formattedText=True,
        fontSize=size,
        fontFamily="Courier New",
        fontColor=color,
        align=align,
        verticalAlign="middle",
        bold=bold,
    )


def cell(
    page: Page,
    title: str,
    file: str = "",
    x: int = 0,
    y: int = 0,
    w: int = 160,
    h: int = 64,
    kind: str = "box",
    parent: Object | None = None,
) -> Object:
    if kind == "hl":
        fill, stroke, tc = ORANGE_BG, ORANGE, ORANGE
    elif kind == "out":
        fill, stroke, tc = GREEN_BG, GREEN, GREEN
    elif kind == "alt":
        fill, stroke, tc = PURPLE_BG, PURPLE, PURPLE
    elif kind == "lane":
        fill, stroke, tc = NAVY, CYAN, CYAN2
    else:
        fill, stroke, tc = TEAL, CYAN, CYAN2

    if file:
        file_html = file.replace("\n", "<br>")
        value = (
            f'<font color="{tc}"><b>{title}</b></font>'
            f'<br><font color="{MUTED}">{file_html}</font>'
        )
    else:
        value = f'<font color="{tc}"><b>{title}</b></font>'

    kwargs = dict(
        page=page,
        value=value,
        position=(x, y),
        width=w,
        height=h,
        rounded=0,
        fillColor=fill,
        strokeColor=stroke,
        text_format=tf(10, False, INK),
    )
    if parent is not None:
        kwargs["parent"] = parent
    obj = Object(**kwargs)
    obj._style_attributes.append("strokeWidth")
    obj.strokeWidth = 2 if kind == "lane" else 1
    return obj


def lane(page: Page, title: str, x: int, y: int, w: int, h: int) -> Object:
    obj = object_from_library(
        "general",
        "labeled_container",
        page=page,
        value=f'<font color="{CYAN2}"><b>{title}</b></font>',
        position=(x, y),
        width=w,
        height=h,
        fillColor=NAVY,
        strokeColor=CYAN,
        text_format=tf(11, True, CYAN2, "left"),
        rounded=0,
    )
    obj._style_attributes.append("strokeWidth")
    obj.strokeWidth = 2
    return obj


def header(page: Page, title: str, subtitle: str) -> None:
    Object(
        page=page,
        value="",
        position=(0, 0),
        width=W,
        height=H,
        rounded=0,
        fillColor=BG,
        strokeColor=BG,
        text_format=tf(1),
    )
    cell(page, title, "", 24, 12, 1672, 40, "lane")
    Object(
        page=page,
        value=f'<font color="{MUTED}">{subtitle}</font>',
        position=(24, 54),
        width=1672,
        height=24,
        rounded=0,
        fillColor=BG,
        strokeColor=BG,
        text_format=tf(10, False, MUTED, "left"),
    )


def footer(page: Page, text: str) -> None:
    Object(
        page=page,
        value=f'<font color="{MUTED}">{text}</font>',
        position=(24, 1048),
        width=1672,
        height=22,
        rounded=0,
        fillColor=BG,
        strokeColor=BG,
        text_format=tf(9, False, MUTED, "left"),
    )


def arrow(page: Page, src: Object, dst: Object, color: str = CYAN, dashed: bool = False, label: str = "") -> Edge:
    return Edge(
        source=src,
        target=dst,
        page=page,
        waypoints="orthogonal",
        rounded=0,
        line_end_target="classic",
        endFill_target=True,
        label=label,
        strokeWidth=1.4,
        stroke_color=color,
        pattern="dashed_small" if dashed else "solid",
        text_format=tf(8, False, color),
    )


def new_file(name: str) -> tuple[File, Page]:
    file = File(file_name=f"{name}.drawio", file_path=str(OUT_DIR))
    page = Page(file=file, name=name, width=W, height=H)
    return file, page


def write_file(file: File) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = Path(file.write())
    print(f"Wrote {path}")
    return path


def row(page: Page, parent: Object, items: list[tuple], y: int, h: int, gap: int = 10) -> list[Object]:
    n = len(items)
    inner = parent.width - 20
    bw = (inner - gap * (n - 1)) // n
    out = []
    x = 10
    for item in items:
        title, file, kind = item if len(item) == 3 else (*item, "box")
        out.append(cell(page, title, file, x, y, bw, h, kind, parent=parent))
        x += bw + gap
    return out


def title_page() -> None:
    file, page = new_file("00-title")
    header(
        page,
        "OPEN SOURCE — SYSTEM ARCHITECTURE APPENDIX",
        "Chen Xingqiang  ·  diagrams restyle DS4/BW01  ·  content from each repo's official architecture + source tree",
    )
    cards = [
        ("TRACESMITH", "docs/architecture.drawio\ninclude/tracesmith/*"),
        ("YIRAGE YPK", "docs/yirage-architecture.drawio\ninclude/backend/*.h"),
        ("JAX-SKLEARN", "xlearn/_jax/*.py\nxlearn/__init__.py"),
        ("SECRET-LEARN", "docs/secret_learn_architecture.drawio\nsrc/secretlearn/"),
        ("YOUTUBE-DNN", "docs/architecture.drawio\nsrc/python + src/scala"),
        ("RESEARCH CLI", "packages/cli + packages/core\nmodelRouterService.ts"),
        ("QUESTIONS-GEN", "src/QuestionsGenTrainer.py\nquestions_gen/"),
    ]
    x = 40
    for title, files in cards:
        cell(page, title, files.replace("\n", "<br>"), x, 160, 220, 140, "box")
        x += 236
    cell(
        page,
        "STYLE",
        "dark canvas · nested containers · Courier · real paths · no invented layers",
        40,
        340,
        1640,
        70,
        "hl",
    )
    footer(page, "v1.0  ·  2026-08-24  ·  github.com/chenxingqiang  ·  source: docs/architecture/drawio/")
    write_file(file)


def tracesmith() -> None:
    """TraceSmith docs/architecture.drawio + src/include tree."""
    file, page = new_file("tracesmith")
    header(
        page,
        "TRACESMITH — SYSTEM ARCHITECTURE",
        "GPU Profiling & Replay  ·  C++17 core + pybind11  ·  source: docs/architecture.drawio  ·  github.com/chenxingqiang/TraceSmith",
    )

    apps = lane(page, "APPLICATION LAYER", 20, 88, 1680, 108)
    a = row(
        page,
        apps,
        [
            ("C++ Application", "user binary", "box"),
            ("Python Application", "import tracesmith", "box"),
            ("C++ CLI", "cli/main.cpp", "box"),
            ("Python CLI", "python/tracesmith/cli.py", "box"),
            ("External Tools", "Perfetto UI / Chrome", "out"),
        ],
        y=36,
        h=60,
    )

    bind = lane(page, "PYTHON BINDINGS", 20, 206, 1680, 88)
    b = row(
        page,
        bind,
        [
            ("pybind11 module", "python/src/bindings.cpp", "hl"),
            ("_tracesmith.so", "native extension", "hl"),
            ("python/tracesmith/__init__.py", "package API", "box"),
        ],
        y=34,
        h=42,
    )

    core = lane(page, "TRACESMITH CORE LIBRARY (C++17)  include/tracesmith + src/", 20, 304, 1680, 430)
    cap = row(
        page,
        core,
        [
            ("CUPTIProfiler", "src/capture/cupti_profiler.cpp", "hl"),
            ("MCPTIProfiler", "src/capture/mcpti_profiler.cpp", "box"),
            ("MetalProfiler", "src/capture/metal_profiler.mm", "box"),
            ("AscendProfiler", "src/capture/ascend_profiler.cpp", "box"),
            ("ROCmProfiler", "src/capture/rocm_profiler.cpp", "box"),
            ("BPFTracer", "src/capture/bpf_tracer.cpp", "box"),
            ("MemoryProfiler", "src/capture/memory_profiler.cpp", "box"),
        ],
        y=34,
        h=58,
    )
    com = row(
        page,
        core,
        [
            ("RingBuffer SPSC", "common/ring_buffer.hpp", "hl"),
            ("Types / TraceEvent", "src/common/types.cpp", "box"),
            ("StackCapture", "src/common/stack_capture.cpp", "box"),
            ("XRayImporter", "src/common/xray_importer.cpp", "box"),
            ("SBTWriter/Reader", "src/format/sbt_format.cpp", "hl"),
        ],
        y=104,
        h=58,
    )
    st = row(
        page,
        core,
        [
            ("GPUStateMachine", "src/state/gpu_state_machine.cpp", "box"),
            ("InstructionStream", "src/state/instruction_stream.cpp", "box"),
            ("TimelineBuilder", "src/state/timeline_builder.cpp", "box"),
            ("TimelineViewer", "src/state/timeline_viewer.cpp", "box"),
            ("PerfettoExporter", "src/state/perfetto_exporter.cpp", "out"),
            ("PerfettoProto", "src/state/perfetto_proto_exporter.cpp", "out"),
        ],
        y=174,
        h=58,
    )
    rp = row(
        page,
        core,
        [
            ("ReplayEngine", "src/replay/replay_engine.cpp", "alt"),
            ("StreamScheduler", "src/replay/stream_scheduler.cpp", "alt"),
            ("OperationExecutor", "src/replay/operation_executor.cpp", "alt"),
            ("DeterminismChecker", "src/replay/determinism_checker.cpp", "alt"),
            ("FrameCapture", "src/replay/frame_capture.cpp", "alt"),
        ],
        y=244,
        h=58,
    )
    cl = row(
        page,
        core,
        [
            ("GPUTopology", "src/cluster/gpu_topology.cpp", "box"),
            ("MultiGPUProfiler", "src/cluster/multi_gpu_profiler.cpp", "box"),
            ("TimeSync NTP/PTP", "src/cluster/time_sync.cpp", "box"),
            ("NCCLTracker", "src/cluster/nccl_tracker.cpp", "box"),
            ("GDB RSP", "src/gdb/rsp_handler.cpp", "box"),
            ("TracyExporter", "src/tracy/tracy_exporter.cpp", "box"),
        ],
        y=314,
        h=58,
    )

    hw = lane(page, "GPU BACKENDS & SYSTEM  (createProfiler + nsys / mcTracer / xctrace / msprof)", 20, 746, 1680, 108)
    row(
        page,
        hw,
        [
            ("NVIDIA CUDA", "CUPTI SDK + nsys", "hl"),
            ("Apple Metal", "Metal API + xctrace", "box"),
            ("MetaX MACA", "MCPTI + mcTracer", "box"),
            ("Huawei Ascend", "CANN + msprof", "box"),
            ("AMD ROCm", "roctracer", "box"),
            ("Linux eBPF", "kernel events", "box"),
            ("libunwind", "host stacks", "box"),
            ("Perfetto SDK", "protobuf", "out"),
        ],
        y=36,
        h=60,
    )

    outp = lane(page, "OUTPUT FORMATS", 20, 866, 1680, 88)
    row(
        page,
        outp,
        [
            ("trace.sbt", "SBT binary", "out"),
            ("trace.json", "Perfetto JSON", "out"),
            ("trace.perfetto", "protobuf", "out"),
            ("graph.dot", "Graphviz", "out"),
            ("ASCII timeline", "terminal", "out"),
            ("comm matrix", "NCCL heatmap", "out"),
        ],
        y=34,
        h=42,
    )

    arrow(page, a[3], b[0], CYAN)
    arrow(page, b[0], cap[0], ORANGE, True, "native")
    arrow(page, cap[0], com[0], CYAN, False, "events")
    arrow(page, com[0], com[4], CYAN)
    arrow(page, com[4], st[2], CYAN)
    arrow(page, st[2], rp[0], PURPLE, True, "replay")
    arrow(page, st[4], a[4], GREEN, True, "ui")
    footer(page, "v0.10+  ·  capture→ring→SBT→state/timeline→replay/export  ·  files from include/tracesmith and src/")
    write_file(file)


def yirage() -> None:
    """YiRage docs/yirage-architecture.drawio + include/backend/*.h."""
    file, page = new_file("yirage")
    header(
        page,
        "YIRAGE (YPK) — SYSTEM ARCHITECTURE",
        "RuntimeFusion × Multi-Backend  ·  source: docs/yirage-architecture.drawio + include/backend/*.h  ·  github.com/chenxingqiang/YiRage",
    )

    eng = lane(page, "INFERENCE ENGINE  (scheduling + KV owner)", 20, 88, 1680, 100)
    e = row(
        page,
        eng,
        [
            ("vLLM", "continuous batch · PagedAttention", "box"),
            ("SGLang", "RadixAttention · extend meta", "box"),
            ("meta", "block_table · seq_lens · SM budget", "box"),
        ],
        y=36,
        h=52,
    )

    rf = lane(page, "RUNTIMEFUSION  yirage.serving  ·  RF.step(inputs, meta) selects 0..N capsules / decode step", 20, 200, 1680, 120)
    r = row(
        page,
        rf,
        [
            ("RF.step()", "yirage.serving", "hl"),
            ("FusionCapsule MLP", "gate_up + down  yirage.core", "hl"),
            ("FusionCapsule seg", "gate_up → down pipeline", "box"),
            ("skip / fallback", "engine native ops", "alt"),
        ],
        y=36,
        h=70,
    )

    search = lane(page, "SEARCH & PLAN  (offline / warm-up)", 20, 332, 1680, 110)
    s = row(
        page,
        search,
        [
            ("superoptimize(backend)", "KN/TB graph search", "box"),
            ("FusionPlan / µGraph", "profile + fingerprint verify", "hl"),
            ("MuGraph cache", "shape-bucket restore", "box"),
            ("Ray coordinator", "distributed search optional", "box"),
            ("serving tiers", "seed_verify · full_tb · full_tb_ray", "box"),
        ],
        y=36,
        h=62,
    )

    api = lane(page, "PYTHON API & BACKEND MANAGER (C++)", 20, 454, 1680, 120)
    p = row(
        page,
        api,
        [
            ("PersistentKernel", "python/yirage", "box"),
            ("KNGraph / TBGraph", "transpiler → kernels", "box"),
            ("BackendRegistry", "include/backend/backend_registry.h", "hl"),
            ("yirage.core", "Cython runtime", "box"),
            ("KernelExecutor factory", "search + execute same backend", "box"),
        ],
        y=36,
        h=70,
    )

    be = lane(page, "BACKEND IMPLEMENTATIONS  include/backend/*.h + include/kernel/{cuda,maca,cpu,mps,ascend}/", 20, 586, 1680, 200)
    row(
        page,
        be,
        [
            ("CUDA", "cuda_backend.h  warp 32  nvcc", "hl"),
            ("MACA", "maca_backend.h  warp 64  mxcc", "box"),
            ("ROCm", "rocm_backend.h  AMD GPU", "box"),
            ("MPS", "mps_backend.h  Apple GPU", "box"),
            ("Ascend", "ascend_backend.h  CANN", "box"),
            ("CPU", "cpu_backend.h  OpenMP/MKL", "box"),
            ("Triton", "triton_backend.h  DSL", "box"),
            ("NKI", "nki_backend.h  SBUF/DMA", "box"),
        ],
        y=36,
        h=70,
    )
    row(
        page,
        be,
        [
            ("cuDNN", "cudnn_backend.h", "box"),
            ("MKL", "mkl_backend.h", "box"),
            ("TPU", "tpu_backend.h", "box"),
            ("XPU", "xpu_backend.h", "box"),
            ("MLIR", "mlir_backend.h  CPU JIT", "box"),
            ("FPGA", "fpga_backend.h  experimental", "alt"),
        ],
        y=118,
        h=62,
    )

    hw = lane(page, "HARDWARE TARGETS", 20, 798, 1680, 100)
    row(
        page,
        hw,
        [
            ("NVIDIA GPU", "Ampere / Hopper", "hl"),
            ("MetaX C500/C550", "MACA", "box"),
            ("x86 / ARM CPU", "Intel / AMD / Apple", "box"),
            ("Apple Silicon", "M1–M4", "box"),
            ("Huawei Ascend", "910 / 910B / 310P", "box"),
            ("AWS Neuron / Intel XPU", "NKI", "box"),
        ],
        y=36,
        h=52,
    )

    arrow(page, e[0], r[0], CYAN, False, "decode")
    arrow(page, r[0], r[1], ORANGE, True, "capsule")
    arrow(page, s[1], r[0], PURPLE, True, "plan")
    arrow(page, p[2], s[0], CYAN)
    footer(page, "Engine owns scheduling & KV; RF owns fusion identity per step  ·  BackendRegistry search+execute same backend")
    write_file(file)


def jax_sklearn() -> None:
    """xlearn/_jax source tree — no invented layers."""
    file, page = new_file("jax-sklearn")
    header(
        page,
        "JAX-SKLEARN (xlearn) — SYSTEM ARCHITECTURE",
        "drop-in sklearn  ·  files: xlearn/__init__.py + xlearn/_jax/*.py  ·  github.com/chenxingqiang/jax-sklearn",
    )

    user = lane(page, "USER CODE", 20, 88, 1680, 90)
    row(
        page,
        user,
        [
            ("import xlearn as sklearn", "public API", "box"),
            ("LinearRegression / KMeans / PCA", "xlearn.linear_model · cluster · decomposition", "box"),
            ("set_config / config_context", "xlearn/_jax/_config.py", "box"),
        ],
        y=34,
        h=44,
    )

    init = lane(page, "PACKAGE INIT  xlearn/__init__.py", 20, 190, 1680, 110)
    i = row(
        page,
        init,
        [
            ("__getattr__(name)", "lazy submodule import", "hl"),
            ("_JAX_ENABLED", "import xlearn._jax", "box"),
            ("_auto_jax_accelerate_module", "replace estimator classes", "hl"),
            ("AcceleratorRegistry", "xlearn/_jax/_accelerator.py", "box"),
        ],
        y=36,
        h=62,
    )

    proxy = lane(page, "PROXY  xlearn/_jax/_proxy.py", 20, 314, 1680, 130)
    p = row(
        page,
        proxy,
        [
            ("create_intelligent_proxy", "wrap estimator type", "hl"),
            ("EstimatorProxy.__init__", "_create_implementation()", "box"),
            ("JAX path", "create_accelerated_estimator", "box"),
            ("sklearn fallback", "original_class(*args)", "alt"),
        ],
        y=36,
        h=80,
    )

    jax = lane(page, "JAX KERNELS  xlearn/_jax/", 20, 456, 1680, 160)
    row(
        page,
        jax,
        [
            ("_universal_jax.py", "generic mixins JIT/vmap", "box"),
            ("_accelerator.py", "dispatch + registry", "box"),
            ("_data_conversion.py", "NumPy ↔ JAX", "box"),
            ("_gp.py", "Gaussian process", "box"),
            ("_mlp.py", "neural_network", "box"),
            ("_svm.py", "SVM", "box"),
            ("_tree.py", "trees", "box"),
        ],
        y=36,
        h=110,
    )

    cfg = lane(page, "CONFIG / HEURISTICS  xlearn/_jax/_config.py", 20, 630, 1680, 120)
    row(
        page,
        cfg,
        [
            ("enable_jax", "on/off", "box"),
            ("jax_platform", "cpu | gpu | tpu | metal", "box"),
            ("LinearRegression", "min_complexity 1e8", "box"),
            ("KMeans", "min_complexity 1e6", "box"),
            ("PCA", "min_complexity 1e7", "box"),
        ],
        y=36,
        h=70,
    )

    hw = lane(page, "HARDWARE  (JAX backends)", 20, 764, 1680, 100)
    row(
        page,
        hw,
        [
            ("CPU jaxlib", "default", "box"),
            ("CUDA jax[gpu]", "NVIDIA", "hl"),
            ("TPU jax[tpu]", "Google Cloud", "box"),
            ("Metal jax-metal", "Apple experimental", "alt"),
        ],
        y=36,
        h=52,
    )

    arrow(page, i[0], i[2], CYAN)
    arrow(page, i[2], p[0], ORANGE, True, "inject")
    arrow(page, p[1], p[2], CYAN, False, "JAX")
    arrow(page, p[1], p[3], PURPLE, True, "fallback")
    footer(page, "Injection is lazy: xlearn.__getattr__ → proxy class in module → fit() chooses JAX or sklearn")
    write_file(file)


def secret_learn() -> None:
    """docs/secret_learn_architecture.drawio + src/secretlearn/."""
    file, page = new_file("secret-learn")
    header(
        page,
        "SECRET-LEARN — SYSTEM ARCHITECTURE",
        "Privacy-preserving ML  ·  source: docs/secret_learn_architecture.drawio + src/secretlearn/  ·  github.com/chenxingqiang/Secret-Learn",
    )

    app = lane(page, "APPLICATION & USE CASES", 20, 88, 1680, 90)
    row(
        page,
        app,
        [
            ("Healthcare", "hospital FL", "box"),
            ("Finance", "cross-bank fraud", "box"),
            ("IoT / Edge", "distributed sensors", "box"),
            ("Research", "multi-institution", "box"),
            ("Government", "census / tax", "box"),
        ],
        y=34,
        h=44,
    )

    api = lane(page, "SKLEARN-COMPATIBLE API  191 algorithms", 20, 190, 1680, 100)
    row(
        page,
        api,
        [
            ("Linear 39", "Ridge Lasso SGD", "box"),
            ("Ensemble 18", "RF AdaBoost", "box"),
            ("Clustering 14", "KMeans DBSCAN", "box"),
            ("Decomposition 14", "PCA NMF ICA", "box"),
            ("SVM 7", "SVC SVR NuSVC", "box"),
            ("NN 4", "MLP BernoulliRBM", "box"),
            ("+95", "neighbors trees NB …", "box"),
        ],
        y=36,
        h=52,
    )

    modes = lane(page, "PRIVACY MODES  src/secretlearn/{federated_learning,secret_sharing,split_learning}/", 20, 304, 1680, 200)
    row(
        page,
        modes,
        [
            ("FEDERATED LEARNING", "federated_learning/\nFLLinearRegression\nlocal PYU · HEU aggregate\n191 algos · 3–5×", "box"),
            ("SECRET SHARING", "secret_sharing/\nSSPCA\nSPU MPC ABY3/CHEETAH\n191 algos · max privacy", "hl"),
            ("SPLIT LEARNING", "split_learning/\nSLMLPClassifier\nmodel split · HEU acts\n191 algos · vertical FL", "box"),
        ],
        y=36,
        h=150,
    )

    intel = lane(page, "INTELLIGENT SYSTEM + JAX", 20, 518, 1680, 130)
    row(
        page,
        intel,
        [
            ("algorithm_classifier.py", "src/secretlearn/algorithm_classifier.py", "hl"),
            ("JIT / XLA", "xlearn backend", "box"),
            ("jax.vmap", "batch + autodiff", "box"),
            ("smart fallback", "original sklearn", "alt"),
        ],
        y=36,
        h=80,
    )

    dev = lane(page, "SECRETFLOW DEVICES", 20, 662, 1680, 120)
    row(
        page,
        dev,
        [
            ("PYU", "plaintext party compute", "box"),
            ("HEU", "homomorphic aggregate", "hl"),
            ("SPU", "MPC ABY3 / CHEETAH", "hl"),
            ("TEE", "trusted execution", "box"),
        ],
        y=36,
        h=70,
    )

    hw = lane(page, "INFRASTRUCTURE & HARDWARE", 20, 796, 1680, 90)
    row(
        page,
        hw,
        [
            ("CPU 1.5–2.5×", "local JAX", "box"),
            ("GPU 5–8×", "CUDA", "box"),
            ("TPU 9–15×", "Google", "box"),
            ("M1/M2 2–4×", "Metal beta", "alt"),
        ],
        y=34,
        h=44,
    )

    footer(page, "Same sklearn call surface; mode directory picks FL / SS / SL  ·  191 × 3 = 573 implementations")
    write_file(file)


def youtube_recsys() -> None:
    """docs/architecture.drawio + src/python and src/scala files."""
    file, page = new_file("youtube-recsys")
    header(
        page,
        "YOUTUBE-DNN-RECSYS — SYSTEM ARCHITECTURE",
        "Covington two-tower recall  ·  source: docs/architecture.drawio  ·  github.com/chenxingqiang/YouTube-DNN-RecSys",
    )

    data = lane(page, "DATA PROCESSING", 20, 88, 1680, 140)
    d = row(
        page,
        data,
        [
            ("data2tfrecords.py", "src/python/data/data2tfrecords.py\nrandom + TFRecords train/eval", "box"),
            ("read_tfrecords.py", "src/python/data/read_tfrecords.py", "box"),
            ("MakeDataOne.scala", "src/scala/data/MakeDataOne.scala\nSpark distributed generate", "alt"),
            ("MakeDataTwo.scala", "src/scala/data/MakeDataTwo.scala\nHDFS TFRecords", "alt"),
        ],
        y=36,
        h=90,
    )

    store = lane(page, "STORAGE", 20, 240, 1680, 80)
    row(
        page,
        store,
        [
            ("data/tfrecords/", "train + eval TFRecords", "out"),
            ("data/checkpoints/", "TF ckpt + SavedModel", "out"),
        ],
        y=32,
        h=36,
    )

    train = lane(page, "MODEL  src/python/models/dnn.py  (TensorFlow Estimator)", 20, 332, 1680, 180)
    t = row(
        page,
        train,
        [
            ("Input", "visit_items_index (5)\ncontinuous_features (16)", "box"),
            ("Embedding", "item table 500 × 16\naverage pooling on history", "hl"),
            ("MLP tower", "dense layers → user vector u", "box"),
            ("Softmax", "500-way next-item\ncross entropy · Top-K", "hl"),
        ],
        y=36,
        h=128,
    )

    pred = lane(page, "PREDICTION", 20, 526, 1680, 150)
    pr = row(
        page,
        pred,
        [
            ("load_dnn_model.py", "src/python/models/load_dnn_model.py\nSavedModel online / batch", "box"),
            ("PredictUserVector.scala", "src/scala/prediction/PredictUserVector.scala", "alt"),
            ("ItemEmbeddingPredictor.scala", "src/scala/prediction/ItemEmbeddingPredictor.scala", "alt"),
            ("ItemEmbedding.scala", "src/scala/models/ItemEmbedding.scala", "alt"),
        ],
        y=36,
        h=100,
    )

    util = lane(page, "UTILITIES & CONFIG", 20, 690, 1680, 150)
    row(
        page,
        util,
        [
            ("tensor_board.py", "src/python/utils/tensor_board.py", "box"),
            ("feature_column.py", "src/python/reference/feature_column.py", "box"),
            ("self_defined_network_layer.py", "src/python/reference/self_defined_network_layer.py", "box"),
            ("FeatureBuilder.scala", "src/scala/models/FeatureBuilder.scala", "alt"),
            ("BaseSparkLocal/Online", "src/scala/core/*.scala", "alt"),
            ("vars.prod/sit.properties", "src/scala/config/", "alt"),
        ],
        y=36,
        h=100,
    )

    arrow(page, d[0], t[0], CYAN, False, "TFRecords")
    arrow(page, t[3], pr[0], GREEN, True, "SavedModel")
    footer(page, "Python/TF path and Scala/Spark path share TFRecords + the same two-tower (history pool → user vec · item table)")
    write_file(file)


def research_cli() -> None:
    """packages/cli + packages/core source tree."""
    file, page = new_file("research-cli")
    header(
        page,
        "RESEARCH CLI — SYSTEM ARCHITECTURE",
        "TypeScript monorepo  ·  packages/cli + packages/core  ·  github.com/iechor-research/research-cli",
    )

    ui = lane(page, "packages/cli", 20, 88, 1680, 130)
    u = row(
        page,
        ui,
        [
            ("research.tsx / TUI", "packages/cli/src", "box"),
            ("commands/", "mcp.ts skills.tsx hooks.tsx", "box"),
            ("config/config.ts", "packages/cli/src/config/config.ts", "box"),
            ("acp/", "acpSession.ts acpCommandHandler.ts", "box"),
        ],
        y=36,
        h=80,
    )

    core = lane(page, "packages/core  orchestration", 20, 230, 1680, 150)
    c = row(
        page,
        core,
        [
            ("config.ts", "packages/core/src/config/config.ts", "box"),
            ("research-config-manager.ts", "packages/core/src/config/", "box"),
            ("modelRouterService.ts", "packages/core/src/routing/", "hl"),
            ("routingStrategy.ts", "default/classifier/composite", "box"),
            ("memory.ts / storage.ts", "session + compress", "box"),
        ],
        y=36,
        h=100,
    )

    tools = lane(page, "TOOLS + MCP", 20, 394, 1680, 130)
    row(
        page,
        tools,
        [
            ("workspace tools", "fs / shell  packages/core/src/tools", "box"),
            ("MCP", "packages/cli/src/commands/mcp.ts", "hl"),
            ("sandbox", "config/sandbox-integration", "box"),
            ("packages/sdk", "programmatic embed", "box"),
            ("packages/a2a-server", "agent protocol", "box"),
            ("vscode-ide-companion", "IDE bridge", "box"),
        ],
        y=36,
        h=80,
    )

    research = lane(page, "ACADEMIC MODULES  packages/core/src/tools/research/", 20, 538, 1680, 130)
    row(
        page,
        research,
        [
            ("writing", "outline / LaTeX", "alt"),
            ("bibliography", "arXiv / PubMed / BibTeX", "alt"),
            ("analysis", "stats / citation net", "alt"),
            ("investigation", "experiment codegen", "alt"),
            ("submission", "journal matcher", "alt"),
        ],
        y=36,
        h=80,
    )

    providers = lane(page, "PROVIDERS  model-provider-config.ts + /model config", 20, 682, 1680, 110)
    pv = row(
        page,
        providers,
        [
            ("Gemini / Vertex", "", "box"),
            ("OpenAI", "", "box"),
            ("Anthropic", "", "box"),
            ("Baidu ERNIE", "", "box"),
            ("DeepSeek", "", "box"),
            ("Qwen / Groq / Kimi", "", "box"),
        ],
        y=36,
        h=60,
    )

    arrow(page, u[0], c[0], CYAN)
    arrow(page, c[2], pv[0], ORANGE, True, "route")
    footer(page, "CLI TUI → core config/router → provider + tools/MCP/research modules → streamed result")
    write_file(file)


def questions_gen() -> None:
    """src/*.py + questions_gen/ package."""
    file, page = new_file("questions-gen")
    header(
        page,
        "QUESTIONS-GEN — SYSTEM ARCHITECTURE",
        "Qwen3-14B contest problems  ·  src/*.py + questions_gen/  ·  github.com/chenxingqiang/GenQuestion",
    )

    data = lane(page, "DATA", 20, 88, 1680, 110)
    d = row(
        page,
        data,
        [
            ("QuestionDataPreparer.py", "src/QuestionDataPreparer.py", "box"),
            ("data_preparer.py", "questions_gen/data/data_preparer.py", "box"),
            ("real_math_data_processor.py", "src/real_math_data_processor.py", "box"),
            ("mixture", "historical 50% · variants 30% · novel 20%", "box"),
        ],
        y=36,
        h=62,
    )

    train = lane(page, "THREE-STAGE TRAINER", 20, 212, 1680, 200)
    t = row(
        page,
        train,
        [
            ("QuestionsGenTrainer.py", "src/QuestionsGenTrainer.py\nquestions_gen/core/trainer.py\nStage1 SFT Qwen3-14B", "box"),
            ("RewardCalculator.py", "src/RewardCalculator.py\n0.4 diff 0.3 nov 0.2 rigor 0.1 div", "hl"),
            ("NoveltyConstraint.py", "src/NoveltyConstraint.py\nGRPO 8-problem groups", "hl"),
            ("DeepSeekTeacher.py", "src/DeepSeekTeacher.py\nStage3 distill R1", "box"),
            ("config.py", "src/config.py\nquestions_gen/core/config.py", "box"),
        ],
        y=36,
        h=148,
    )

    val = lane(page, "VALIDATION  questions_gen/validation/", 20, 426, 1680, 130)
    v = row(
        page,
        val,
        [
            ("model_validator.py", "single-model n tests", "box"),
            ("batch_validator.py", "algebra/calculus/geometry/NT", "box"),
            ("quality_evaluator.py", "content clarity difficulty originality", "box"),
        ],
        y=36,
        h=80,
    )

    pkg = lane(page, "PACKAGE / CLI / DEPLOY", 20, 570, 1680, 160)
    row(
        page,
        pkg,
        [
            ("main_cli.py", "questions_gen/cli/main_cli.py\nvalidate batch quality", "box"),
            ("ollama_manager.py", "questions_gen/utils/ollama_manager.py", "out"),
            ("hf_utils.py", "questions_gen/utils/hf_utils.py", "out"),
            ("questions_gen_training.py", "scripts/questions_gen_training.py", "box"),
        ],
        y=36,
        h=110,
    )

    models = lane(page, "ARTIFACTS  Hugging Face xingqiang/*", 20, 746, 1680, 100)
    row(
        page,
        models,
        [
            ("stage1-fp-merged", "SFT", "out"),
            ("stage2-merged-16bit", "GRPO", "out"),
            ("final-merged-16bit", "distill  quality 0.847", "hl"),
            ("Ollama questions-gen-final", "local generate", "out"),
        ],
        y=36,
        h=52,
    )

    arrow(page, d[0], t[0], CYAN)
    arrow(page, t[0], t[1], ORANGE, True, "reward")
    arrow(page, t[1], t[2], ORANGE, True)
    arrow(page, t[3], v[0], GREEN, True, "eval")
    footer(page, "Stage1 SFT → Stage2 GRPO (RewardCalculator + NoveltyConstraint) → Stage3 DeepSeekTeacher → HF/Ollama")
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
