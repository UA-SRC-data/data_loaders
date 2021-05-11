DATA = raw_data

run:
	find $(DATA) -type f -name \*.csv | grep -v Variables | \
		xargs ./to_scrutinizer.py -v $(DATA)/ArizonaEPHT_Variables.csv -f 
