#!/usr/bin/env python


import glob
import argparse
import os.path
from shutil import copyfile
from collections import defaultdict
import sys, getopt
import numpy as np
from collections import defaultdict

imagesets = []
#cFiles    = []
# hFiles    = []
# classMap  = defaultdict(list)

def getImageSets(array, extension, ignore):
    for file in glob.glob('./**/*.' + extension, recursive=True):
        if ignore not in file:
            array.append(file)

def makedir(path):
    if os.path.exists(path):
        if not os.path.isdir(path):
            os.remove(path)
            os.makedirs(path)
    else:
            os.makedirs(path)

def makedirs():
        makedir("./res")
        makedir("./drawable-ldpi")
        makedir("./drawable-mdpi")
        makedir("./drawable-hdpi")
        makedir("./drawable-xhdpi")
        makedir("./drawable-xxhdpi")
        makedir("./drawable-xxxhdpi")

def parseImageset(imageset):
    if os.path.isdir(imageset) == False:
        return

    images = []
    content_json = ""

    for filename in glob.glob(imageset + '/*', recursive=True):
        if 'Contents.json' in filename:
            file = open(filename, "r")
            content_json = file.read()
        else:
            images.append(filename)




def main(argv):
    appIconFolderName = ''
    scaleFactor = 1

    parser = argparse.ArgumentParser(description='Short sample app')

    parser.add_argument('-i', action="store_true", default=False)
    parser.add_argument('-f', action="store", dest="appIconFolder", default="AppIcon")
    parser.add_argument('-s', action="store", dest="scaleFactor", type=int, default=1)

    args = parser.parse_args()

    # TODO: Parse App Icon folder different, or update command line args for ignoring/not ignoring it

    print("App Icon Folder: " + args.appIconFolder)

    getImageSets(imagesets, 'imageset', 'AppIcon')

    print("Found imagesets: " + str(imagesets))

    makedirs()

    for imageset in imagesets:
        parseImageset(imageset)


if __name__ == "__main__":
    main(sys.argv[1:])
