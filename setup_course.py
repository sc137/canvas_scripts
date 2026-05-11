#!/usr/bin/env python3
# setup_course.py
# Interactive setup script for Canvas course credentials

import os
import sys
import subprocess

def ensure_venv():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(root_dir, 'venv')
    venv_python = os.path.join(venv_dir, 'bin', 'python')
    if os.name == 'nt':
        venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')
        
    # Check if we are running from the venv
    if os.path.abspath(sys.executable) != os.path.abspath(venv_python):
        print("=> Ensuring virtual environment exists...")
        if not os.path.exists(venv_dir):
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        
        print("=> Installing/Updating dependencies...")
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])
        
        print("=> Restarting setup inside virtual environment...\n")
        os.execv(venv_python, [venv_python] + sys.argv)

def main():
    ensure_venv()
    print("=========================================")
    print(" Canvas Scripts - Course Setup Onboarding")
    print("=========================================\n")
    print("This script will help you configure your local course credentials.")
    print("It will generate the '_credentials.py' file required by the other scripts.\n")

    # Auto-detect root dir
    root_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
    
    existing_creds = {}
    cred_file = os.path.join(root_dir, 'scripts', '_credentials.py')
    if os.path.exists(cred_file):
        try:
            sys.path.insert(0, os.path.join(root_dir, 'scripts'))
            import _credentials
            existing_creds['MY_PATH'] = getattr(_credentials, 'MY_PATH', root_dir)
            existing_creds['API_URL'] = getattr(_credentials, 'API_URL', '')
            existing_creds['API_KEY'] = getattr(_credentials, 'API_KEY', '')
            existing_creds['COURSE_NUM'] = getattr(_credentials, 'COURSE_NUM', '')
            sys.path.pop(0)
            print("=> Found existing _credentials.py. Press Enter to keep current values.\n")
        except Exception:
            if 'scripts' in sys.path[0]:
                sys.path.pop(0)

    # 1. Path
    print("1. Local Course Path")
    default_path = existing_creds.get('MY_PATH', root_dir)
    print(f"Default: {default_path}")
    my_path = input("Press Enter to accept, or type the full path: ").strip()
    if not my_path:
        my_path = default_path
    if not my_path.endswith('/'):
        my_path += '/'

    # 2. API_URL
    print("\n2. Canvas API URL")
    print("Example: https://example.instructure.com")
    default_url = existing_creds.get('API_URL', '')
    if default_url:
        print(f"Current: {default_url}")
    api_url = input("API URL: ").strip()
    if not api_url and default_url:
        api_url = default_url
    api_url = api_url.rstrip('/')

    # 3. API_KEY
    print("\n3. Canvas API Key")
    print("Go to your Canvas profile Settings -> 'New Access Token' to generate this.")
    default_key = existing_creds.get('API_KEY', '')
    if default_key:
        print(f"Current: {'*' * 10}{default_key[-4:] if len(default_key) > 4 else ''}")
    api_key = input("API Key: ").strip()
    if not api_key and default_key:
        api_key = default_key

    # 4. COURSE_NUM
    print("\n4. Course Number")
    print("Example: For https://example.instructure.com/courses/123456, enter 123456")
    default_course = existing_creds.get('COURSE_NUM', '')
    if default_course:
        print(f"Current: {default_course}")
        
    course_num_input = input("Course Number: ").strip()
    if not course_num_input and default_course:
        course_num_input = str(default_course)
        
    while not course_num_input.isdigit():
        print("Please enter digits only.")
        course_num_input = input("Course Number: ").strip()
    
    course_num = int(course_num_input)

    print("\nAttempting to connect to Canvas and verify credentials...")
    user_id = None
    
    try:
        from canvasapi import Canvas
        canvas = Canvas(api_url, api_key)
        
        # Verify course
        course = canvas.get_course(course_num)
        print(f"  [+] Successfully connected to Course: {course.name}")
        
        # Get user ID
        current_user = canvas.get_current_user()
        user_id = current_user.id
        print(f"  [+] Successfully verified User: {current_user.name} (ID: {user_id})")
        
    except ImportError:
        print("\nWARNING: canvasapi module is not installed. Please run 'python3 -m pip install -r requirements.txt'")
        print("We will save your credentials without verification.")
    except Exception as e:
        print(f"\nFailed to verify connection to Canvas: {e}")
        print("Please double check your API URL, Key, and Course Number.")
        choice = input("Do you want to save these credentials anyway? (y/n): ")
        if choice.lower() != 'y':
            print("Exiting without saving.")
            sys.exit(1)

    if user_id is None:
        user_id = "123456 # Verify failed or canvasapi missing. Replace manually or run api_get_user_id.py later"

    # Write to _credentials.py
    cred_file = os.path.join(root_dir, 'scripts', '_credentials.py')
    
    print(f"\nWriting credentials to {cred_file}...")
    try:
        with open(cred_file, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python3\n")
            f.write("# _credentials.py\n")
            f.write("# Generated by setup_course.py\n\n")
            f.write(f'MY_PATH = "{my_path}"\n')
            f.write('MY_PAGES = MY_PATH + "pages/"\n')
            f.write('MY_ANNOUNCEMENTS = MY_PATH + "announcements/"\n')
            f.write('MY_DISCUSSIONS = MY_PATH + "discussions/"\n')
            f.write('MY_ASSIGNMENTS = MY_PATH + "assignments/"\n\n')
            f.write(f'API_URL = "{api_url}"\n')
            f.write(f'API_KEY = "{api_key}"\n')
            f.write(f'COURSE_NUM = {course_num}\n')
            f.write(f'USER_ID = {user_id}\n')
        
        print("Success! You are all set.")
        print("You can now use the other scripts in this repository.")
    except Exception as e:
        print(f"Failed to write to file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
