# import the necessary packages
'''
Once done the weights of the finetuned model (with new FC layer)
are in settings.CHECKPOINTFILE.
'''
import argparse
import os
import shutil

#globals
import utils
import settings
import logging
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
import bcolz


logging.basicConfig(
    #filename = 'parse_data.log', #comment this line out if you want data in the console
    format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s",
    level = logging.DEBUG
)

#which dataset?  The large or the small
path = settings.DATA_ALL
# path = settings.DATA_SAMPLE

# where are we?
datadir = os.path.join(os.getcwd(), path)

# Import our class, and instantiate
from vgg16 import Vgg16
vgg = Vgg16()

# Grab a few images at a time for training and validation.
# NB: They must be in subdirectories named based on their category
batches = vgg.get_batches(path+settings.TRAIN, batch_size=settings.BATCH_SIZE)
val_batches = vgg.get_batches(path+ settings.VALIDATE, batch_size=settings.BATCH_SIZE*2)

# add a different fully connected layer at the end
vgg.finetune(batches, checkpointfile =settings.CHECKPOINTFILE)

# create checkpoint to be used by model.fit to save the best model via callback
filepath = settings.CHECKPOINTFILE
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

vgg.fit(batches, val_batches, nb_epoch=settings.NUMBER_EPOCHS, callbacks = callbacks_list)








