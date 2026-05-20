#!/usr/bin/env python3
# list_modules.py
# sable cantus

import _venv
from _client import get_canvas_and_course, USER_ID

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# get all modules for a course

modules = course.get_modules()

for module in modules:
    if module.published:
        is_published = "Published"
    else:
        is_published = "Unpublished"
    print(module, "-", is_published)
    items = module.get_module_items()
    for item in items:
        if item.published:
            is_published = "Published"
        else:
            is_published = "Unpublished"
        print("\t", item.type, "-", item.title, "-", is_published)
    print()


