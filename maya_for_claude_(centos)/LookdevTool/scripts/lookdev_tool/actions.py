# -*- coding: utf-8 -*-
"""Functions called from the Lookdev menu.

Add new functions here and register them in menu_items.py.
"""
import os
import subprocess
import sys

import maya.cmds as cmds

try:
    reload
except NameError:
    from importlib import reload


def reload_tool():
    import lookdev_tool.menu_items as menu_items
    import lookdev_tool.menu_builder as menu_builder

    reload(menu_items)
    reload(menu_builder)

    menu_builder.destroy_menu()
    menu_builder.build_menu()
    cmds.inViewMessage(amg="Lookdev tool reloaded.", pos="midCenter", fade=True)


def open_script_folder():
    folder = os.path.dirname(os.path.abspath(__file__))
    if sys.platform.startswith("win"):
        os.startfile(folder)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", folder])
    else:
        subprocess.Popen(["xdg-open", folder])


def example_script():
    cmds.inViewMessage(
        amg="Hello from the Lookdev menu! Edit actions.py to add your own tools.",
        pos="midCenter",
        fade=True,
    )
