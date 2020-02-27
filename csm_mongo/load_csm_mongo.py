#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-24
Purpose: Load CSM data into Mongo
"""

import argparse
import csv
import os
import dateparser
import datetime
from pymongo import MongoClient, GEO2D
from pprint import pprint
from typing import Dict, List, Tuple, NamedTuple, Optional, TextIO

LOCATIONS = {
    'ABOVE RUSSEL': (39.764606, -105.446683),
    'CC MAIN ABOVE NFCC': (39.740397, -105.411517),
    'CONFLUENCE': (39.742069, -105.390567),
    'PUMPHOUSE': (39.812636, -105.498117),
    'RAIL-LESS': (39.792289, -105.472406),
    'RIVIERA': (39.798722, -105.483097),
    'UPPER REFERENCE': (39.815519, -105.500403),
    'USGS GAUGE STATION': (39.749308, -105.399631),
}


class Args(NamedTuple):
    file: List[TextIO]
    headers: Optional[TextIO]
    mongo_uri: str
    mongo_db: str
    delimiter: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Load CSM data into Mongo',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        nargs='+',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        help='Input file(s)')

    parser.add_argument('-H',
                        '--headers',
                        help='Headers file',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        default=None)

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

    parser.add_argument('-D',
                        '--delimiter',
                        metavar='str',
                        type=str,
                        default='\t',
                        help='Field delimiter')

    args = parser.parse_args()

    return Args(args.file, args.headers, args.mongo_uri, args.db,
                args.delimiter)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    client = MongoClient(args.mongo_uri)
    db = client[args.mongo_db]
    num_inserted = 0
    headers = get_headers(args.headers)

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        num_inserted += process(fh, headers, db, args)

    print(f'Done, inserted {num_inserted}.')


# --------------------------------------------------
def get_headers(fh: Optional[TextIO]) -> Dict[str, str]:
    """Reader headers (optional)"""

    headers = {}

    if fh:
        reader = csv.DictReader(fh, delimiter='\t')
        flds = reader.fieldnames
        print(f'>>>{flds}')

        expected = 'header order family genus'.split()
        missing = list(filter(lambda f: f not in flds, expected))

        if missing:
            msg = f'"{fh.name}" missing fields: {", ".join(missing)}'
            raise Exception(msg)

        for rec in reader:
            hdr = rec['header']
            if hdr:
                order, family, genus = map(lambda h: rec[h].strip(),
                                           'order family genus'.split())
                if all([order, family, genus]):
                    headers[hdr.lower()] = ' '.join([order, family, genus])
                elif order:
                    headers[hdr.lower()] = order
                else:
                    headers[hdr.lower()] = hdr

    return headers


# --------------------------------------------------
def process(fh: TextIO, headers: Optional[Dict[str, str]], db: str, args: Args) -> int:
    """Process the file into Mongo (client)"""

    reader = csv.DictReader(fh, delimiter=args.delimiter)
    flds = reader.fieldnames
    coll = db['csm']
    num_inserted = 0

    coll.create_index([("location", GEO2D)])

    for i, row in enumerate(reader, start=1):
        if not row.get('stream'):
            continue

        for fld in flds[5:-8]:
            date = dateparser.parse(row['date'])
            if not date:
                continue

            measurement = headers.get(fld.lower(), fld) if headers else fld

            # Base record has station/date
            date = datetime.datetime.utcfromtimestamp(date.timestamp())
            rec = {
                'station': row['station'],
                'collection_date': date,
                'measurement': measurement,
            }

            if row['station'] in LOCATIONS:
                rec['location'] = LOCATIONS.get(row['station'])

            # Remove leading "="?
            val = row[fld]
            if val.startswith('='):
                val = val[1:]

            # Try to convert value to float
            try:
                val = float(val)
            except Exception:
                pass

            print(f'{i:4}: {fld} => {val}')

            # Look for the base record w/o the value
            exists = coll.find_one(rec)

            # If we need to insert, add the value, maybe float or str
            if exists:
                coll.update_one(rec, {"$set": {'val': val}})
            else:
                rec['val'] = val
                coll.insert_one(rec)

            num_inserted += 1

    return num_inserted


# --------------------------------------------------
if __name__ == '__main__':
    main()
