# import the necessary packages
import os
import settings
import logging
import numpy as np
import bcolz

logging.basicConfig(
    #filename = 'parse_data.log', #comment this line out if you want data in the console
    format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s",
    level = logging.DEBUG
)

traindir = os.path.join(os.getcwd(), os.path.join(settings.DATA_SAMPLE, settings.TRAIN))    #used to load model
datadir = os.path.join(os.getcwd(), settings.DATA_TEST)                                     #kaggle data
resultsdir = os.getcwd()

# Import our class, and instantiate
from vgg16 import Vgg16
vgg = Vgg16()

# get an image batch, used only to set up the model
modelsetupbatches = vgg.get_batches(traindir, batch_size=settings.BATCH_SIZE)

# add a different fully connected layer at the end, load best weights used
vgg.finetune(modelsetupbatches, checkpointfile =settings.CHECKPOINTFILE)

# #here is the training data
# batches = vgg.get_batches(datadir, batch_size=settings.BATCH_SIZE)

#TODO there is something wrong with batchsize here, if set to 1 and I have 10 images in datadir, I get 10 preds (fast)
#TODO is set to 2 I get 2*10 preds and it takes twice as long?
import timeit
starttime = timeit.default_timer()
batches, preds = vgg.test(datadir, batch_size = 1, verbose=1)
logging.info("prediction took " + str(timeit.default_timer()-starttime) + ' seconds to complete')

#save all the data for later
# c=bcolz.carray(filenames, rootdir=os.path.join(os.getcwd(), "filenames.dat"), mode='w')
# c.flush()
# c=bcolz.carray(preds, rootdir=os.path.join(os.getcwd(), "preds.dat"), mode='w')
# c.flush()

#lets get the dog prediction column, and the filenames
isDog = preds[:,1]
isDog = isDog.clip(min = 0.05,max=0.95)

filenames = batches.filenames
ids = [float((file.split('.')[0]).split('/')[1]) for file in filenames]

#if this fails make sure batch_size=1 in vgg.test func above
submission = np.stack([ids,isDog], axis=1)

#generate submission file as per kaggle requirements
submission_file_name = 'submission.csv'
np.savetxt(submission_file_name, submission, fmt='%d,%.5f', header='id,label', comments='')








