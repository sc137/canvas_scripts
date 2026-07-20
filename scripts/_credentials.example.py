#!/usr/bin/env python3
# _credentials.example.py
#
# Copy this file to _credentials.py and fill in your local Canvas settings.
# Do not commit _credentials.py with real API credentials or course IDs.

import os

from _profiles import load_canvas_profile

# Set your system path to this course folder.
# Include the trailing slash.
MY_PATH = "/path/to/your/course/folder/"
MY_PAGES = MY_PATH + "pages/"
MY_ANNOUNCEMENTS = MY_PATH + "announcements/"
MY_DISCUSSIONS = MY_PATH + "discussions/"
MY_ASSIGNMENTS = MY_PATH + "assignments/"

# Canvas connection profile
# The profile stores the institution URL and API key in the user-level profile
# store. CANVAS_PROFILE, CANVAS_API_URL, and CANVAS_API_KEY can override these
# values for one command.
_DEFAULT_CANVAS_PROFILE = "college-name"
CANVAS_PROFILE = os.environ.get("CANVAS_PROFILE", _DEFAULT_CANVAS_PROFILE)
API_URL, API_KEY = load_canvas_profile(CANVAS_PROFILE)

# Current Canvas course
# This is the number in the course URL after /courses/.
COURSE_NUM = 123456

# Your Canvas user ID
# Run api_get_user_id.py after setting API_URL, API_KEY, and COURSE_NUM.
USER_ID = 123456
