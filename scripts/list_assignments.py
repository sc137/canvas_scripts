#!/usr/bin/env python3
# list_assignments.py
# sable cantus

import _venv
from _client import get_canvas_and_course, USER_ID

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# list all assignments
print("All assignments for the course:")
assignments = course.get_assignments()

for assignment in assignments:
    print(assignment)
