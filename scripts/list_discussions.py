#!/usr/bin/env python3
# list_discussions.py
# sable cantus

import _venv
from _client import get_canvas_and_course, USER_ID

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()


# list all discussion topics
print("All discussion topics for the course:")
topics = course.get_discussion_topics(order_by='title')
for topic in topics:
    print(topic)
