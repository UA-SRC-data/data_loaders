#!/usr/bin/env python3
""" Merge GEOID """

import argparse
import csv
import os
import re
import sys


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

    return parser.parse_args()


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
        out_file = os.path.join(out_dir, root + '_bg' + ext)
        out_fh = open(out_file, 'wt')
        flds = reader.fieldnames + ['geoid', 'geoid_type']
        out_fh.write(','.join(flds) + '\n')

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
            out_fh.write(','.join(map(row.get, flds)) + '\n')


# --------------------------------------------------
def normalize(name):
    """ Format """

    match = re.search(r'^([A-Z]+)[-\s]?(\d+)', name)
    if match:
        name = match.group(1) + str(int(match.group(2)))

    return name


# --------------------------------------------------
if __name__ == '__main__':
    main()
