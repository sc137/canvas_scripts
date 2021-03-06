#!/usr/bin/env python3
# create_discussion_post.py
# sable cantus
# August 2020
# create a discussion post from a mardown file

import os
import sys
import pkg_resources
import _chooseFile

# check that the canvasapi is installed
try:
    pkg_resources.require('canvasapi')
except:
    sys.exit('dependency needed: $ pip3 install canvasapi')

from canvasapi import Canvas

# check that the markdown module is installed
try:
    pkg_resources.require('markdown')
except:
    sys.exit('dependency needed: $ pip3 install markdown')
import markdown
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID, MY_DISCUSSIONS

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
    title, file_name = _chooseFile.chooseFile(MY_DISCUSSIONS)

os.chdir(MY_DISCUSSIONS)
with open(file_name, "r", encoding="utf-8") as input_file:
    text = input_file.read()
message = markdown.markdown(text)

post = course.create_discussion_topic(
        title=title,
        message=message,
        published=True,
        discussion_type='threaded',
        allow_rating=True
        )

print('Created: ', post)

print(post.url)

##############################################################################
# To-Do
#
# [X] How can I attach images to the uploaded post?
# --- Upload them to 3c and use a public link
