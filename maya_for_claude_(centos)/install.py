# -*- coding: utf-8 -*-
"""Lookdev Tool installer for Linux/CentOS - drag this file into the
Maya viewport.

Installs the LookdevTool module into Maya's user modules folder
(~/maya/modules), which every installed Maya version scans by
default, and loads the plug-in immediately in the current session.
"""
import os
import shutil

import maya.cmds as cmds


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

    maya_app_dir = cmds.internalVar(userAppDir=True)
    modules_dir = os.path.join(maya_app_dir, "modules")
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

    plugin_path = os.path.join(dest_root, "plug-ins", "lookdev_menu.py")
    cmds.loadPlugin(plugin_path, quiet=True)

    cmds.confirmDialog(
        title="Lookdev Tool",
        message="Lookdev menu installed. Check the main menu bar.",
        icon="information",
    )
