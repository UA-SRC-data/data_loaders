MK_PKG = ../datapackage/mk_pkg.py
P2S = ../point2shape/point2shape.py
BG_SHAPE = ../point2shape/shapefiles/block_group/tl_2017_04_bg

scrutinizer:
	./scripts/to_scrutinizer.py -f ./datapackage.json

ll:
	./scripts/clean_latlon.py v3groots_lat_lon.csv -o gardenroot_latlon.csv

bg:
	$(P2S) -s $(BG_SHAPE) -f gardenroot_latlon.csv -o data/gardenroot_bg.csv -r -t block_group --bom --skipna

merge_bg:
	./scripts/merge_geoid.py -g data/gardenroot_bg.csv -f data/plants.csv data/soil.csv data/water.csv

centroid:
	$(P2S) -s $(BG_SHAPE) -f gardenroot_latlon.csv -o data/gardenroot_centroid.csv -r -t centroid --bom --skipna

merge_centroid:
	./scripts/merge_geoid.py -g data/gardenroot_centroid.csv -f data/plants.csv data/soil.csv data/water.csv

pkg:
	$(MK_PKG) data/plants_*.csv data/water_*.csv data/soil_*.csv \
		-o datapackage.json -f -m '#VALUE!' '≤LOD' '<LOD'

install:
	python3 -m pip install -r requirements.txt
