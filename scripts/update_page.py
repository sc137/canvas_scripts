#!/usr/bin/env python3
# update_page.py
# sable cantus

import _venv
import os
import os
import _chooseFile
import markdown
from _client import get_canvas_and_course, choose_item, upload_and_replace_assets
from _credentials import API_URL, COURSE_NUM, MY_PAGES

# Initiate Canvas and Course
_, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

#########################################
# get a specific page to update
#
print("Select a page to update:")
pages = list(course.get_pages(sort="title"))

# Sort pages by URL to match original behavior
pages.sort(key=lambda p: p.url)

selected_page = choose_item(pages, display_attr="url")
page_url = selected_page.url
print("You selected: ", page_url)

user_choice = input("Is this correct? (y/n) ")
if user_choice.lower() != 'y':
    exit()
print()

# call the page object
page = course.get_page(page_url)

#########################################
# choose the file from the pages directory
# 
title, file_name = _chooseFile.chooseFile(MY_PAGES)

os.chdir(MY_PAGES)
with open(file_name, "r", encoding="utf-8") as input_file:
    text = input_file.read()

# Convert markdown to HTML
updated_body = markdown.markdown(text, extensions=['sane_lists'])

# Get markdown file's folder to resolve local assets
markdown_dir = os.path.dirname(os.path.abspath(file_name))

# Scan and upload local assets, replacing their URLs
updated_body = upload_and_replace_assets(updated_body, course, markdown_dir)

page.edit(wiki_page={
    "body": updated_body}
    )

updated_page_url = API_URL + "/courses/" + str(COURSE_NUM) + "/pages/" + page_url
print("Updated: ", updated_page_url)

