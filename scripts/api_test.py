#!/usr/bin/env python3
# api_test.py
# sable cantus
# Run this to confirm everything is working 
# and you have the correct class selected
# This script will display your canvas user ID

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)
"""
# select user sable
user = canvas.get_user(USER_ID)
# get info for sable
courses = user.get_courses()
print('All Courses for Sable')
for course in courses:
    print(course)
print()
print(user.email)
"""

# get a specific course 
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

"""
# get all users for a course
users = course.get_users()
for user in users:
    print(user)
"""

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

"""
# get all assignments
assignments = course.get_assignments()
print("All assignments: ")
for assignment in assignments:
    print(assignment)
print()
"""


# get a single assignment
"""
assignment = course.get_assignment(217019)
print(assignment)
"""

"""
# get all quizzes
print("All quizzes")
quizzes = course.get_quizzes()
for quiz in quizzes:
    print(quiz)
print()
"""

# get questions for a quiz 40476
#quiz = course.get_quiz(40476)
#questions = quiz.get_questions()
#for question in questions:
#    print()
#    print("question {}".format(question.question_name))
#    print(question.question_text)
#    print()
#    for answer in question.answers:
#        print(answer["weight"], answer["text"])

