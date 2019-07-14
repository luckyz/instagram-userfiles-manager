import os
import shutil
import re

quantity = 0
regex = "(.*)_\d+_\d+_\d+_n.[jpg|mp4]"

if os.path.exists("/Users/lucas/Desktop/instagram/.DS_Store"):
    os.remove("/Users/lucas/Desktop/instagram/.DS_Store")

for root, dirs, files in os.walk("/Users/lucas/Desktop/instagram"):
    for i, entry in enumerate(files):
        match = re.search(regex, entry)
        # Delete Mac OS X attributes file
        os.system("rm {0}/.DS_Store".format(root))
        print entry, match
        user = match.group(1)
        dir_from = root + "/{}".format(entry)
        dir_to = root + "/{}".format(user)
        try:
            os.makedirs(dir_to)
        except OSError:
            pass
        print "Moving: {0} {1}".format(match, dir_to)
        os.system("mv {0} {1}".format(dir_from, dir_to))
        quantity += 1
raw_input("""
{0} files moved succesfully.
Press any key to contiune...
""".format(quantity))
