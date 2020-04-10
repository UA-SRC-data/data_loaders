.PHONY = sample bom lat lon both clean
PRG = ./point2shape.py
BLOCK_GROUP = shapefiles/block_group/tl_2017_04_bg
BLOCK = shapefiles/block/tl_2017_04_tabblock10
TRACT = shapefiles/tract/tl_2016_04_tract

sample:
	$(PRG) -s $(TRACT) -f inputs/sample.csv -t tract -o out-sample.csv

bom:
	$(PRG) -s $(BLOCK_GROUP) -f inputs/bom.csv -t block_group -o out-bom.csv

lat:
	$(PRG) -s $(TRACT) -f inputs/missing-lat.csv -t tract

lon:
	$(PRG) -s $(TRACT) -f inputs/missing-lon.csv -t tract

both:
	$(PRG) -s $(TRACT) -f inputs/missing-both.csv -t tract

clean:
	rm -rf out*.csv
