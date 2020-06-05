# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
import re
import logging
import shutil
from PIL import Image
from sys import argv, exc_info

regex = r"(.*)(\_\d+(\_n)?){3}\.(jpg|png|mp4)"
unclassified_folder = "0_unclassified/"
workdir = "."
errors = []

class Organizer(object):

    def __init__(self, dir=workdir):
        super(Organizer, self).__init__()
        self.dir = os.path.abspath(os.path.expanduser(dir))
        self.quantity = 0
        os.chdir(self.dir)

    def get_dirs(self):
        self.dirs = [dir for dir in os.listdir(self.dir) if os.path.isdir(dir)]
        return self.dirs

    def get_files(self):
        self.files = [file for file in os.listdir(self.dir) if os.path.isfile(file)]

        try:
            self.files.remove(".DS_Store")
        except Exception as e:
            # TODO: ignore when ds_store file not exists
            # logging.info(e)
            # errors.append([exc_info()[-1].tb_lineno, e])
            pass
        finally:
            return self.files

    def get_username(self, entry):
        match = re.search(regex, entry)
        if not match is None:
            return match.group(1)

    def open_image(self, entry):
        dir = os.getcwd()
        return Image.open("{}/{}".format(dir, entry))

    def close_image(self, image):
        return image.close()

    def remove_image(self, image):
        return os.remove("{}/crop.png".format(dir))

    def crop_image(self, image):
        return image.crop((70,30,300,60))

    def convert_to_grayscale(self):
        return image.convert('L')

    def perform_image(self, image):
        threshold = 170
        return image.point(lambda p: p > threshold and 255)

    def save_image(self, image):
        return image.save("crop.png", "PNG")

    def create_dir(self, username):
        if not username in self.files:
            return os.makedirs(r"{}/{}".format(self.dir, username))

    def dir_exists(self, name):
        return os.path.exists(r"{}/{}".format(self.dir, name))

    def organize(self):
        try:
            self.get_files()
            self.get_dirs()
            for file in self.files:
                username = self.get_username(file)
                if not username is None:
                    if not self.dir_exists(username):
                        self.create_dir(username)
                    self.quantity += 1


                else:
                    if not self.dir_exists(unclassified_folder):
                        self.create_dir(unclassified_folder)
                    username = unclassified_folder

                shutil.move(r"{}/{}".format(self.dir, file), r"{}/{}".format(self.dir, username))

        except Exception as e:
            print(errors.append([exc_info()[-1].tb_lineno, e]))


def main():
    try:
        # Get commandline arguments
        if len(argv) > 1:
            workdir = argv[1]
        else:
            workdir = str(input(">> Please, enter the working directory: "))

        obj = Organizer(workdir)
        obj.organize()

        print("{} files moved succesfully.".format(obj.quantity))

        input("\nPress [ENTER] to continue...")

    except Exception as e:
        # TODO: ignore last input error
        # errors.append([exc_info()[-1].tb_lineno, e])
        pass

    finally:
        if len(errors) > 0:
            print("\nErrors:")
            for error in errors:
                print("line {}: {}".format(error[0], error[1]))

if __name__ == '__main__':
    main()
