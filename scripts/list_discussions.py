#!/usr/bin/env python3
# list_discussions.py
# sable cantus

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()


# list all discussion topics
print("All discussion topics for the course:")
topics = course.get_discussion_topics(order_by='title')
for topic in topics:
    print(topic)
