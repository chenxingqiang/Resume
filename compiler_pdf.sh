#!/bin/bash

# Compile all resume PDF files

echo "Compiling English resume..."
xelatex xingqiangchen-en.tex

echo "Compiling Chinese resume..."
xelatex xingqiangchen-zn.tex

echo "Compiling Chinese adjusted resume..."
xelatex xingqiangchen-zn-adjust.tex

echo "All PDFs compiled successfully!"

echo "Building draw.io architecture appendix and merging into resume PDFs..."
python3 scripts/build_architecture_appendix.py

# Copy merged PDFs to docs/
cp xingqiangchen-en.pdf xingqiangchen-zn.pdf xingqiangchen-zn-adjust.pdf docs/
cp docs/architecture/architecture-appendix.pdf docs/ 2>/dev/null || true

echo ""
echo "Generated files:"
echo "  - xingqiangchen-en.pdf"
echo "  - xingqiangchen-zn.pdf"
echo "  - xingqiangchen-zn-adjust.pdf"