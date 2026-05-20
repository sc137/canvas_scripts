#!/usr/bin/env python3
# create_page.py
# sable cantus

import _venv
import sys
import _chooseFile
import markdown
import _chooseFile
import markdown
import os
from _client import get_canvas_and_course, upload_and_replace_assets
from _credentials import MY_PAGES

# Initiate Canvas and Course
_, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# Use the filename if specified
if len(sys.argv) > 1:
    file_name = str(sys.argv[1])
    print('Selected file: {}'.format(file_name))
    title = input("Please select your page title (blank to ignore): ")
else:
    # use the _chooseFile to list options
    title, file_name = _chooseFile.chooseFile(MY_PAGES)

# read the body from a markdown file
with open(file_name, "r", encoding="utf-8") as input_file:
    text = input_file.read()

# Convert markdown to HTML
page_body = markdown.markdown(text, extensions=['sane_lists'])

# Get markdown file's folder to resolve local assets
markdown_dir = os.path.dirname(os.path.abspath(file_name))

# Scan and upload local assets, replacing their URLs
page_body = upload_and_replace_assets(page_body, course, markdown_dir)

# create the page
new_page = course.create_page({
    'title': title,
    'body': page_body,
    'published': True})

print("Created: ", new_page)