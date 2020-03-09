#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-24
Purpose: Load EJSCREEN data into Mongo
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


class Args(NamedTuple):
    file: List[TextIO]
    headers: Optional[TextIO]
    mongo_uri: str
    mongo_db: str
    collection: str
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

    parser.add_argument('-c',
                        '--collection',
                        help='Mongo collection name',
                        metavar='str',
                        type=str,
                        default='ejscreen')

    parser.add_argument('-D',
                        '--delimiter',
                        metavar='str',
                        type=str,
                        default='\t',
                        help='Field delimiter')

    args = parser.parse_args()

    return Args(args.file, args.headers, args.mongo_uri, args.db,
                args.collection, args.delimiter)


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
        reader = csv.DictReader(fh, delimiter=',')
        flds = reader.fieldnames
        expected = 'FIELD_NAME,DESCRIPTION,CATEGORY'.split(',')
        missing = list(filter(lambda f: f not in flds, expected))

        if missing:
            msg = f'"{fh.name}" missing fields: {", ".join(missing)}'
            raise Exception(msg)

        for rec in reader:
            headers[rec['FIELD_NAME']] = rec['DESCRIPTION']

    return headers


# --------------------------------------------------
def process(fh: TextIO, headers: Optional[Dict[str, str]], db: str,
            args: Args) -> int:
    """Process the file into Mongo (client)"""

    _, ext = os.path.splitext(os.path.basename(fh.name))
    delimiter = ',' if ext == '.csv' else args.delimiter
    reader = csv.DictReader(fh, delimiter=delimiter)
    flds = reader.fieldnames
    coll = db[args.collection]
    num_inserted = 0

    for i, row in enumerate(reader, start=1):
        block_id = row['ID']
        if not block_id:
            continue

        if not block_id.startswith('04'):
            continue

        for fld in filter(lambda f: f != 'ID', flds):
            val = row.get(fld)
            if val == "":
                continue

            desc = headers.get(fld)
            if not desc:
                continue

            # Try to convert value to float
            try:
                val = float(val)
            except Exception:
                pass

            print(f'{i:4}: {block_id} {fld} => {val}')
            rec = {
                'block_id': block_id,
                'variable': fld,
            }

            # Look for the base record w/o the value
            exists = coll.find_one(rec)

            # If we need to insert, add the value, maybe float or str
            if exists:
                coll.update_one(rec, {"$set": {
                    'val': val,
                    'desc': desc,
                }})
            else:
                rec['val'] = val
                rec['desc'] = desc
                coll.insert_one(rec)

            num_inserted += 1

    return num_inserted


# --------------------------------------------------
if __name__ == '__main__':
    main()
