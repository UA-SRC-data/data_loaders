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
from shapely.geometry import shape, Point


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
                        default='data.csv',
                        help='Input file')

    parser.add_argument('-s',
                        '--shapefile',
                        metavar='FILE',
                        type=str,
                        default='shape/tl_2017_04_bg.dbf',
                        help='Input file')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='scrutinizer.csv',
                        help='Output file')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    data = reader(args.file)
    hdrs = list(map(normalize, data.pop(0)))
    units = dict(zip(hdrs, data.pop(0)))
    shapes = read_shapefile(args.shapefile)
    wanted = """
        top5_as top5_ba top5_fe top5_hg top5_pb
    """.split()

    args.outfile.write(','.join([
        'location_name', 'location_type', 'variable_name', 'variable_desc',
        'collected_on', 'value'
    ]) + '\n')

    num_exported = 0
    for row in data:
        rec = dict(zip(hdrs, row))
        if rec['stateid'] == 'AZ':
            point = Point(float(rec['longitude']), float(rec['latitude']))
            block = list(filter(lambda s: s['SHAPE'].contains(point), shapes))
            if len(block) == 1:
                block = block[0]
                for fld in wanted:
                    val = None
                    try:
                        val = float(rec[fld])
                        num_exported += 1
                        args.outfile.write(
                            ','.join([
                            str(block['GEOID']), 'census_block',
                            fld.replace('top5_', ''), fld, '2013-09-18',
                            str(val)
                        ]) + '\n')
                    except Exception:
                        pass

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
def read_shapefile(file):
    """Read the shapefile"""

    sf = shapefile.Reader(file)
    shapes = sf.shapes()
    counties = {
        '001': 'Apache',
        '003': 'Cochise',
        '011': 'Greenlee',
        '025': 'Yavapai'
    }

    data = []
    for shp in sf.shapeRecords():
        rec = shp.record.as_dict()
        if rec['COUNTYFP'] not in counties:
            continue

        rec['COUNTYNAME'] = counties[rec['COUNTYFP']]
        rec['SHAPE'] = shape(shp.__geo_interface__['geometry'])
        data.append(rec)

    return data


# --------------------------------------------------
if __name__ == '__main__':
    main()
