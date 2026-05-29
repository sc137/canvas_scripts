#!/usr/bin/env python3
# create_assignment.py
# sable cantus

import _venv
import sys
import _chooseFile
import markdown
import os
from _client import get_canvas_and_course, resolve_content_path, upload_and_replace_assets, MY_ASSIGNMENTS

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
    title, file_name = _chooseFile.chooseFile(MY_ASSIGNMENTS)

print(title)
print(file_name)

# read the body from a markdown file
markdown_path = resolve_content_path(file_name, MY_ASSIGNMENTS)
with open(markdown_path, "r", encoding="utf-8") as input_file:
    text = input_file.read()
page_body = markdown.markdown(text, extensions=['sane_lists'])
markdown_dir = os.path.dirname(markdown_path)
page_body = upload_and_replace_assets(page_body, course, markdown_dir)

points_possible = input("How many points for this? ")

new_assignment = course.create_assignment({
    'name': title,
    'description': page_body,
    'published': False,
    'points_possible': points_possible
})

print(new_assignment)
print("Assignment created at: ", new_assignment.html_url)
