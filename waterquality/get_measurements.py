#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-06-26
Purpose: Extract measurements
"""

import argparse
import csv
from typing import NamedTuple, TextIO, List


class Args(NamedTuple):
    file: List[TextIO]
    outfile: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Extract measurements',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input file(s)',
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('rt'))

    parser.add_argument('-o',
                        '--outfile',
                        help='Output file',
                        metavar='FILE',
                        default='measurements.csv',
                        type=argparse.FileType('wt'))

    args = parser.parse_args()

    return Args(args.file, args.outfile)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    uniq = set()
    for fh in args.file:
        reader = csv.DictReader(fh)
        for rec in reader:
            uniq.add((rec['CharacteristicName'],
                      rec['ResultMeasure/MeasureUnitCode']))

    writer = csv.DictWriter(args.outfile, ['name', 'unit'])
    writer.writeheader()
    num = 0
    for name, unit in uniq:
        num += 1
        writer.writerow({'name': name, 'unit': unit})

    print(f'Done, wrote {num} to {args.outfile.name}.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
