#!/usr/bin/env python3
# get_page_contents.py
# sable cantus
# August 2020
# Get the contents of a specific page

import sys
import pkg_resources

# check that the canvasapi is installed
try:
    pkg_resources.require('canvasapi')
except:
    sys.exit('dependency needed: $ pip3 install canvasapi')

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID, MY_PAGES

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

#########################################
# get a specific page to update
# list all pages
print("Select a page to get:")
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

page = course.get_page(page_url)
print(page.body)