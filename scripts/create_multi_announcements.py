#!/usr/bin/env python3
# create_multi_announcements.py
# sable cantus
# create a discussion post from a mardown file
# schedule multiple announcements

import _venv
import sys

try:
    import markdown
except:
    print("Please install markdown")
    sys.exit(0)
from _client import get_canvas_and_course, MY_ANNOUNCEMENTS

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# list announcement files and delay times
# 'Announcement Title', 'Markdown File Name', 'Delay posting time (blank for now)'

announcements = [
    # ['Announcement 1', 'announcement1.md','2024-08-07T18:00:00Z'],
    # ['','','']
]

for announcement in announcements:
    title = announcement[0]
    file_name = MY_ANNOUNCEMENTS + announcement[1]
    delayed_post = announcement[2]

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

"""
YYYY-MM-DDTHH:MM:SSZ - literal characters T and Z
All timestamps are sent and returned in ISO 8601 format.
All timestamps default to UTC time zone unless specified
"""