#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-09
Purpose: Make datapackage
"""

import argparse
import os
import sys
from datapackage import Package
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Make datapackage',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+',
                        help='Input file')

    parser.add_argument('-o',
                        '--outfile',
                        help='Output file',
                        metavar='FILE',
                        type=str,
                        default='datapackage.json')

    parser.add_argument('-m',
                        '--missing',
                        help='Missing value',
                        metavar='missing',
                        type=str,
                        nargs='*')

    parser.add_argument('-f',
                        '--force',
                        help='Force overwrite of existing --outfile',
                        action='store_true')

    args = parser.parse_args()

    if os.path.isfile(args.outfile) and not args.force:
        parser.error(f'--outfile "{args.outfile}" exists!'
                     'Use --force to overwrite')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    package = Package()

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        fh.close()
        package.infer(fh.name)

    if args.missing:
        for res in package.resources:
            res.descriptor['schema']['missingValues'].extend(args.missing)
            package.remove_resource(res.name)
            package.add_resource(res.descriptor)

    package.save(args.outfile)

    print(f'Done, see "{args.outfile}"')


# --------------------------------------------------
if __name__ == '__main__':
    main()
