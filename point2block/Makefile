.PHONY = sample bom
PRG = ./p2b.py
SHAPEFILE = shape/tl_2017_04_bg.dbf

sample:
	$(PRG) -s $(SHAPEFILE) sample.csv -o out-sample.csv

bom:
	$(PRG) -s $(SHAPEFILE) bom.csv -o out-bom.csv
