#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-24
Purpose: Load CSM Scrutinizer-formatted data into Mongo
"""

import argparse
import csv
import os
import dateparser
import datetime
import re
from pymongo import MongoClient, GEO2D
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
    'GAUGE': (39.749308, -105.399631),
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
                        nargs='+',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Input file(s)')

    parser.add_argument('-m',
                        '--mongo_uri',
                        help='Mongo URI',
                        metavar='uri',
                        type=str,
                        default='mongodb://localhost:27017/')

    parser.add_argument('-d',
                        '--db',
                        help='Mongo DB name',
                        metavar='db',
                        type=str,
                        default='uasrc')

    parser.add_argument('-c',
                        '--collection',
                        help='Mongo collection name',
                        metavar='coll',
                        type=str,
                        default='csm')

    args = parser.parse_args()

    return Args(args.file, args.mongo_uri, args.db, args.collection)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    client = MongoClient(args.mongo_uri)
    db = client[args.mongo_db]
    num_inserted = 0

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        num_inserted += process(fh, db, args)

    print(f'Done, inserted {num_inserted:,}.')


# --------------------------------------------------
def process(fh: TextIO, db: str, args: Args) -> int:
    """Process the file into Mongo (client)"""

    _, ext = os.path.splitext(os.path.basename(fh.name))
    delimiter = ',' if ext == '.csv' else args.delimiter
    reader = csv.DictReader(fh, delimiter=delimiter)
    flds = reader.fieldnames
    coll = db[args.mongo_collection]
    num_inserted = 0

    coll.create_index([("location", GEO2D)])

    for i, rec in enumerate(reader, start=1):
        # pprint(rec)
        value = float(rec.get('value'))
        dp = dateparser.parse(rec.get('collected_on'))
        date = str(datetime.datetime.utcfromtimestamp(dp.timestamp()))
        station = rec.get('location_name')
        lat_lon = STATION_LOCATION.get(station)

        if not lat_lon:
            print(f'Skipping station "{station}"')
            pprint(rec)
            continue

        # Look for the base record w/o the value
        exists = coll.find_one({
            'collected_on': date,
            'location_name': rec.get('location_name'),
            'variable_name': rec.get('variable_name')
        })

        # If we need to insert, add the value, maybe float or str
        if exists:
            coll.update_one(rec,
                            {"$set": {
                                'value': value,
                                'location': lat_lon,
                            }})
        else:
            rec['value'] = value
            rec['location'] = lat_lon
            rec['collected_on'] = date
            coll.insert_one(rec)

        num_inserted += 1

    return num_inserted


# --------------------------------------------------
if __name__ == '__main__':
    main()
