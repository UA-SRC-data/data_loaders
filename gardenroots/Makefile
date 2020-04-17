MK_PKG = ../datapackage/mk_pkg.py
P2S = ../point2shape/point2shape.py
BG_SHAPE = ../point2shape/shapefiles/block_group/tl_2017_04_bg

ll:
	./scripts/clean_latlon.py ~/Desktop/v2-Groots\ LatLong.csv -o gardenroot_latlon.csv

pkg:
	$(MK_PKG) data/*.csv -o datapackage.json -f -m 'no standard given'

bg:
	$(P2S) -s $(BG_SHAPE) -f gardenroot_latlon.csv -o data/gardenroot_bg.csv -r -t block_group --bom

merge:
	./scripts/merge_geoid.py -g data/gardenroot_bg.csv -f data/plants.csv data/soil.csv data/water.csv
