import os
import re
import sys
from urllib.parse import urlparse
from canvasapi import Canvas
from _credentials import (
    API_URL,
    API_KEY,
    COURSE_NUM,
    USER_ID,
    MY_PATH,
    MY_PAGES,
    MY_ANNOUNCEMENTS,
    MY_DISCUSSIONS,
    MY_ASSIGNMENTS,
)

def get_canvas_and_course():
    """Initializes the Canvas API client and fetches the configured Course."""
    try:
        canvas = Canvas(API_URL, API_KEY)
        course = canvas.get_course(COURSE_NUM)
        return canvas, course
    except Exception as e:
        sys.exit(
            f"[-] Canvas connection failed: {e}\n"
            "Please run setup_course.py and check the course's Canvas profile."
        )

def choose_item(items, display_attr="name"):
    """Generic interactive selection menu for Canvas list items with O(N) display."""
    for idx, item in enumerate(items, start=1):
        name = getattr(item, display_attr, str(item))
        print(f"{idx} - {name}")
    
    selection = input("Your selection: ").strip()
    try:
        return items[int(selection) - 1]
    except (ValueError, IndexError):
        sys.exit("Invalid selection.")

def resolve_content_path(file_name, content_dir):
    """Resolve a content filename from either the current directory or its content folder."""
    if os.path.isabs(file_name):
        return file_name
    if os.path.exists(file_name):
        return os.path.abspath(file_name)
    return os.path.abspath(os.path.join(content_dir, file_name))

def upload_and_replace_assets(html_content, course, markdown_dir):
    """
    Parses HTML content for local img src attributes, uploads them to Canvas,
    and replaces them with Canvas preview URLs.
    """
    # Regex to find all src attributes in img tags
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content)
    if not img_srcs:
        return html_content

    for src in img_srcs:
        # Skip remote links and embedded data URLs
        parsed = urlparse(src)
        if parsed.scheme or parsed.netloc or src.startswith('data:'):
            continue

        # Resolve local path relative to markdown file directory
        local_path = os.path.join(markdown_dir, src)
        if not os.path.exists(local_path):
            # Fallback to repo root or absolute path
            local_path = os.path.abspath(src)

        if os.path.exists(local_path) and os.path.isfile(local_path):
            print(f"  [+] Uploading local asset: {src} -> Canvas folder 'uploaded_assets'...")
            try:
                # ucfopen/canvasapi Course.upload returns a tuple (success, response)
                success, response = course.upload(local_path, parent_folder_path="uploaded_assets")
                if success:
                    file_id = getattr(response, "id", None) or response.get("id")
                    if file_id:
                        canvas_url = f"/courses/{course.id}/files/{file_id}/preview"
                        html_content = html_content.replace(src, canvas_url)
                        print(f"  [+] Replaced URL in HTML: {canvas_url}")
                    else:
                        print(f"  [-] Failed to extract File ID from Canvas response.")
                else:
                    print(f"  [-] Upload rejected by Canvas for: {src}")
            except Exception as e:
                print(f"  [-] Error uploading asset '{src}': {e}")
        else:
            print(f"  [-] Local file not found: '{src}' (tried '{os.path.join(markdown_dir, src)}')")

    return html_content
