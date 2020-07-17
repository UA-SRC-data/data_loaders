MYSQL_LOADER = "./scripts/mysql_loader.py"
MONGO_LOADER = "./scripts/mongo_loader.py"

load:
	$(MYSQL_LOADER) ../ejscreen/scrutinizer.csv ../usgs/scrutinizer.csv

json:
	./scripts/scrutinizer2json.py

mongo:
	./scripts/mongoimport.sh scrutinizer

pwiz:
	pwiz.py -e mysql -u kyclark -P scrutinizer > scripts/scrutinizer.py

mysqldb:
	mysql scrutinizer < sql/mysql.schema

gardenroots:
	$(MYSQL_LOADER) ../gardenroots/scrutinizer/*.csv

ejscreen:
	$(MYSQL_LOADER) ../ejscreen/scrutinizer.csv

usgs:
	$(MYSQL_LOADER) ../usgs/scrutinizer.csv

acs:
	$(MYSQL_LOADER) ../acs5/scrutinizer.csv

csm:
	$(MYSQL_LOADER) ../csm/sqlite/scrutinizer.csv

mongodump:
	zip -r uasrc_mongo.zip scrutinizer 

mysqldump:
	mysqldump scrutinizer > scrutinizer.sql

install:
	python3 -m pip install -r requirements.txt
