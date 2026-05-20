#!/usr/bin/env python3 
# list_students.py
# sable cantus

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
    #profile = user.get_profile()
    #email = profile["primary_email"]
    #name = profile["name"]
    #print(name)
    print(user)
print()

# get students for the course
users = course.get_users(
        enrollment_type=['student'])

print("All Students")
print()
for user in users:
    profile = user.get_profile()
    email = profile["primary_email"]
    print(user, email)

print()
print("Recently Active Students")
print()
students = course.get_recent_students()
for student in students:
    print(student)