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
W, H = 1440, 1230


@dataclass(frozen=True)
class Box:
    title: str
    lines: tuple[str, ...] = ()
    palette: str = "blue"


@dataclass(frozen=True)
class Zone:
    label: str
    boxes: tuple[Box, ...]
    palette: str = "slate"
    height: int = 150


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


def _header(title: str, subtitle: str, locale: str = "zh") -> list[str]:
    legend = {
        "en": ("Primary flow", "Fallback / feedback", "Dashed = architecture zone", "Box = module + responsibility"),
        "zh": ("主数据流", "回退 / 反馈", "虚线框 = 架构分区", "盒内 = 模块 + 职责"),
    }[locale]
    return [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 1230" '
            'font-family="WenQuanYi Micro Hei, DejaVu Sans, sans-serif">'
        ),
        "<defs>",
        '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2563eb"/></marker>',
        '<marker id="arrP" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7c3aed"/></marker>',
        "</defs>",
        '<rect x="0" y="0" width="1440" height="1230" fill="#ffffff"/>',
        _text(40, 44, title, 22, "#111827", 700),
        _text(40, 68, subtitle, 13, "#475569"),
        '<rect x="1035" y="18" width="365" height="54" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>',
        '<line x1="1052" y1="36" x2="1084" y2="36" stroke="#2563eb" stroke-width="2.2" marker-end="url(#arr)"/>',
        _text(1092, 40, legend[0], 11.5),
        '<line x1="1052" y1="58" x2="1084" y2="58" stroke="#7c3aed" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#arrP)"/>',
        _text(1092, 62, legend[1], 11.5),
        _text(1215, 40, legend[2], 11.5),
        _text(1215, 62, legend[3], 11.5),
    ]


def _zone(lines: list[str], zone: Zone, y: int) -> tuple[int, tuple[float, float]]:
    fill, stroke, _ = PALETTES[zone.palette]
    lines.append(
        f'<rect x="40" y="{y}" width="1360" height="{zone.height}" rx="10" '
        f'fill="{fill}" fill-opacity="0.42" stroke="{stroke}" stroke-dasharray="7,5"/>'
    )
    lines.append(_text(56, y + 25, zone.label, 13, "#475569", 700))
    count = len(zone.boxes)
    gap, left = 20, 60
    width = (1320 - gap * (count - 1)) / count
    box_y, box_h = y + 43, zone.height - 61
    for i, item in enumerate(zone.boxes):
        x = left + i * (width + gap)
        bfill, bstroke, btext = PALETTES[item.palette]
        lines.append(
            f'<rect x="{x:.1f}" y="{box_y}" width="{width:.1f}" height="{box_h}" '
            f'rx="8" fill="{bfill}" stroke="{bstroke}"/>'
        )
        n = len(item.lines)
        title_y = box_y + (box_h - 18 * n) / 2 + 5
        lines.append(_text(x + width / 2, title_y, item.title, 13.5, btext, 700, "middle"))
        for j, value in enumerate(item.lines):
            lines.append(_text(x + width / 2, title_y + 19 + j * 17, value, 11.5, btext, 400, "middle"))
    return y + zone.height, (720, y + zone.height)


def build_diagram(title: str, subtitle: str, zones: tuple[Zone, ...],
                  footer: str, feedback: str = "", locale: str = "zh",
                  introduction: tuple[str, str] = ("", "")) -> str:
    lines = _header(title, subtitle, locale)
    overview_label = "PROJECT OVERVIEW" if locale == "en" else "项目介绍"
    lines.extend([
        '<rect x="40" y="82" width="1360" height="55" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>',
        _text(56, 103, overview_label, 11.5, "#475569", 700),
        _text(180, 103, introduction[0], 11.5, "#334155"),
        _text(180, 124, introduction[1], 11.5, "#334155"),
    ])
    y = 150
    boundaries: list[tuple[int, int]] = []
    for zone in zones:
        end, _ = _zone(lines, zone, y)
        boundaries.append((y, end))
        y = end + 20
    for (_, end), (next_y, _) in zip(boundaries, boundaries[1:]):
        lines.append(
            f'<line x1="720" y1="{end}" x2="720" y2="{next_y}" '
            'stroke="#2563eb" stroke-width="2.2" marker-end="url(#arr)"/>'
        )
    if feedback and len(boundaries) > 2:
        start_y = boundaries[-1][0] + 45
        end_y = boundaries[1][0] + 45
        lines.append(
            f'<path d="M 1400,{start_y} L 1420,{start_y} L 1420,{end_y} L 1400,{end_y}" '
            'fill="none" stroke="#7c3aed" stroke-width="1.6" '
            'stroke-dasharray="5,3" marker-end="url(#arrP)"/>'
        )
        lines.append(_text(1388, (start_y + end_y) / 2, feedback, 11, "#7c3aed", 400, "end"))
    lines.append(_text(40, 1202, footer, 11.5, "#475569"))
    lines.append("</svg>")
    return "\n".join(lines)


