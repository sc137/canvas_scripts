#!/usr/bin/env python3
# update_multi_pages.py
# sable cantus

import _venv
import os
import markdown
from _client import get_canvas_and_course, upload_and_replace_assets
from _credentials import API_URL, COURSE_NUM, MY_PAGES

# Initiate Canvas and Course
_, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# list the page_url and file_name
updated_pages = [
    # ['canvas-page-url', 'local-page.md'],
    # ['', '']
]

# catch errors
not_found = ""

for updated_page in updated_pages:
    page_url = updated_page[0]
    file_name = updated_page[1]

    # call the page object
    page = course.get_page(page_url)

    os.chdir(MY_PAGES)
    try:
        with open(file_name, "r", encoding="utf-8") as input_file:
            text = input_file.read()
        updated_body = markdown.markdown(text, extensions=['sane_lists'])
    except FileNotFoundError:
        # any pages that are present when this loop is run
        # will be added to the not_found and displayed later
        not_found += file_name + "\n"
        continue

    # Scan and upload local assets, replacing their URLs
    updated_body = upload_and_replace_assets(updated_body, course, MY_PAGES)

    page.edit(wiki_page={
        "body": updated_body}
    )

    updated_page_url = API_URL + "/courses/" + \
        str(COURSE_NUM) + "/pages/" + page_url
    print("Updated: ", updated_page_url)

if not_found != "":
    print("Not updated:\n", not_found)
