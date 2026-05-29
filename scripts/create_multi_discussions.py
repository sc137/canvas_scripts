#!/usr/bin/env python3
# create_multi_discussions.py
# sable cantus
# create multiple discussion posts from markdown files

import _venv
import os
import sys


try:
    import markdown
except:
    print("Please install markdown")
    sys.exit(0)
from _client import get_canvas_and_course, upload_and_replace_assets, MY_DISCUSSIONS

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# List discussion posts to create.
# Available discussion_type values:
# - 'threaded': fully threaded replies
# - 'side_comment': one level of nested replies
# - 'not_threaded': flat replies
# Set points_possible to a number to create a graded discussion assignment.
# Leave points_possible as None or '' to create a regular ungraded discussion.
discussions = [
    # {
    #     'title': 'Discussion Title',
    #     'file_name': 'discussion-prompt.md',
    #     'discussion_type': 'threaded',
    #     'published': False,
    #     'points_possible': None,
    #     'grading_type': 'points',
    #     'due_at': '',
    #     'require_initial_post': False,
    #     'allow_rating': True,
    #     'pinned': False
    # },
    # {
    #     'title': 'Graded Discussion Title',
    #     'file_name': 'graded-discussion-prompt.md',
    #     'discussion_type': 'threaded',
    #     'published': False,
    #     'points_possible': 10,
    #     'grading_type': 'points',
    #     'due_at': '2026-08-28T06:59:00Z',
    #     'require_initial_post': True,
    #     'allow_rating': False,
    #     'pinned': False
    # }
]

not_created = ""

for discussion in discussions:
    title = discussion['title']
    file_name = os.path.join(MY_DISCUSSIONS, discussion['file_name'])

    try:
        with open(file_name, "r", encoding="utf-8") as input_file:
            text = input_file.read()
    except FileNotFoundError:
        not_created += discussion['file_name'] + "\n"
        continue

    message = markdown.markdown(text, extensions=['sane_lists'])
    markdown_dir = os.path.dirname(os.path.abspath(file_name))
    message = upload_and_replace_assets(message, course, markdown_dir)

    discussion_settings = {
        'title': title,
        'message': message,
        'published': discussion.get('published', False),
        'discussion_type': discussion.get('discussion_type', 'threaded'),
        'require_initial_post': discussion.get('require_initial_post', False),
        'allow_rating': discussion.get('allow_rating', True),
        'pinned': discussion.get('pinned', False)
    }

    for optional_field in ['delayed_post_at', 'lock_at', 'group_category_id']:
        if discussion.get(optional_field) not in [None, '']:
            discussion_settings[optional_field] = discussion[optional_field]

    points_possible = discussion.get('points_possible')
    if points_possible not in [None, '']:
        assignment = {
            'points_possible': points_possible,
            'grading_type': discussion.get('grading_type', 'points')
        }
        if discussion.get('due_at') not in [None, '']:
            assignment['due_at'] = discussion['due_at']
        if discussion.get('assignment_group_id') not in [None, '']:
            assignment['assignment_group_id'] = discussion['assignment_group_id']
        discussion_settings['assignment'] = assignment

    post = course.create_discussion_topic(**discussion_settings)

    print('Created: ', post)
    print(getattr(post, 'html_url', getattr(post, 'url', '')))

if not_created != "":
    print("Not created:\n", not_created)

"""
YYYY-MM-DDTHH:MM:SSZ - literal characters T and Z
All timestamps are sent and returned in ISO 8601 format.
All timestamps default to UTC time zone unless specified.
"""
