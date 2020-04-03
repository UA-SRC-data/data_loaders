DB = scrutinizer.db

load:
	./loader.py ../ejscreen/scrutinizer.csv ../usgs/scrutinizer.csv

pwiz:
	pwiz.py -e sqlite $(DB) > scrutinizer.py

sqlitedb:
	sqlite3 $(DB) < sqlite.schema

mysqldb:
	mysql scrutinizer < mysql.schema
