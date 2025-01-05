#!/usr/bin/env python3
# create_multi_assignment.py
# sable cantus
# Add many assignments to your shell

import os
import markdown
from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, MY_ASSIGNMENTS

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

# Set a points value for all assignments
points_possible = 10

# List the file name and assignment title
file_names = [
    # ['MARKDOWN-FILENAME.md','Assignment Name']
]

os.chdir(MY_ASSIGNMENTS)

for file_name in file_names:
    with open(file_name[0], "r", encoding="utf-8") as input_file:
        text = input_file.read()
    page_body = markdown.markdown(text, extensions=['sane_lists'])

    new_assignment = course.create_assignment({
        'name': file_name[1],
        'description': page_body,
        'published': True,      # False
        'points_possible': points_possible
    })

    print(new_assignment)
    print("Assignment created at: ", new_assignment.html_url)
