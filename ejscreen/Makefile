INPUT = ../../data/ejscreen/EJSCREEN_2019_USPR.csv
COLLECTED_ON = "2019-01-01"

scrutinizer:
	./to_scrutinizer.py --headers variables.csv -c $(COLLECTED_ON) $(INPUT)

mongo:
	./load_mongo.py --headers variables.csv $(INPUT)
