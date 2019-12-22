import os
import shutil
import re

quantity = 0
regex = "(.*)_\d+_\d+_\d+_n.[jpg|mp4]"

errors = []

try:
    workdir = raw_input("> Please, enter the working directory: ")

    if os.path.exists("{}/.DS_Store".format(workdir)):
        os.remove("{}/.DS_Store".format(workdir))

    for root, dirs, files in os.walk(workdir):
        for i, entry in enumerate(files):
            match = re.search(regex, entry)
            user = match.group(1)
            dir_from = root + "/{}".format(entry)
            dir_to = root + "/{}".format(user)
            if not user in dirs:
                os.makedirs(dir_to)
            if entry in dirs:
                print entry, dirs
            os.system("mv {0} {1}".format(dir_from, dir_to))
            quantity += 1
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
raw_input("""Press [ENTER] to continue...""")
