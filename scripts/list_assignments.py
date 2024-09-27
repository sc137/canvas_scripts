#!/usr/bin/env python3
# list_assignments.py
# sable cantus

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

# list all assignments
print("All assignments for the course:")
assignments = course.get_assignments()

for assignment in assignments:
    print(assignment)
