# GardenRoots 

## Raw data
Raw data are available to project personnel at /iplant/home/rwalls/ua-src-data/gardenroots/. We are not publishing the raw data at this time due to privacy concerns for the participants. Preprocessed data at the census block level (in the scrutinizer subfolder) are available with the same level of detail for metal(oid) concentrations but with sufficient privacy.

## Preprocess data
This dataset uses the code in `../datapackage/mk_pkg.py`, `../point2shape/point2shape.py`, and `../point2shape/shapefiles/block_group/tl_2017_04_bg` to create a set of preprocessed files. For more details see `Makefile`.

## Datapackage

This directory also contains the start of a [Frictionless Data](https://frictionlessdata.io/) package for the GardenRoots data.

## Author

Ken Youens-Clark <kyclark@arizona.edu>
