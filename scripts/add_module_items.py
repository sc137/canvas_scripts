#!/usr/bin/env python3
# add_module_items.py
# Add URLs and text headers to a Canvas module.

import _venv
import sys

from _client import get_canvas_and_course

##############################################################################
# Script settings
#
# Set MODULE_ID to run without prompts. If MODULE_ID is None, the script will
# list the course modules and ask which one to update.
#
# Run list_modules.py to see module IDs ahead of time.
##############################################################################

MODULE_ID = None

MODULE_ITEMS = [
    # {
    #     "type": "SubHeader",
    #     "title": "Text Header Title",
    #     "position": 1,
    #     "indent": 0,
    #     "published": True,
    # },
    # {
    #     "type": "ExternalUrl",
    #     "title": "Example Resource",
    #     "external_url": "https://example.com/",
    #     "position": 2,
    #     "indent": 1,
    #     "published": True,
    #     "new_tab": True,
    # },
]


def choose_module(course):
    modules = list(course.get_modules())
    if not modules:
        sys.exit("No modules found in this course.")

    print("Select a module:")
    for index, module in enumerate(modules, start=1):
        print(f"{index} - {module.name} (id: {module.id})")

    selection = input("Your selection: ").strip()
    try:
        selected_index = int(selection)
        return modules[selected_index - 1]
    except (ValueError, IndexError):
        sys.exit("Invalid module selection.")


def clean_module_item(item_settings):
    module_item = {
        "type": item_settings["type"],
        "title": item_settings["title"],
    }

    for key in ("position", "indent", "external_url", "new_tab"):
        if key in item_settings and item_settings[key] is not None:
            module_item[key] = item_settings[key]

    return module_item


def main():
    if not MODULE_ITEMS:
        sys.exit("No module items configured. Add items to MODULE_ITEMS first.")

    canvas, _ = get_canvas_and_course()
    _, course = get_canvas_and_course()
    print("Selected course: \n", course.name)
    print()

    if MODULE_ID is None:
        module = choose_module(course)
    else:
        module = course.get_module(MODULE_ID)

    print("Selected module:", module)
    print()

    for item_settings in MODULE_ITEMS:
        item = module.create_module_item(clean_module_item(item_settings))
        print("Created:", item, item.id)

        if item_settings.get("published", False):
            created_item = module.get_module_item(item.id)
            created_item.edit(module_item={"published": True})
            print("Published:", created_item)


if __name__ == "__main__":
    main()
