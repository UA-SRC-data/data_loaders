DB = "acs5.db"

# Use the variables from Dorsey/Monica to fetch the data
download:
	./fetch_from_acs.py -f dorsey_variables.txt -V

# Convert the downloaded data to Scrutinizer format
scrutinizer:
	./to_scrutinizer.py -v acs_variables_to_download.csv -f data/* 2>err

acs5_vars:
	wget -O acs5_vars.json https://api.census.gov/data/2018/acs/acs5/variables

db:
	sqlite3 $(DB) < schema.sql
