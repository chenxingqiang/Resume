# Resume / 简历

Personal resume in LaTeX format with English and Chinese versions, deployed as GitHub Pages.

个人简历的 LaTeX 格式，包含英文和中文版本，并部署为 GitHub Pages。

## 📄 Available Versions / 可用版本

### PDF Versions
- **English Resume**: [`xingqiangchen-en.pdf`](xingqiangchen-en.pdf)
- **Chinese Resume**: [`xingqiangchen-zn.pdf`](xingqiangchen-zn.pdf)
- **Chinese Adjusted**: [`xingqiangchen-zn-adjust.pdf`](xingqiangchen-zn-adjust.pdf)

### Online Versions (GitHub Pages)
- **English Resume**: [View Online](https://chenxingqiang.github.io/Resume/en.html)
- **Chinese Resume**: [View Online](https://chenxingqiang.github.io/Resume/zn.html)
- **Chinese Adjusted**: [View Online](https://chenxingqiang.github.io/Resume/zn-adjust.html)

## 🚀 Quick Start / 快速开始

### Compile PDFs / 编译 PDF

```bash
./compiler_pdf.sh
```

This will compile all three resume versions:
- `xingqiangchen-en.pdf`
- `xingqiangchen-zn.pdf`
- `xingqiangchen-zn-adjust.pdf`

### Requirements / 环境要求

- XeLaTeX (TeX Live 2024 or later)
- Chinese fonts: PingFang SC (for Chinese versions)
- Bash shell

## 📂 Project Structure / 项目结构

```
Resume/
├── README.md                      # This file
├── compiler_pdf.sh                # Script to compile all PDFs
├── resume.cls                     # LaTeX resume class
├── xingqiangchen-en.tex          # English resume source
├── xingqiangchen-zn.tex          # Chinese resume source
├── xingqiangchen-zn-adjust.tex   # Chinese adjusted resume source
├── *.pdf                          # Generated PDF files
├── docs/                          # GitHub Pages HTML files
│   ├── index.html                # Landing page
│   ├── en.html                   # English resume
│   ├── zn.html                   # Chinese resume
│   └── zn-adjust.html            # Chinese adjusted resume
└── project-docs/                  # Project documentation
    ├── secret-learn.md           # Secret-Learn project
    ├── jax-learn.md              # JAX-sklearn project
    ├── yirage.md                 # YiRage project
    ├── youtube.md                # YouTube-DNN-RecSys
    ├── deepmicropath.md          # DeepMicroPath
    ├── genquestion.md            # Questions-Gen
    └── research-cli.md           # Research CLI
```

## 🛠️ Development / 开发

### Compile Individual PDFs / 单独编译 PDF

```bash
xelatex xingqiangchen-en.tex
xelatex xingqiangchen-zn.tex
xelatex xingqiangchen-zn-adjust.tex
```

### Generate HTML for GitHub Pages / 生成 GitHub Pages HTML

```bash
./generate_html.sh
```

## 📝 Content / 内容

This resume showcases:
- **LLM Inference Systems** & **AI Compiler** experience
- **Privacy-Preserving ML** expertise
- **Recommendation Systems** development
- **Open Source** contributions
- Interdisciplinary background in Physics, Biology, and Computer Science

本简历展示：
- **大语言模型推理系统** 与 **AI编译器** 经验
- **隐私保护机器学习** 专业技能
- **推荐系统** 开发经验
- **开源** 贡献
- 物理学、生物学和计算机科学跨学科背景

## 🔗 Key Projects / 核心项目

- **YiRage YPK**: LLM megakernel compiler (1.2×–6.7× latency reduction)
- **Secret-Learn**: Privacy-preserving ML library (573 implementations)
- **JAX-sklearn**: scikit-learn with JAX acceleration (13,058 tests passed)
- **Research CLI**: AI workflow tool with academic features
- **YouTube-DNN-RecSys**: Recommendation system implementation
- **Questions-Gen**: Math problem generator with RL & KD
- **DeepMicroPath**: Multi-mode research agent
- **Medical-NER**: Fine-tuned medical entity extraction

## 📫 Contact / 联系方式

- **Name**: Chen Xingqiang (陈星强)
- **Location**: Hangzhou, China / 杭州，中国
- **Phone**: +86 150-0133-4125
- **Email**: joy6677@outlook.com
- **GitHub**: [@chenxingqiang](https://github.com/chenxingqiang)

## 📜 License / 许可证

This repository is for personal use. All rights reserved.

本仓库仅供个人使用，保留所有权利。

---

© 2025 Chen Xingqiang (陈星强). All rights reserved.

