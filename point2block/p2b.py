#!/usr/bin/env python3
"""
Author : Ken Youens-Clark<kyclark@gmail.com>
Date   : 2020-04-01
Purpose: Add census block group to file containing lat/lon
"""

import argparse
import os
import shapefile
import sys
import csv
from shapely.geometry import shape, Point


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Add census block group to file containing lat/lon',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Can't use argparse.FileType('r') here because I need to
    # know about the BOM to handle the open
    parser.add_argument('file', metavar='FILE', type=str, help='Input file')

    parser.add_argument('-d',
                        '--delimiter',
                        metavar='delimiter',
                        type=str,
                        default=',',
                        help='Input file field delimiter')

    parser.add_argument('-s',
                        '--shapefile',
                        metavar='FILE',
                        type=str,
                        default='',
                        help='Input file')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='out.csv',
                        help='Output file')

    parser.add_argument('-b',
                        '--bom',
                        action='store_true',
                        help='Input file has byte-order mark')

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f'"{args.file}" is not a valid file')

    args.file = open(args.file, encoding='utf-8-sig' if args.bom else 'utf-8')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    reader = csv.DictReader(args.file, delimiter=args.delimiter)

    flds = reader.fieldnames
    missing = list(filter(lambda f: f not in flds, ['latitude', 'longitude']))
    if missing:
        print('Error: "{}" missing "{}"'.format(args.file.name,
                                                ', '.join(missing)),
              file=sys.stderr)
        sys.exit(1)

    shapes = read_shapefile(args.shapefile)

    out_flds = flds + ['block_group']

    args.outfile.write(','.join(out_flds) + '\n')

    num = 0
    for rec in reader:
        point = Point(float(rec['longitude']), float(rec['latitude']))
        block = list(filter(lambda s: s['SHAPE'].contains(point), shapes))
        rec['block_group'] = block[0]['GEOID'] if len(block) == 1 else 'NA'
        args.outfile.write(','.join(map(rec.get, out_flds)) + '\n')
        num += 1

    print(f'Done, exported {num} to "{args.outfile.name}"')


# --------------------------------------------------
def read_shapefile(file):
    """Read the shapefile"""

    sf = shapefile.Reader(file)

    def shp2rec(shp):
        rec = shp.record.as_dict()
        rec['SHAPE'] = shape(shp.__geo_interface__['geometry'])
        return rec

    return list(map(shp2rec, sf.shapeRecords()))


# --------------------------------------------------
if __name__ == '__main__':
    main()
