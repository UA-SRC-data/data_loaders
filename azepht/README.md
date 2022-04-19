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

*Not in scrutinizer. The to_scrutinizer file was not finished.*



### Create mapping file

azepht_traits.csv was created manually.

