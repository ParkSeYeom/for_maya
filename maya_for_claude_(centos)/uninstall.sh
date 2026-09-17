#!/usr/bin/env bash
# Removes the Lookdev Tool module installed by install.sh, restoring
# ~/maya/modules to its pre-install state.
set -e

MODULES_DIR="$HOME/maya/modules"

echo "[Lookdev] Removing installed files..."
rm -rf "$MODULES_DIR/LookdevTool"
rm -f "$MODULES_DIR/LookdevTool.mod"

# Remove the modules folder itself only if it's now empty.
if [ -d "$MODULES_DIR" ] && [ -z "$(ls -A "$MODULES_DIR")" ]; then
    rmdir "$MODULES_DIR"
fi

echo
echo "[Lookdev] Uninstall complete."
echo "[Lookdev] If Maya is currently open, close it - the Lookdev menu"
echo "[Lookdev] will not come back on the next launch."
