#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-02-07
Purpose: Load "data_with_overlays" into SQLite
"""

import argparse
import csv
import os
import re
import sqlite3
import sys
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Load "data_with_overlays" into SQLite',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help='Input file(s)')

    parser.add_argument('-d',
                        '--db',
                        metavar='DB',
                        default=os.path.join(os.getcwd(), 'census.db'),
                        help='SQLite db')

    parser.add_argument('-s',
                        '--sep',
                        metavar='SEP',
                        default=',',
                        help='Field separator')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    db = sqlite3.connect(args.db)
    num_imported = 0

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        num_imported += process(fh, db, args)

    print(f'Done, imported {num_imported}')


# --------------------------------------------------
def process(fh, db, args):
    """Import file into db"""

    # The "real" headers are in the 2nd row
    _ = fh.readline()

    location_header = 'Geographic Area Name'
    reader = csv.DictReader(fh, delimiter=args.sep)
    headers = reader.fieldnames

    if location_header not in headers:
        print(f'Missing "{location_header}" column!')
        return 0

    i = 0
    for rec in reader:
        #rec = dict(zip(headers, map(dequote, row.rstrip().split(args.sep))))

        location = rec.get(location_header)
        if not location:
            print(f'Missing "{location_header}" value!')
            continue

        location_id = find_or_create_location(location, db)

        for attr_type in filter(lambda col: col != 'id', headers):
            value = rec[attr_type]
            if value == '':
                continue

            attr_type_id = find_or_create_attr_type(attr_type, db)
            attr_id = find_or_create_attr(location_id, attr_type_id, value, db)

        i += 1

    return i


# --------------------------------------------------
def find_or_create_location(location, db):
    """Find or create the location"""

    cur = db.cursor()
    cur.execute('select location_id from location where name=?', (location, ))
    res = cur.fetchone()
    location_id = 0

    if res is None:
        print(f'Loading location "{location}"')
        cur.execute('insert into location (name) values (?)', (location, ))
        location_id = cur.lastrowid
        db.commit()
    else:
        location_id = res[0]

    return location_id


# --------------------------------------------------
def find_or_create_attr_type(attr_type, db):
    """Find or create the attr_type"""

    cur = db.cursor()
    cur.execute('select attr_type_id from attr_type where attr_type=?',
                (attr_type, ))
    res = cur.fetchone()
    attr_type_id = 0

    if res is None:
        print(f'Loading attr_type "{attr_type}"')
        cur.execute('insert into attr_type (attr_type) values (?)',
                    (attr_type, ))
        attr_type_id = cur.lastrowid
        db.commit()
    else:
        attr_type_id = res[0]

    return attr_type_id


# --------------------------------------------------
def find_or_create_attr(location_id, attr_type_id, value, db):
    """Find or create the attr"""

    cur = db.cursor()
    find_sql = ('select attr_id from attr '
                'where location_id=? '
                'and   attr_type_id=?')

    insert_sql = ('insert into attr '
                  '(location_id, attr_type_id, value) '
                  'values (?, ?, ?)')
    cur.execute(find_sql, (location_id, attr_type_id))
    res = cur.fetchone()
    attr_id = 0

    if res is None:
        print(f'Loading attr "{value}"')
        cur.execute(insert_sql, (location_id, attr_type_id, value))
        attr_id = cur.lastrowid
        db.commit()
    else:
        attr_id = res[0]

    return attr_id


# --------------------------------------------------
def dequote(s):
    """Remove leading/trailing quotes"""

    return re.sub('^"|"$', '', s)


# --------------------------------------------------
if __name__ == '__main__':
    main()
