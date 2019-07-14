import os
import shutil
import re

quantity = 0
regex = "(.*)_\d+_\d+_\d+_n.[jpg|mp4]"

errors = []

if os.path.exists("/Users/lucas/Desktop/instagram/.DS_Store"):
    os.remove("/Users/lucas/Desktop/instagram/.DS_Store")

try:
    for root, dirs, files in os.walk("/Users/lucas/Desktop/instagram"):
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

print """{0} files moved succesfully.""".format(quantity)
if len(errors) > 0:
    print "\nErrors:"
    for i, error in enumerate(errors):
        print "[{0}] - {1}".format(i, error)
raw_input("""Press [ENTER] to continue...""")
