#!/usr/bin/env python3
# update_multi_pages.py
# sable cantus

import os
from canvasapi import Canvas
import markdown
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID, MY_PAGES

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

# list the page_url and file_name
updated_pages = [
    # ['canvas-page-url', 'local-page.md'],
    # ['', '']
]

for updated_page in updated_pages:
    page_url = updated_page[0]
    file_name = updated_page[1]

    # call the page object
    page = course.get_page(page_url)

    os.chdir(MY_PAGES)
    not_found = ""
    try:
        with open(file_name, "r", encoding="utf-8") as input_file:
            text = input_file.read()
        updated_body = markdown.markdown(text, extensions=['sane_lists'])
    except FileNotFoundError:
        # any pages that are present when this loop is run
        # will be added to the not_found and displayed later
        not_found += file_name + "\n"

    page.edit(wiki_page={
        "body": updated_body}
    )

    updated_page_url = API_URL + "/courses/" + \
        str(COURSE_NUM) + "/pages/" + page_url
    print("Updated: ", updated_page_url)

if not_found != "":
    print("Not updated:\n", not_found)
