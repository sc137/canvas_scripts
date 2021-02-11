################
# _chooseFile.py
#
# Call this to list and choose files
# sable cantus
# Jan 2021
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
    print("Please select a file by number:")

    os.chdir(directory_name)
    path = os.getcwd()
    dir = os.listdir(path)
    for i in sorted(dir):
        print(dir.index(i)+1, "-", i)

    length = len(dir)
    selection = input("Your selection: ")
    selection = int(selection)
    file_name = dir[selection-1]
    print("You selected: ", file_name)

    user_choice = input("Is this correct? (y/n/q) ")
    if user_choice.lower() == 'y':
        pass
    elif user_choice.lower() == 'q':
        print("Goodbye")
        exit()
    else:
        print("Goodbye. Please try again.")
        exit()

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

##############################################################################
# TODO
# [ ] Allow user to select a different page if they choose 'n'
# [X] Sort the directory alpha - it's random in the array
