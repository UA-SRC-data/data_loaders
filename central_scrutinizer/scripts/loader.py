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
from scrutinizer import database, Location, LocationType, Measurement, Variable, Medium
from typing import NamedTuple


class Record(NamedTuple):
    location_name: str
    location_type: str
    variable_name: str
    variable_desc: str
    medium: str
    collected_on: str
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
    total = 0

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        total += process(fh, database)

    print(f'Done, processed {total:,} records.')


# --------------------------------------------------
def process(fh, db):
    """Put the data into the db"""

    reader = csv.DictReader(fh, delimiter=',')
    num = 0
    for rec in map(lambda r: Record(**r), reader):
        value = rec.value

        try:
            value = float(value)
        except Exception:
            # we'll skip loading non-numeric values
            continue

        loc_type, _ = LocationType.get_or_create(
            location_type=rec.location_type)

        location, _ = Location.get_or_create(
            location_name=rec.location_name,
            location_type_id=loc_type.location_type_id)

        variable, _ = Variable.get_or_create(variable=rec.variable_name)

        if rec.variable_desc:
            variable.description = rec.variable_desc
            variable.save()

        medium, _ = Medium.get_or_create(medium=rec.medium)

        measurement, _ = Measurement.get_or_create(
            variable_id=variable.variable_id,
            location_id=location.location_id,
            medium_id=medium.medium_id,
            value=value)

        if rec.collected_on:
            measurement.collected_on = rec.collected_on
            measurement.save()

        num += 1

    return num


# --------------------------------------------------
if __name__ == '__main__':
    main()
