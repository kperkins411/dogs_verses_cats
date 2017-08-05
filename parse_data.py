#!/usr/bin/env python

# USAGE
# python parse_data.py --train train.zip --test test.zip

#splits the train data into 90% train and 10% validation
#the test set is for testing model, results submitted to kaggle
'''
#dir structure
all
        unknown
            kaggle
               #uncategorized kaggle test data
        all
            train
                dogs
                cats
            validate
                dogs
                cats
        sample
            train
                dogs
                cats
            validate
                dogs
                cats
     train.zip # zip of all data
     test.zip  #zip of kaggle data
'''


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
    split_dogs_dir = os.path.join(split_dir, settings.CLASS1_NAME)
    split_cats_dir = os.path.join(split_dir, settings.CLASS2_NAME)
    return split_dir,split_cats_dir, split_dogs_dir

def makeDirs(*dirs):
    if not dirs:
        logging.debug("called makedirs with no dirs to make!")
    for dir in dirs:
        utilities.makeDir(dir)

def create_uncategorized_dataset(homeDir, split, zipfile, subset = None):
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

    split_dir = os.path.join(split_dir, "kaggle")
    utilities.makeDir(split_dir)

    # unzip all
    utilities.unzip_to_dir(os.path.join(homeDir, zipfile), split_dir)

    # the zip unzips into a parent directory where all images are
    # get the parent dir
    parentdir = os.listdir(split_dir)[0]
    allfilespath = os.path.join(split_dir, parentdir)

    allfiles =  os.listdir(allfilespath)
    # len = len(allfiles)
    # if subset != None:
    #     len = subset

    length = len(allfiles) if subset == None else subset

    for file in allfiles[:length]:
        os.rename(os.path.join(allfilespath, file), os.path.join(split_dir, file))

    #get rid of empty dir
    try:
        os.rmdir(allfilespath)
    except OSError:
        return


def create_sample_dataset(datadir):
    # where training data resides
    alldatadir = os.path.join(datadir, settings.ALL_FOLDER_NAME)
    train_dir, train_cats_dir, train_dogs_dir = getDirs(alldatadir, settings.TRAIN_FOLDER_NAME)
    validate_dir, validate_cats_dir, validate_dogs_dir = getDirs(alldatadir, settings.VALIDATE_FOLDER_NAME)

    # create all dirs
    sampledatadir = os.path.join(datadir, "sample")
    sample_train_dir, sample_train_cats_dir, sample_train_dogs_dir = getDirs(sampledatadir, settings.TRAIN_FOLDER_NAME)
    makeDirs(sampledatadir, sample_train_dir, sample_train_cats_dir, sample_train_dogs_dir)

    sample_validate_dir, sample_validate_cats_dir, sample_validate_dogs_dir = getDirs(sampledatadir, settings.VALIDATE_FOLDER_NAME)
    makeDirs( sample_validate_dir, sample_validate_cats_dir, sample_validate_dogs_dir)

    # how many train/test/validate samples
    numbtraincats = numbtraindogs = int(settings.TRAIN_PERCENT * (settings.NUMBER_OF_SAMPLES / 2))
    numbvalcats = numbvaldogs = int(settings.VALIDATE_PERCENT * (settings.NUMBER_OF_SAMPLES  / 2))

    # copy in  cats and dogs
    cats = os.listdir(train_cats_dir)
    for cat in cats[:numbtraincats]:
        shutil.copy2( os.path.join(train_cats_dir,cat), os.path.join(sample_train_cats_dir,cat))

    cats = os.listdir(validate_cats_dir)
    for cat in cats[:numbvalcats]:
        shutil.copy2(os.path.join(validate_cats_dir, cat), os.path.join(sample_validate_cats_dir, cat))

    dogs = os.listdir(train_dogs_dir)
    for dog in dogs[:numbtraindogs]:
        shutil.copy2(os.path.join(train_dogs_dir, dog), os.path.join(sample_train_dogs_dir, dog))

    dogs = os.listdir(validate_dogs_dir)
    for dog in dogs[:numbvaldogs]:
        shutil.copy2(os.path.join(validate_dogs_dir, dog), os.path.join(sample_validate_dogs_dir, dog))
def create_train_validate_split(datadir,zipfile):
    '''
     unzips and parses zipfile into train/validate splits

     :param homeDir: where zipfile is
     :param zipfile: name of zipfile
     :return:

     '''

    # create all dirs
    alldatadir = os.path.join(datadir, "all")
    train_dir, train_cats_dir, train_dogs_dir = getDirs(alldatadir, settings.TRAIN_FOLDER_NAME)
    makeDirs(alldatadir,train_dir, train_cats_dir, train_dogs_dir)

    validate_dir, validate_cats_dir, validate_dogs_dir = getDirs(alldatadir, settings.VALIDATE_FOLDER_NAME)
    makeDirs(alldatadir,validate_dir, validate_cats_dir, validate_dogs_dir)

    # unzip all
    utilities.unzip_to_dir(os.path.join(datadir, zipfile), train_dogs_dir)

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

    destdir = None
    for file in allfiles:
        if 'cat' in file:
            if numbtraincats != 0:
                numbtraincats-=1
                destdir = train_cats_dir
            else :
                numbvalcats -=1
                destdir = validate_cats_dir

            os.rename(os.path.join(allfilespath, file), os.path.join(destdir, file))
        else:
            if numbtraindogs != 0:
                numbtraindogs-=1
                destdir = train_dogs_dir
            else:
                numbvaldogs -=1
                destdir = validate_dogs_dir
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
    thisdir = os.getcwd()
    alldatadir = os.path.join(thisdir,settings.DATA_FOLDER_NAME)

    #create the datasets
    create_uncategorized_dataset(alldatadir,settings.KAGGLE_TEST_FOLDER_NAME, kaggle_testzip)
    create_train_validate_split(alldatadir,trainzip)
    create_sample_dataset(alldatadir)

if __name__ == '__main__':
    main()

