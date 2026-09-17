# -*- coding: utf-8 -*-
"""Builds and tears down the Lookdev main menu."""
import importlib

import maya.cmds as cmds
import maya.mel as mel

try:
    reload
except NameError:
    from importlib import reload

MENU_NAME = "LookdevMainMenu"
MENU_LABEL = "Lookdev"


def _dispatch(dotted_path):
    module_path, func_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    reload(module)
    func = getattr(module, func_name)
    func()


def _make_callback(dotted_path):
    def _callback(*_args):
        _dispatch(dotted_path)
    return _callback


def build_menu():
    destroy_menu()

    main_window = mel.eval("$tempVar = $gMainWindow")
    cmds.menu(MENU_NAME, label=MENU_LABEL, parent=main_window, tearOff=True)

    from lookdev_tool import menu_items
    reload(menu_items)

    for item in menu_items.MENU_ITEMS:
        if item == "---":
            cmds.menuItem(divider=True, parent=MENU_NAME)
            continue
        cmds.menuItem(
            label=item["label"],
            command=_make_callback(item["command"]),
            annotation=item.get("tooltip", ""),
            parent=MENU_NAME,
        )


def destroy_menu():
    if cmds.menu(MENU_NAME, exists=True):
        cmds.deleteUI(MENU_NAME, menu=True)
