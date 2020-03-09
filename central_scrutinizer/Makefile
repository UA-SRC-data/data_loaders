DB = scrutinizer.db

load:
	./loader.py ../ejscreen/scrutinizer.csv ../csm/sqlite/scrutinizer.csv

pwiz:
	pwiz.py -e sqlite $(DB) > scrutinizer.py

db:
	sqlite3 $(DB) < schema.sql
