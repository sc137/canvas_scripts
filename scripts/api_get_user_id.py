#!/usr/bin/env python3
# api_get_current_user.py
# sable cantus
# Run this to get the user ID for the current user

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

# Get the current user (you)
current_user = canvas.get_current_user()
USER_ID = current_user.id
print(current_user)
print(f'Add {USER_ID} to the _credentials.py file.')