def tracesmith(locale: str = "zh") -> str:
    return build_diagram(
        "TraceSmith — 系统架构 · GPU Trace 端到端数据流",
        "Application → bindings → capture / state / format → replay & export → GPU backends",
        (
            Zone("APPLICATION · 用户入口", (
                Box("C++ / Python Application", ("嵌入业务进程",), "orange"),
                Box("CLI", ("profile · record · view · export",), "orange"),
                Box("External UI", ("Perfetto · Chrome",), "purple"),
            ), "orange", 125),
            Zone("BINDINGS · Python / C++ 边界", (
                Box("_tracesmith.so", ("pybind11 native extension",), "blue"),
            ), "blue", 112),
            Zone("CORE LIBRARY · C++17", (
                Box("Capture Module", ("CUPTIProfiler · MCPTIProfiler", "Metal · Ascend · ROCm · eBPF"), "green"),
                Box("Common + Format", ("RingBuffer SPSC · StackCapture", "SBTWriter / SBTReader"), "blue"),
                Box("State Module", ("GPUStateMachine", "TimelineBuilder · PerfettoExporter"), "cyan"),
                Box("Replay Module", ("ReplayEngine · StreamScheduler", "DeterminismChecker · FrameCapture"), "purple"),
            ), "blue", 185),
            Zone("CROSS-CUTTING · 集群与调试", (
                Box("Cluster Module", ("GPUTopology · TimeSync", "NCCLTracker"), "yellow"),
                Box("GDB / Tracy", ("RSPHandler · GPUDebugEngine", "TracyExporter"), "pink"),
            ), "slate", 135),
            Zone("GPU BACKENDS · 系统接口", (
                Box("NVIDIA", ("CUDA · CUPTI · nsys",), "green"),
                Box("MetaX", ("MACA · MCPTI · mcTracer",), "cyan"),
                Box("Apple / AMD", ("Metal · xctrace · ROCm",), "slate"),
                Box("Huawei / Linux", ("CANN · msprof · eBPF",), "red"),
            ), "slate", 135),
            Zone("OUTPUTS · Trace 产物", (
                Box("trace.sbt", ("compact binary",), "red"),
                Box("trace.json / .perfetto", ("Perfetto timeline",), "cyan"),
                Box("graph.dot / ASCII", ("analysis views",), "green"),
            ), "cyan", 125),
        ),
        "主链：GPU event → lock-free ring → SBT/state → replay 或 Perfetto；Cluster / GDB 为旁路能力。",
        "replay / debug feedback",
        locale=locale,
        introduction=PROJECT_INTRODUCTIONS["tracesmith"][locale],
    )


def yirage(locale: str = "zh") -> str:
    return build_diagram(
        "YiRage (YPK) — 系统架构 · RuntimeFusion 数据流",
        "Inference engine owns scheduling/KV; RF owns fusion identity; search and execute use the same backend",
        (
            Zone("INFERENCE ENGINE · 调度与 KV 所有者", (
                Box("vLLM", ("continuous batch · PagedAttention",), "orange"),
                Box("SGLang", ("RadixAttention · extend meta",), "orange"),
                Box("Decode Metadata", ("block table · seq lens · SM budget",), "slate"),
            ), "orange", 140),
            Zone("RUNTIMEFUSION · 每个 decode step", (
                Box("RF.step(inputs, meta)", ("select 0..N capsules",), "blue"),
                Box("FusionCapsule", ("MLP gate_up + down", "segment pipeline"), "green"),
                Box("Native Fallback", ("skip → engine native ops",), "purple"),
            ), "blue", 150),
            Zone("SEARCH & PLAN · offline / warm-up", (
                Box("superoptimize(backend)", ("KN / TB graph search",), "blue"),
                Box("FusionPlan / µGraph", ("profile · fingerprint verify",), "green"),
                Box("Persistent Cache", ("shape bucket restore",), "cyan"),
                Box("Ray Coordinator", ("optional distributed search",), "purple"),
            ), "green", 155),
            Zone("BACKEND MANAGER · 编译与执行边界", (
                Box("BackendRegistry", ("search + execute same backend",), "blue"),
                Box("KNGraph / TBGraph", ("transpiler → kernels",), "green"),
                Box("yirage.core", ("Cython runtime",), "slate"),
            ), "blue", 140),
            Zone("BACKENDS → HARDWARE", (
                Box("CUDA / MACA", ("NVIDIA GPU · MetaX C500/C550",), "red"),
                Box("ROCm / MPS", ("AMD GPU · Apple Silicon",), "orange"),
                Box("Ascend / NKI", ("Huawei 910 · AWS Neuron",), "yellow"),
                Box("CPU / MLIR / Triton", ("x86 · ARM · extra targets",), "slate"),
            ), "slate", 145),
        ),
        "主链：Engine metadata → RF.step → FusionCapsule → BackendRegistry → target hardware。",
        "fallback / re-search",
        locale=locale,
        introduction=PROJECT_INTRODUCTIONS["yirage"][locale],
    )


