INPUT = ../../data/ejscreen/EJSCREEN_2019_USPR.csv
COLLECTED_ON = "2019-01-01"
MEDIUM = "Population"

scrutinizer:
	./to_scrutinizer.py --headers variables.csv \
		-c $(COLLECTED_ON) -m $(MEDIUM) $(INPUT)

mongo:
	./load_mongo.py --headers variables.csv $(INPUT)

data:
	wget ftp://newftp.epa.gov/EJSCREEN/2019/EJSCREEN_2019_USPR.csv.zip
