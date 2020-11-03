# USGS Soil data
This directory contains code for processing USGS data on metal(oid) concentrations in soil in the state of Arizona.

Source:

https://pubs.usgs.gov/ds/801/downloads/

You need the shapefile for the US census blocks for Arizona to be in a directory called "shape."

https://catalog.data.gov/dataset/tiger-line-shapefile-2017-state-arizona-current-block-group-state-based

## Preprocess data

```bash
$ ./to_scrutinizer.py -h
usage: to_scrutinizer.py [-h] [-f FILE] [-u FILE] [-o FILE] [-m medium]
                         [-s source]

Load USGS data

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file (default: az_data_bg.csv)
  -u FILE, --units FILE
                        Input file (default: units.csv)
  -o FILE, --outfile FILE
                        Output file (default: scrutinizer.csv)
  -m medium, --medium medium
                        Medium for data (default: soil)
  -s source, --source source
                        Source for data (default: USGS)
 ```

### Create mapping file

Create a list of unique variables using `cut -d',' -f6,7 scrutinizer.csv | uniq > usgs_traits.csv`. Note that this is shifted by 1 column to allow for the common in the location column (seperating lat and long). The header row therefore needs to be corrected manually.

Manually edit `usgs_traits.csv` to fix header row and to add mappings to SRPDIO. Save as `usgs-srpdio-mapping.csv`.
