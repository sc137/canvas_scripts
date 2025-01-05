#!/usr/bin/env python3
# add_module_items.py
# sable cantus
# add URLs and text items to a module

from canvasapi import Canvas
from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID

# Initiate the new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get a specific course 
course = canvas.get_course(COURSE_NUM)
print("Selected course: \n", course.name)
print()

# get a specific module id to add items to
module_id = ######
module = course.get_module(module_id)
print(module)

# You can add text headers or URLs

# Create a text header with indentation specified
title = 'Text Header Title'

# Step 1: Create a text item
item = module.create_module_item({
    'type': 'SubHeader',
    'title': title,
    'position': 1,  # Position in the module
    'indent': 0,  # Indentation level
})

print(item, item.id)

# Step 2: Publish the item
item_id = module.get_module_item(item.id)  # Get the newly created item ID
item_id.edit(module_item={'published': True})  # Publish the item

# Create an external URL item and specificy indentation
module.create_module_item({
    'type': 'ExternalUrl',
    'title': 'Your external URL',
    'external_url': 'https://example.com/',
    'indent': 1,  # Indentation level
})

# Publish the URL in the module
item_id = module.get_module_item(item.id)  # Get the newly created item ID
item_id.edit(module_item={'published': True})  # Publish the item