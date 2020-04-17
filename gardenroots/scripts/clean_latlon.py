#!/usr/bin/env python3
"""
Clean up the lat/lon file
"""

import argparse
import csv
import re
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Clean up the lat/lon file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input file',
                        metavar='FILE',
                        type=argparse.FileType('rt', encoding='utf-8-sig'))

    parser.add_argument('-o',
                        '--outfile',
                        help='Output file',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='gardenroot_latlon.csv')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    reader = csv.DictReader(args.file, delimiter=',')
    writer = csv.DictWriter(args.outfile,
                            delimiter=',',
                            fieldnames=['sample', 'latitude', 'longitude'])
    writer.writeheader()
    regex = re.compile(r'^([A-Z]+)[-\s]?(\d+)')

    for i, rec in enumerate(reader, start=1):
        sample = rec.get('Kit Number')
        lat = rec.get('Lat')
        lon = rec.get('Long')

        if not sample:
            continue

        if not all([sample, lat, lon]):
            print(f'Line {i} missing req fld: "{rec}"', file=sys.stderr)
            continue

        match = regex.search(sample)
        if not match:
            print(f'Line {i} weird sample "{sample}"', file=sys.stderr)
            continue

        sample = match.group(1) + str(int(match.group(2)))
        writer.writerow({'sample': sample, 'latitude': lat, 'longitude': lon})

    print(f'Done, see outfile "{args.outfile.name}"')


# --------------------------------------------------
if __name__ == '__main__':
    main()
