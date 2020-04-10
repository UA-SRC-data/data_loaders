# Point2Shape

This program will add census "GEOID" field to delimited (CSV) file containing fields "latitude" and "longitude".

You need the shapefile(s) for the US census tracts, blocks, or block_groups for Arizona:

* [TIGER/Line Shapefile, 2017, 2010 state, Arizona, 2010 Census Block State-based](https://www2.census.gov/geo/tiger/TIGER2017//TABBLOCK/tl_2017_04_tabblock10.zip)
* [TIGER/Line Shapefile, 2017, state, Arizona, Current Block Group State-based](https://www2.census.gov/geo/tiger/TIGER2017/BG/tl_2017_04_bg.zip)
* [TIGER/Line Shapefile, 2016, state, Arizona, Current Census Tract State-based](https://www2.census.gov/geo/tiger/TIGER2016/TRACT/tl_2016_04_tract.zip)

I would suggest creating a `shapefiles` directory containing directories for each type:

```
$ tree shapefiles/
shapefiles/
├── block
│   ├── tl_2017_04_tabblock10.cpg
│   ├── tl_2017_04_tabblock10.dbf
│   ├── tl_2017_04_tabblock10.prj
│   ├── tl_2017_04_tabblock10.shp
│   ├── tl_2017_04_tabblock10.shp.ea.iso.xml
│   ├── tl_2017_04_tabblock10.shp.iso.xml
│   ├── tl_2017_04_tabblock10.shp.xml
│   └── tl_2017_04_tabblock10.shx
├── block_group
│   ├── tl_2017_04_bg.cpg
│   ├── tl_2017_04_bg.dbf
│   ├── tl_2017_04_bg.prj
│   ├── tl_2017_04_bg.shp
│   ├── tl_2017_04_bg.shp.ea.iso.xml
│   ├── tl_2017_04_bg.shp.iso.xml
│   ├── tl_2017_04_bg.shp.xml
│   ├── tl_2017_04_bg.shx
│   └── tl_2017_04_bg.zip
└── tract
    ├── tl_2016_04_tract.cpg
    ├── tl_2016_04_tract.dbf
    ├── tl_2016_04_tract.prj
    ├── tl_2016_04_tract.shp
    ├── tl_2016_04_tract.shp.ea.iso.xml
    ├── tl_2016_04_tract.shp.iso.xml
    ├── tl_2016_04_tract.shp.xml
    └── tl_2016_04_tract.shx
```

The `--shapefile` option needs the basename of the shapefile, so `shapefiles/tract/tl_2016_04_tract` is sufficient.

Given the `inputs/sample.csv` file with this structure:

```
// ****** Record 1 ****** //
id        : 1
latitude  : 36.4526
longitude : -109.1665
```

Run with:

```
$ ./point2shape.py -s shapefiles/block_group/tl_2017_04_bg -t block_group \
  -f inputs/sample.csv -o out-sample.csv
```

The output file will look like this:

```
// ****** Record 1 ****** //
id         : 1
latitude   : 36.4526
longitude  : -109.1665
geoid      : 040019441005
geoid_type : block_group
```

When run with a "tract" shapefile:

```
$ ./point2shape.py -s shapefiles/tract/tl_2016_04_tract -t tract \
  -f inputs/sample.csv -o out-sample.csv
```

The output file will look like this:

```
// ****** Record 1 ****** //
id         : 1
latitude   : 36.4526
longitude  : -109.1665
geoid      : 04001944100
geoid_type : tract
```

When a shape cannot be found in the shapefile for a given lat/lon, the value will be "NA."

The program can handle files with BOM (byte-order marks) if you use the `--bom` flag.

Run the program with `-h` or `--help` for the usage:

```
$ ./point2shape.py -h
usage: point2shape.py [-h] -f FILE -s FILE -t shapetype [-d delimiter]
                      [-o FILE] [-b]

Add census block group to file containing lat/lon

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file (default: None)
  -s FILE, --shapefile FILE
                        Input file (default: None)
  -t shapetype, --type shapetype
                        Shapefile type (default: None)
  -d delimiter, --delimiter delimiter
                        Input file field delimiter (default: ,)
  -o FILE, --outfile FILE
                        Output file (default: out.csv)
  -b, --bom             Input file has byte-order mark (default: False)
```

See Makefile for examples of how to run.

# Author

Ken Youens-Clark <kyclark@arizona.edu>
