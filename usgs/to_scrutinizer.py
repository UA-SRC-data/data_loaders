#!/usr/bin/env python3
"""
Author : Ken Youens-Clark<kyclark@gmail.com>
Date   : 2020-04-01
Purpose: Load USGS data
"""

import argparse
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
                        type=argparse.FileType('r'),
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

    args.outfile.write(','.join([
        'location_name', 'location_type', 'variable_name', 'variable_desc',
        'collected_on', 'medium', 'value'
    ]) + '\n')

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
                continue

            if val is None:
                continue

            num_exported += 1
            args.outfile.write(','.join([
                str(rec['geoid']), rec['geoid_type'],
                fld.replace('top5_', ''), fld, args.medium,
                '2013-09-18',
                str(val)
            ]) + '\n')

    print(f'Done, exported {num_exported} to "{args.outfile.name}"')


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
