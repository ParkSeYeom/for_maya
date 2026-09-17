#!/usr/bin/env bash
# Lookdev Tool installer for Linux/CentOS.
# Run this outside Maya: ./install.sh
#
# Copies the LookdevTool module into ~/maya/modules, which every
# installed Maya version scans by default (no Maya.env editing
# needed, unlike the Windows installer).
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/LookdevTool"
MODULES_DIR="$HOME/maya/modules"
DEST="$MODULES_DIR/LookdevTool"

if [ ! -d "$SRC" ]; then
    echo "[Lookdev] LookdevTool folder not found next to install.sh."
    exit 1
fi

mkdir -p "$MODULES_DIR"

rm -rf "$DEST"
cp -r "$SRC" "$DEST"

cat > "$MODULES_DIR/LookdevTool.mod" <<EOF
+ LookdevTool 1.0 LookdevTool
scripts: scripts
plug-ins: plug-ins
EOF

echo
echo "[Lookdev] Install complete. Restart Maya to see the Lookdev menu."
echo "[Lookdev] Installed to: $DEST"
