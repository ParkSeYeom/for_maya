# -*- coding: utf-8 -*-
"""Lookdev menu Maya plug-in.

Load this plug-in (Windows > Settings/Preferences > Plug-in Manager, or
cmds.loadPlugin) to add a "Lookdev" menu to Maya's main menu bar.
Unloading it removes the menu again.

Add your own scripts to the menu by editing:
    ../scripts/lookdev_tool/menu_items.py
"""
import os
import sys

import maya.api.OpenMaya as om
import maya.cmds as cmds

maya_useNewAPI = True

VENDOR = "Lookdev Tools"
VERSION = "1.0.0"


def _ensure_scripts_on_path(plugin_fn):
    # __file__ is not reliably set when Maya loads a plug-in this way,
    # so get the plug-in's own directory from MFnPlugin instead.
    plugin_dir = os.path.dirname(plugin_fn.loadPath())
    module_root = os.path.dirname(plugin_dir)
    scripts_dir = os.path.join(module_root, "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)


def initializePlugin(plugin):
    plugin_fn = om.MFnPlugin(plugin, VENDOR, VERSION)

    try:
        _ensure_scripts_on_path(plugin_fn)

        if cmds.about(batch=True):
            return

        from lookdev_tool import menu_builder
        menu_builder.build_menu()
    except Exception:
        om.MGlobal.displayError("Lookdev: failed to initialize plug-in.")
        raise


def uninitializePlugin(plugin):
    om.MFnPlugin(plugin)

    if cmds.about(batch=True):
        return

    try:
        from lookdev_tool import menu_builder
        menu_builder.destroy_menu()
    except Exception:
        om.MGlobal.displayWarning("Lookdev: failed to remove menu cleanly.")
