#!/usr/bin/env python3
"""
Attempt to use datapackage
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
        description='Use datapackage',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        metavar='FILE',
                        help='Input file',
                        type=argparse.FileType('rt'),
                        default='datapackage.json')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    args.file.close()
    package = Package(args.file.name)
    for resource in package.resources:
        print(f'==> {resource.name} <==')
        pprint(resource.descriptor)
        for row in resource.iter(keyed=True):
            print(row.get('contaminant'), row.get('value'))
            break


# --------------------------------------------------
if __name__ == '__main__':
    main()
