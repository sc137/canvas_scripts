#!/usr/bin/env python3
# create_Weeks.py
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

module_list = [
    'Your List of Modules',
    'Go Here...'
]

for module in module_list:
    new_Week = course.create_module({
        'name': module,
        'published': False})
    print("Created: ", new_Week)
