#!/usr/bin/env python3
# list_courses.py
# sable cantus

import _venv
from _client import get_canvas_and_course, USER_ID

# Initiate the new Canvas object
canvas, _ = get_canvas_and_course()

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
