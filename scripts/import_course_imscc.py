#!/usr/bin/env python3
# import_course_imscc.py
# Imports an IMSCC archive into the Canvas course.

import os
import sys
import time
import requests

try:
    from canvasapi import Canvas
except ImportError:
    sys.exit("Please run setup_course.py to install requirements.")

try:
    from _credentials import API_URL, API_KEY, COURSE_NUM, MY_PATH
except ImportError:
    sys.exit("Please run setup_course.py to create _credentials.py")

ARCHIVES_DIR = os.path.join(MY_PATH, "archives")

def choose_file(directory_name):
    if not os.path.isdir(directory_name):
        sys.exit(f"No archives directory found at {directory_name}")
        
    files = sorted([f for f in os.listdir(directory_name) if f.endswith('.imscc')])
    if not files:
        sys.exit(f"No .imscc files found in {directory_name}")

    while True:
        print("Please select an archive to import:")
        for i, item in enumerate(files):
            print(f"{i + 1} - {item}")

        selection = input("Your selection: ")
        try:
            selection = int(selection)
            file_name = files[selection-1]
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.\n")
            continue

        print("You selected:", file_name)
        user_choice = input("Is this correct? (y/n/q) ")
        if user_choice.lower() == 'y':
            return os.path.join(directory_name, file_name)
        elif user_choice.lower() == 'q':
            print("Goodbye")
            sys.exit(0)
        else:
            print("Please try again.\n")

def main():
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(COURSE_NUM)
    print(f"Selected course: {course.name}")
    print()

    filepath = choose_file(ARCHIVES_DIR)
    file_size = os.path.getsize(filepath)

    print("\n" + "!" * 50)
    print(" WARNING: DANGEROUS OPERATION")
    print("!" * 50)
    print(f"You are about to import a full course archive into:")
    print(f"COURSE: {course.name} (ID: {COURSE_NUM})")
    print(f"FILE:   {os.path.basename(filepath)}")
    print("This may overwrite existing course content or create duplicates.")
    
    confirm = input('\nType "IMPORT" in all caps to confirm and proceed: ')
    if confirm != "IMPORT":
        sys.exit("Aborted.")

    print("\nInitiating upload and migration... this will take some time.")
    
    try:
        # Request a content migration with pre_attachment
        migration = course.create_content_migration(
            migration_type='canvas_cartridge_importer',
            pre_attachment={'name': os.path.basename(filepath), 'size': file_size}
        )
        
        # If Canvas API returned pre_attachment data, we upload the file manually
        if hasattr(migration, 'pre_attachment'):
            upload_url = migration.pre_attachment['upload_url']
            upload_params = migration.pre_attachment['upload_params']
            
            print(f"Uploading {os.path.basename(filepath)}...")
            with open(filepath, 'rb') as f:
                response = requests.post(upload_url, data=upload_params, files={'file': f})
                response.raise_for_status()
                
            print("Upload complete! Canvas is now unpacking the course.")
        else:
            print("Warning: Canvas did not return an upload URL in pre_attachment. It's possible the library handles this differently.")
            
        print("Polling migration status...")
        while True:
            migration = course.get_content_migration(migration.id)
            status = migration.workflow_state
            if status == 'completed':
                print("\nMigration completed successfully!")
                break
            elif status == 'failed':
                sys.exit("\nMigration failed on Canvas servers.")
            else:
                print(f"Status: {status}... waiting 10 seconds.")
                time.sleep(10)
                
    except Exception as e:
        sys.exit(f"\nMigration failed: {e}")

if __name__ == "__main__":
    main()
