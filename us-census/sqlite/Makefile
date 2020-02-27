BLOCK_DIR = "$(HOME)/work/uasrc/data/census-blocks/"

blocks:
	find $(BLOCK_DIR) -name \*overlay\* | xargs ./db_loader.py -d blocks.db

towns:
	find ../ -name \*overlay\* | xargs ./db_loader.py -d towns.db
