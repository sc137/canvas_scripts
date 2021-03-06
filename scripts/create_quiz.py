#!/usr/bin/env python3
# create_quiz.py
# sable cantus
# Feb 2021

import os
import sys
import pkg_resources
import _chooseFile

# check that the canvasapi is installed
try:
    pkg_resources.require('canvasapi')
except:
    sys.exit('dependency needed: $ pip3 install canvasapi')

# check that the markdown module is installed
try:
    pkg_resources.require('markdown')
except:
    sys.exit('dependency needed: $ pip3 install markdown')
import markdown

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

title = input("Please enter quiz title: ")
body = input("Please enter quiz body: ")

new_quiz = course.create_quiz({
    'title': title,
    'description': body,
    'published': False,
    'quiz_type': 'assignment',
    # practice_quiz, assignment, graded_survey, survey
    'shuffle_answers': True,
    'hide_results': 'always'
    })

print(new_quiz)
print("Quiz created at: ", new_quiz.html_url)
