# dogs_verses_cats
First Kaggle competition

setup project with /data directory containing both test.zip and train.zip datasets (available from kaggle).  
Run parse_data to unzip data, create proper directory structure(see below, tree-d output), and slot dogs/cats images into correct directories.
.
└── data<BR>
    ├── all
    │   ├── train
    │   │   ├── cats
    │   │   └── dogs
    │   └── validate
    │       ├── cats
    │       └── dogs
    ├── sample
    │   ├── train
    │   │   ├── cats
    │   │   └── dogs
    │   └── validate
    │       ├── cats
    │       └── dogs
    └── test


Then run train.py to train vgg16 predictor (first on sample dataset then on all data, see comment #which dataset? The large or the small
? in train.py to select)
