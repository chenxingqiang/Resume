#!/bin/bash

# Compile all resume PDF files

echo "Compiling English resume..."
xelatex xingqiangchen-en.tex

echo "Compiling Chinese resume..."
xelatex xingqiangchen-zn.tex

echo "Compiling Chinese adjusted resume..."
xelatex xingqiangchen-zn-adjust.tex

echo "All PDFs compiled successfully!"
echo ""
echo "Generated files:"
echo "  - xingqiangchen-en.pdf"
echo "  - xingqiangchen-zn.pdf"
echo "  - xingqiangchen-zn-adjust.pdf"