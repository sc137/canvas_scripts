#!/usr/bin/env python3
# create_multi_assignment.py
# sable cantus
# Add many assignments to your shell

import _venv
import os
import markdown
from _client import get_canvas_and_course, upload_and_replace_assets, MY_ASSIGNMENTS

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# Set a points value for all assignments
points_possible = 10

# List the file name and assignment title
file_names = [
    # ['MARKDOWN-FILENAME.md','Assignment Name']
]

os.chdir(MY_ASSIGNMENTS)

for file_name in file_names:
    markdown_path = os.path.abspath(file_name[0])
    with open(file_name[0], "r", encoding="utf-8") as input_file:
        text = input_file.read()
    page_body = markdown.markdown(text, extensions=['sane_lists'])
    markdown_dir = os.path.dirname(markdown_path)
    page_body = upload_and_replace_assets(page_body, course, markdown_dir)

    new_assignment = course.create_assignment({
        'name': file_name[1],
        'description': page_body,
        'published': True,      # False
        'points_possible': points_possible
    })

    print(new_assignment)
    print("Assignment created at: ", new_assignment.html_url)
