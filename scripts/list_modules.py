#!/usr/bin/env python3
# list_modules.py
# sable cantus

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
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


