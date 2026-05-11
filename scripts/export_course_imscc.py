#!/usr/bin/env python3
import _venv
# export_course_imscc.py
# Exports the Canvas course to an IMSCC archive.

import os
import sys
import time
import requests
from datetime import datetime

try:
    from canvasapi import Canvas
except ImportError:
    sys.exit("Please run setup_course.py to install requirements.")

try:
    from _credentials import API_URL, API_KEY, COURSE_NUM, MY_PATH
except ImportError:
    sys.exit("Please run setup_course.py to create _credentials.py")

# Ensure archives directory exists
ARCHIVES_DIR = os.path.join(MY_PATH, "archives")
if not os.path.exists(ARCHIVES_DIR):
    os.makedirs(ARCHIVES_DIR)

def main():
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(COURSE_NUM)
    print(f"Selected course: {course.name}")
    print("Initiating IMSCC export... this may take a few minutes.")

    # Initiate export
    export = course.export_content(export_type="common_cartridge")
    print(f"Export job started (ID: {export.id}).")

    # Poll status
    while True:
        export = course.get_content_export(export.id)
        status = export.workflow_state
        if status == 'exported':
            print("\nExport completed successfully on Canvas servers!")
            break
        elif status == 'failed':
            sys.exit("\nExport failed on Canvas servers.")
        else:
            print(f"Status: {status}... waiting 10 seconds.")
            time.sleep(10)

    # Download file
    if hasattr(export, 'attachment') and 'url' in export.attachment:
        download_url = export.attachment['url']
        filename = f"{course.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.imscc"
        # Sanitize filename
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '.', '_', '-')]).rstrip()
        filepath = os.path.join(ARCHIVES_DIR, filename)
        
        print(f"Downloading to {filepath} ...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print("Download complete!")
    else:
        print("Export finished but no download URL was found in the attachment payload.")

if __name__ == "__main__":
    main()
