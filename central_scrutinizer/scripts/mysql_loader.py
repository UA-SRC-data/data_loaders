#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-03-09
Purpose: Load the Central Scrutinizer's MySQL database
"""

import argparse
import csv
import os
import sys
from scrutinizer import database, Location, LocationType, Measurement, \
    Variable, Medium, Source
from typing import NamedTuple, List, TextIO


class Args(NamedTuple):
    file: List[TextIO]


class Record(NamedTuple):
    source: str
    unit: str
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
        description="Load the Central Scrutinizer's MySQL database",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('rt'),
                        help='Input file(s)')

    args = parser.parse_args()

    return Args(args.file)


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
        value = None

        try:
            value = float(rec.value)
        except Exception:
            pass

        # we'll skip loading non-numeric values
        if value is None:
            continue

        loc_type, _ = LocationType.get_or_create(
            location_type=rec.location_type)

        location, _ = Location.get_or_create(
            location_name=rec.location_name,
            location_type_id=loc_type.location_type_id)

        source, _ = Source.get_or_create(source=rec.source)

        variable, _ = Variable.get_or_create(
            variable=rec.variable_name,
            source_id=source.source_id)

        if rec.unit:
            variable.unit = rec.unit
            variable.save()

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
