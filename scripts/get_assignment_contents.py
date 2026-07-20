#!/usr/bin/env python3
# get_assignment_contents.py
# sable cantus
# Get the contents of one or more assignments

import _venv
import os
import re
import sys

try:
    import html2text
except ImportError:
    sys.exit('dependency needed: $ pip3 install html2text')

from _client import get_canvas_and_course, MY_ASSIGNMENTS

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

#########################################
# pre-specify assignment IDs to skip the menu
# run list_assignments.py to find IDs
# leave empty to use the interactive menu
assignment_ids = []

#########################################
# get one or more assignments to view
# list all assignments
assignment_list = course.get_assignments()

# drop the paginated list into assignments
assignments = []
for i in assignment_list:
    assignments.append(i)

# sort by name
assignments.sort(key=lambda a: a.name)

if assignment_ids:
    # build selected list from pre-specified IDs
    id_set = set(assignment_ids)
    selected = [a for a in assignments if a.id in id_set]
    print("Using pre-specified assignments:")
    for a in selected:
        print(" -", a.name)
    print()
else:
    # interactive menu
    print("Select assignment(s) to get (e.g. 1 or 1,3,5 or 2-5):")
    for i, assignment in enumerate(assignments):
        print(i+1, "-", assignment.name)

    raw = input("Your selection: ").strip()

    # parse comma-separated values and ranges (e.g. "1,3,5" or "2-5" or "1,3-5")
    indices = set()
    for part in raw.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-', 1)
            indices.update(range(int(start), int(end) + 1))
        else:
            indices.add(int(part))

    selected = [assignments[i-1] for i in sorted(indices)]

    print("You selected:")
    for a in selected:
        print(" -", a.name)

    user_choice = input("Is this correct? (y/n) ")
    if user_choice.lower() != 'y':
        exit()

print()

converter = html2text.HTML2Text()
converter.ignore_links = False

for a in selected:
    assignment = course.get_assignment(a.id)

    # convert HTML description to markdown
    md_content = converter.handle(assignment.description or '')

    # build filename from assignment name
    slug = a.name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    file_path = os.path.join(MY_ASSIGNMENTS, slug + '.md')

    if os.path.exists(file_path):
        print("Skipped (file exists):", file_path)
        continue

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print("Saved:", file_path)
