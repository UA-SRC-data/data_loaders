csm:
	./load_csm_mongo.py ../../../data/csm/NFCC_Benthic_Biomonitoring_2011-2018_MASTER.csv -H ../../../data/csm/NFCC_TaxaList_02112020.csv

install:
	python3 -m pip install -r requirements.txt

start:
	brew services start mongodb-community@4.2

stop:
	brew services stop mongodb-community@4.2
