# dogs_verses_cats
First Kaggle competition

setup project with /data directory containing both test.zip and train.zip datasets (available from kaggle).  
Run parse_data to unzip data, create proper directory structure(see below, tree-d output), and slot dogs/cats images into correct directories.
<BR>
data<BR>
    ├ all<BR>
    │   ├ train<BR>
    │   │   ├ cats<BR>
    │   │   └ dogs<BR>
    │   └ validate<BR>
    │       ├ cats<BR>
    │       └ dogs<BR>
    ├ sample<BR>
    │   ├ train<BR>
    │   │   ├ cats<BR>
    │   │   └ dogs<BR>
    │   └ validate<BR>
    │       ├ cats<BR>
    │       └ dogs<BR>
    └ test<BR>


Then run train.py to train vgg16 predictor (first on sample dataset then on all data, see code after following comment to select) <BR>
#which dataset? The large or the small
