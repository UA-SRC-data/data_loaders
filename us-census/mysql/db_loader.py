#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-02-07
Purpose: Load "data_with_overlays" into SQLite
"""

import argparse
import configparser
import csv
import os
import re
import mysql.connector
import sys
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Load "data_with_overlays" into MySQL',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help='Input file(s)')

    parser.add_argument('-d',
                        '--db',
                        metavar='DB',
                        default='uasrc',
                        help='MySQL db')

    parser.add_argument('-u',
                        '--user',
                        metavar='USER',
                        default='kyclark',
                        help='MySQL user')

    parser.add_argument('-p',
                        '--password',
                        metavar='PASSWORD',
                        default='',
                        help='MySQL password')

    parser.add_argument('-H',
                        '--host',
                        metavar='HOST',
                        default='127.0.0.1',
                        help='MySQL host')

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
    db_name = args.db
    db_user = args.user
    db_host = args.host
    db_pass = args.password
    my_cnf = os.path.join(os.path.expanduser("~"), '.my.cnf')

    if not db_pass and os.path.isfile(my_cnf):
        config = configparser.ConfigParser()
        print(f'Reading "{my_cnf}"')
        config.read(my_cnf)
        if 'client' in config:
            db_pass = config['client']['password']

    if not db_pass:
        print('Error: Missing --password')
        sys.exit(1)

    dbh = mysql.connector.connect(user=db_user,
                                  password=db_pass,
                                  host=db_host,
                                  database=db_name)
    num_imported = 0

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        num_imported += process(fh, dbh, args)

    print(f'Done, imported {num_imported}')


# --------------------------------------------------
def process(fh, dbh, args):
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
        location = rec.get(location_header)

        if not location:
            print(f'Missing "{location_header}" value!')
            continue

        location_id = find_or_create_location(location, dbh)

        for attr_type in filter(lambda col: col != 'id', headers):
            value = rec[attr_type]
            if value == '':
                continue

            attr_type_id = find_or_create_attr_type(attr_type, dbh)
            attr_id = find_or_create_attr(location_id, attr_type_id, value, dbh)

        i += 1

    return i


# --------------------------------------------------
def find_or_create_location(location, dbh):
    """Find or create the location"""

    cur = dbh.cursor()
    cur.execute('select location_id from location where name = %s', (location, ))
    res = cur.fetchone()
    location_id = 0

    if res is None:
        print(f'Loading location "{location}"')
        cur.execute('insert into location (name) values (%s)', (location, ))
        location_id = cur.lastrowid
        dbh.commit()
    else:
        location_id = res[0]

    return location_id


# --------------------------------------------------
def find_or_create_attr_type(attr_type, dbh):
    """Find or create the attr_type"""

    cur = dbh.cursor()
    cur.execute('select attr_type_id from attr_type where attr_type = %s',
                (attr_type, ))
    res = cur.fetchone()
    attr_type_id = 0

    if res is None:
        print(f'Loading attr_type "{attr_type}"')
        cur.execute('insert into attr_type (attr_type) values (%s)',
                    (attr_type, ))
        attr_type_id = cur.lastrowid
        dbh.commit()
    else:
        attr_type_id = res[0]

    return attr_type_id


# --------------------------------------------------
def find_or_create_attr(location_id, attr_type_id, value, dbh):
    """Find or create the attr"""

    cur = dbh.cursor()
    find_sql = ('select attr_id from attr '
                'where location_id = %s '
                'and   attr_type_id = %s')

    insert_sql = ('insert into attr '
                  '(location_id, attr_type_id, value) '
                  'values (%s, %s, %s)')
    cur.execute(find_sql, (location_id, attr_type_id))
    res = cur.fetchone()
    attr_id = 0

    if res is None:
        print(f'Loading attr "{value}"')
        cur.execute(insert_sql, (location_id, attr_type_id, value))
        attr_id = cur.lastrowid
        dbh.commit()
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
