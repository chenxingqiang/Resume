# TraceSmith — GPU Profiling & Replay System

**TraceSmith** is an open-source, cross-platform GPU profiling and replay system for AI compiler engineers, deep learning framework developers, and GPU driver engineers.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/chenxingqiang/TraceSmith/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/tracesmith.svg)](https://pypi.org/project/tracesmith/)
[![GitHub](https://img.shields.io/badge/GitHub-TraceSmith-blue)](https://github.com/chenxingqiang/TraceSmith)
[![C++](https://img.shields.io/badge/C++-17-orange.svg)](https://isocpp.org/)

*Author: Chen Xingqiang (陈星强) · [github.com/chenxingqiang/TraceSmith](https://github.com/chenxingqiang/TraceSmith)*

---

## About

TraceSmith captures GPU execution traces — kernel launches, memory operations, synchronization, and host call stacks — then provides analysis, visualization, and deterministic replay.

It is designed as infrastructure for LLM/AI compiler work: understanding kernel timelines, validating fused operators, and replaying traces without re-running the original workload.

## Key Features

- **High-performance capture**: 10,000+ GPU instruction-level call stacks without interrupting execution; lock-free SPSC ring buffer; `<1%` overhead
- **SBT binary format**: compact traces with string interning and delta timestamps (~3× vs JSON)
- **Multi-platform backends**: NVIDIA CUDA (CUPTI/nsys), AMD ROCm, Apple Metal + Instruments (xctrace), MetaX MACA (MCPTI), Huawei Ascend (CANN/msprof), Linux eBPF
- **Replay engine**: full / partial / dry-run modes; stream scheduler; determinism checker
- **Cluster profiling**: multi-GPU topology, time sync (NTP/PTP/CUDA), NCCL tracking
- **Integrations**: Perfetto (protobuf 85% smaller than JSON), Tracy Profiler, PyTorch Kineto schema, LLVM XRay, GDB RSP GPU debugging
- **Python bindings & CLI**: `pip install tracesmith`; `profile / record / view / export / analyze / replay`

## Architecture (core modules)

| Module | Description |
|--------|-------------|
| Capture | GPU profiling backends (CUPTI, Metal, BPF, Memory, ROCm, Ascend, MACA) |
| Common | Core types, lock-free ring buffer, stack capture, XRay import |
| Format | SBT binary trace format (read/write) |
| State | GPU state machine, timeline builder, Perfetto exporters |
| Replay | Replay engine, stream scheduler, determinism checker |
| Cluster | Multi-GPU profiling, time sync, NCCL tracking |
| GDB | GDB RSP backend, GPU breakpoints, trace replay debugging |

## Benchmark (NVIDIA GeForce RTX 4090 D, CUDA 12.8)

| Metric | Result |
|--------|--------|
| CUDA kernels launched | 10,000 |
| GPU events (CUPTI) | 20,011 |
| Host call stacks | 10,000 (7 frames/stack avg) |
| Events with stacks | 19,989 (99.9%) |
| Total time | 107 ms (non-intrusive) |
| Throughput | 93,457 kernels/sec |
| Event collection overhead | `<1%` |
| Perfetto protobuf | 85% smaller than JSON |

## Resume bullets (EN)

- Designed and built **TraceSmith**, a cross-platform GPU Profiling & Replay System for AI compilers, DL frameworks, and GPU driver engineers (C++ core, Python bindings; PyPI).
- Implemented lock-free SPSC ring-buffer capture of **10,000+** GPU instruction-level call stacks with **<1%** overhead; **93K+** kernels/sec on RTX 4090.
- Delivered multi-backend profilers: NVIDIA CUDA (CUPTI/nsys), AMD ROCm, Apple Metal/xctrace, MetaX MACA, Huawei Ascend (CANN/msprof).
- Built a deterministic replay engine, compact SBT format, and integrations with Perfetto, Tracy, PyTorch Kineto, and GDB RSP.

## Resume bullets (ZH)

- 设计并实现 **TraceSmith** 跨平台 GPU Profiling & Replay 系统，面向 AI 编译器、深度学习框架与 GPU 驱动工程师（C++ 核心、Python 绑定，PyPI 发布）。
- 无锁 SPSC 环形缓冲采集，非侵入捕获 **10,000+** GPU 指令级调用栈，开销 **<1%**；RTX 4090 上吞吐 **93K+** kernels/秒。
- 多后端 Profiler：NVIDIA CUDA（CUPTI/nsys）、AMD ROCm、Apple Metal/xctrace、MetaX MACA、华为昇腾（CANN/msprof）。
- 确定性 Replay 引擎、SBT 二进制格式，并集成 Perfetto、Tracy、PyTorch Kineto 与 GDB RSP GPU 调试。

## Links

- GitHub: https://github.com/chenxingqiang/TraceSmith
- PyPI: https://pypi.org/project/tracesmith/
- DeepWiki: https://deepwiki.com/chenxingqiang/TraceSmith
