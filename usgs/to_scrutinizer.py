#!/usr/bin/env python3
"""
Author : Ken Youens-Clark<kyclark@gmail.com>
Date   : 2020-04-01
Purpose: Load USGS data
"""

import argparse
import csv
import os
import re
import shapefile
import sys
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Load USGS data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='az_data_bg.csv',
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

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    data = reader(args.file)
    hdrs = list(map(normalize, data.pop(0)))
    units = dict(zip(hdrs, data.pop(0)))
    wanted = """
        top5_as top5_ba top5_fe top5_hg top5_pb
    """.split()

    symbol_to_name = {
        'as': 'arsenic',
        'ba': 'barium',
        'fe': 'iron',
        'hg': 'mercury',
        'pb': 'lead'
    }

    flds = [
        'location_name', 'location_type', 'variable_name', 'variable_desc',
        'collected_on', 'medium', 'value'
    ]
    writer = csv.DictWriter(args.outfile, fieldnames=flds)
    writer.writeheader()

    num_exported = 0
    for row in data:
        rec = dict(zip(hdrs, row))
        if rec['stateid'] != 'AZ':
            continue

        for fld in wanted:
            val = None
            try:
                val = float(rec[fld])
            except Exception:
                pass

            if val is None:
                continue

            point = ','.join([rec['latitude'], rec['longitude']])
            symbol = fld.replace('top5_', '')
            element = symbol_to_name.get(symbol)
            if element:
                num_exported += 1
                writer.writerow({
                    'location_name': point,
                    'location_type': 'point',
                    'variable_name': element,
                    'variable_desc': '',
                    'medium': args.medium,
                    'collected_on': '2013-09-18',
                    'value': str(val)
                })

    print(f'Done, exported {num_exported:,} to "{args.outfile.name}"')


# --------------------------------------------------
def reader(fh):
    """ Handle BOM (byte order mark) in Excel output """

    BOM = "\ufeff"
    text = fh.read()
    if text.startswith(BOM):
        text = text[1:]

    return list(map(lambda s: s.split(','), text.splitlines()))


# --------------------------------------------------
def normalize(s):
    """ Normalize a string """

    return re.sub('[^a-z0-9_]', '_', re.sub('[()]', '', s.lower()))


# --------------------------------------------------
if __name__ == '__main__':
    main()
