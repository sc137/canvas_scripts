#!/usr/bin/env python3
# create_multi_pages.py
# sable cantus
# January 2021

import _venv
import os
import markdown
from _client import get_canvas_and_course, upload_and_replace_assets, MY_PAGES

# Initiate Canvas and Course
_, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# set the title and filename for new pages ['Title Here','file-name.md']
new_pages = [
        # ['Testing Multipage Script', 'test1.md']
        ]

# catch errors
not_created = ""

# create many pages from the array and convert md to html
for new_page in new_pages:
    page_title = new_page[0]
    page_file = new_page[1]
    markdown_path = os.path.join(MY_PAGES, page_file)
    
    try:
        with open(markdown_path, "r", encoding="utf-8") as input_file:
            text = input_file.read()
        page_body = markdown.markdown(text, extensions=['sane_lists'])
    except FileNotFoundError:
        not_created += page_file + "\n"
        continue

    # Scan and upload local assets, replacing their URLs
    markdown_dir = os.path.dirname(os.path.abspath(markdown_path))
    page_body = upload_and_replace_assets(page_body, course, markdown_dir)

    # create the page
    created_page = course.create_page({
        'title': page_title,
        'body': page_body,
        'published': True})
    print("Created:", created_page)

if not_created != "":
    print("Not created:\n", not_created)

