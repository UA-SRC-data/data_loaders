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
    parser.add_argument('-f',
                        '--file',
                        metavar='FILE',
                        type=str,
                        required=True,
                        help='Input file')

    parser.add_argument('-s',
                        '--shapefile',
                        metavar='FILE',
                        type=str,
                        required=True,
                        help='Input file')

    parser.add_argument('-t',
                        '--type',
                        metavar='shapetype',
                        type=str,
                        required=True,
                        choices=['tract', 'block', 'block_group'],
                        help='Shapefile type')

    parser.add_argument('-d',
                        '--delimiter',
                        metavar='delimiter',
                        type=str,
                        default=',',
                        help='Input file field delimiter')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='out.csv',
                        help='Output file')

    parser.add_argument('-c',
                        '--cols',
                        metavar='keepcols',
                        nargs='*',
                        type=str,
                        help='Keep listed columns')

    parser.add_argument('-b',
                        '--bom',
                        action='store_true',
                        help='Input file has byte-order mark')

    parser.add_argument('-r',
                        '--rmlatlon',
                        action='store_true',
                        help='Remove the original latitude/longitude fields')

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

    lat_lon = ['latitude', 'longitude']
    flds = reader.fieldnames
    missing = list(filter(lambda f: f not in flds, lat_lon))
    if missing:
        print('Error: "{}" missing "{}"'.format(args.file.name,
                                                ', '.join(missing)),
              file=sys.stderr)
        sys.exit(1)

    shapes = read_shapefile(args.shapefile)

    if args.cols:
        flds = list(filter(lambda f: f in args.cols, flds))

    out_flds = flds + ['geoid', 'geoid_type']

    if args.rmlatlon:
        out_flds = list(filter(lambda f: f not in lat_lon, out_flds))

    args.outfile.write(','.join(out_flds) + '\n')

    total, exported = 0, 0
    for i, rec in enumerate(reader, start=1):
        total += 1
        point = None
        try:
            point = Point(float(rec['longitude']), float(rec['latitude']))
        except Exception:
            pass

        if not point:
            print('Line {} ({}) could not convert ({}, {}) to Point'.format(
                i, rec[flds[0]], rec['longitude'], rec['longitude']), file=sys.stderr)
            continue

        block = list(filter(lambda s: s['SHAPE'].contains(point), shapes))
        rec['geoid'] = block[0].get('GEOID', 'NA') if len(block) == 1 else 'NA'
        rec['geoid_type'] = args.type
        args.outfile.write(','.join(map(rec.get, out_flds)) + '\n')
        exported += 1

    print(f'Done, exported {exported} of {total} to "{args.outfile.name}"')


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
