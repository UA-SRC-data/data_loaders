# GardenRoots 

## Raw data
Raw data are available to project personnel at /iplant/home/rwalls/ua-src-data/gardenroots/. We are not publishing the raw data at this time due to privacy concerns for the participants. Preprocessed data at the census block level (in the scrutinizer subfolder) are available with the same level of detail for metal(oid) concentrations but with sufficient privacy.

## Preprocess data
This dataset uses the code in `../datapackage/mk_pkg.py`, `../point2shape/point2shape.py`, and `../point2shape/shapefiles/block_group/tl_2017_04_bg` to create a set of preprocessed files. For more details see `Makefile`.

### Create mapping file
Scrutinized data are in three separate sets, in the folder `scrutinizer`. To create mappings, first pull lists of traits from the three files that use block group for location (contain "_bg") in the file name.

**Plants:** Create a list of unique variables using `cut -d',' -f5,8 plants_bg.csv | tail +2 | sort | uniq > grplant_traits.csv`. Note that for this dataset, we must pull the "medium" column to see what material the metal concentrations were measured in. The `variable_desc` column is currently empty.

**Soil:** Create a list of unique variables using `cut -d',' -f5,8 soil_bg.csv | tail +2 | sort | uniq > grsoil_traits.csv`. Note that for this dataset, we must pull the "medium" column to see what material the metal concentrations were measured in. The `variable_desc` column is currently empty.

**Water:** Create a list of unique variables using `cut -d',' -f5,8 water_bg.csv | tail +2 | sort | uniq > grwater_traits.csv`. Note that for this dataset, we must pull the "medium" column to see what material the metal concentrations were measured in. The `variable_desc` column is currently empty.

Merge all three trait lists into `gr_traits.csv` and manually edit to fix header row and to add mappings to SRPDIO. Save as `gr-srpdio-mapping.csv`.


## Datapackage

This directory also contains the start of a [Frictionless Data](https://frictionlessdata.io/) package for the GardenRoots data.

## Author

Ken Youens-Clark <kyclark@arizona.edu>
