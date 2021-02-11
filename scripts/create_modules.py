#!/usr/bin/env python3
# create_modules.py
# sable cantus
# Jan 2021

import sys
import pkg_resources

# check that the canvasapi is installed
try:
    pkg_resources.require('canvasapi')
except:
    sys.exit('dependency needed: $ pip3 install canvasapi')

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

# add all desired module names to this array
module_list = [
        'Module 1 - Topic 1',
        'Module 2 - Topic 2'
       ]

for module in module_list:
    new_module = course.create_module({
        'name': module,
        'published': False})
    print("Created: ", new_module)
