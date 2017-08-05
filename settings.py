NUMBER_OF_SAMPLES = 100

TRAIN_PERCENT = 0.9
VALIDATE_PERCENT = 0.1
CLASS1_NAME = "dogs"
CLASS2_NAME = "cats"

ALL_FOLDER_NAME = "all"
SAMPLES_FOLDER_NAME="samples"
DATA_FOLDER_NAME = "data"
TRAIN_FOLDER_NAME = "train"
VALIDATE_FOLDER_NAME = "validate"
KAGGLE_TEST_FOLDER_NAME="unknown"

# As large as you can, but no larger than 64 is recommended.
# If you have an older or cheaper GPU, you'll run out of memory, so will have to decrease this.
BATCH_SIZE = 8
TEST_BATCH_SIZE = 128
NUMBER_EPOCHS = 2

DATA_ALL = "data/all/"
DATA_SAMPLE = "data/sample/"
DATA_TEST = "data/unknown"
TRAIN = 'train'
VALIDATE = 'validate'

CHECKPOINTFILE = "bestweights.hdf5"








