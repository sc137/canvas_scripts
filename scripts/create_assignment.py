#!/usr/bin/env python3
# create_assignment.py
# sable cantus

import _venv
import sys
import _chooseFile
import markdown
from _client import get_canvas_and_course, MY_ASSIGNMENTS

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
