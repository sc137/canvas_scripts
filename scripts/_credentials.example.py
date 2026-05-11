#!/usr/bin/env python3
# _credentials.example.py
#
# Copy this file to _credentials.py and fill in your local Canvas settings.
# Do not commit _credentials.py with real API credentials or course IDs.

# Set your system path to this course folder.
# Include the trailing slash.
MY_PATH = "/path/to/your/course/folder/"
MY_PAGES = MY_PATH + "pages/"
MY_ANNOUNCEMENTS = MY_PATH + "announcements/"
MY_DISCUSSIONS = MY_PATH + "discussions/"
MY_ASSIGNMENTS = MY_PATH + "assignments/"

# Canvas API URL
# This is the base URL for your institution's Canvas account.
# Example: https://example.instructure.com
API_URL = "https://example.instructure.com"

# Canvas API key
# Create this in Canvas profile settings.
API_KEY = "replace-with-your-canvas-access-token"

# Current Canvas course
# This is the number in the course URL after /courses/.
COURSE_NUM = 123456

# Your Canvas user ID
# Run api_get_user_id.py after setting API_URL, API_KEY, and COURSE_NUM.
USER_ID = 123456
