#!/usr/bin/env python3 
# list_students.py
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

# get a specific course 
course = canvas.get_course(COURSE_NUM)
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