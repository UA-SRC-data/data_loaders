#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-24
Purpose: Load CSM data into Mongo
"""

import argparse
import csv
import os
import sys
import dateparser
import datetime
from pprint import pprint as pp
from pymongo import MongoClient
from typing import List, NamedTuple, Optional, TextIO


class Args(NamedTuple):
    file: List[TextIO]
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
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help='Input file(s)')

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

    return Args(args.file, args.mongo_uri, args.db, args.delimiter)


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

    print(f'Done, inserted {num_inserted}.')


# --------------------------------------------------
def process(fh: TextIO, db: str, args: Args) -> int:
    """Process the file into Mongo (client)"""

    reader = csv.DictReader(fh, delimiter=args.delimiter)
    flds = reader.fieldnames
    coll = db['csm']
    num_inserted = 0

    for i, row in enumerate(reader):
        print(i)
        for fld in flds[5:-8]:
            date = dateparser.parse(row['date'])
            if not date:
                continue

            # Base record has station/date
            date = datetime.datetime.utcfromtimestamp(date.timestamp())
            rec = {
                'station': row['station'],
                'collection_date': date,
                'measurement': fld,
            }

            # Look for the base record w/o the value
            exists = coll.find_one(rec)

            # If we need to insert, add the value, maybe float or str
            if not exists:
                # Try to convert value to float
                val = row[fld]

                # Remove leading "="?
                if val.startswith('='):
                    val = val[1:]

                try:
                    val = float(val)
                except:
                    pass

                rec['val'] = val
                coll.insert_one(rec)
                num_inserted += 1

    return num_inserted


# --------------------------------------------------
if __name__ == '__main__':
    main()
