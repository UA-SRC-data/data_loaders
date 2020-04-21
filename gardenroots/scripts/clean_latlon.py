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
    reqd = ['Kit Number', 'Lat', 'Long']
    seen, exported = 0, 0

    for i, rec in enumerate(reader, start=1):
        sample = rec.get('Kit Number')
        lat = rec.get('Lat')
        lon = rec.get('Long')

        # skip blank lines
        if not any([sample, lat, lon]):
            continue

        seen += 1
        missing = list(filter(lambda f: not rec.get(f), reqd))
        if missing:
            print('Line {} "{}" missing req fld: {}'.format(i,
                                                            sample,
                                                            ', '.join(missing),
                                                            file=sys.stderr))
            continue

        match = regex.search(sample)

        if not match:
            print(f'Line {i} weird sample "{sample}"', file=sys.stderr)
            continue

        sample = match.group(1) + '{:02d}'.format(int(match.group(2)))
        writer.writerow({'sample': sample, 'latitude': lat, 'longitude': lon})
        exported += 1

    print(
        f'Done, exported {exported} of {seen} to outfile "{args.outfile.name}"'
    )


# --------------------------------------------------
if __name__ == '__main__':
    main()
