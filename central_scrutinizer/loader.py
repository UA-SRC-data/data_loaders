#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-03-09
Purpose: Load the Central Scrutinizer
"""

import argparse
import csv
import os
import sys
from scrutinizer import database, Location, LocationType, Measurement, Variable
from typing import NamedTuple


class Record(NamedTuple):
    location_name: str
    location_type: str
    variable_name: str
    variable_desc: str
    value: str


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Load the Central Scrutinizer',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help='Input file(s)')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    #args.db.close()
    #dbh = sqlite3.connect(args.db.name)
    total = 0

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')

        total += process(fh, database)

    print(f'Done, processed {total} records.')


# --------------------------------------------------
def process(fh, db):
    """Put the data into the db"""

    reader = csv.DictReader(fh, delimiter=',')
    num = 0
    for rec in map(lambda r: Record(**r), reader):
        loc_type, _ = LocationType.get_or_create(
            location_type=rec.location_type)

        location, _ = Location.get_or_create(
            location_name=rec.location_name,
            location_type_id=loc_type.location_type_id)

        variable, _ = Variable.get_or_create(
            variable=rec.variable_name,
            description=rec.variable_desc)

        measurement, _ = Measurement.get_or_create(
            variable_id=variable.variable_id,
            location_id=location.location_id,
            value=rec.value)

        num += 1

    return num


# --------------------------------------------------
if __name__ == '__main__':
    main()
