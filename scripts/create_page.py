#!/usr/bin/env python3
# create_page.py
# sable cantus
# updated: 1/21

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

#####################################
# set the title and choose the file
title, file_name = _chooseFile.chooseFile('../pages')

# read the body from a markdown file
with open(file_name, "r", encoding="utf-8") as input_file:
    text = input_file.read()
page_body = markdown.markdown(text)

# create the page
new_page = course.create_page({
    'title': title,
    'body': page_body,
    'published': True})
print("Created: ", new_page)

#####################################
# TODO
#
# [X] read html from file when creating page
# [X] choose from a list of files and input title
#####################################
