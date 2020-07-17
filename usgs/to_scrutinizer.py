#!/usr/bin/env python3
"""
Author : Ken Youens-Clark<kyclark@gmail.com>
Date   : 2020-04-01
Purpose: Load USGS data
"""

import argparse
import csv
import re
from pprint import pprint
from typing import TextIO, NamedTuple, Dict


class Args(NamedTuple):
    file: TextIO
    units: TextIO
    outfile: TextIO
    medium: str
    source: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Load USGS data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        metavar='FILE',
                        type=argparse.FileType('rt', encoding='utf-8-sig'),
                        default='az_data_bg.csv',
                        help='Input file')

    parser.add_argument('-u',
                        '--units',
                        metavar='FILE',
                        type=argparse.FileType('rt', encoding='utf-8-sig'),
                        default='units.csv',
                        help='Input file')

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
                        default='soil',
                        help='Medium for data')

    parser.add_argument('-s',
                        '--source',
                        metavar='source',
                        type=str,
                        default='USGS',
                        help='Source for data')

    args = parser.parse_args()

    return Args(file=args.file,
                units=args.units,
                outfile=args.outfile,
                medium=args.medium,
                source=args.source)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    units = read_units(args.units)
    reader = csv.DictReader(args.file, delimiter=',')
    reader.fieldnames = list(map(normalize, reader.fieldnames))

    # wanted = """
    #     top5_as top5_ba top5_fe top5_hg top5_pb
    # """.split()

    wanted = list(filter(lambda f: f.startswith('top5_'), reader.fieldnames))

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
        if rec['stateid'] != 'AZ':
            continue

        for fld in wanted:
            val = None
            try:
                val = float(rec[fld])
            except Exception:
                pass

            if val is not None:
                point = ','.join([rec['latitude'], rec['longitude']])
                symbol = fld.replace('top5_', '')
                num_exported += 1
                writer.writerow({
                    'source': args.source,
                    'unit': units.get(fld, ''),
                    'location_name': point,
                    'location_type': 'point',
                    'variable_name': symbol,
                    'variable_desc': f'Concentration of {symbol}',
                    'medium': args.medium,
                    'collected_on': '2013-09-18',
                    'value': str(val)
                })

    print(f'Done, exported {num_exported:,} to "{args.outfile.name}"')


# --------------------------------------------------
def normalize(s):
    """ Normalize a string """

    return re.sub('[^a-z0-9_]', '_', re.sub('[()]', '', s.lower()))


# --------------------------------------------------
def read_units(fh: TextIO) -> Dict[str, str]:
    """Read units file"""

    reader = csv.DictReader(fh, delimiter=',')
    units = next(reader)
    return {normalize(key): val for key, val in units.items()}


# --------------------------------------------------
if __name__ == '__main__':
    main()
