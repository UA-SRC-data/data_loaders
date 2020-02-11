CENSUS = "../../../data/us-census/"
DB = "uasrc"

load:
	find $(CENSUS) -name \*overlay\* | xargs ./db_loader.py

db:
	mysql $(DB) < create.sql
