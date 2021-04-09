# Arizona Public Health Tracking Network (AZEPHT)

## Download data

AData source: https://gis.azdhs.gov/ephtexplorer/
Download date: April 4, 2021

Each variable was downloaded separately after selecting the categories described in ArizonaEPHT_Variables.csv. 
For all variables, "All Months", "All Ages", and "Any Gender" were selected.
After download, the zip archive as unzipped, renamed to reflect the variables, and the files within each folder were renamed with the suffix in ArizonaEPHT_Variables.csv. 
The data file was opend in Excel and saved as a CSV with the same name (e.g., EPHTdata_dwartest.csv).


## Preprocess data

Use the "to_scrutinizer.py" program to create a file suitable for loading into the "scrutinizer" database.
Run the `make scrutinizer` target for an example.

*The example below is from an old readme file. Will need to update.*


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


The resulting file should contain xxxx rows and will have a format like:

*The example below is from an old readme file. Will need to update.*

```bash
$ csvchk scrutinizer.csv
// ****** Record 1 ****** //
location_name : xxx
location_type : xxx
variable_name : xxx
variable_desc : xxx
collected_on  : xxx
medium        : xxx
value         : xxx
```
### Create mapping file

Create a list of unique variables using `cut -d',' -f5,6 scrutinizer.csv | tail +2 | sort | uniq > ejs_traits.csv`. Note that this is shifted by 1 column to allow for the comma in the location column (seperating lat and long). The header row therefore needs to be corrected manually.

Manually edit `ejs_traits.csv` to fix header row and to add mappings to SRPDIO. Save as `ejs-srpdio-mapping.csv`.

