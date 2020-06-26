DB = scrutinizer.db

load:
	./scripts/loader.py ../ejscreen/scrutinizer.csv ../usgs/scrutinizer.csv

mongo:
	./scripts/load_mongo.py

pwiz:
	pwiz.py -e sqlite $(DB) > scripts/scrutinizer.py

sqlitedb:
	sqlite3 $(DB) < sql/sqlite.schema

mysqldb:
	mysql scrutinizer < sql/mysql.schema

gardenroots:
	./scripts/gardenroots.py -f ../gardenroots/datapackage.json -o data/gardenroots # --verbose
	./scripts/loader.py data/gardenroots/*.csv

ejscreen:
	./scripts/loader.py ../ejscreen/scrutinizer.csv

usgs:
	./scripts/loader.py ../usgs/scrutinizer.csv

mongodump:
	mongoexport -d uasrc -c scrutinizer -o scrutinizer.json

mysqldump:
	mysqldump scrutinizer > scrutinizer.sql
