#!/usr/bin/env python3
# list_discussions_entries.py
# sable cantus
# August 2020

import sys
import pkg_resources

# check that the canvasapi is installed
try:
    pkg_resources.require('canvasapi')
except:
    sys.exit('dependency needed: $ pip3 install canvasapi')

from canvasapi import Canvas

from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

#########################################
# choose a discussion to list entries
#
# list all discussions
print("Select a discussion:")
topics = course.get_discussion_topics(order_by='title')

# drop the paginated list into discussions
discussions = []
for topic in topics:
    discussions.append(topic)

length = len(discussions)
for title in discussions:
    print(discussions.index(title)+1, "-", title)

selection = input("Your selection: ")
selection = int(selection)
discussion = discussions[selection-1]
print("You selected: ", discussion)
print("There are", discussion.discussion_subentry_count, "entries.")

user_choice = input("Is this correct? (y/n) ")
if user_choice.lower() == 'y':
    pass
else:
    exit()
print()

print("All entries for", discussion)

entries = discussion.get_topic_entries()
for entry in entries:
    #print(entry)
    print(entry.user_name, entry.user_id)
    print(entry.message)

#########################################
# Output is in HTML, convert to markdown
