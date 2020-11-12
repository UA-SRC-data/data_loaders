# Dump "variable" table to tab-delimited
mysql -B scrutinizer < ../sql/variables.sql > variables.tab

# Convert tab to JSON
# cf https://github.com/kyclark/bioinformatics_primer/tree/master/tab2json
tab2json.py variables.tab

# Import JSON file, maybe db.variables.drop() firest?
mongoimport -d uasrc -c variables --jsonArray variables.json
