# -*- coding: utf-8 -*-
"""Auto-run by Maya at startup because this folder is registered as a
Maya module "scripts" path (see LookdevTool.mod). Loads the Lookdev
plug-in so the menu appears without the user opening Plug-in Manager.
"""
import maya.cmds as cmds
import maya.utils as utils


def _lookdev_load_plugin():
    if not cmds.pluginInfo("lookdev_menu.py", query=True, loaded=True):
        cmds.loadPlugin("lookdev_menu.py", quiet=True)


utils.executeDeferred(_lookdev_load_plugin)
