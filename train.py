# import the necessary packages
import argparse
import os
import shutil

#globals
import utils
import settings
import logging
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping

logging.basicConfig(
    #filename = 'parse_data.log', #comment this line out if you want data in the console
    format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s",
    level = logging.DEBUG
)

# path = "data/all/"
path = "data/sample/"

# where are we?
thisdir = os.getcwd()
datadir = os.path.join(thisdir, path)

# As large as you can, but no larger than 64 is recommended.
# If you have an older or cheaper GPU, you'll run out of memory, so will have to decrease this.
batch_size=8
number_of_epochs = 5

# Import our class, and instantiate
from vgg16 import Vgg16
vgg = Vgg16()

# Grab a few images at a time for training and validation.
# NB: They must be in subdirectories named based on their category
batches = vgg.get_batches(path+'train', batch_size=batch_size)
val_batches = vgg.get_batches(path+'validate', batch_size=batch_size*2)

# add a different fully connected layer at the end
vgg.finetune(batches)

# create checkpoint to be used by model.fit to save the best model via callback
filepath = "./best.weights.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=2, verbose=0, mode='auto')
callbacks_list = [checkpoint]

vgg.fit(batches, val_batches, nb_epoch=number_of_epochs, callbacks = callbacks_list)

