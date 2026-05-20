#!/usr/bin/env python3
# create_modules.py
# sable cantus

import _venv
from _client import get_canvas_and_course, USER_ID

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# Add your canvas modules 
module_list = [
    # 'Example Module 1',
    # 'Example Module 2'
]

for module in module_list:
    new_module = course.create_module({
        'name': module,
        'published': False})
    print("Created: ", new_module)
