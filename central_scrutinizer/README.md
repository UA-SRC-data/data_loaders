# Central Scrutinizer

Code for loading preprocessed data into an internal database for validation and initial visualization.

A MySQL database (sql/mysql.schema) is used to aggregate the datasets.
To initialize the db, run:

```
$ make mysqldb
```

To build the database, first you must create all the individual "scrunitizer.csv" files for the various projects.
Then you can run the "mysql_loader.py" to put these into the MySQL db.
See the Makefile for targets like "gardenroots," etc.
The "mysqlload" target will load all these:

```
$ make mysqlload
```

Once all the data is in MySQL, you should run the "scrutinizer2json.py" to dump the measurements and variables to JSON that can be loaded into MongoDB:

```
$ make json
```

That will create a "scrutinizer" directory containing JSON files to import:

```
$ make mongo
```

## Author

Ken Youens-Clark <kycalrk@arizona.edu>
