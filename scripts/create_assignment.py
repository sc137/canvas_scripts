#!/usr/bin/env python3
# create_assignment.py
# sable cantus
# August 2020
# updated: 10/22

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

try:
    pkg_resources.require('pyperclip')
except:
    sys.exit('dependency needed: $ pip3 install pyperclip')
import pyperclip

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, MY_ASSIGNMENTS

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

# Use the filename if specified
if len(sys.argv) > 1:
    file_name = str(sys.argv[1])
    print('Selected file: {}'.format(file_name))
    title = input("Please select your page title (blank to ignore): ")
else:
    # use the _chooseFile to list options
    title, file_name = _chooseFile.chooseFile(MY_ASSIGNMENTS)

print(title)
print(file_name)

# read the body from a markdown file
with open(file_name, "r", encoding="utf-8") as input_file:
    text = input_file.read()
page_body = markdown.markdown(text, extensions=['sane_lists'])

points_possible = input("How many points for this? ")

new_assignment = course.create_assignment({
    'name': title,
    'description': page_body,
    'published': False,
    'points_possible': points_possible
})

print(new_assignment)
print("Assignment created at: ", new_assignment.html_url)
pyperclip.copy(new_assignment.html_url)
