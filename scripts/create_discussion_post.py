#!/usr/bin/env python3
# create_discussion_post.py
# sable cantus
# create a discussion post from a mardown file

import _venv
import os
import sys
import _chooseFile
import markdown
from _client import get_canvas_and_course, resolve_content_path, upload_and_replace_assets, MY_DISCUSSIONS

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# Use the filename if specified
if len(sys.argv) > 1:
    file_name = str(sys.argv[1])
    print('Selected file: {}'.format(file_name))
    title = input("Please select your page title (blank to ignore): ")
else:
    # use the _chooseFile to list options
    title, file_name = _chooseFile.chooseFile(MY_DISCUSSIONS)

markdown_path = resolve_content_path(file_name, MY_DISCUSSIONS)
with open(markdown_path, "r", encoding="utf-8") as input_file:
    text = input_file.read()
message = markdown.markdown(text, extensions=['sane_lists'])
markdown_dir = os.path.dirname(markdown_path)
message = upload_and_replace_assets(message, course, markdown_dir)

post = course.create_discussion_topic(
    title=title,
    message=message,
    published=False,
    discussion_type='threaded',
    allow_rating=True
)

print('Discussion not published.')
print('Created: ', post)
print(post.url)

##############################################################################
# To-Do
#
# [X] How can I attach images to the uploaded post?
# --- Use hosted image URLs or local relative image paths in the Markdown.
