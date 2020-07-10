#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Purpose: Load CSM scrutinizer data directory into Mongo (no MySQL)
"""

import argparse
import csv
import os
import dateparser
import datetime
import re
import pymongo
from pprint import pprint
from typing import Dict, List, Tuple, NamedTuple, Optional, TextIO

STATION_LOCATION = {
    'ABOVE_RUSSEL': (39.764606, -105.446683),
    'CC_MAIN_ABOVE_NFCC': (39.740397, -105.411517),
    'CONFLUENCE': (39.742069, -105.390567),
    'PUMPHOUSE': (39.812636, -105.498117),
    'RAIL_LESS': (39.792289, -105.472406),
    'RIVIERA': (39.798722, -105.483097),
    'UPPER_REFERENCE': (39.815519, -105.500403),
    'USGS_GAUGE_STATION': (39.749308, -105.399631),
}

STAITION_ALIAS = {
    'RIVIERA': ['RIVERA'],
    'USGS_GAUGE_STATION': ['GUAGE'],
}


class Args(NamedTuple):
    file: List[TextIO]
    mongo_uri: str
    mongo_db: str
    mongo_collection: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Load CSM data into Mongo',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Input file')

    parser.add_argument('-m',
                        '--mongo_uri',
                        help='Mongo URI',
                        metavar='str',
                        type=str,
                        default='mongodb://localhost:27017/')

    parser.add_argument('-d',
                        '--db',
                        help='Mongo DB name',
                        metavar='str',
                        type=str,
                        default='uasrc')

    parser.add_argument('-c',
                        '--collection',
                        metavar='str',
                        type=str,
                        default='csm',
                        help='Mongo collection name')

    args = parser.parse_args()

    return Args(args.file, args.mongo_uri, args.db, args.collection)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    client = pymongo.MongoClient(args.mongo_uri)
    db = client[args.mongo_db]

    print(f'Importing {os.path.basename(args.file.name)}')
    num_inserted = process(args.file, db, args.mongo_collection)
    print(f'Done, inserted {num_inserted}.')


# --------------------------------------------------
def process(fh: TextIO, db: pymongo.database.Database, collection_name: str) -> int:
    """Process the file into Mongo (client)"""

    _, ext = os.path.splitext(os.path.basename(fh.name))
    delimiter = ',' if ext == '.csv' else '\t'
    reader = csv.DictReader(fh, delimiter=delimiter)
    flds = reader.fieldnames
    num_inserted = 0

    collection = db[collection_name]
    collection.create_index([("location", pymongo.GEO2D)])

    variables = set()

    for i, row in enumerate(reader, start=1):
        val = None

        # Try to convert value to float
        try:
            val = float(row.get('value'))
        except Exception:
            continue

        # Base record has station/date
        date = dateparser.parse(row.get('collected_on'))
        if not date:
            continue

        date = datetime.datetime.utcfromtimestamp(date.timestamp())

        rec = {
            'location_name': row.get('location_name'),
            'variable_name': row.get('variable_name'),
            'collection_date': date,
        }

        print(f"{i:4}: {rec['variable_name']} => {val}")

        # Look for the base record w/o the value
        exists = collection.find_one(rec)

        # If we need to insert, add the value, maybe float or str
        if exists:
            collection.update_one(
                rec, {
                    "$set": {
                        'val': val,
                        'medium': row.get('medium'),
                        'variable_desc': row.get('variable_desc'),
                        'location_type': row.get('location_type'),
                    }
                })
        else:
            rec['val'] = val
            rec['medium'] = row.get('medium')
            rec['variable_desc'] = row.get('variable_desc')
            rec['location_type'] = row.get('location_type')
            collection.insert_one(rec)

        num_inserted += 1
        variables.add((row.get('variable_name'), row.get('variable_desc')))

    var_collection = db['csm_variables']
    for name, desc in variables:
        var = {'name': name, 'desc': desc}
        exists = var_collection.find_one(var)
        if not exists:
            var_collection.insert_one(var)

    return num_inserted


# --------------------------------------------------
if __name__ == '__main__':
    main()
