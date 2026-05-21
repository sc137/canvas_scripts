#!/usr/bin/env python3
# update_multi_discussions.py
# sable cantus
# update multiple discussion posts from markdown files

import _venv
import os
import sys

try:
    import markdown
except:
    print("Please install markdown")
    sys.exit(0)
from _client import get_canvas_and_course, API_URL, COURSE_NUM, MY_DISCUSSIONS

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# List discussions to update.
# discussion_id can be found in the Canvas URL:
# https://mtsac.instructure.com/courses/XXXXXX/discussion_topics/DISCUSSION_ID
discussions = [
    # ['discussion_id', 'file_name.md'],
    ['2112559', '02-reflection.md'],
    ['2112560', '03-reflection.md'],
    ['2112562', '04-reflection.md'],
    ['2112563', '05-reflection.md'],
    ['2112564', '06-reflection.md'],
    ['2112565', '07-reflection.md'],
    ['2112566', '08-reflection.md'],
    ['2112567', '09-reflection.md'],
    ['2112568', '10-reflection.md'],
    ['2112569', '11-reflection.md'],
    ['2112570', '12-reflection.md'],
    ['2112571', '13-reflection.md'],
    ['2112572', '14-reflection.md'],
]

not_found = ""

for discussion in discussions:
    discussion_id = discussion[0]
    file_name = os.path.join(MY_DISCUSSIONS, discussion[1])

    try:
        with open(file_name, "r", encoding="utf-8") as input_file:
            text = input_file.read()
    except FileNotFoundError:
        not_found += discussion[1] + "\n"
        continue

    message = markdown.markdown(text, extensions=['sane_lists'])

    topic = course.get_discussion_topic(discussion_id)
    topic.update(message=message)

    updated_url = API_URL + "/courses/" + str(COURSE_NUM) + "/discussion_topics/" + discussion_id
    print("Updated: ", updated_url)

if not_found != "":
    print("Not updated:\n", not_found)
