#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-06-26
Purpose: Separate water by years
"""

import argparse
import csv
import dateparser
import os
from collections import defaultdict
from typing import NamedTuple, TextIO, List


class Args(NamedTuple):
    file: TextIO
    year: List[int]
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Separate water by years',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-y',
                        '--year',
                        help='Restrict to year(s)',
                        metavar='int',
                        type=int,
                        nargs='*')

    parser.add_argument('-f',
                        '--file',
                        help='Input file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='narrowresult.csv')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output dir',
                        metavar='DIR',
                        type=str,
                        default=os.path.join(os.getcwd(), 'years'))

    args = parser.parse_args()

    return Args(args.file, args.year, args.outdir)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    reader = csv.DictReader(args.file)
    years = defaultdict(list)
    for rec in reader:
        # Skip records with no units
        if not rec.get('ResultMeasure/MeasureUnitCode'):
            continue

        # Attempt to parse the date
        if date := rec.get('ActivityStartDate'):
            dp = dateparser.parse(date)
            if year := dp.year:
                if not args.year or year in args.year:
                    years[year].append(rec)

    for year in sorted(years):
        print(f'Writing year "{year}"')
        out_file = os.path.join(out_dir, str(year) + '.csv')
        with open(out_file, 'wt') as out_fh:
            writer = csv.DictWriter(out_fh, reader.fieldnames)
            writer.writeheader()
            for rec in years[year]:
                writer.writerow(rec)

    print('Done.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
