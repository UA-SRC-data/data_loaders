# Colorado School of Mines data

This directory contains data from the Colorado school of Mines (CSM) on water chemistry and benthic invertebrate diversity.

These data are **not** being integrated with Gardenroots data and are used for a separate project.

## Data
Preprocessed data are available to team members at 

Publications:

## Prepprocessing
There are two datasets from CSM. Preprocessing scripts are stored in the corresponding folders (`benthic` and `chemistry`).

Scripts still need some work:

```bash
$ ./to_scrutinizer.py -h
Traceback (most recent call last):
  File "to_scrutinizer.py", line 11, in <module>
    import dateparser
ModuleNotFoundError: No module named 'dateparser'
 ```
### Create mapping file

**Benthic:** Create a list of unique variables using `cut -d',' -f5,6 scrutinizer.csv | tail +2 | sort | uniq > benthic_traits.csv`. 

Manually edit `benthic_traits.csv` to add header row and to add mappings to SRPDIO. Save as `benthic-srpdio-mapping.csv`.

**Chemistry:** 
