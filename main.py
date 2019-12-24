import os
import shutil
import re
from sys import argv

quantity = 0
regex = "(.*)_\d+_\d+_\d+_n.(jpg|png|mp4)"

# Picture username recognition
#flag = None
#count = 0

errors = []

try:
    # Get commandline arguments
    if argv[1] != None:
        workdir = argv[1]
    else:
        workdir = raw_input("> Please, enter the working directory: ")

    # Deletes MacOs file
    if os.path.exists("{}/.DS_Store".format(workdir)):
        os.remove("{}/.DS_Store".format(workdir))

    # Explores subdirectories
    for root, dirs, files in os.walk(workdir):
        for i, entry in enumerate(files):
            match = re.search(regex, entry)
            # Detects username
            user = match.group(1)
            dir_from = root + "/{}".format(entry)
            dir_to = root + "/{}".format(user)

            # Moves picture to user dir
            if user in dirs:
                print entry, dirs
            # Creates dir if not exist
            else:
                os.makedirs(dir_to)
            os.system("mv {0} {1}".format(dir_from, dir_to))
            quantity += 1

            # # Picture username recognition
            # while flag not in ("yes", "y", "no", "n"):
            #     count =+ 1
            #     if count == 1:
            #         flag = raw_input("> Use picture username recognition? (default: [n]): ")
            #     else:
            #         flag = raw_input("> Sorry, you should answer 'yes' [y] or 'no [n]. Use picture username recognition? (default: [n]): ")
            # if flag in ("yes", "y"):
            #     os.system("python3.7 image2text/main.py -i {0}/{1} -o {0}".format(workdir, entry))

except Exception as e:
    errors.append(e)
    pass
except FileExists:
    pass

print """{} files moved succesfully.""".format(quantity)
if len(errors) > 0:
    print "\nErrors:"
    for i, error in enumerate(errors):
        print "[{0}] - {1}".format(i, error)
raw_input("""\nPress [ENTER] to continue...""")
