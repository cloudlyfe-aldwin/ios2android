#!/usr/bin/env python


import glob
import argparse
import os.path
import json
from shutil import copyfile
import PIL
from PIL import Image
import sys
import collections
import shutil
import re

imagesets = []
ImagePaths = collections.namedtuple('ImagePaths', 'ios android')


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


def makedirs(shouldClear):
    if shouldClear:
        if os.path.exists("./res"):
            shutil.rmtree('./res')

    makedir("./res")
    makedir("./res/drawable-ldpi")
    makedir("./res/drawable-mdpi")
    makedir("./res/drawable-hdpi")
    makedir("./res/drawable-xhdpi")
    makedir("./res/drawable-xxhdpi")
    makedir("./res/drawable-xxxhdpi")


def getExtension(fileName):
    filename, file_extension = os.path.splitext(fileName)
    return file_extension


def getFileNames(iosPath, androidPath, fileName, universalName):
    return ImagePaths(iosPath + "/" + fileName, androidPath + universalName + getExtension(fileName))


def commonPrefix(fileNames):
    "Given a list of path names, returns the longest common leading component"
    if not fileNames: return ''
    s1 = min(fileNames)
    s2 = max(fileNames)

    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]

    return s1


def convertCamel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def cleanedUp(imageFileName):

    if imageFileName.endswith("@"):
        imageFileName = imageFileName[:-len("@")]

    imageFileName = imageFileName.replace("-", "_")
    imageFileName = convertCamel(imageFileName)
    imageFileName = imageFileName.lower()

    #TODO: Convert camel case to snake case

    return imageFileName


def scale(image, scaleFactor):
    img = Image.open(image)
    newWidth = img.size[0] * scaleFactor
    newHeight = img.size[1] * scaleFactor

    print("Rescaling image from " + str(img.size[0]) + " x " + str(img.size[1]) + " to " + str(newWidth) + " x " + str(newHeight))

    img = img.resize((int(newWidth), int(newHeight)), PIL.Image.ANTIALIAS)

    img.save(image)


def parseAppIconImageset(imageset, scaleFactor):
    return # TODO



def parseImageset(imageset, scaleFactor): #TODO: Optional skipping of certain *dpi files passed in through command-line args
    if os.path.isdir(imageset) == False:
        return

    contents = {}
    path = ""

    for filename in glob.glob(imageset + '/*', recursive=True):
        if 'Contents.json' in filename:
            with open(filename) as data_file:
                contents = json.load(data_file)
                path = os.path.dirname(filename)

    ldpi___p75x_filenames = {}
    mdpi___1x___filenames = {}
    hdpi___1p5__filenames = {}
    xhdpi__2x___filenames = {}
    xxhdpi_3x___filenames = {}

    # Find common prefix of the image name
    imageNames = []
    for image in contents["images"]:
        imageNames.append(image["filename"])

    universalFilename = cleanedUp(commonPrefix(imageNames))

    print("Processing: " + universalFilename)

    for image in contents["images"]:
        if image["idiom"] == "universal": # TODO: Other idioms (e.g, iPhone, iPad)
            if image["scale"] == "1x":
                ldpi___p75x_filenames = getFileNames(path, "./res/drawable-ldpi/",   image["filename"], universalFilename)
                mdpi___1x___filenames = getFileNames(path, "./res/drawable-mdpi/",   image["filename"], universalFilename)
            if image["scale"] == "2x":
                hdpi___1p5__filenames = getFileNames(path, "./res/drawable-hdpi/",   image["filename"], universalFilename)
                xhdpi__2x___filenames = getFileNames(path, "./res/drawable-xhdpi/",  image["filename"], universalFilename)
            if image["scale"] == "3x":
                xxhdpi_3x___filenames = getFileNames(path, "./res/drawable-xxhdpi/", image["filename"], universalFilename)

    copyfile(ldpi___p75x_filenames.ios, ldpi___p75x_filenames.android)
    copyfile(mdpi___1x___filenames.ios, mdpi___1x___filenames.android)
    copyfile(hdpi___1p5__filenames.ios, hdpi___1p5__filenames.android)
    copyfile(xhdpi__2x___filenames.ios, xhdpi__2x___filenames.android)
    copyfile(xxhdpi_3x___filenames.ios, xxhdpi_3x___filenames.android)

    scale(ldpi___p75x_filenames.android, .75)
    scale(hdpi___1p5__filenames.android, .75)

    if not scaleFactor == 1:
        scale(ldpi___p75x_filenames.android, scaleFactor)
        scale(mdpi___1x___filenames.android, scaleFactor)
        scale(hdpi___1p5__filenames.android, scaleFactor)
        scale(xhdpi__2x___filenames.android, scaleFactor)
        scale(xxhdpi_3x___filenames.android, scaleFactor)





def main(argv):
    appIconFolderName = ''
    scaleFactor = 1

    parser = argparse.ArgumentParser(description='Short sample app')

    parser.add_argument('-i', action="store_true", default=False)
    parser.add_argument('-c', action="store_true", default=False, help="Clear the drawable folders")
    parser.add_argument('-f', action="store", dest="appIconFolder", default="AppIcon")
    parser.add_argument('-s', action="store", dest="scaleFactor", type=int, default=1)

    args = parser.parse_args()

    # TODO: Parse App Icon folder different, or update command line args for ignoring/not ignoring it

    print("App Icon Folder: " + args.appIconFolder)

    getImageSets(imagesets, 'imageset', 'AppIcon')

    print("Found imagesets: " + str(imagesets))

    makedirs(args.c)

    for imageset in imagesets:
        parseImageset(imageset, args.scaleFactor)


if __name__ == "__main__":
    main(sys.argv[1:])
