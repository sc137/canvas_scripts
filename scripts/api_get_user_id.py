#!/usr/bin/env python3
# api_get_current_user.py
# sable cantus
# Run this to get the user ID for the current user

import _venv
from _client import get_canvas_and_course

canvas, course = get_canvas_and_course()
print("Selected course: \n", course.name)
print()

# Get the current user (you)
current_user = canvas.get_current_user()
USER_ID = current_user.id
print(current_user)
print(f'Add {USER_ID} to the _credentials.py file.')