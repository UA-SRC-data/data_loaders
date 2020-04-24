RAWFILE = data.csv
OUTFILE = az_data.csv

scrutinizer.csv: az_data_bg.csv
	./to_scrutinizer.py -f az_data_bg.csv -o scrutinizer.csv

az_data.csv:
	head -1 $(RAWFILE) > $(OUTFILE)
	awk -F',' '$$3 == "AZ"' $(RAWFILE) >> $(OUTFILE)

az_data_bg.csv: az_data.csv 
	../point2shape/point2shape.py -t block_group -s ../point2shape/shapefiles/block_group/tl_2017_04_bg -f az_data.csv  -o az_data_bg.csv

