#!/usr/bin/env python3
"""
Author : Ken Youens-Clark<kyclark@gmail.com>
Date   : 2020-04-01
Purpose: Format water quality
"""

import argparse
import dateparser
import datetime
import csv
import re
import sys
import recordparser
from pprint import pprint
from typing import TextIO, NamedTuple, Dict, Tuple


class Args(NamedTuple):
    file: TextIO
    stations: TextIO
    outfile: TextIO
    medium: str
    source: str


class Record(NamedTuple):
    variable: str
    location_name: str
    collected_on: str
    value: float
    unit: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Format water quality',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='narrowresult.csv',
                        help='Input file')

    parser.add_argument('-s',
                        '--station_file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='station.csv',
                        help='Station file')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='scrutinizer.csv',
                        help='Output file')

    parser.add_argument('-m',
                        '--medium',
                        metavar='medium',
                        type=str,
                        default='water',
                        help='Medium for data')

    parser.add_argument('-r',
                        '--source',
                        metavar='source',
                        type=str,
                        default='USGS Arizona Water Science Center',
                        help='Source for data')

    args = parser.parse_args()

    return Args(file=args.file,
                stations=args.station_file,
                outfile=args.outfile,
                medium=args.medium,
                source=args.source)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    stations = read_stations(args.stations)
    reader = csv.DictReader(args.file, delimiter=',')
    writer = csv.DictWriter(args.outfile,
                            fieldnames=[
                                'source', 'unit', 'location_name',
                                'location_type', 'variable_name',
                                'variable_desc', 'collected_on', 'medium',
                                'value'
                            ])
    writer.writeheader()

    mapping = {
        'CharacteristicName': 'variable',
        'MonitoringLocationIdentifier': 'location_name',
        'ActivityStartDate': 'collected_on',
        'ResultMeasureValue': 'value',
        'ResultMeasure/MeasureUnitCode': 'unit',
    }

    parser = recordparser.parse(fh=args.file,
                                cls=Record,
                                delimiter=',',
                                mapping=mapping)

    num_exported = 0
    for i, rec in enumerate(parser, start=1):
        dt = dateparser.parse(rec.collected_on)
        if dt.year != 2018:
            continue

        if not rec.location_name:
            continue

        if rec.location_name not in stations:
            print('Missing location "{rec.location_name}"', file=sys.stderr)
            continue

        collected_on = '{:02d}-{:02d}-{:02d}'.format(dt.year, dt.month, dt.day)

        num_exported += 1
        writer.writerow({
            'source': args.source,
            'unit': rec.unit or 'NA',
            'location_name': ','.join(stations.get(rec.location_name)),
            'location_type': 'point',
            'variable_name': rec.variable,
            'variable_desc': f'Concentration of {rec.variable} in water',
            'medium': args.medium,
            'collected_on': collected_on,
            'value': str(rec.value)
        })

    print(f'Done, exported {num_exported:,} to "{args.outfile.name}"')


# --------------------------------------------------
def read_stations(fh: TextIO) -> Dict[str, Tuple[str, str]]:
    """Read the stations file"""

    reader = csv.DictReader(fh)
    return {
        r['MonitoringLocationIdentifier']:
        (r['LatitudeMeasure'], r['LongitudeMeasure'])
        for r in reader
    }


# --------------------------------------------------
def normalize(s):
    """ Normalize a string """

    return re.sub('[^a-z0-9_]', '_', re.sub('[()]', '', s.lower()))


# --------------------------------------------------
if __name__ == '__main__':
    main()