def jax_sklearn(locale: str = "zh") -> str:
    return build_diagram(
        "JAX-sklearn (xlearn) — 五层架构 · 透明加速数据流",
        "100% sklearn API → runtime injection → proxy dispatch → array conversion → JAX hardware",
        (
            Zone("USER CODE · sklearn-compatible API", (
                Box("import xlearn as sklearn", ("LinearRegression · KMeans · PCA",), "orange"),
                Box("Estimator Calls", ("fit · predict · transform",), "orange"),
            ), "orange", 135),
            Zone("COMPATIBILITY · xlearn/__init__.py", (
                Box("__getattr__", ("lazy module loading",), "blue"),
                Box("_auto_jax_accelerate_module", ("runtime class injection",), "blue"),
                Box("AcceleratorRegistry", ("algorithm implementation map",), "green"),
            ), "blue", 150),
            Zone("JAX ACCELERATION · xlearn/_jax", (
                Box("EstimatorProxy", ("fit-time dispatch",), "blue"),
                Box("Universal JAX", ("JIT · vmap · accelerated estimator",), "green"),
                Box("sklearn Fallback", ("original estimator",), "purple"),
            ), "green", 150),
            Zone("DATA MANAGEMENT · boundary conversion", (
                Box("NumPy → JAX", ("dtype · shape normalization",), "cyan"),
                Box("Policy / Thresholds", ("dataset size · platform · config",), "yellow"),
                Box("JAX → NumPy", ("sklearn-compatible outputs",), "cyan"),
            ), "cyan", 145),
            Zone("HARDWARE ABSTRACTION · JAX backend", (
                Box("CPU", ("jaxlib",), "slate"),
                Box("CUDA GPU", ("JAX XLA",), "green"),
                Box("TPU", ("JAX XLA",), "blue"),
                Box("Apple Metal", ("experimental",), "purple"),
            ), "slate", 140),
        ),
        "代理根据算法、数据规模和配置选择 JAX；不满足条件或执行失败时回退原生 sklearn。",
        "graceful fallback",
        locale=locale,
        introduction=PROJECT_INTRODUCTIONS["jax-sklearn"][locale],
    )


def secret_learn(locale: str = "zh") -> str:
    return build_diagram(
        "Secret-Learn — 六层架构 · 隐私计算数据流",
        "sklearn-compatible API → privacy mode → JAX / SecretFlow compute → secure devices",
        (
            Zone("APPLICATION · 多方隐私数据", (
                Box("Healthcare / Finance", ("cross-party modeling",), "orange"),
                Box("IoT / Research", ("distributed learning",), "orange"),
            ), "orange", 125),
            Zone("SKLEARN API · 统一算法入口", (
                Box("secretlearn.*", ("fit · predict · transform",), "blue"),
                Box("algorithm_classifier.py", ("classify fit signature / epochs",), "blue"),
            ), "blue", 130),
            Zone("PRIVACY MODES · execution placement", (
                Box("FEDERATED LEARNING", ("PYU local compute", "HEU secure aggregation"), "yellow"),
                Box("SECRET SHARING", ("SPU MPC · ABY3 / CHEETAH",), "green"),
                Box("SPLIT LEARNING", ("split model · encrypted activations",), "cyan"),
            ), "green", 160),
            Zone("ACCELERATION & COMPUTE", (
                Box("JAX Acceleration", ("JIT · vmap · xlearn",), "pink"),
                Box("SecretFlow Runtime", ("party orchestration",), "purple"),
            ), "purple", 135),
            Zone("SECURE DEVICES", (
                Box("PYU", ("party-local plaintext",), "green"),
                Box("HEU", ("homomorphic aggregation",), "yellow"),
                Box("SPU", ("secure MPC",), "cyan"),
                Box("TEE", ("optional enclave",), "slate"),
            ), "cyan", 140),
            Zone("INFRASTRUCTURE & HARDWARE", (
                Box("SecretFlow", ("distributed secure runtime",), "orange"),
                Box("JAX / XLA", ("CPU · GPU · TPU",), "pink"),
                Box("sklearn", ("API compatibility",), "blue"),
            ), "slate", 125),
        ),
        "同一 sklearn 调用由 FL / SS / SL 决定数据驻留与执行设备；JAX 加速可公开的本地计算。",
        locale=locale,
        introduction=PROJECT_INTRODUCTIONS["secret-learn"][locale],
    )


