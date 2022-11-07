#!/usr/bin/env python3
# update_multi_pages.py
# sable cantus
# updated 11/22

import os
import sys
import pkg_resources
import _chooseFile

# check that the canvasapi is installed
try:
    pkg_resources.require('canvasapi')
except:
    sys.exit('dependency needed: $ pip3 install canvasapi')

from canvasapi import Canvas

# check that the markdown module is installed
try:
    pkg_resources.require('markdown')
except:
    sys.exit('dependency needed: $ pip3 install markdown')
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
    # ['', ''],
    # ['', ''],
    # ['', '']

]

for updated_page in updated_pages:
    page_url = updated_page[0]
    file_name = updated_page[1]

    # call the page object
    page = course.get_page(page_url)

    os.chdir(MY_PAGES)
    with open(file_name, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    updated_body = markdown.markdown(text, extensions=['sane_lists'])

    page.edit(wiki_page={
        "body": updated_body}
    )

    updated_page_url = API_URL + "/courses/" + \
        str(COURSE_NUM) + "/pages/" + page_url
    print("Updated: ", updated_page_url)

##############################################################################
# TODO
# [X] validate that page URL is correct
# [X] validate updated html page is correct
# [X] accept input from CLI?
# [X] convert markdown to html
##############################################################################
