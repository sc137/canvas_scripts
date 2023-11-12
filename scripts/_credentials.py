#!/usr/bin/env python3
# _credentials.py
# sable cantus
# from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID,
# MY_PAGES, MY_ANNOUNCEMENTS, MY_DISCUSSIONS, MY_ASSIGNMENTS

# Set your system path to the course folder
MY_PATH = "/path/to/your/course/folder/"
MY_PAGES = MY_PATH + "pages/"
MY_ANNOUNCEMENTS = MY_PATH + "announcements/"
MY_DISCUSSIONS =  MY_PATH + "discussions/"
MY_ASSIGNMENTS =  MY_PATH + "assignments/"

# Canvas API URL
# This will be the URL used to access your institutions canvas account
# e.g. https://<collegename>.instructure.com
API_URL = ""

# Canvas API key
# You will generate this in canvas <<canvas url>>/profile/settings
# Click New Access token and name it something you recognize
API_KEY = ""

# Current Course
# This is the course you will be working with
# Open canvas to your specific course and the number will be in the url
# following the <<canvas url>>/courses/#####
COURSE_NUM = 11111

# My user ID
# Run the api_test.py script to check all other settings and that will list
# all TA's and Instructors for the specified course.
# Grab YOUR user ID and put it here
USER_ID = 111111
