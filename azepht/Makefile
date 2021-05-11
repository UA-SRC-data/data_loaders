PRG = ./to_scrutinizer.py
DATA = ./raw_data
VARS = $(DATA)/ArizonaEPHT_Variables.csv 

all: clean counties towns

clean:
	rm -f err

counties:
	$(PRG) -v $(VARS) -l county -f \
		$(DATA)/EPHTdata_aemageadj.csv \
		$(DATA)/EPHTdata_aemcrude.csv \
		$(DATA)/EPHTdata_aemvisit.csv \
		$(DATA)/EPHTdata_ahosp.csv \
		$(DATA)/EPHTdata_ahospageadj.csv \
		$(DATA)/EPHTdata_ahospcrude.csv \
		$(DATA)/EPHTdata_cbladder.csv \
		$(DATA)/EPHTdata_cbrainnerv.csv \
		$(DATA)/EPHTdata_cbreast.csv \
		$(DATA)/EPHTdata_cdag.csv \
		$(DATA)/EPHTdata_cddev.csv \
		$(DATA)/EPHTdata_cesoph.csv \
		$(DATA)/EPHTdata_ckidney.csv \
		$(DATA)/EPHTdata_clarynx.csv \
		$(DATA)/EPHTdata_cleuk.csv \
		$(DATA)/EPHTdata_cliver.csv \
		$(DATA)/EPHTdata_clung.csv \
		$(DATA)/EPHTdata_clymph.csv \
		$(DATA)/EPHTdata_coral.csv \
		$(DATA)/EPHTdata_cpanc.csv \
		$(DATA)/EPHTdata_ctest.csv \
		$(DATA)/EPHTdata_cthyroid.csv \
		$(DATA)/EPHTdata_dwarcws.csv \
		$(DATA)/EPHTdata_dwcws.csv 2>err

towns:
	$(PRG) -v $(VARS) -l municipality -f \
		$(DATA)/EPHTdata_cdhighway.csv \
		$(DATA)/EPHTdata_cdpark.csv 2>>err