def youtube_recsys(locale: str = "zh") -> str:
    return build_diagram(
        "YouTube-DNN-RecSys — 系统架构 · 召回数据流",
        "Python / Spark data preparation → TFRecords → dnn.py → user & item vectors → prediction",
        (
            Zone("DATA PROCESSING · 离线样本构建", (
                Box("Python Pipeline", ("data2tfrecords.py", "read_tfrecords.py"), "orange"),
                Box("Spark Pipeline", ("MakeDataOne.scala", "MakeDataTwo.scala"), "purple"),
                Box("FeatureBuilder", ("history + continuous features",), "green"),
            ), "orange", 155),
            Zone("STORAGE · 训练与模型产物", (
                Box("TFRecords", ("train / evaluation",), "green"),
                Box("Checkpoints", ("ckpt / eval / modelpath",), "cyan"),
            ), "green", 135),
            Zone("MODEL TRAINING · src/python/models/dnn.py", (
                Box("Input", ("visit_items_index × 5", "continuous_features × 16"), "blue"),
                Box("Item Embedding", ("500 × 16 · average pooling",), "green"),
                Box("User Tower", ("Dense 64 → 32 → vector 16",), "yellow"),
                Box("Softmax Output", ("500 classes · Top-K",), "orange"),
            ), "pink", 170),
            Zone("PREDICTION · serving paths", (
                Box("Python SavedModel", ("load_dnn_model.py",), "blue"),
                Box("User Vector", ("PredictUserVector.scala",), "purple"),
                Box("Item Table", ("ItemEmbeddingPredictor.scala",), "purple"),
            ), "purple", 145),
            Zone("RECOMMENDATION OUTPUT", (
                Box("Candidate Recall", ("user vector × item embedding",), "cyan"),
                Box("Top-K Items", ("next-item recommendation",), "green"),
            ), "cyan", 130),
        ),
        "主链：行为历史 → TFRecords → embedding mean-pool → user vector → item table matching → Top-K。",
        "evaluation feedback",
        locale=locale,
        introduction=PROJECT_INTRODUCTIONS["youtube-recsys"][locale],
    )


def research_cli(locale: str = "zh") -> str:
    return build_diagram(
        "Research CLI — 系统架构 · Agent 请求数据流",
        "Terminal UI → core orchestration & routing → tools / MCP / research modules → model providers",
        (
            Zone("CLI FRONTEND · packages/cli", (
                Box("Interactive TUI", ("research.tsx · sessions",), "orange"),
                Box("Commands", ("mcp · skills · hooks",), "orange"),
                Box("ACP", ("acpSession.ts",), "purple"),
            ), "orange", 145),
            Zone("CORE ORCHESTRATION · packages/core", (
                Box("Context & Memory", ("config.ts · memory.ts",), "blue"),
                Box("modelRouterService", ("provider selection",), "green"),
                Box("Routing Strategy", ("default · classifier · approval",), "blue"),
            ), "blue", 155),
            Zone("TOOLS & INTEGRATIONS", (
                Box("Workspace Tools", ("filesystem · shell",), "slate"),
                Box("MCP", ("external service adapters",), "green"),
                Box("Research Modules", ("writing · bibliography · analysis",), "purple"),
                Box("SDK / A2A / VS Code", ("embedded clients",), "blue"),
            ), "green", 155),
            Zone("MODEL PROVIDERS · provider config", (
                Box("Gemini / Vertex", ("hosted models",), "blue"),
                Box("OpenAI / Anthropic", ("hosted models",), "green"),
                Box("Baidu / DeepSeek / Qwen", ("hosted models",), "orange"),
            ), "purple", 145),
            Zone("RESULT STREAM", (
                Box("Tool Results", ("structured observations",), "cyan"),
                Box("Assistant Response", ("streamed to terminal",), "green"),
            ), "cyan", 130),
        ),
        "主链：prompt → packages/cli → packages/core router → provider / tools → structured result → terminal。",
        "tool result loop",
        locale=locale,
        introduction=PROJECT_INTRODUCTIONS["research-cli"][locale],
    )


