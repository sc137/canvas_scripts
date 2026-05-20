#!/usr/bin/env python3
# upload_files.py
# Bulk upload files or folders to Canvas course files.

import _venv
import os
import sys
import argparse
from _client import get_canvas_and_course

def parse_args():
    parser = argparse.ArgumentParser(
        description="Bulk upload files or directories to Canvas course files."
    )
    parser.add_argument(
        "source",
        help="Local file path or directory containing files to upload."
    )
    parser.add_argument(
        "--folder",
        default=None,
        help="Destination folder path in Canvas (e.g., 'Slides', 'Lectures'). Defaults to course root."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    source_path = os.path.abspath(args.source)

    if not os.path.exists(source_path):
        sys.exit(f"[-] Error: Source path does not exist: {source_path}")

    # Gather files
    files_to_upload = []
    if os.path.isdir(source_path):
        for root, _, files in os.walk(source_path):
            for file in files:
                # Skip hidden/system files
                if file.startswith('.'):
                    continue
                files_to_upload.append(os.path.join(root, file))
    else:
        files_to_upload.append(source_path)

    if not files_to_upload:
        sys.exit("[-] No files found to upload.")

    # Initiate Canvas and Course
    _, course = get_canvas_and_course()
    print("Selected course: \n", course.name)
    print()

    target_folder = args.folder if args.folder else "Course Root (/)"
    print(f"Ready to upload {len(files_to_upload)} file(s) to Canvas folder: '{target_folder}'")
    for f in files_to_upload:
        print(f"  - {os.path.basename(f)}")
    print()

    confirm = input("Proceed with upload? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Upload cancelled.")
        return 0

    success_count = 0
    fail_count = 0

    for idx, filepath in enumerate(files_to_upload, start=1):
        filename = os.path.basename(filepath)
        print(f"[{idx}/{len(files_to_upload)}] Uploading {filename}...", end="", flush=True)
        try:
            # Upload to Canvas course
            kwargs = {}
            if args.folder:
                kwargs["parent_folder_path"] = args.folder

            success, response = course.upload(filepath, **kwargs)
            if success:
                print(" Success!")
                success_count += 1
            else:
                print(" Failed (Canvas rejected).")
                fail_count += 1
        except Exception as e:
            print(f" Failed (Error: {e})")
            fail_count += 1

    print("\n" + "=" * 30)
    print(f"Upload complete!")
    print(f"Successfully uploaded: {success_count}")
    print(f"Failed uploads:        {fail_count}")
    print("=" * 30)

    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
