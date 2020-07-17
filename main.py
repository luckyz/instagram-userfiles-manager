# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
import subprocess
import re
import logging
import shutil
from PIL import Image
from moviepy.editor import VideoFileClip
from sys import argv, exc_info

regex = r"(.*)(\_\d+(\_n)?){3}\.(jpg|png|mp4)"
time_regex = r"(\w*)\s\w*"
unclassified_folder = "0_unclassified/"
workdir = "."
errors = []

BOX = (80, 40, 350, 70)

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

    def get_username(self, file):
        match = re.search(regex, file)
        if not match is None:
            return match.group(1)

    def create_dir(self, username):
        if not username in self.files:
            return os.makedirs(r"{}/{}".format(self.dir, username))

    def dir_exists(self, name):
        return os.path.exists(r"{}/{}".format(self.dir, name))

    def picture_recognition(self, file, threshold=190, lang="eng"):
        path = os.path.dirname("{}/{}".format(os.getcwd(), file))
        os.chdir(path)
        image = Image.open(file)
        image = image.crop(BOX)
        image = image.convert('L')
        image = image.point(lambda p: p > threshold and 255)
        image.save("{}/crop.png".format(os.getcwd()), dpi=(500, 500))
        FNULL = open(os.devnull, "w")
        command = subprocess.call(["tesseract", "{}/{}.png".format(os.getcwd(), "crop"), "crop", "-l", "{}".format(lang)], stdout=FNULL, stderr=subprocess.STDOUT)
        # os.system("tesseract {}/{}.png crop -l {}".format(os.getcwd(), "crop", lang))
        text = open("{}/crop.txt".format(os.getcwd()), "r").read()
        image.close()
        os.remove("{}/crop.png".format(path))
        os.remove("{}/crop.txt".format(path))
        match = re.search(time_regex, text)
        if not match is None:
            text = match.group(1)

        return text

    def video_capture(self, file, frame=10):
        picture = VideoFileClip(file)
        filename = os.path.basename(picture.filename)
        frame_filename = filename.split(".")[0] + ".png"
        picture.save_frame("crop.png", frame)
        # temp_frame = Image.open(frame_filename)

        return "crop.png"

    def organize(self):
        try:
            # Media with any pattern
            self.get_files()
            self.get_dirs()
            for file in self.files:
                username = self.get_username(file)
                if not username is None:
                    if not self.dir_exists(username):
                        self.create_dir(username)

                # Media without pattern
                else:
                    if not self.dir_exists(unclassified_folder):
                        self.create_dir(unclassified_folder)
                    username = unclassified_folder
                    filename_without_ext, ext = os.path.basename(file).split(".")
                    if ext == "mp4":
                        temp_frame = self.video_capture(file)
                        self.picture_recognition(temp_frame)
                    else:
                        self.picture_recognition(file)

                self.quantity += 1

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
            workdir = os.path.abspath(os.path.expanduser(workdir))
        obj = Organizer(workdir)
        obj.organize()

        print("\n{} files moved succesfully.".format(obj.quantity))

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
