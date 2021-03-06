#!/usr/bin/env python3
# list_courses.py
# sable cantus
# March 2021

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

# get courses for a user
user = canvas.get_user(USER_ID)
courses = canvas.get_courses()

profile = user.get_profile()
name = profile["name"]
email = profile["primary_email"]
print(name)
print(email)
print()

print('All Courses:')
for course in courses:
    print(course.name, ' - ', course.workflow_state)
print()
