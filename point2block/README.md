# Point2Block

This program will add census "block_group" field to delimited (CSV) file containing fields "latitude" and "longitude".

You need the shapefile for the US census blocks for Arizona:

https://catalog.data.gov/dataset/tiger-line-shapefile-2017-state-arizona-current-block-group-state-based

Given the `inputs/sample.csv` file with this structure:

```
// ****** Record 1 ****** //
id        : 1
latitude  : 36.4526
longitude : -109.1665
```

Run with:

```
$ ./p2b.py -s shape/tl_2017_04_bg.dbf inputs/sample.csv -o out-sample.csv
```

The output file will look like this:

```
// ****** Record 1 ****** //
id          : 1
latitude    : 36.4526
longitude   : -109.1665
block_group : 040019441005
```

When a block group cannot be found in the shapefile, the value will be "NA."

The program can handle files with BOM (byte-order marks) if you use the `--bom` flag:

```
$ ./p2b.py -h
usage: p2b.py [-h] [-d delimiter] [-s FILE] [-o FILE] [-b] FILE

Add census block group to file containing lat/lon

positional arguments:
  FILE                  Input file

optional arguments:
  -h, --help            show this help message and exit
  -d delimiter, --delimiter delimiter
                        Input file field delimiter (default: ,)
  -s FILE, --shapefile FILE
                        Input file (default: )
  -o FILE, --outfile FILE
                        Output file (default: out.csv)
  -b, --bom             Input file has byte-order mark (default: False)
```

See Makefile for examples of how to run.

# Author

Ken Youens-Clark <kyclark@arizona.edu>
