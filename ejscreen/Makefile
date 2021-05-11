INPUT = ../../data/ejscreen/EJSCREEN_2019_USPR.csv
COLLECTED_ON = "2019-01-01"
MEDIUM = "Population"
SOURCE = "EJSCREEN"

scrutinizer:
	./to_scrutinizer.py --headers variables.csv --quiet \
		-c $(COLLECTED_ON) -m $(MEDIUM) -s $(SOURCE) $(INPUT)

mongo:
	./load_mongo.py --headers variables.csv $(INPUT)

data:
	# wget ftp://newftp.epa.gov/EJSCREEN/2019/EJSCREEN_2019_USPR.csv.zip
	wget ftp://newftp.epa.gov/EJSCREEN/2020/EJSCREEN_2020ZZ_USPR.csv.zip
