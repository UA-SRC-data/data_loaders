# Loader for Colorado School of Mines data

Loads data into Mongo as records like:

```
> db.csm.findOne()
{
	"_id" : ObjectId("5e2b642b2d37f0b1d9b6f761"),
	"station" : "UPPER REFERENCE",
	"collection_date" : ISODate("2011-11-15T07:00:00Z"),
	"measurement" : "acentr",
	"value" : 0
}
```

To run, see Makefile.

# Author

Ken Youens-Clark <kyclark@email.arizona.edu>
