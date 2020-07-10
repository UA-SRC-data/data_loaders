# EJSCREEN

The EJSCREEN data is available at this FTP site:

```bash
ftp://newftp.epa.gov/EJSCREEN/2019/
```

To get the data, run `make data` or:

```bash
wget ftp://newftp.epa.gov/EJSCREEN/2019/EJSCREEN_2019_USPR.csv.zip
```

This is a large file (282M zipped, 764M unzipped), so it will not be committed to GitHub.

The three main data files you'll need:

* EJSCREEN_2019_USPR.csv: The data for 2019 from EJScreen, 220K records
* EJScreen_Index_DescriptionsV4_Pub.xlsx: Excel spreadsheet of the variable names, descriptions
* EJScreen_Index_DescriptionsV4_Pub.csv: CSV of the former

The EJSCREEN_2019_USPR.csv file contains 367 fields.
You may want to install the `csvchk` (https://pypi.org/project/csvchk/) program to help you see the structure:

```bash
$ csvchk EJSCREEN_2019_USPR.csv
// ****** Record 1 ****** //
OBJECTID     : 1
ID           : 010010201001
ACSTOTPOP    : 692
ACSIPOVBAS   : 692
ACSEDUCBAS   : 441
ACSTOTHH     : 300
ACSTOTHU     : 300
MINORPOP     : 58
MINORPCT     : 0.0838150289017
...
AREALAND     : 4249517.0
AREAWATER    : 28435.0
NPL_CNT      : 0
TSDF_CNT     : 0
Shape_Length : 13435.9755601
Shape_Area   : 6026827.88668
```

The fields are described in the EJScreen_Index_DescriptionsV4_Pub.csv file.
For instance, you can look up the value of "T_PTSDF_D2" like so:

```bash
$ grep T_PTSDF_D2 EJScreen_Index_DescriptionsV4_Pub.csv
T_PTSDF_D2	Descriptive Text for TSDF Proximity--Primary EJ Index based on Primary 2-factor Demographics
```

This same data exists as "variables.csv" for the purposes of loading the data.

The "ID" field notes the census block group.
It is constructed by combining: 

* State FIPS code
* County FIPS code
* Tract ID
* block group ID

An ID of "0400194442012" would translate to "Block Group 2, Census Tract 9442.01, Apache County, Arizona.":

```
04    001    9444201  2
^^    ^^^    ^^^^^^^  ^
state county tract    block group
```

* The first 2-digits is the State FIPS code. Arizona is “04”. 
* The following 3-digits arg the county FIPS, e.g., Apache county is “001”. 
* The census Tract ID is “944201," and the block group 2 is the last digit.

Note: I had to change "Ñ" to spaces in variables.csv to parse.

## Digest

Use the "to_scrutinizer.py" program to create a file suitable for loading into the "scrutinizer" database.
Run the `make scrutinizer` target for an example.

```bash
$ ./to_scrutinizer.py -h
usage: to_scrutinizer.py [-h] -H FILE -c str [-m str] [-o FILE]
                         FILE [FILE ...]

Convert EJSCREEN data to Scrutinizer format

positional arguments:
  FILE                  Input file(s)

optional arguments:
  -h, --help            show this help message and exit
  -H FILE, --headers FILE
                        Headers file (default: None)
  -c str, --collected_on str
                        Date for "collected_on" field (default: None)
  -m str, --medium str  Dummy value for "medium" (default: Population)
  -o FILE, --outfile FILE
                        Output filename (default: scrutinizer.csv)
```

This program is hard-coded to take only data for state code "04" (Arizona" and the counties "001" (Apache), "003" (Cochise), "011" (Greenlee), and "025" (Yavapai).
The resulting file should contain 39,898 rows and will have a format like:

```bash
$ csvchk scrutinizer.csv
// ****** Record 1 ****** //
location_name : 040019426001
location_type : census_block
variable_name : ACSTOTPOP
variable_desc : Total Population
collected_on  : 2019-01-01
medium        : Population
value         : 781.0
```
