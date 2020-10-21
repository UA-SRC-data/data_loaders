# US Census America Community Survey (ACS5)

## Using the US Census API

Wherein we learn to query for the variables.

### Background

* The Decennial census data summary data: https://www.census.gov/data/developers/data-sets/decennial-census.html
* Variables for querying: https://api.census.gov/data/2018/acs/acs5/variables.html
* Gitter/Help: https://gitter.im/uscensusbureau/general?source=orgpage#

### Data

Arizona is state "04" in the census API.
We can only get data by census block/group for a county for which we need the county numbers available here

https://api.census.gov/data/2017/acs/acs5?get=NAME&for=county:*&in=state:04

| County     | Number |
| ---------- | ------ |
| Apache     | 001    |
| Cochise    | 003    |
| Coconino   | 005    |
| Gila       | 007    |
| Graham     | 009    |
| Greenlee   | 011    |
| La Paz     | 012    |
| Maricopa   | 013    |
| Mohave     | 015    |
| Navajo     | 017    |
| Pima       | 019    |
| Pinal      | 021    |
| Santa Cruz | 023    |
| Yavapai    | 025    |
| Yuma       | 027    |

Example query for females under 5 in Yavapai:

https://api.census.gov/data/2017/acs/acs5?get=NAME,B01001_027E&for=block%20group:*&in=state:04&in=county:025&in=tract:*

## Preprocess data

```bash
$ ./to_scrutinizer.py -h
usage: to_scrutinizer.py [-h] [-f FILE [FILE ...]] [-v FILE] [-o FILE]
                         [-s source]

Create Scrutinizer format

optional arguments:
  -h, --help            show this help message and exit
  -f FILE [FILE ...], --file FILE [FILE ...]
                        A readable file (default: None)
  -v FILE, --variables FILE
                        Variable description file (default:
                        acs_variables_to_download.csv)
  -o FILE, --outfile FILE
                        Output file (default: scrutinizer.csv)
  -s source, --source source
                        Data source (default: ACS5)
```
