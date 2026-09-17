# -*- coding: utf-8 -*-
"""Lookdev Tool installer - drag this file into the Maya viewport.

Installs the LookdevTool module to an ASCII-only folder under
%LOCALAPPDATA%. Maya's plug-in loader cannot reliably load a .py
plug-in from a path containing non-ASCII characters (e.g. a
OneDrive-redirected "Documents" folder with a localized name such as
"문서"), so the module is kept out of that folder entirely.

Registers the install folder with every installed Maya version via
Maya.env (MAYA_MODULE_PATH), and loads the plug-in immediately in the
current session.
"""
import os
import re
import shutil
import subprocess

import maya.cmds as cmds

MARKER = "# --- Lookdev Tool module path ---"


def onMayaDroppedPythonFile(installer_path=None):
    install(installer_path)


def install(installer_path=None):
    if installer_path:
        base_dir = os.path.dirname(os.path.abspath(installer_path))
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    src_root = os.path.join(base_dir, "LookdevTool")
    if not os.path.isdir(src_root):
        cmds.confirmDialog(
            title="Lookdev Tool - Install",
            message="LookdevTool folder not found next to install.py.",
            icon="critical",
        )
        return

    local_app_data = os.environ.get("LOCALAPPDATA")
    modules_dir = os.path.join(local_app_data, "MayaModules")
    dest_root = os.path.join(modules_dir, "LookdevTool")

    if not os.path.isdir(modules_dir):
        os.makedirs(modules_dir)

    if os.path.isdir(dest_root):
        shutil.rmtree(dest_root)
    shutil.copytree(src_root, dest_root)

    mod_file = os.path.join(modules_dir, "LookdevTool.mod")
    with open(mod_file, "w") as handle:
        handle.write("+ LookdevTool 1.0 LookdevTool\n")
        handle.write("scripts: scripts\n")
        handle.write("plug-ins: plug-ins\n")

    _register_module_path(base_dir, modules_dir)

    plugin_path = os.path.join(dest_root, "plug-ins", "lookdev_menu.py")
    cmds.loadPlugin(plugin_path, quiet=True)

    cmds.confirmDialog(
        title="Lookdev Tool",
        message="Lookdev menu installed. Check the main menu bar.",
        icon="information",
    )


def _register_module_path(base_dir, modules_dir):
    """Best-effort: also write MAYA_MODULE_PATH into every installed
    Maya version's Maya.env, via the bundled PowerShell script, so the
    menu loads on future Maya launches (any version) without needing
    to re-run this installer. Falls back to a pure-Python single
    version write for the currently running Maya if PowerShell is
    unavailable."""
    ps1 = os.path.join(base_dir, "register_module_path.ps1")
    if os.path.isfile(ps1):
        try:
            subprocess.call([
                "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", ps1, "-ModulesDir", modules_dir,
            ])
            return
        except Exception:
            pass

    maya_app_dir = cmds.internalVar(userAppDir=True)
    if not os.path.isdir(maya_app_dir):
        return
    for name in os.listdir(maya_app_dir):
        version_dir = os.path.join(maya_app_dir, name)
        if not os.path.isdir(version_dir) or not re.match(r"^\d{4}$", name):
            continue
        env_file = os.path.join(version_dir, "Maya.env")
        existing = ""
        if os.path.isfile(env_file):
            with open(env_file, "r") as handle:
                existing = handle.read()
        if MARKER in existing:
            continue
        with open(env_file, "a") as handle:
            handle.write(
                "\n" + MARKER + "\n"
                "MAYA_MODULE_PATH = " + modules_dir + ";%MAYA_MODULE_PATH%\n"
                + MARKER + "\n"
            )
