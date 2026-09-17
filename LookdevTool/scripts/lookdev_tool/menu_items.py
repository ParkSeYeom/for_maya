# -*- coding: utf-8 -*-
"""Menu entries for the Lookdev menu.

Add your own scripts here - no need to touch the plug-in or menu builder.

Each entry is a dict:
    label   - text shown in the menu
    command - "module.submodule.function_name" dotted path, called with no args
    tooltip - optional annotation text

Use the string "---" to add a separator line.
"""

MENU_ITEMS = [
    {
        "label": "Reload Lookdev Tool",
        "command": "lookdev_tool.actions.reload_tool",
        "tooltip": "Reload all lookdev_tool modules (useful while developing).",
    },
    {
        "label": "Open Script Folder",
        "command": "lookdev_tool.actions.open_script_folder",
        "tooltip": "Open the lookdev_tool scripts folder in Explorer.",
    },
    "---",
    {
        "label": "Example Script",
        "command": "lookdev_tool.actions.example_script",
        "tooltip": "Placeholder - replace with your own script.",
    },
]
