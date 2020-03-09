INPUT = ../../data/ejscreen/EJSCREEN_2019_USPR.csv

scrutinizer:
	./to_scrutinizer.py --headers variables.csv $(INPUT)

mongo:
	./load_mongo.py --headers variables.csv $(INPUT)
