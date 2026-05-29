#!/usr/bin/env python3
# create_announcement.py
# sable cantus
# create a discussion post annnouncement from a mardown file

import _venv
import sys
import _chooseFile
import os
import markdown
from _client import get_canvas_and_course, resolve_content_path, upload_and_replace_assets, MY_ANNOUNCEMENTS

# Initiate Canvas and Course
_, course = get_canvas_and_course()
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
markdown_path = resolve_content_path(file_name, MY_ANNOUNCEMENTS)
with open(markdown_path, "r", encoding="utf-8") as input_file:
    text = input_file.read()
message = markdown.markdown(text, extensions=['sane_lists'])

# Get markdown file's folder to resolve local assets
markdown_dir = os.path.dirname(markdown_path)

# Scan and upload local assets, replacing their URLs
message = upload_and_replace_assets(message, course, markdown_dir)


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
