#!/usr/bin/env python3
""" Merge GEOID """

import argparse
import csv
import os
import re
import sys
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Merge GEOID',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        help='Input file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-g',
                        '--geoid',
                        help='GEOID input file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        required=True)

    parser.add_argument('-t',
                        '--type',
                        help='GEOID type',
                        metavar='type',
                        type=str,
                        choices=['bg', 'centroid'],
                        default='')

    args = parser.parse_args()

    if not args.type:
        root, _ = os.path.splitext(os.path.basename(args.geoid.name))
        if root.endswith('_bg'):
            args.type = 'bg'
        elif root.endswith('_centroid'):
            args.type = 'centroid'
        else:
            parser.error('Cannot guess --type from "{root}"')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    geoid = {
        normalize(row['sample']): row
        for row in csv.DictReader(args.geoid, delimiter=',')
    }

    for fh in args.file:
        reader = csv.DictReader(fh, delimiter=',')
        basename = os.path.basename(fh.name)
        out_dir = os.path.dirname(fh.name)
        root, ext = os.path.splitext(basename)
        out_file = os.path.join(out_dir, f'{root}_{args.type}{ext}')
        out_fh = open(out_file, 'wt')
        flds = list(filter(lambda f: f,
                           reader.fieldnames)) + ['geoid', 'geoid_type']
        writer = csv.DictWriter(out_fh, fieldnames=flds)
        writer.writeheader()

        for row in reader:
            sample = normalize(row.get('sample'))
            if not sample:
                continue

            geo = geoid.get(sample)
            if not geo:
                #print(f'No GEOID for sample "{sample}"', file=sys.stderr)
                print(sample, file=sys.stderr)
                continue

            row['geoid'] = geo.get('geoid') or 'NA'
            row['geoid_type'] = geo.get('geoid_type') or 'NA'
            writer.writerow(row)


# --------------------------------------------------
def normalize(name):
    """ Format """

    match = re.search(r'^([A-Z]+)[-\s]?(\d+)', name)
    if match:
        name = match.group(1) + '{:02d}'.format(int(match.group(2)))

    return name


# --------------------------------------------------
if __name__ == '__main__':
    main()
