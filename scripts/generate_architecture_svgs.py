#!/usr/bin/env python3
"""Generate clean, zone-based project architecture SVGs.

The visual grammar follows the toolchain-palladium-casemaker reference:
white canvas, dashed subsystem zones, compact responsibility boxes, one
blue end-to-end flow, and an optional dashed purple feedback path.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "docs" / "architecture" / "svg"
PAGE_W = 1720
ZONE_X, ZONE_W = 28, 1560


@dataclass(frozen=True)
class Box:
    title: str
    lines: tuple[str, ...] = ()
    palette: str = "blue"


@dataclass(frozen=True)
class Panel:
    title: str
    boxes: tuple[Box, ...]
    palette: str = "slate"
    columns: int = 2


@dataclass(frozen=True)
class Zone:
    label: str
    palette: str = "slate"
    rows: tuple[tuple[Box, ...], ...] = ()
    panels: tuple[Panel, ...] = ()
    panel_columns: int = 4


PALETTES = {
    "blue": ("#dbeafe", "#2563eb", "#1e3a8a"),
    "green": ("#dcfce7", "#16a34a", "#14532d"),
    "orange": ("#fff7ed", "#ea580c", "#7c2d12"),
    "purple": ("#fdf4ff", "#a21caf", "#701a75"),
    "yellow": ("#fef9c3", "#ca8a04", "#713f12"),
    "red": ("#fee2e2", "#dc2626", "#7f1d1d"),
    "cyan": ("#ecfeff", "#0891b2", "#155e75"),
    "pink": ("#fce7f3", "#db2777", "#831843"),
    "slate": ("#f8fafc", "#64748b", "#1e293b"),
}

PROJECT_INTRODUCTIONS = {
    "tracesmith": {
        "en": (
            "TraceSmith is a cross-platform GPU profiling and deterministic replay system for AI compiler, framework, and driver engineers.",
            "Its C++17 core captures low-overhead execution events, stores compact SBT traces, and exports timelines for analysis and debugging.",
        ),
        "zh": (
            "TraceSmith 是面向 AI 编译器、深度学习框架与 GPU 驱动工程师的跨平台性能分析和确定性回放系统。",
            "C++17 核心以低开销采集执行事件，写入紧凑 SBT 轨迹，并导出时间线用于分析、调试与问题复现。",
        ),
    },
    "yirage": {
        "en": (
            "YiRage is a multi-backend LLM kernel compiler and runtime centered on graph superoptimization and RuntimeFusion.",
            "It searches backend-specific fusion plans offline, then injects verified FusionCapsules into vLLM or SGLang decode steps.",
        ),
        "zh": (
            "YiRage 是面向大模型推理的多后端算子编译与运行时系统，核心能力是计算图超优化和 RuntimeFusion。",
            "系统离线搜索并验证后端特定融合计划，再将 FusionCapsule 注入 vLLM 或 SGLang 的逐步解码流程。",
        ),
    },
    "jax-sklearn": {
        "en": (
            "JAX-sklearn provides a drop-in scikit-learn API while transparently accelerating supported estimators with JAX.",
            "Runtime proxies select JAX or native sklearn by algorithm, data size, and platform, preserving familiar inputs and outputs.",
        ),
        "zh": (
            "JAX-sklearn 在保持 scikit-learn 调用接口不变的前提下，透明地以 JAX 加速受支持的估计器。",
            "运行时代理依据算法、数据规模与硬件平台选择 JAX 或原生 sklearn，并保持输入输出兼容。",
        ),
    },
    "secret-learn": {
        "en": (
            "Secret-Learn exposes sklearn-compatible machine learning across federated, secret-sharing, and split-learning modes.",
            "It combines JAX acceleration with SecretFlow devices so each workflow can choose where plaintext, shares, and activations reside.",
        ),
        "zh": (
            "Secret-Learn 以 sklearn 兼容接口提供联邦学习、秘密分享和拆分学习三种隐私机器学习模式。",
            "系统结合 JAX 加速与 SecretFlow 安全设备，使工作流能够明确控制明文、秘密份额和中间激活的驻留位置。",
        ),
    },
    "youtube-recsys": {
        "en": (
            "YouTube-DNN-RecSys is a TensorFlow and Spark implementation of the candidate-generation stage of YouTube recommendations.",
            "It turns behavior histories into TFRecords, learns user and item embeddings, and produces Top-K recall candidates for serving.",
        ),
        "zh": (
            "YouTube-DNN-RecSys 使用 TensorFlow 与 Spark 实现 YouTube 推荐系统中的候选召回阶段。",
            "系统将用户行为历史转换为 TFRecords，训练用户与物品向量，并为在线服务生成 Top-K 召回候选。",
        ),
    },
    "research-cli": {
        "en": (
            "Research CLI is a terminal-first AI agent workflow that connects interactive sessions to models, tools, and MCP services.",
            "Its core router manages context and provider selection while research modules cover writing, bibliography, analysis, and submission.",
        ),
        "zh": (
            "Research CLI 是终端优先的 AI Agent 工作流，将交互会话连接到模型、工作区工具和 MCP 服务。",
            "核心路由负责上下文与模型供应商选择，研究模块覆盖论文写作、文献管理、数据分析和投稿准备。",
        ),
    },
    "questions-gen": {
        "en": (
            "Questions-Gen is a Qwen3-14B system for generating and evaluating mathematical competition problems through staged training.",
            "The pipeline combines supervised fine-tuning, GRPO reward optimization, DeepSeek-R1 distillation, validation, and local deployment.",
        ),
        "zh": (
            "Questions-Gen 是基于 Qwen3-14B 的数学竞赛题生成与评估系统，采用分阶段训练策略。",
            "训练链路结合监督微调、GRPO 奖励优化、DeepSeek-R1 蒸馏、质量验证以及 Hugging Face 和 Ollama 部署。",
        ),
    },
}


def _text(x: float, y: float, value: str, size=12, color="#334155",
          weight=400, anchor="start", family="") -> str:
    fam = f' font-family="{family}"' if family else ""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}" text-anchor="{anchor}"{fam}>{escape(value)}</text>'
    )


def L(locale: str, en: str, zh: str) -> str:
    return zh if locale == "zh" else en


def B(title: str, *lines: str, palette: str = "blue") -> Box:
    return Box(title, lines, palette)


def P(title: str, boxes: tuple[Box, ...], palette: str = "slate", columns: int = 2) -> Panel:
    return Panel(title, boxes, palette, columns)


def _header(title: str, subtitle: str, locale: str, page_h: int) -> list[str]:
    legend = {
        "en": ("Primary flow", "Fallback / feedback", "Dashed = architecture zone", "Box = module + responsibility"),
        "zh": ("主数据流", "回退 / 反馈", "虚线框 = 架构分区", "盒内 = 模块 + 职责"),
    }[locale]
    return [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PAGE_W} {page_h}" '
            'font-family="WenQuanYi Micro Hei, DejaVu Sans, sans-serif">'
        ),
        "<defs>",
        '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2563eb"/></marker>',
        '<marker id="arrP" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7c3aed"/></marker>',
        "</defs>",
        f'<rect x="0" y="0" width="{PAGE_W}" height="{page_h}" fill="#ffffff"/>',
        _text(28, 42, title, 22, "#111827", 700),
        _text(28, 66, subtitle, 13, "#475569"),
        '<rect x="1248" y="16" width="444" height="54" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>',
        '<line x1="1264" y1="34" x2="1296" y2="34" stroke="#2563eb" stroke-width="2.2" marker-end="url(#arr)"/>',
        _text(1304, 38, legend[0], 11.5),
        '<line x1="1264" y1="56" x2="1296" y2="56" stroke="#7c3aed" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#arrP)"/>',
        _text(1304, 60, legend[1], 11.5),
        _text(1490, 38, legend[2], 11.5),
        _text(1490, 60, legend[3], 11.5),
    ]


def _box_height(box: Box) -> int:
    return 36 + 15 * len(box.lines)


def _panel_height(panel: Panel) -> int:
    columns = max(1, panel.columns)
    height = 30
    for start in range(0, len(panel.boxes), columns):
        chunk = panel.boxes[start:start + columns]
        height += max(_box_height(box) for box in chunk) + 6
    return height + 8


def _zone_height(zone: Zone) -> int:
    height = 36
    for boxes in zone.rows:
        height += max(_box_height(box) for box in boxes) + 8
    columns = max(1, zone.panel_columns)
    for start in range(0, len(zone.panels), columns):
        chunk = zone.panels[start:start + columns]
        height += max(_panel_height(panel) for panel in chunk) + 8
    return height + 8


def _draw_box(lines: list[str], box: Box, x: float, y: float, w: float, h: float) -> None:
    fill, stroke, color = PALETTES[box.palette]
    lines.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="{fill}" stroke="{stroke}"/>'
    )
    block = 14 + 15 * len(box.lines)
    title_y = y + (h - block) / 2 + 11
    lines.append(_text(x + w / 2, title_y, box.title, 12, color, 700, "middle"))
    for index, line in enumerate(box.lines):
        lines.append(_text(x + w / 2, title_y + 16 + index * 15, line, 10.5, color, 400, "middle"))


def _draw_row(lines: list[str], boxes: tuple[Box, ...], x: float, y: float, width: float) -> int:
    gap = 10
    height = max(_box_height(box) for box in boxes)
    box_w = (width - gap * (len(boxes) - 1)) / len(boxes)
    for index, box in enumerate(boxes):
        _draw_box(lines, box, x + index * (box_w + gap), y, box_w, height)
    return height


def _draw_panel(lines: list[str], panel: Panel, x: float, y: float, w: float, h: float) -> None:
    _, stroke, color = PALETTES[panel.palette]
    lines.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="#ffffff" fill-opacity="0.94" stroke="{stroke}"/>'
    )
    lines.append(_text(x + 10, y + 18, panel.title, 12, color, 700))
    columns = max(1, panel.columns)
    gap = 6
    inner_x, inner_w = x + 8, w - 16
    box_w = (inner_w - gap * (columns - 1)) / columns
    cursor_y = y + 28
    for start in range(0, len(panel.boxes), columns):
        chunk = panel.boxes[start:start + columns]
        row_h = max(_box_height(box) for box in chunk)
        for index, box in enumerate(chunk):
            _draw_box(lines, box, inner_x + index * (box_w + gap), cursor_y, box_w, row_h)
        cursor_y += row_h + 6


def _draw_zone(lines: list[str], zone: Zone, y: int) -> int:
    height = _zone_height(zone)
    fill, stroke, _ = PALETTES[zone.palette]
    lines.append(
        f'<rect x="{ZONE_X}" y="{y}" width="{ZONE_W}" height="{height}" rx="10" '
        f'fill="{fill}" fill-opacity="0.38" stroke="{stroke}" stroke-dasharray="7,5"/>'
    )
    lines.append(_text(ZONE_X + 14, y + 22, zone.label, 13, "#475569", 700))
    cursor = y + 34
    inner_x, inner_w = ZONE_X + 12, ZONE_W - 24
    for boxes in zone.rows:
        cursor += _draw_row(lines, boxes, inner_x, cursor, inner_w) + 8
    columns = max(1, zone.panel_columns)
    for start in range(0, len(zone.panels), columns):
        chunk = zone.panels[start:start + columns]
        row_h = max(_panel_height(panel) for panel in chunk)
        gap = 10
        panel_w = (inner_w - gap * (len(chunk) - 1)) / len(chunk)
        for index, panel in enumerate(chunk):
            _draw_panel(lines, panel, inner_x + index * (panel_w + gap), cursor, panel_w, row_h)
        cursor += row_h + 8
    return height


def build_diagram(title: str, subtitle: str, zones: tuple[Zone, ...],
                  footer: str, feedback: str = "", locale: str = "zh",
                  introduction: tuple[str, str] = ("", "")) -> str:
    y = 156
    placed: list[tuple[Zone, int, int]] = []
    for zone in zones:
        height = _zone_height(zone)
        placed.append((zone, y, height))
        y += height + 18
    footer_y = y + 12
    page_h = footer_y + 24
    lines = _header(title, subtitle, locale, page_h)
    overview = "PROJECT OVERVIEW" if locale == "en" else "项目介绍"
    lines.extend([
        f'<rect x="{ZONE_X}" y="84" width="{ZONE_W}" height="58" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>',
        _text(ZONE_X + 14, 106, overview, 11.5, "#475569", 700),
        _text(210, 106, introduction[0], 11.5, "#334155"),
        _text(210, 128, introduction[1], 11.5, "#334155"),
    ])
    boundaries = []
    for zone, zone_y, height in placed:
        _draw_zone(lines, zone, zone_y)
        boundaries.append((zone_y, zone_y + height))
    center = ZONE_X + ZONE_W / 2
    for (_, end), (next_y, _) in zip(boundaries, boundaries[1:]):
        lines.append(
            f'<line x1="{center}" y1="{end}" x2="{center}" y2="{next_y}" '
            'stroke="#2563eb" stroke-width="2.2" marker-end="url(#arr)"/>'
        )
    if feedback and len(boundaries) > 2:
        start_y = boundaries[-1][0] + 36
        end_y = boundaries[1][0] + 36
        lines.append(
            f'<path d="M 1608,{start_y} L 1676,{start_y} L 1676,{end_y} L 1608,{end_y}" '
            'fill="none" stroke="#7c3aed" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#arrP)"/>'
        )
        lines.append(_text(1642, (start_y + end_y) / 2, feedback, 11, "#7c3aed", 400, "middle"))
    lines.append(_text(28, footer_y, footer, 11.5, "#475569"))
    lines.append("</svg>")
    return "\n".join(lines)


def tracesmith(locale: str = "zh") -> str:
    return build_diagram(
        L(locale, "TraceSmith — GPU Profiling & Replay Architecture", "TraceSmith — 系统架构 · GPU Trace 端到端数据流"),
        "Application → _tracesmith.so → Capture / State / Format → Replay → GPU backends → trace outputs",
        (
            Zone(L(locale, "APPLICATION · user entry", "APPLICATION · 用户入口"), "orange", (
                (B("C++ Application", L(locale, "in-process capture", "嵌入业务进程"), palette="orange"),
                 B("Python Application", L(locale, "in-process capture", "嵌入业务进程"), palette="orange"),
                 B("C++ CLI", "tracesmith", "profile · record · view", palette="orange"),
                 B("Python CLI", "tracesmith-cli", "export · analyze · replay", palette="orange"),
                 B("External UI", "Perfetto UI", "Chrome tracing", palette="purple")),
            )),
            Zone(L(locale, "BINDINGS · pybind11 boundary", "BINDINGS · Python / C++ 边界"), "blue", (
                (B("_tracesmith.so", "python/src/bindings.cpp", "pybind11 native extension", palette="blue"),),
            )),
            Zone("CORE LIBRARY · C++17", "blue", panels=(
                P("Cluster Module", (
                    B("GPUTopology", "NVLink · PCIe · NVML", palette="yellow"),
                    B("MultiGPUProfiler", L(locale, "cross-device capture", "跨设备采集"), palette="yellow"),
                    B("TimeSync", "NTP / PTP / CUDA", palette="yellow"),
                    B("NCCLTracker", L(locale, "collective ops", "集合通信"), palette="yellow"),
                    B("ClockCorrelator", L(locale, "clock alignment", "时钟对齐"), palette="yellow"),
                    B("CommAnalysis", L(locale, "communication matrix", "通信矩阵"), palette="yellow"),
                ), "yellow"),
                P("Capture Module", (
                    B("CUPTIProfiler", "NVIDIA CUDA", palette="green"),
                    B("MCPTIProfiler", "MetaX MACA", palette="green"),
                    B("MetalProfiler", "Apple Metal", palette="green"),
                    B("MemoryProfiler", L(locale, "GPU memory", "GPU 内存"), palette="green"),
                    B("AscendProfiler", "Huawei CANN", palette="green"),
                    B("createProfiler()", "nsys · mcTracer", "xctrace · msprof", palette="green"),
                ), "green"),
                P("State Module", (
                    B("GPUStateMachine", L(locale, "state analysis", "状态分析"), palette="cyan"),
                    B("InstructionStream", L(locale, "dependency graph", "依赖图"), palette="cyan"),
                    B("TimelineBuilder", L(locale, "ordered events", "事件排序"), palette="cyan"),
                    B("TimelineViewer", L(locale, "ASCII rendering", "ASCII 渲染"), palette="cyan"),
                    B("PerfettoExporter", "JSON", palette="cyan"),
                    B("PerfettoProtoExporter", "Protobuf", palette="cyan"),
                ), "cyan"),
                P("Replay Module", (
                    B("ReplayEngine", L(locale, "core orchestrator", "回放编排"), palette="purple"),
                    B("StreamScheduler", L(locale, "operation order", "操作顺序"), palette="purple"),
                    B("OperationExecutor", L(locale, "launch replay", "执行回放"), palette="purple"),
                    B("DeterminismChecker", L(locale, "result compare", "结果比对"), palette="purple"),
                    B("FrameCapture", "RenderDoc-style", palette="purple"),
                ), "purple"),
                P("Common Module", (
                    B("Types", "TraceEvent · EventType", "KernelParams", palette="slate"),
                    B("RingBuffer", "lock-free SPSC", palette="slate"),
                    B("StackCapture", "libunwind", palette="slate"),
                    B("XRayImporter", "LLVM XRay", palette="slate"),
                    B("Timestamps", "ns precision", palette="slate"),
                    B("TraceMetadata", "DeviceInfo", palette="slate"),
                )),
                P("Format Module", (
                    B("SBTWriter", L(locale, "binary writer", "二进制写入"), palette="red"),
                    B("SBTReader", L(locale, "binary reader", "二进制读取"), palette="red"),
                    B(".sbt", "header + events", "counters", palette="red"),
                ), "red", 1),
                P("Configuration", (
                    B("ProfilerConfig", L(locale, "buffer · overflow", "缓冲与溢出"), palette="slate"),
                    B("ReplayConfig", L(locale, "mode · speed", "模式与速度"), palette="slate"),
                    B("StackCaptureConfig", L(locale, "stack policy", "调用栈策略"), palette="slate"),
                    B("NCCLTrackerConfig", L(locale, "collective policy", "集合通信策略"), palette="slate"),
                )),
                P("GDB Module", (
                    B("RSPHandler", "GDB protocol", palette="pink"),
                    B("ProcessController", "ptrace / Mach", palette="pink"),
                    B("GPUDebugEngine", L(locale, "breakpoints · replay", "断点与回放"), palette="pink"),
                    B("tracesmith-gdbserver", "v0.10.0", palette="pink"),
                ), "pink"),
            ), panel_columns=4),
            Zone(L(locale, "GPU BACKENDS · system interfaces", "GPU BACKENDS · 系统接口"), "slate", (
                (B("NVIDIA CUDA", "CUPTI SDK", palette="green"),
                 B("Apple Metal", "Metal API", palette="slate"),
                 B("MetaX MACA", "MCPTI SDK", palette="cyan"),
                 B("NCCL", L(locale, "distributed", "分布式"), palette="orange"),
                 B("Nsight Systems", "nsys", palette="green"),
                 B("mcTracer", "MetaX", palette="cyan"),
                 B("xctrace", "Apple", palette="slate"),
                 B("libunwind", L(locale, "host stacks", "主机调用栈"), palette="blue"),
                 B("Perfetto SDK", L(locale, "trace export", "轨迹导出"), palette="purple")),
            )),
            Zone(L(locale, "OUTPUTS · trace artifacts", "OUTPUTS · Trace 产物"), "cyan", (
                (B("trace.sbt", L(locale, "binary format", "二进制格式"), palette="red"),
                 B("trace.json", "Perfetto JSON", palette="cyan"),
                 B("trace.perfetto", "Protobuf", palette="purple"),
                 B("graph.dot", "Graphviz", palette="green"),
                 B("ASCII Timeline", L(locale, "terminal", "终端"), palette="slate"),
                 B("Comm Matrix", L(locale, "heatmap JSON", "热力图 JSON"), palette="yellow")),
            )),
        ),
        L(locale, "Primary path: GPU event → RingBuffer → SBT/state → replay or Perfetto. Cluster, config, and GDB are adjacent capabilities.",
          "主链：GPU event → RingBuffer → SBT/state → replay 或 Perfetto。Cluster、配置与 GDB 是并列能力。"),
        L(locale, "replay", "回放"), locale, PROJECT_INTRODUCTIONS["tracesmith"][locale],
    )


def yirage(locale: str = "zh") -> str:
    return build_diagram(
        L(locale, "YiRage (YPK) — RuntimeFusion Architecture", "YiRage (YPK) — 系统架构 · RuntimeFusion 数据流"),
        "Engine owns schedule + KV; RF owns fusion identity; BackendRegistry searches and executes the same backend",
        (
            Zone(L(locale, "INFERENCE ENGINE · scheduling owner", "INFERENCE ENGINE · 调度与 KV 所有者"), "orange", (
                (B("vLLM", "continuous batch", "PagedAttention", palette="orange"),
                 B("SGLang", "RadixAttention", "extend meta", palette="orange"),
                 B("Decode Metadata", "block_table · seq_lens", "radix hit · SM budget · batch", palette="purple")),
            )),
            Zone("RuntimeFusion · RF.step(inputs, meta)", "green", (
                (B("RF.step", "select 0..N capsules", "per decode step", palette="blue"),
                 B("FusionCapsule", "MLP gate_up + down", "yirage.core", palette="green"),
                 B("FusionCapsule", "segment pipeline", "gate_up → down", palette="green"),
                 B("Native Fallback", "skip → engine native ops", palette="yellow")),
            )),
            Zone(L(locale, "SEARCH & PLAN · offline / warm-up", "SEARCH & PLAN · 离线搜索与预热"), "yellow", (
                (B("superoptimize", "KN / TB graph search", palette="yellow"),
                 B("FusionPlan", "µGraph", "profile + fingerprint", palette="yellow"),
                 B("MuGraph cache", "shape bucket restore", palette="cyan"),
                 B("Ray Coordinator", L(locale, "optional distributed search", "可选分布式搜索"), palette="purple"),
                 B("Serving Tiers", "seed_verify · full_tb", "full_tb_ray", palette="purple")),
            )),
            Zone(L(locale, "PYTHON API & BACKEND MANAGER", "PYTHON API 与 BACKEND MANAGER"), "blue", (
                (B("KNGraph / TBGraph", "transpiler → kernels", palette="blue"),
                 B("BackendRegistry", "search + execute", "same backend", palette="blue"),
                 B("yirage.core", "Cython runtime", palette="slate"),
                 B("yirage.serving", "RF · Capsule · cert", palette="green"),
                 B("MACA Config", "warp = 64 · mxcc", palette="orange"),
                 B("CPU MLIR JIT", L(locale, "optional", "可选"), palette="green")),
            )),
            Zone(L(locale, "BACKEND IMPLEMENTATIONS", "BACKEND IMPLEMENTATIONS · 后端实现"), "orange", (
                (B("CUDA", "nvcc · warp 32", palette="red"),
                 B("MACA", "mxcc · warp 64", palette="orange"),
                 B("CPU", "OpenMP · MKL", palette="green"),
                 B("MPS", "Apple GPU", palette="blue"),
                 B("Ascend", "CANN", palette="red"),
                 B("ROCm", "AMD GPU", palette="red"),
                 B("Triton", "DSL kernels", palette="purple"),
                 B("+ extra", "TPU · XPU", "FPGA · MLIR", palette="slate")),
            )),
            Zone(L(locale, "HARDWARE TARGETS", "HARDWARE TARGETS · 硬件目标"), "slate", (
                (B("NVIDIA GPU", palette="red"),
                 B("MetaX C500/C550", palette="orange"),
                 B("x86 / ARM CPU", palette="green"),
                 B("Apple Silicon", palette="blue"),
                 B("Huawei Ascend", palette="red"),
                 B("AWS Neuron", "Intel XPU", palette="yellow")),
            )),
        ),
        L(locale, "Primary path: decode metadata → RF.step → FusionCapsule → BackendRegistry → selected backend and hardware.",
          "主链：decode metadata → RF.step → FusionCapsule → BackendRegistry → 同一后端与硬件。"),
        L(locale, "fallback", "回退"), locale, PROJECT_INTRODUCTIONS["yirage"][locale],
    )


def jax_sklearn(locale: str = "zh") -> str:
    return build_diagram(
        L(locale, "JAX-sklearn (xlearn) — Transparent Acceleration Architecture", "JAX-sklearn (xlearn) — 五层架构 · 透明加速数据流"),
        "xlearn/__init__.py injects proxies; xlearn/_jax dispatches to JAX or the original sklearn estimator",
        (
            Zone(L(locale, "USER CODE · sklearn-compatible API", "USER CODE · sklearn 兼容接口"), "orange", (
                (B("import xlearn as sklearn", "100% call surface", palette="orange"),
                 B("Estimators", "linear_model · cluster", "decomposition · preprocessing", palette="orange"),
                 B("Calls", "fit · predict · transform", palette="orange")),
            )),
            Zone(L(locale, "COMPATIBILITY · xlearn/__init__.py", "COMPATIBILITY · xlearn/__init__.py"), "blue", (
                (B("__getattr__", L(locale, "lazy submodule import", "惰性导入子模块"), palette="blue"),
                 B("_auto_jax_accelerate_module", L(locale, "replace estimator classes", "替换估计器类"), palette="blue"),
                 B("AcceleratorRegistry", "_accelerator.py", palette="green"),
                 B("create_intelligent_proxy", "_proxy.py", palette="blue"),
                 B("monkey_patch_estimator", L(locale, "install proxy class", "安装代理类"), palette="blue")),
            )),
            Zone(L(locale, "JAX ACCELERATION · xlearn/_jax", "JAX ACCELERATION · xlearn/_jax"), "green", (
                (B("EstimatorProxy", "fit-time dispatch", palette="blue"),
                 B("create_accelerated_estimator", "_accelerator.py", palette="green"),
                 B("_universal_jax.py", "JIT · vmap", palette="green"),
                 B("original_class", L(locale, "sklearn fallback", "sklearn 回退"), palette="purple")),
                (B("_gp.py", "Gaussian process", palette="green"),
                 B("_mlp.py", "neural net", palette="green"),
                 B("_svm.py", "SVM kernels", palette="green"),
                 B("_tree.py", "tree models", palette="green")),
            )),
            Zone(L(locale, "DATA MANAGEMENT · arrays and policy", "DATA MANAGEMENT · 数组与策略"), "cyan", (
                (B("_data_conversion.py", "NumPy ↔ JAX", "dtype · shape", palette="cyan"),
                 B("_config.py", "enable_jax", "jax_platform", palette="yellow"),
                 B("jax_auto_threshold", "complexity >= 1e8", palette="yellow"),
                 B("detect_hardware", "install command", "platform probe", palette="slate")),
            )),
            Zone(L(locale, "HARDWARE · JAX extras", "HARDWARE · JAX 后端"), "slate", (
                (B("CPU", "jax-cpu · jaxlib", palette="slate"),
                 B("CUDA GPU", "jax-gpu", "jax-cuda11", palette="green"),
                 B("TPU", "jax-tpu", palette="blue"),
                 B("Apple Metal", "jax-metal", "float32 · experimental", palette="purple")),
            )),
        ),
        L(locale, "Primary path: sklearn call → injected proxy → JAX estimator. Small data, missing ops, or errors return through original_class.",
          "主链：sklearn 调用 → 注入代理 → JAX 估计器。小数据、缺算子或执行失败时回到 original_class。"),
        L(locale, "fallback", "回退"), locale, PROJECT_INTRODUCTIONS["jax-sklearn"][locale],
    )


def secret_learn(locale: str = "zh") -> str:
    return build_diagram(
        L(locale, "Secret-Learn — Privacy-Preserving ML Architecture", "Secret-Learn — 六层架构 · 隐私计算数据流"),
        "secretlearn API → FL / SS / SL placement → JAX acceleration → SecretFlow devices",
        (
            Zone(L(locale, "APPLICATION · multi-party use cases", "APPLICATION · 多方使用场景"), "orange", (
                (B("Healthcare", L(locale, "hospital collaboration", "跨院协作"), L(locale, "patient privacy", "患者隐私"), palette="orange"),
                 B("Finance", L(locale, "cross-bank analysis", "跨行分析"), L(locale, "fraud detection", "欺诈检测"), palette="orange"),
                 B("IoT / Edge", L(locale, "edge intelligence", "边缘智能"), L(locale, "distributed learning", "分布式学习"), palette="orange"),
                 B("Research", L(locale, "genomics", "基因组"), L(locale, "multi-institution", "多机构"), palette="orange"),
                 B("Government", L(locale, "census analytics", "普查分析"), L(locale, "cross-agency data", "跨部门数据"), palette="orange")),
            )),
            Zone(L(locale, "SKLEARN API · 191 algorithms", "SKLEARN API · 191 个算法"), "purple", (
                (B("Linear Models", "39", "Ridge · Lasso · SGD", palette="purple"),
                 B("Ensemble", "18", "RF · XGBoost", palette="purple"),
                 B("Clustering", "14", "KMeans · DBSCAN", palette="purple"),
                 B("Decomposition", "14", "PCA · NMF · ICA", palette="purple"),
                 B("SVM", "7", "SVC · SVR", palette="purple"),
                 B("Neural Networks", "4", "MLP · BernoulliRBM", palette="purple"),
                 B("+ 95 More", "Neighbors · Trees", "Naive Bayes", palette="slate")),
            )),
            Zone(L(locale, "PRIVACY MODES · execution placement", "PRIVACY MODES · 执行位置"), "green", panels=(
                P(L(locale, "FEDERATED LEARNING", "FEDERATED LEARNING · 联邦学习"), (
                    B("Local PYU", L(locale, "data stays local", "数据留在本地"), palette="yellow"),
                    B("HEU Aggregate", L(locale, "secure averaging", "安全聚合"), palette="yellow"),
                    B("FLLinearRegression", "federated_learning/", palette="yellow"),
                    B("Horizontal FL", "3–5×", palette="yellow"),
                ), "yellow"),
                P(L(locale, "SECRET SHARING", "SECRET SHARING · 秘密分享"), (
                    B("SPU MPC", L(locale, "ciphertext compute", "密文计算"), palette="green"),
                    B("ABY3 / CHEETAH", L(locale, "MPC protocols", "MPC 协议"), palette="green"),
                    B("SSPCA", "secret_sharing/", palette="green"),
                    B("Maximum Privacy", "1–2×", palette="green"),
                ), "green"),
                P(L(locale, "SPLIT LEARNING", "SPLIT LEARNING · 拆分学习"), (
                    B("Model Split", L(locale, "across parties", "跨参与方切分"), palette="cyan"),
                    B("HEU Activations", L(locale, "protected tensors", "保护中间激活"), palette="cyan"),
                    B("SLMLPClassifier", "split_learning/", palette="cyan"),
                    B("Vertical FL", "2–4×", palette="cyan"),
                ), "cyan"),
            ), panel_columns=3),
            Zone(L(locale, "JAX ACCELERATION · xlearn bridge", "JAX ACCELERATION · xlearn 桥接"), "pink", (
                (B("JIT / XLA", L(locale, "traced execution", "跟踪执行"), palette="pink"),
                 B("jax.vmap", L(locale, "batching · autodiff", "批处理与自动微分"), palette="pink"),
                 B("xlearn Backend", L(locale, "JAX-sklearn bridge", "JAX-sklearn 桥"), palette="pink"),
                 B("Smart Fallback", L(locale, "original sklearn", "回退原生 sklearn"), palette="purple"),
                 B("CPU", "1.5–2.5×", palette="slate"),
                 B("GPU", "5–8×", palette="green"),
                 B("TPU", "9–15×", palette="blue"),
                 B("M1 / M2", "2–4×", palette="purple")),
            )),
            Zone(L(locale, "SECURE DEVICES · SecretFlow", "SECURE DEVICES · SecretFlow 设备"), "cyan", panels=(
                P("SPU", (
                    B("MPC", "ABY3 · CHEETAH", palette="cyan"),
                    B("Ciphertext", L(locale, "zero plaintext leak", "不暴露明文"), palette="cyan"),
                ), "cyan", 1),
                P("HEU", (
                    B("Schemes", "Paillier · CKKS", palette="yellow"),
                    B("Aggregation", L(locale, "gradient protection", "梯度保护"), palette="yellow"),
                ), "yellow", 1),
                P("TEE", (
                    B("Enclaves", "Intel SGX · AMD SEV", palette="slate"),
                    B("Occlum", L(locale, "attestation", "证明"), palette="slate"),
                ), "slate", 1),
                P("PYU", (
                    B("Party Local", L(locale, "data ownership", "数据归属"), palette="green"),
                    B("JAX Local", L(locale, "plaintext compute", "本地明文计算"), palette="green"),
                ), "green", 1),
            ), panel_columns=4),
            Zone(L(locale, "INFRASTRUCTURE · runtime stack", "INFRASTRUCTURE · 运行时基础设施"), "orange", (
                (B("SecretFlow", "Ray distributed", "gRPC · DP-SGD", palette="orange"),
                 B("JAX / XLA", "CUDA / cuDNN", "TPU runtime", palette="pink"),
                 B("sklearn", "NumPy · SciPy", palette="blue")),
            )),
        ),
        L(locale, "Primary path: one sklearn call selects FL, SS, or SL, then runs on PYU, HEU, SPU, or TEE.",
          "主链：同一次 sklearn 调用选择 FL、SS 或 SL，再落到 PYU、HEU、SPU 或 TEE。"),
        "", locale, PROJECT_INTRODUCTIONS["secret-learn"][locale],
    )


def youtube_recsys(locale: str = "zh") -> str:
    return build_diagram(
        L(locale, "YouTube-DNN-RecSys — Candidate Generation Architecture", "YouTube-DNN-RecSys — 系统架构 · 召回数据流"),
        "Python / Spark samples → TFRecords → dnn.py user tower → Spark or Python prediction",
        (
            Zone(L(locale, "DATA PROCESSING · offline sample build", "DATA PROCESSING · 数据处理层"), "orange", panels=(
                P(L(locale, "Python Pipeline", "Python 数据处理"), (
                    B("data2tfrecords.py", L(locale, "random training data", "生成训练数据"), palette="orange"),
                    B("TFRecords", L(locale, "train / evaluation", "训练与评估集"), palette="orange"),
                    B("read_tfrecords.py", L(locale, "dataset reader", "数据集读取"), palette="orange"),
                ), "orange", 1),
                P(L(locale, "Spark Pipeline", "Scala + Spark 数据处理"), (
                    B("MakeDataOne.scala", L(locale, "distributed generation", "分布式生成"), palette="purple"),
                    B("MakeDataTwo.scala", "TFRecords output", palette="purple"),
                    B("HDFS", L(locale, "dataset storage", "数据集存储"), palette="purple"),
                ), "purple", 1),
            ), panel_columns=2),
            Zone(L(locale, "STORAGE · datasets and checkpoints", "STORAGE · 存储层"), "green", (
                (B("data/tfrecords/", "train/train.tfrecords", "evaluation/evaluation.tfrecords", palette="green"),
                 B("data/checkpoints/", "ckpt/checkpoint", "ckpt/eval · modelpath/", palette="cyan")),
            )),
            Zone("MODEL TRAINING · dnn.py", "pink", (
                (B("Input", "visit_items_index × 5", "continuous_features × 16", palette="blue"),
                 B("Item Embedding", "500 items × 16", palette="green"),
                 B("Average Pooling", L(locale, "history vector", "历史向量"), palette="green"),
                 B("DNN Tower", "Dense 64 + ReLU", "Dropout · Dense 32 + ReLU", "user vector 16", palette="yellow"),
                 B("Softmax Output", "500 classes", "cross entropy · Top-K", palette="orange")),
            )),
            Zone(L(locale, "PREDICTION · serving paths", "PREDICTION · 预测服务层"), "purple", (
                (B("PredictUserVector.scala", "SavedModel", "embedding_average → user_vector", palette="purple"),
                 B("ItemEmbeddingPredictor.scala", "item embedding table", "FeatureBuilder", palette="purple"),
                 B("load_dnn_model.py", "SavedModel load", L(locale, "online / batch inference", "在线与批量推理"), palette="blue")),
            )),
            Zone(L(locale, "UTILITIES · training support", "UTILITIES · 工具与辅助层"), "slate", (
                (B("tensor_board.py", "TensorBoard", palette="orange"),
                 B("feature_column.py", L(locale, "feature spec", "特征列"), palette="green"),
                 B("self_defined_network_layer.py", L(locale, "custom TF layers", "自定义网络层"), palette="yellow"),
                 B("Spark Base", "BaseSparkLocal.scala", "BaseSparkOnline.scala", palette="purple"),
                 B("Configuration", "vars.prod.properties", "vars.sit.properties", palette="slate")),
            )),
        ),
        L(locale, "Primary path: behavior history → TFRecords → embedding average pool → user vector → item table → Top-K.",
          "主链：行为历史 → TFRecords → embedding average pool → user vector → item table → Top-K。"),
        L(locale, "eval", "评估"), locale, PROJECT_INTRODUCTIONS["youtube-recsys"][locale],
    )


def research_cli(locale: str = "zh") -> str:
    return build_diagram(
        L(locale, "Research CLI — Agent Request Architecture", "Research CLI — 系统架构 · Agent 请求数据流"),
        "packages/cli → packages/core routing → tools / MCP / research modules → model providers",
        (
            Zone("CLI FRONTEND · packages/cli", "orange", (
                (B("research.tsx", L(locale, "interactive TUI", "交互终端"), palette="orange"),
                 B("commands/", "mcp.ts", "skills.tsx · hooks.tsx", palette="orange"),
                 B("ui/commands/research", "arxivCommand", "paper · investigate · submit", palette="yellow"),
                 B("acpSession.ts", "ACP session", "stdio transport", palette="purple")),
            )),
            Zone("CORE ORCHESTRATION · packages/core", "blue", panels=(
                P(L(locale, "Session", "会话"), (
                    B("researchChat.ts", "researchRequest.ts", palette="blue"),
                    B("research-config-manager.ts", L(locale, "academic settings", "学术配置"), palette="blue"),
                    B("config / memory", L(locale, "context window", "上下文"), palette="slate"),
                ), "blue", 1),
                P(L(locale, "Routing", "路由"), (
                    B("modelRouterService", "routing/modelRouterService.ts", palette="green"),
                    B("defaultStrategy", "routingStrategy.ts", palette="green"),
                    B("classifierStrategy", "gemma · numerical", palette="green"),
                    B("compositeStrategy", "approval · fallback", "override", palette="green"),
                ), "green"),
            ), panel_columns=2),
            Zone(L(locale, "TOOLS & RESEARCH MODULES", "TOOLS 与 RESEARCH MODULES"), "green", panels=(
                P("Workspace", (
                    B("edit.ts · grep.ts", "filesystem changes", palette="slate"),
                    B("shell / ls", L(locale, "local execution", "本地执行"), palette="slate"),
                ), "slate", 1),
                P("MCP", (
                    B("mcp-client.ts", L(locale, "server sessions", "服务会话"), palette="green"),
                    B("mcp-client-manager.ts", L(locale, "resource routing", "资源路由"), palette="green"),
                ), "green", 1),
                P("analysis/", (
                    B("bibliography-manager", "citations", palette="purple"),
                    B("experiment-code-generator", "Python · R · Julia", palette="purple"),
                    B("research-data-analyzer", L(locale, "statistics · ML", "统计与机器学习"), palette="purple"),
                ), "purple", 1),
                P("bibliography/", (
                    B("arxiv-mcp-client", "arXiv search", palette="yellow"),
                    B("google-scholar-client", "scholar search", palette="yellow"),
                    B("literature-investigator", "keyword-generator", "reference-classifier", palette="yellow"),
                ), "yellow", 1),
                P("submission/", (
                    B("latex-manager", "project compile", palette="pink"),
                    B("journal-matcher", L(locale, "venue selection", "期刊匹配"), palette="pink"),
                    B("arxiv-latex-extractor", L(locale, "template extract", "模板提取"), palette="pink"),
                ), "pink", 1),
            ), panel_columns=5),
            Zone(L(locale, "MODEL PROVIDERS", "MODEL PROVIDERS · 模型供应商"), "purple", (
                (B("Gemini / Vertex", palette="blue"),
                 B("OpenAI", palette="green"),
                 B("Anthropic", palette="purple"),
                 B("Baidu ERNIE", palette="orange"),
                 B("DeepSeek", palette="cyan"),
                 B("Qwen", palette="yellow"),
                 B("Groq / Mistral", "Cohere · Moonshot", palette="slate")),
            )),
            Zone(L(locale, "EMBEDDED RUNTIMES", "EMBEDDED RUNTIMES · 嵌入运行时"), "cyan", (
                (B("packages/sdk", L(locale, "library embedding", "库嵌入"), palette="cyan"),
                 B("packages/a2a-server", "agent executor", "HTTP task API", palette="blue"),
                 B("vscode-ide-companion", "IDE companion", palette="purple"),
                 B("packages/devtools", L(locale, "development tools", "开发工具"), palette="slate")),
            )),
        ),
        L(locale, "Primary path: prompt → research.tsx → modelRouterService → provider, with tools and research modules supplying observations.",
          "主链：prompt → research.tsx → modelRouterService → provider；工具和研究模块返回观察结果。"),
        L(locale, "loop", "回路"), locale, PROJECT_INTRODUCTIONS["research-cli"][locale],
    )


def questions_gen(locale: str = "zh") -> str:
    return build_diagram(
        L(locale, "Questions-Gen — Three-Stage Training Architecture", "Questions-Gen — 系统架构 · 三阶段训练数据流"),
        "Question data → Qwen3-14B SFT → GRPO reward → DeepSeek-R1 distillation → validation → publish",
        (
            Zone(L(locale, "TRAINING DATA · documented mixture", "TRAINING DATA · 训练数据混合"), "orange", (
                (B("Historical", "50%", "QuestionDataPreparer.py", palette="orange"),
                 B("Conditional Variants", "30%", "data_preparer.py", palette="orange"),
                 B("Innovative Types", "20%", "real_math_data_processor.py", palette="yellow")),
            )),
            Zone(L(locale, "Stage 1 · SFT", "Stage 1 · SFT · 监督微调"), "blue", (
                (B("Qwen3-14B", L(locale, "base checkpoint", "基座模型"), palette="blue"),
                 B("QuestionsGenTrainer.py", "src/ + questions_gen/core/trainer.py", palette="blue"),
                 B("stage1-fp-merged", "Hugging Face", palette="cyan")),
            )),
            Zone(L(locale, "Stage 2 · GRPO", "Stage 2 · GRPO · 奖励优化"), "green", panels=(
                P("RewardCalculator.py", (
                    B("Difficulty", "0.4 difficulty", palette="green"),
                    B("Novelty", "0.3", palette="green"),
                    B("Rigor", "0.2", palette="green"),
                    B("Diversity", "0.1", palette="green"),
                ), "green"),
                P(L(locale, "Optimization", "优化"), (
                    B("GRPO Groups", "8 problems/group", palette="yellow"),
                    B("NoveltyConstraint.py", L(locale, "duplication guard", "重复约束"), palette="yellow"),
                    B("stage2-merged-16bit", "variation generation", palette="cyan"),
                ), "yellow", 1),
            ), panel_columns=2),
            Zone(L(locale, "Stage 3 · Distill", "Stage 3 · Distill · 知识蒸馏"), "purple", (
                (B("DeepSeekTeacher.py", "DeepSeek-R1", palette="purple"),
                 B("Teacher Signals", L(locale, "difficulty · rigor", "难度与严谨性"), L(locale, "innovation · education", "创新与教学价值"), palette="purple"),
                 B("final-merged-16bit", "Hugging Face", palette="pink")),
            )),
            Zone(L(locale, "VALIDATION · questions_gen/validation", "VALIDATION · questions_gen/validation"), "blue", (
                (B("model_validator.py", L(locale, "single checkpoint", "单模型"), palette="blue"),
                 B("batch_validator.py", "algebra · calculus", "geometry · number theory", palette="blue"),
                 B("quality_evaluator.py", "clarity · difficulty", "originality", palette="green")),
            )),
            Zone(L(locale, "DEPLOYMENT · interfaces", "DEPLOYMENT · 发布与接口"), "cyan", (
                (B("main_cli.py", "validate · batch · quality", palette="slate"),
                 B("hf_utils.py", "three published stages", palette="cyan"),
                 B("ollama_manager.py", L(locale, "local inference", "本地推理"), palette="green"),
                 B("examples/", "quick_demo.py", "demo_model_validation.py", palette="yellow")),
            )),
        ),
        L(locale, "Primary path: mixed problem set → SFT → GRPO reward and novelty → DeepSeek-R1 distillation → validate → Hugging Face / Ollama.",
          "主链：混合题库 → SFT → GRPO reward 与 novelty → DeepSeek-R1 蒸馏 → 验证 → Hugging Face / Ollama。"),
        L(locale, "quality", "质量"), locale, PROJECT_INTRODUCTIONS["questions-gen"][locale],
    )


def title_page(locale: str = "zh") -> str:
    projects = (
        B("TraceSmith", L(locale, "GPU profiling & replay", "GPU 采集与回放"), palette="green"),
        B("YiRage", "RuntimeFusion", palette="blue"),
        B("JAX-sklearn", L(locale, "transparent JAX acceleration", "透明 JAX 加速"), palette="purple"),
        B("Secret-Learn", L(locale, "FL · SS · SL", "联邦 · 秘密分享 · 拆分"), palette="yellow"),
        B("YouTube-DNN", L(locale, "candidate generation", "候选召回"), palette="orange"),
        B("Research CLI", L(locale, "agent workflow", "Agent 工作流"), palette="cyan"),
        B("Questions-Gen", L(locale, "three-stage training", "三阶段训练"), palette="pink"),
    )
    zone = Zone(L(locale, "CONTENTS · one architecture per page", "目录 CONTENTS · 每页一个项目"), "slate", (projects,))
    zone_h = _zone_height(zone)
    page_h = 188 + zone_h + 120
    lines = _header(
        L(locale, "Open Source Architecture Appendix", "开源项目架构附录"),
        L(locale, "Chen Xingqiang · github.com/chenxingqiang · module-level architecture with one project overview per page",
          "陈星强 · github.com/chenxingqiang · 每页包含项目介绍与模块级系统架构"),
        locale, page_h,
    )
    _draw_zone(lines, zone, 120)
    reading = {
        "en": (
            "READING GUIDE",
            "Read top to bottom. Dashed frames are architecture zones; inner frames are subsystems; boxes are concrete modules.",
            "Solid blue arrows are the primary path. Dashed purple arrows are fallback or feedback, not extra architecture layers.",
        ),
        "zh": (
            "阅读约定",
            "自上而下阅读。虚线框是架构分区，内层实线框是子系统，小盒子是具体模块。",
            "蓝色实线是主数据流，紫色虚线是回退或反馈，不把源码目录本身当成架构层。",
        ),
    }[locale]
    base = 150 + zone_h
    lines.extend([
        _text(PAGE_W / 2, base, reading[0], 18, "#111827", 700, "middle"),
        _text(PAGE_W / 2, base + 34, reading[1], 13, "#475569", 400, "middle"),
        _text(PAGE_W / 2, base + 58, reading[2], 13, "#475569", 400, "middle"),
        "</svg>",
    ])
    return "\n".join(lines)
DIAGRAMS = {
    "00-title": title_page,
    "tracesmith": tracesmith,
    "yirage": yirage,
    "jax-sklearn": jax_sklearn,
    "secret-learn": secret_learn,
    "youtube-recsys": youtube_recsys,
    "research-cli": research_cli,
    "questions-gen": questions_gen,
}


def build_all(locale: str = "zh") -> list[Path]:
    if locale not in {"en", "zh"}:
        raise ValueError(f"Unsupported locale: {locale}")
    output_dir = SVG_DIR if locale == "zh" else SVG_DIR / locale
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, builder in DIAGRAMS.items():
        path = output_dir / f"{name}.svg"
        path.write_text(builder(locale), encoding="utf-8")
        written.append(path)
        print(f"Wrote {path}")
    return written


def main() -> None:
    build_all("zh")
    build_all("en")


if __name__ == "__main__":
    main()