def questions_gen(locale: str = "zh") -> str:
    return build_diagram(
        "Questions-Gen — 系统架构 · 三阶段训练数据流",
        "Training data → SFT → GRPO → DeepSeek distillation → validation → Hugging Face / Ollama",
        (
            Zone("TRAINING DATA · problem mixture", (
                Box("Historical Problems", ("50% source distribution",), "orange"),
                Box("Variants", ("30% conditional variation",), "orange"),
                Box("Novel Problems", ("20% innovation target",), "yellow"),
            ), "orange", 145),
            Zone("Stage 1  SFT · QuestionsGenTrainer.py", (
                Box("Qwen3-14B", ("supervised fine-tuning",), "blue"),
                Box("Stage-1 Checkpoint", ("stage1-fp-merged",), "cyan"),
            ), "blue", 140),
            Zone("Stage 2  GRPO · reward optimization", (
                Box("RewardCalculator", ("0.4 difficulty · 0.3 novelty", "0.2 rigor · 0.1 diversity"), "green"),
                Box("NoveltyConstraint", ("variation / duplication guard",), "yellow"),
                Box("GRPO Trainer", ("group-relative optimization",), "green"),
            ), "green", 165),
            Zone("Stage 3  Distill · teacher supervision", (
                Box("DeepSeekTeacher", ("DeepSeek-R1 reasoning teacher",), "purple"),
                Box("Final Model", ("final-merged-16bit",), "pink"),
            ), "purple", 140),
            Zone("VALIDATION", (
                Box("ModelValidator", ("single checkpoint",), "blue"),
                Box("BatchValidator", ("algebra · geometry · calculus",), "blue"),
                Box("QualityEvaluator", ("clarity · difficulty · originality",), "green"),
            ), "blue", 145),
            Zone("DEPLOYMENT", (
                Box("Hugging Face", ("three published stages",), "cyan"),
                Box("Ollama", ("local inference",), "green"),
                Box("questions-gen CLI", ("validate · batch · quality",), "slate"),
            ), "cyan", 130),
        ),
        "主链：混合题库 → SFT → GRPO reward/novelty → DeepSeek-R1 distill → validate → publish。",
        "quality feedback",
        locale=locale,
        introduction=PROJECT_INTRODUCTIONS["questions-gen"][locale],
    )


def title_page(locale: str = "zh") -> str:
    title = {
        "en": "Open Source Architecture Appendix",
        "zh": "开源项目架构附录",
    }[locale]
    subtitle = {
        "en": "Chen Xingqiang · github.com/chenxingqiang · one project overview and architecture per page",
        "zh": "陈星强 · github.com/chenxingqiang · 每页包含项目介绍与系统架构",
    }[locale]
    lines = _header(title, subtitle, locale)
    projects = (
        Box("TraceSmith", ("GPU profiling & replay",), "green"),
        Box("YiRage", ("RuntimeFusion compiler",), "blue"),
        Box("JAX-sklearn", ("transparent JAX acceleration",), "purple"),
        Box("Secret-Learn", ("privacy-preserving ML",), "yellow"),
        Box("YouTube-DNN", ("two-tower recall",), "orange"),
        Box("Research CLI", ("agent workflow",), "cyan"),
        Box("Questions-Gen", ("three-stage training",), "pink"),
    )
    _zone(lines, Zone("CONTENTS · one architecture per page", projects, "slate", 250), 250)
    reading = {
        "en": (
            "READING GUIDE",
            "Read top to bottom. Dashed containers are architecture zones; boxes are modules and responsibilities.",
            "Solid blue arrows show the primary path; dashed purple arrows show fallback or feedback paths.",
        ),
        "zh": (
            "阅读约定",
            "自上而下读取主数据流；虚线框表示架构分区；盒内仅列模块与职责。",
            "蓝色实线表示主链路，紫色虚线表示回退或反馈，不以源码文件充当架构层。",
        ),
    }[locale]
    lines.extend([
        _text(720, 570, reading[0], 18, "#111827", 700, "middle"),
        _text(720, 610, reading[1], 13, "#475569", 400, "middle"),
        _text(720, 640, reading[2], 13, "#475569", 400, "middle"),
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
