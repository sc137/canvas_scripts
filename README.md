# Canvas Course Scripts

This repository is a collection of Python scripts for managing Canvas LMS course content from local files. It is meant to be cloned for a new class, configured with that course's Canvas credentials, and then used to create, update, list, and export Canvas content as needed.

Credentials are intentionally handled with a local-only file. The repository includes `scripts/_credentials.example.py` as the template, but each user creates their own ignored `scripts/_credentials.py` for real Canvas tokens and course IDs.

The main workflow is:

1. Write course content as Markdown in the content folders.
2. Copy `scripts/_credentials.example.py` to `scripts/_credentials.py`.
3. Configure Canvas credentials in `scripts/_credentials.py`.
4. Run scripts from the repository root to create, update, list, or export Canvas course data.

## What This Is For

Canvas is often slow for repeated content work: creating pages, editing HTML, scheduling announcements, building assignments, and checking large sets of course objects. These scripts keep most reusable course material in plain text so it can be edited, copied to a future course, and versioned outside Canvas.

This is not a complete Canvas course management system. You should still review content in Canvas, publish or unpublish items intentionally, and check course settings, dates, modules, gradebook settings, and student-facing views manually.

## Repository Layout

```text
canvas_scripts/
├── README.md
├── announcements/
│   └── README.md
├── assignments/
│   └── README.md
├── discussions/
│   └── README.md
├── gradebook_export/
│   └── README.md
├── pages/
│   └── README.md
└── scripts/
    ├── _chooseFile.py
    ├── _client.py
    ├── _credentials.example.py
    ├── add_module_items.py
    ├── api_get_user_id.py
    ├── api_test.py
    ├── create_announcement.py
    ├── create_assignment.py
    ├── create_discussion_post.py
    ├── create_modules.py
    ├── create_multi_announcements.py
    ├── create_multi_assignment.py
    ├── create_multi_discussions.py
    ├── create_multi_pages.py
    ├── create_page.py
    ├── generate_photo_roster.py
    ├── get_assignment_contents.py
    ├── get_page_contents.py
    ├── get_student_grades.py
    ├── list_assignments.py
    ├── list_courses.py
    ├── list_discussion_entries.py
    ├── list_discussions.py
    ├── list_modules.py
    ├── list_pages.py
    ├── list_quizzes.py
    ├── list_students.py
    ├── update_multi_pages.py
    ├── update_page.py
    └── upload_files.py
```

## Setup

Ensure you have Python 3 installed, then run the interactive onboarding script from the repository root:

```sh
./setup_course.py
```

This script will automatically create a Python virtual environment (`venv/`), install all required packages, and ask you for your `API_URL`, `API_KEY`, and `COURSE_NUM`. Canvas access tokens are created from Canvas profile settings. `COURSE_NUM` is the number in the course URL after `/courses/`.

Packages automatically installed include:

- `canvasapi` connects the create, update, list, and content scripts to Canvas.
- `markdown` converts local Markdown files to HTML before sending them to Canvas.
- `html2text` converts existing Canvas assignment HTML back into Markdown.
- `requests` is used by the gradebook export and native IMSCC scripts.
- `pandas` writes gradebook data to parquet files.
- `pyarrow` provides the parquet engine used by pandas.

The setup script will then verify your connection, fetch your user ID, and generate your `scripts/_credentials.py` file. This file is intentionally ignored by Git so your real API tokens are not accidentally committed.

> [!TIP]
> **No manual activation needed!** You do not need to run `source venv/bin/activate`. Thanks to our auto-restarting architecture, you can simply run any script normally (e.g., `./scripts/list_pages.py`), and it will instantly detect and use the virtual environment for you.

## Content Folders

Put Markdown files in the matching folder:

- `pages/` for Canvas pages
- `assignments/` for assignment descriptions
- `announcements/` for announcement bodies
- `discussions/` for discussion prompts

You can use hosted image URLs or local relative image paths (e.g., `![diagram](images/diagram.png)`) in your Markdown. The create scripts for pages, assignments, announcements, and discussions, plus the page update scripts, automatically upload referenced local images to the course's `uploaded_assets` folder in Canvas and replace the local paths with Canvas-hosted preview links.

## Common Commands

Create a Canvas page from a Markdown file:

```sh
./scripts/create_page.py
```

Create a Canvas page by passing a file directly:

```sh
./scripts/create_page.py pages/example-page.md
```

List current course objects:

```sh
./scripts/list_pages.py
./scripts/list_assignments.py
./scripts/list_discussions.py
./scripts/list_modules.py
./scripts/list_quizzes.py
```

Create individual course objects:

```sh
./scripts/create_assignment.py
./scripts/create_discussion_post.py
./scripts/create_announcement.py
```

Create multiple course objects from editable lists in the scripts:

```sh
./scripts/create_multi_pages.py
./scripts/create_multi_assignment.py
./scripts/create_multi_discussions.py
./scripts/create_multi_announcements.py
```

Update an existing Canvas page from a local Markdown file:

```sh
./scripts/update_page.py
```

Upload local files or directories directly to Canvas files:

```sh
# Upload a single PowerPoint file to course root files
./scripts/upload_files.py lectures/week1.pptx

# Upload all files in a directory to a "Lectures" folder in Canvas
./scripts/upload_files.py lectures/ --folder Lectures
```

Export Canvas content or course data:

```sh
./scripts/get_page_contents.py
./scripts/get_assignment_contents.py
./scripts/get_student_grades.py
./scripts/generate_photo_roster.py
```

## Script Notes

Some scripts are interactive and ask you to select a file, enter a title, confirm a Canvas item, or enter a date. Announcement scheduling uses Canvas timestamps in ISO 8601 format, such as:

```text
2026-08-17T18:00:00Z
```

The multi-create scripts contain editable lists near the top of each file. Review those lists before running them so you know exactly what will be created in Canvas.

## Project Links

- [UCFOPEN CanvasAPI GitHub](https://github.com/ucfopen/canvasapi)
- [CanvasAPI Documentation](https://canvasapi.readthedocs.io/en/stable/getting-started.html)
- [Canvas LMS API Documentation](https://canvas.instructure.com/doc/api/index.html)

*Do we even need to mention that AI tools have read, reviewed, or updated any of the code here? Well, it has.*
