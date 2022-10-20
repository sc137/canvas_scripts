# Canvas Course Builder & Updater

This project uses a series of python scripts to build and update your Canvas LMS course pages, discussions, assignments, and more.

We create markdown documents in the various folders and run the appropriate script from the scripts folder. I have found this helps with large courses that have dozens of pages, discussions, and assignments.

The scripts are written with this hierarchy in mind.

## Why use scripts?

### This is very fast for me to use

Markdown is fast. Canvas LMS is slow. I have wasted hours of time on one class navigating to pages, clicking edit, clicking html, saving, publishing, etc.

With this project I write my content as I desire. I include images that are web hosted (e.g. amazon s3, b2, 3cmediasolutions, etc.) and use embed codes for videos. Another great embeddable resource is any kind of google doc or form.

When I update content I can use any text editor to make the updates and then run a script to update that page on canvas.

### Repeatable

I can run the script twice to update 2 courses in canvas. I have multiple sections of the same course.

### I own my work

You may be able to export your canvas course and keep a copy. Then you can import that to your new course and make changes as needed. I have found this time consuming for large courses I teach.

You may not be able to delete your course content depending on settings of a particular college.

In either case all of my work is in my course directory in plain text. I can make a copy of it and push it up to the next course.

In many cases, the URL created will be copied to the clipboard for you to modify (announcements, assignments, discussions, and pages).

## Is this a complete solution?

Nope. This is a tool to help me with the parts that Canvas is bad at. I still have to login to the course to manage discussions and to publish modules (I prefer to do this manually)

## Project Files

<pre>
canvas_scripts
├── README.md
├── announcements
│   └── README.md
├── assignments
│   └── README.md
├── discussions
│   └── README.md
├── pages
│   └── README.md
└── scripts
    ├── _chooseFile.py
    ├── _credentials.py
    ├── api_test.py
    ├── create_announcement.py
    ├── create_assignment.py
    ├── create_discussion_post.py
    ├── create_modules.py
    ├── create_multi_pages.py
    ├── create_page.py
    ├── create_quiz.py
    ├── get_page_contents.py
    ├── list_assignments.py
    ├── list_courses.py
    ├── list_discussion_entries.py
    ├── list_discussions.py
    ├── list_modules.py
    ├── list_pages.py
    ├── list_quizzes.py
    ├── list_students.py
    └── update_page.py
</pre>

## Get started

### Setup the course

Start by opening the scripts folder and editing the \_credentials.py file.

Next run the api_test.py to make sure everything is working and to get your user ID. Put that in the \_credentials.py file too.

### Create a test page

Create a test page in the pages folder in Markdown and run the create_page.py script.

usage with no filename:

<pre>
./scripts/create_page.py
# this will provide a list of all markdown files in the pages folder
# choose by number
</pre>

usage with filename:

<pre>
./scripts/create_page.py pages/module-2-learning-guide.md
# immediately prompts for the title
</pre>

## Requirements

- Python 3
- pip3 canvasapi
- pip3 markdown
- pip3 pyperclip

## Project Links

- [UCFOPEN CanvasAPI Github](https://github.com/ucfopen/canvasapi)
- [CanvasAPI Documentation](https://canvasapi.readthedocs.io/en/stable/getting-started.html)
- [Canvas LMS API Documentation](https://canvas.instructure.com/doc/api/index.html)
