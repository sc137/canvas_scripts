#!/usr/bin/env python3
# create_modules.py
# sable cantus

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
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
