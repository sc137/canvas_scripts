#!/usr/bin/env python3
# create_announcement.py
# sable cantus
# create a discussion post from a mardown file

import sys
import _chooseFile
from canvasapi import Canvas
import markdown
from _credentials import API_URL, API_KEY, COURSE_NUM, MY_ANNOUNCEMENTS

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
    title = input("Subject: ")
else:
    # use the _chooseFile to list options
    title, file_name = _chooseFile.chooseFile(MY_ANNOUNCEMENTS)

#####################################
# set the time to post
delayed_post = _chooseFile.delayPost()

# read in the message from a markdown file
with open(file_name, "r", encoding="utf-8") as input_file:
    text = input_file.read()
message = markdown.markdown(text, extensions=['sane_lists'])

post = course.create_discussion_topic(
    title=title,
    message=message,
    discussion_type='threaded',
    is_announcement=True,
    delayed_post_at=delayed_post
)

print('Created: ', post)

print(post.url)

##############################################################################
# To-Do
# [X] Accept input for Subject of announcement and filename
# [X] Set announcement date and time for later with delayed_post_at
# YYYY-MM-DDTHH:MM:SSZ
# literal characters T and Z
# All timestamps are sent and returned in ISO 8601 format.
# All timestamps default to UTC time zone unless specified
