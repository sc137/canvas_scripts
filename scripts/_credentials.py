#!/usr/bin/env python3
# _credentials.py
# sable cantus
# 1/15/21
# call api url and key for each school from this file
#
# from _credentials import API_URL, API_KEY, COURSE_NUM, USER_ID
# print(API_URL)
# print(API_KEY)


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
