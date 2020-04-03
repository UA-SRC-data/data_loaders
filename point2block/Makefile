.PHONY = sample bom lat lon both clean
PRG = ./p2b.py
SHAPEFILE = shape/tl_2017_04_bg.dbf

sample:
	$(PRG) -s $(SHAPEFILE) inputs/sample.csv -o out-sample.csv

bom:
	$(PRG) -s $(SHAPEFILE) inputs/bom.csv -o out-bom.csv

lat:
	$(PRG) -s $(SHAPEFILE) inputs/missing-lat.csv

lon:
	$(PRG) -s $(SHAPEFILE) inputs/missing-lon.csv

both:
	$(PRG) -s $(SHAPEFILE) inputs/missing-both.csv

clean:
	rm -rf out*.csv
