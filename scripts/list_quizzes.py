#!/usr/bin/env python3
# list_quizzes.py
# sable cantus
# Feb 2021

import sys
import pkg_resources
import _chooseFile

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

# list all quizzes 
print("All quizzes for the course:")
quizzes = course.get_quizzes()

for quiz in quizzes:
    print(quiz)

""" list quiz questions """
print(quiz.id)
#print(quiz.get_questions)

for quiz_q in quiz.questions:
    print(quiz_q)
