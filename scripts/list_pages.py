#!/usr/bin/env python3
# list_pages.py
# sable cantus

import _venv
from _client import get_canvas_and_course, USER_ID

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()


# list all pages
print("All pages for the course:")
page_list = course.get_pages(sort="title")

# drop the paginated list into pages
pages = []
for i in page_list:
    pages.append(i)

# drop page ulrs and sort
page_urls = []
for page in pages:
    page_urls.append(page.url)
page_urls.sort()

length = len(page_urls)
print("There are", length, "pages.")

# print the sorted urls
for url in page_urls:
    print(page_urls.index(url)+1, "-", url)
