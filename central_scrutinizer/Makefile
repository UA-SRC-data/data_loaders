MYSQL_LOADER = "./scripts/mysql_loader.py"
MONGO_LOADER = "./scripts/mongo_loader.py"

# Initialize the MySQL db with the table defs
mysqldb:
	mysql scrutinizer < sql/mysql.schema

# Generate a PeeWee ORM
pwiz:
	pwiz.py -e mysql -u kyclark -P scrutinizer > scripts/scrutinizer.py

# Export the MySQL db to JSON for MongoDB
json:
	./scripts/scrutinizer2json.py

# Import the JSON files into MongoDB
mongo:
	./scripts/mongoimport.sh scrutinizer

# Load the various datasets into MySQL
mysqlload: gardenroots ejscreen usgs csm acs

gardenroots:
	$(MYSQL_LOADER) ../gardenroots/scrutinizer/[psw]*.csv

ejscreen:
	$(MYSQL_LOADER) ../ejscreen/scrutinizer.csv

usgs:
	$(MYSQL_LOADER) ../usgs/scrutinizer.csv

acs:
	$(MYSQL_LOADER) ../acs5/scrutinizer.csv

csm:
	$(MYSQL_LOADER) ../csm/benthic/scrutinizer.csv

# Python module prereqs
install:
	python3 -m pip install -r requirements.txt
