#!/bin/bash
# Export docs/architecture/drawio/*.drawio to SVG and PDF via drawio-desktop (Xvfb).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DRAWIO_DIR="$ROOT/docs/architecture/drawio"
SVG_DIR="$ROOT/docs/architecture/svg"
PDF_DIR="$ROOT/docs/architecture/pdf"

mkdir -p "$SVG_DIR" "$PDF_DIR"

export ELECTRON_DISABLE_GPU=1
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-/tmp/drawio-config}"
mkdir -p "$XDG_CONFIG_HOME"

if ! command -v drawio >/dev/null 2>&1; then
  echo "drawio CLI not found. Install draw.io desktop (https://github.com/jgraph/drawio-desktop/releases)." >&2
  exit 1
fi

for src in "$DRAWIO_DIR"/*.drawio; do
  name="$(basename "$src" .drawio)"
  svg="$SVG_DIR/${name}.svg"
  pdf="$PDF_DIR/${name}.pdf"
  echo "Exporting $name -> SVG + PDF"
  xvfb-run -a drawio --no-sandbox --export --format svg --crop --output "$svg" "$src"
  xvfb-run -a drawio --no-sandbox --export --format pdf --crop --output "$pdf" "$src"
done

echo "Export complete: $SVG_DIR and $PDF_DIR"
