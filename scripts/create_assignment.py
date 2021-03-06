#!/usr/bin/env python3
# create_assignment.py
# sable cantus
# August 2020

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
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID, MY_ASSIGNMENTS

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

#####################################
# set the title and choose the file
# if a file is specified, then use that file
print("choosing a file")
if len(sys.argv) > 1:
    file_name = str(sys.argv[1])
    print("File chose: ", file_name)
    title = input("Please enter the title: ")
else:
    title, file_name = _chooseFile.chooseFile(MY_ASSIGNMENTS)

# read the body from a markdown file
with open(file_name, "r", encoding="utf-8") as input_file:
    text = input_file.read()
page_body = markdown.markdown(text)

points = input("How many points possible? ")
if points == '':
    points = '5'
    print('points: ', points)

new_assignment = course.create_assignment({
    'name': title,
    'description': page_body,
    'published': False,
    'points_possible': points,
    'submission_types': 'online_upload'
                        # online_upload
                        # online_text_entry
                        # online_url
    })

print(new_assignment)
print("Assignment created at: ", new_assignment.html_url)
