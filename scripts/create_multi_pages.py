#!/usr/bin/env python3
# create_multi_pages.py
# sable cantus
# January 2021

import os
import markdown
from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID, MY_PAGES

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

# set the title and filename for new pages ['Title Here','file-name.md']
new_pages = [
        ['Testing Multipage Script', 'test1.md']
        ]

# create many pages from the array and convert md to html
for new_page in new_pages:
    page_title = new_page[0]

    # read the body from a markdown file 
    page_file = new_page[1]
    os.chdir(MY_PAGES)
    # catch errors
    not_created = ""
    try:
        with open(page_file, "r", encoding="utf-8") as input_file:
            text = input_file.read()
        page_body = markdown.markdown(text)
    except FileNotFoundError:
        not_created += page_file + "\n"

    course.create_page({
        'title': page_title,
        'body': page_body,
        'published': True})
    print(new_page)

if not_created != "":
    print("Not created:\n", not_created)

##########
# TODO
#
# [X] read html from file when creating page
# [X] create multiple pages from an array
##########
