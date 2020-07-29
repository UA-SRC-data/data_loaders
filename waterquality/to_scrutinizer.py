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
from pprint import pprint
from typing import TextIO, NamedTuple, Dict, Tuple


class Args(NamedTuple):
    file: TextIO
    stations: TextIO
    outfile: TextIO
    medium: str
    source: str


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

    num_exported = 0
    for i, rec in enumerate(reader, start=1):
        val = None
        try:
            val = float(rec['ResultMeasureValue'])
        except Exception:
            pass

        if val is None:
            continue

        dt = dateparser.parse(rec['ActivityStartDate'])
        if dt.year != 2018:
            continue

        loc_id = rec.get('MonitoringLocationIdentifier')
        if not loc_id:
            continue

        if loc_id not in stations:
            print('Missing location "{loc_id}"', file=sys.stderr)
            continue

        variable = rec.get('CharacteristicName')

        num_exported += 1
        writer.writerow({
            'source': args.source,
            'unit': rec.get('ResultMeasure/MeasureUnitCode', 'NA'),
            'location_name': ','.join(stations.get(loc_id)),
            'location_type': 'point',
            'variable_name': variable,
            'variable_desc': f'Concentration of {variable} in water',
            'medium': args.medium,
            'collected_on': '{}-{}-{}'.format(dt.year, dt.month, dt.day),
            'value': str(val)
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
