#!/usr/bin/env python3
# api_test.py
# sable cantus
# Run this to confirm everything is working 
# and you have the correct class selected
# This script will display your canvas user ID

import _venv
from _client import get_canvas_and_course, USER_ID

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# get teachers / TA's / designers
type_list = ['teacher', 'ta', 'designer']
users = course.get_users(enrollment_type=type_list)
print("Teachers / TAs / Designers")
for user in users:
    profile = user.get_profile()
    email = profile["primary_email"]
    name = profile["name"]
    print(name)
    print(user)
    print(email)
print()

# get students for the course
"""
users = course.get_users(
        enrollment_type=['student'],
        enrollment_stat=['active'])

print("Active Students")
print()
for user in users:
    print(user)
"""
