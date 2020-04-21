DB = scrutinizer.db

load:
	./scripts/loader.py ../ejscreen/scrutinizer.csv ../usgs/scrutinizer.csv

pwiz:
	pwiz.py -e sqlite $(DB) > scripts/scrutinizer.py

sqlitedb:
	sqlite3 $(DB) < sql/sqlite.schema

mysqldb:
	mysql scrutinizer < sql/mysql.schema
