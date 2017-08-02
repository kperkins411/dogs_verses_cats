#!/usr/bin/env python

# USAGE
# python parse_data.py --train train.zip --test test.zip --validate validate.zip

# import the necessary packagesimport argparse
import os


#globals
import utils
utilities = utils.utils()

def create_uncategorized_dataset(homeDir, split, zipfile):
    '''
    unzips zipfile into splitdir

    :param homeDir: where zipfile is
    :param split: train, test or val
    :param zipfile: name of zipfile
    :return:
    '''
    # create all dirs

    split_dir = os.path.join(homeDir, split)
    utilities.makeDir(split_dir)

    # unzip all
    utilities.unzip_to_dir(os.path.join(homeDir, zipfile), split_dir)

    # the zip unzips into a parent directory where all images are
    # get the parent dir
    parentdir = os.listdir(split_dir)[0]
    allfilespath = os.path.join(split_dir, parentdir)

    allfiles =  os.listdir(allfilespath)

    for file in allfiles:
        os.rename(os.path.join(allfilespath, file), os.path.join(split_dir, file))

    #get rid of empty dir
    os.rmdir(allfilespath)


def create_dataset(homeDir, split, zipfile):
    '''
    unzips zipfile into dogs/cats subfolders under splitdir
    dir structure looks like
        splitdir
           dogs
           cats
    :param homeDir: where zipfile is
    :param split: train, test or val
    :param zipfile: name of zipfile
    :return:
    '''
    # create all dirs

    split_dir = os.path.join(homeDir, split)
    utilities.makeDir(split_dir)
    split_dogs_dir = os.path.join(split_dir, "dogs")
    utilities.makeDir(split_dogs_dir)
    split_cats_dir = os.path.join(split_dir, "cats")
    utilities.makeDir(split_cats_dir)

    # unzip all
    utilities.unzip_to_dir(os.path.join(homeDir, zipfile), split_dogs_dir)

    # the zip unzips into a parent directory where all images are
    # get the parent dir
    parentdir = os.listdir(split_dogs_dir)[0]
    allfilespath = os.path.join(split_dogs_dir, parentdir)

    allfiles =  os.listdir(allfilespath)

    for file in allfiles:
        if 'cat' in file:
            os.rename(os.path.join(allfilespath, file), os.path.join(split_cats_dir, file))
        else:
            os.rename(os.path.join(allfilespath, file), os.path.join(split_dogs_dir, file))

    #get rid of empty dir
    os.rmdir(allfilespath)

def main():
    # construct the argument parser
    parser = argparse.ArgumentParser(description='prepare data for dogs verses cats competition')
    parser.add_argument("-train", "--train", default="train.zip", help="train zip file, default = train.zip")
    parser.add_argument("-test", "--test", default="test.zip",help="test zip file, default = test.zip")
    parser.add_argument("-validate", "--validate", default="validate.zip",help="validate zip file, default = validate.zip")
    args = vars(parser.parse_args())

    #get zip names
    trainzip = args["train"]
    testzip = args["test"]
    validatezip = args["validate"]

    # where are we?
    root = os.path.abspath(os.path.dirname(__file__))
    homedir = os.getcwd()

    create_uncategorized_dataset(homedir,"test", testzip)
    create_dataset(homedir,"train", trainzip)
    create_dataset(homedir,"validate", validatezip)

if __name__ == '__main__':
    main()

