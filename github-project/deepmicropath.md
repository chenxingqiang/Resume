# 🎯 多模式服务 - 快速参考

DeepMicroPath 现支持**可选的专业模式**，无需修改原有系统！

---

## 🚀 三种使用方式

### 1️⃣ 原始系统（不受影响）

```bash
cd inference
bash run_react_infer.sh  # 原来怎么用，现在还怎么用
```

### 2️⃣ 自动模式（推荐）

```bash
# 系统自动根据问题选择合适的Prompt
bash run_deepresearch.sh --mode auto --dataset your_data.jsonl
```

### 3️⃣ 指定模式

```bash
# 通用模式
bash run_deepresearch.sh --mode default --dataset questions.jsonl

# 微生物分析模式
bash run_deepresearch.sh --mode microbiology --dataset micro_data.jsonl
```

---

## 📦 新增文件（仅3个核心文件）

```
DeepMicroPath/
├── inference/
│   ├── prompt_selector.py          # ✨ Prompt智能选择器
│   ├── react_agent_wrapper.py      # ✨ 多模式Agent包装器
│   ├── run_react_multimode.sh      # ✨ 多模式启动脚本
│   ├── prompt_microbiology.py      # 📄 微生物专用Prompt（可选）
│   └── run_multi_react_multimode.py # 📄 多模式推理脚本
└── run_deepresearch.sh              # 🎯 统一启动入口
```

**关键特性：**
- ✅ **零代码修改**：原有文件 `react_agent.py`、`run_multi_react.py`、`run_react_infer.sh` 完全不变
- ✅ **向后兼容**：原始使用方式100%保留
- ✅ **可选安装**：只需要时才安装微生物模式

---

## 🔍 工作原理

### 架构图

```
┌─────────────────────────────────────────┐
│         用户问题                         │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     Prompt Selector（智能选择器）        │
│  - 检测问题关键词                        │
│  - 选择合适的Prompt                      │
└─────────────┬───────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
┌─────────┐      ┌──────────────┐
│ Default │      │ Microbiology │
│ Prompt  │      │   Prompt     │
└─────────┘      └──────────────┘
    │                   │
    └─────────┬─────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  MultiModeReactAgent (包装器)           │
│  - 继承原始Agent                         │
│  - 仅覆盖Prompt选择逻辑                  │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  原始 MultiTurnReactAgent               │
│  - 工具调用                              │
│  - 推理逻辑                              │
│  - 完全不变                              │
└─────────────────────────────────────────┘
```

### 自动检测规则

```python
# 微生物分析关键词
keywords = [
    '微生物', '细菌', '真菌', '菌群',
    'gpas', 'result_table', '丰度',
    'microbe', 'bacteria', 'pathogen'
]

# 匹配到 → microbiology模式
# 未匹配 → default模式
```

---

## 📝 使用示例

### 示例1：单个微生物分析

```bash
# 1. 准备CSV数据
cat > inference/eval_data/file_corpus/result.csv << 'EOF'
微生物名称,英文名,Taxonomy_ID,丰度(%),分类
金黄色葡萄球菌,Staphylococcus aureus,1280,45.2,革兰氏阳性菌
EOF

# 2. 创建问题
echo '{"question": "(Uploaded 1 file: [\"result.csv\"])\n\n分析微生物", "answer": ""}' > test.jsonl

# 3. 运行（自动检测为微生物模式）
bash run_deepresearch.sh --dataset test.jsonl
```

### 示例2：通用研究问题

```bash
# 1. 创建问题
echo '{"question": "What is quantum computing?", "answer": ""}' > research.jsonl

# 2. 运行（自动使用通用模式）
bash run_deepresearch.sh --dataset research.jsonl
```

### 示例3：混合问题批处理

```bash
# 数据集包含不同类型问题
cat > mixed.jsonl << 'EOF'
{"question": "量子计算原理是什么？", "answer": ""}
{"question": "分析result_table.csv中的微生物丰度", "answer": ""}
{"question": "Explain blockchain", "answer": ""}
EOF

# 自动为每个问题选择合适的模式
bash run_deepresearch.sh --mode auto --dataset mixed.jsonl
```

---

## ⚙️ 配置

### 环境变量控制

```bash
# 在.env中添加（可选）
PROMPT_MODE=auto          # auto | default | microbiology
```

### 命令行参数

```bash
bash run_deepresearch.sh \
  --mode microbiology \    # 指定模式
  --dataset data.jsonl \   # 数据集
  --output ./reports       # 输出目录
```

---

## 🔧 验证安装

```bash
# 检查系统配置
bash check_microbiology_setup.sh

# 检查可用模式
cd inference
python3 prompt_selector.py
```

期望输出：
```
==================================================
Prompt选择器 - 可用模式
==================================================

default:
  名称: 默认通用模式
  状态: ✅ 可用

microbiology:
  名称: 微生物分析模式
  状态: ✅ 可用
```

---

## 🆚 对比

| 特性 | 原始系统 | 多模式系统 |
|------|---------|-----------|
| **使用方式** | `bash run_react_infer.sh` | `bash run_deepresearch.sh` |
| **Prompt** | 固定（通用） | 可选（自动/通用/专业） |
| **代码修改** | - | 无需修改原有代码 |
| **向后兼容** | - | 100%兼容 |
| **专业模式** | 不支持 | 支持（微生物等） |
| **自动检测** | 否 | 是 |

---

## 🎓 最佳实践

### ✅ 推荐做法

```bash
# 1. 大多数情况使用自动模式
bash run_deepresearch.sh --mode auto --dataset data.jsonl

# 2. 批量处理同类问题时指定模式
bash run_deepresearch.sh --mode microbiology --dataset all_patients.jsonl

# 3. 保持原系统作为备用
cd inference && bash run_react_infer.sh  # 始终可用
```

### ❌ 不推荐做法

```bash
# 不要混合使用两种启动方式
bash run_react_infer.sh           # 原始
bash run_deepresearch.sh          # 新的
# 选择一种即可

# 不要在auto模式下强行覆盖
export PROMPT_MODE=auto
# 然后在代码中硬编码模式（会冲突）
```

---

## 📞 快速支持

### 常见问题

**Q: 会不会影响原有功能？**
A: 不会。原有文件完全不变，可以随时切回原始系统。

**Q: 如何验证使用了哪个模式？**
A: 查看运行日志，会显示 `[PromptSelector] 使用XX模式`

**Q: 能否添加自定义模式？**
A: 可以！参考 `MULTIMODE_GUIDE.md` 的"添加新模式"章节

**Q: 不需要微生物模式怎么办？**
A: 不创建 `prompt_microbiology.py` 即可，系统会自动回退到默认模式

---

## 📚 完整文档

- **详细使用指南**: [MULTIMODE_GUIDE.md](MULTIMODE_GUIDE.md)
- **微生物模式文档**: [MICROBIOLOGY_QUICKSTART.md](MICROBIOLOGY_QUICKSTART.md)
- **原始系统文档**: [README.md](README.md)

---

## 🎯 核心优势总结

1. ✅ **非侵入式**：不修改任何现有代码
2. ✅ **完全可选**：不需要时可以完全不安装
3. ✅ **智能自动**：auto模式自动选择最佳Prompt
4. ✅ **易于扩展**：添加新模式只需3个步骤
5. ✅ **向后兼容**：原有使用方式100%保留

---

**开始使用：**
```bash
chmod +x run_deepresearch.sh
bash run_deepresearch.sh --help
```
