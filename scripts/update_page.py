#!/usr/bin/env python3
# update_pages.py
# sable cantus
# August 2020

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

#########################################
# get a specific page to update
#
# list all pages
print("Select a page to update:")
page_list = course.get_pages(sort="title")

# drop the paginated list into pages
pages = []
for i in page_list:
    pages.append(i)

# drop page urls and sort
page_urls = []
for page in pages:
    page_urls.append(page.url)
page_urls.sort()

length = len(page_urls)
#print("There are", length, "pages.")
# print the sorted urls
for url in page_urls:
    print(page_urls.index(url)+1, "-", url)

selection = input("Your selection: ")
selection = int(selection)
page_url = page_urls[selection-1]
print("You selected: ", page_url)

user_choice = input("Is this correct? (y/n) ")
if user_choice.lower() == 'y':
    pass
else:
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
updated_body = markdown.markdown(text)

# help from the slack channel - this cmd works
# page.edit(wiki_page={"title": "Updated title", "body": "Updated body."})

page.edit(wiki_page={
    "body": updated_body}
    )

updated_page_url = API_URL + "/courses/" + str(COURSE_NUM) + "/pages/" + page_url
print("Updated: ", updated_page_url)

##############################################################################
# TODO
# [X] validate that page URL is correct
# [X] validate updated html page is correct
# [X] accept input from CLI?
# [X] convert markdown to html
##############################################################################
