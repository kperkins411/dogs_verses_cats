#!/usr/bin/env python

# USAGE
# python parse_data.py --train train.zip --test test.zip

#splits the train data into 90% train and 10% validation
#the test set is for testing model, results submitted to kaggle


# import the necessary packages
import argparse
import os
import shutil

#globals
import utils
import settings
import logging

logging.basicConfig(
    #filename = 'parse_data.log', #comment this line out if you want data in the console
    format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s",
    level = logging.DEBUG
)
utilities = utils.utils()


#the next 2 functions used to create proper directory structure
def getDirs(homeDir, split):
    split_dir = os.path.join(homeDir, split)
    split_dogs_dir = os.path.join(split_dir, "dogs")
    split_cats_dir = os.path.join(split_dir, "cats")
    return split_dir,split_cats_dir, split_dogs_dir

def makeDirs(split_dir, split_cats_dir, split_dogs_dir):
    utilities.makeDir(split_dir)
    utilities.makeDir(split_dogs_dir)
    utilities.makeDir(split_cats_dir)

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

def create_sample_dataset(homeDir):
    # create all dirs
    sample_dir, sample_cats_dir, sample_dogs_dir = getDirs(homeDir, "sample")
    makeDirs(sample_dir,sample_cats_dir, sample_dogs_dir)

    #where training data resides
    _,train_cats_dir, train_dogs_dir = getDirs(homeDir, "train")

    # copy in  cats and dogs
    cats = os.listdir(train_cats_dir)
    for cat in cats[:settings.NUMBER_OF_SAMPLES]:
        shutil.copy2( os.path.join(train_cats_dir,cat), os.path.join(sample_cats_dir,cat))

    dogs = os.listdir(train_dogs_dir)
    for dog in dogs[:100]:
        shutil.copy2( os.path.join(train_dogs_dir,dog), os.path.join(sample_dogs_dir,dog))

def create_train_validate_test_split(homeDir,zipfile):
    '''
     unzips and parses zipfile into train/test/validate splits
     :param homeDir: where zipfile is
     :param zipfile: name of zipfile
     :return:
     '''

    # create all dirs
    train_dir, train_cats_dir, train_dogs_dir = getDirs(homeDir, "train")
    makeDirs(train_dir, train_cats_dir, train_dogs_dir)

    test_dir, test_cats_dir, test_dogs_dir = getDirs(homeDir, "test")
    makeDirs(test_dir, test_cats_dir, test_dogs_dir)

    validate_dir, validate_cats_dir, validate_dogs_dir = getDirs(homeDir, "validate")
    makeDirs(validate_dir, validate_cats_dir, validate_dogs_dir)

    # unzip all
    utilities.unzip_to_dir(os.path.join(homeDir, zipfile), train_dogs_dir)

    # the zip unzips into a parent directory where all images are
    # get the parent dir
    try:
        parentdir = os.listdir(train_dogs_dir)[0]
    except IndexError:
        print("error getting parentdir")
        return
    allfilespath = os.path.join(train_dogs_dir, parentdir)
    allfiles = os.listdir(allfilespath)

    #how many files do we have?
    numbfiles = len(allfiles)

    #how many train/test/validate samples
    numbtraincats = numbtraindogs = int(settings.TRAIN_PERCENT*(numbfiles/2))
    numbvalcats = numbvaldogs = int(settings.VALIDATE_PERCENT*(numbfiles/2))
    numbtestcats = numbtestdogs = int(settings.TEST_PERCENT * (numbfiles/2))

    destdir = None
    for file in allfiles:
        if 'cat' in file:
            if numbtraincats != 0:
                numbtraincats-=1
                destdir = train_cats_dir
            elif numbvalcats != 0:
                numbvalcats -=1
                destdir = validate_cats_dir
            else:
                numbtestcats -=1
                destdir = test_cats_dir
            os.rename(os.path.join(allfilespath, file), os.path.join(destdir, file))
        else:
            if numbtraindogs != 0:
                numbtraindogs-=1
                destdir = train_dogs_dir
            elif numbvaldogs != 0:
                numbvaldogs -=1
                destdir = validate_dogs_dir
            else:
                numbtestdogs -=1
                destdir = test_dogs_dir
            os.rename(os.path.join(allfilespath, file), os.path.join(destdir, file))

    # get rid of empty dir
    os.rmdir(allfilespath)

def main():
    # construct the argument parser
    parser = argparse.ArgumentParser(description='prepare data for dogs verses cats competition')
    parser.add_argument("-train", "--train", default="train.zip", help="train zip file, default = train.zip")
    parser.add_argument("-test", "--test", default="test.zip",help="test zip file, default = test.zip")
    args = vars(parser.parse_args())

    #get zip names
    trainzip = args["train"]
    kaggle_testzip = args["test"]

    # where are we?
    root = os.path.abspath(os.path.dirname(__file__))
    homedir = os.getcwd()

    #create the datasets
    create_uncategorized_dataset(homedir,"test", kaggle_testzip)
    create_train_validate_test_split(homedir,trainzip)
    create_sample_dataset(homedir)

if __name__ == '__main__':
    main()

