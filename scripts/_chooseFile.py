import _venv
# Call this to list and choose files
# sable cantus
# import _chooseFile
# _chooseFile.chooseFile('../pages')

import os


def chooseFile(directory_name):
    # Make sure the ../pages directory exists
    if os.path.isdir(directory_name):
        pass
    else:
        print('no dir found', directory_name)
        exit()

    # Select a file to work with
    os.chdir(directory_name)
    path = os.getcwd()
    dir_list = sorted(os.listdir(path))

    while True:
        print("Please select a file by number:")
        for i, item in enumerate(dir_list):
            print(i + 1, "-", item)

        selection = input("Your selection: ")
        try:
            selection = int(selection)
            file_name = dir_list[selection-1]
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.\n")
            continue

        print("You selected: ", file_name)

        user_choice = input("Is this correct? (y/n/q) ")
        if user_choice.lower() == 'y':
            break
        elif user_choice.lower() == 'q':
            print("Goodbye")
            exit()
        else:
            print("Please try again.\n")

    # Choose a title
    title = input("Please select your page title (blank to ignore): ")

    # Confirm the output

    # Return the title and Filename
    return title, file_name


def delayPost():
    print("post format is: YYYY-MM-DDTHH:MM:SSZ")
    print("literal characters T and Z")
    print("All timestamps are UTC (add 8 hours)")
    delayed_post = input("Please enter the time to post: ")
    return delayed_post

