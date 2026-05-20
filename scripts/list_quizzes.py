#!/usr/bin/env python3
# list_quizzes.py
# sable cantus

import _venv
from _client import get_canvas_and_course, USER_ID

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# list all quizzes 
print("All quizzes for the course:")
quizzes = course.get_quizzes()

for quiz in quizzes:
    print(quiz)
