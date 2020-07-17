#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-03-09
Purpose: Scrutinizer to JSON for Mongo load
"""

import argparse
import csv
import os
from scrutinizer import Measurement
from typing import NamedTuple


class Args(NamedTuple):
    outdir: str
    verbose: bool


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Scrutinizer to JSON for Mongo load',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='scrutinizer')

    parser.add_argument('-v',
                        '--verbose',
                        help='Talk about (pop music)',
                        action='store_true')

    args = parser.parse_args()

    return Args(args.outdir, args.verbose)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    print('Starting export... (--verbose for updates)')

    variables = set()
    measurements_file = os.path.join(args.outdir, 'scrutinizer.csv')
    with open(measurements_file, 'wt') as measurements_fh:
        writer = csv.DictWriter(measurements_fh,
                                fieldnames=[
                                    'source', 'unit', 'variable_name',
                                    'location_name', 'location_type', 'value',
                                    'collected_on', 'medium', 'variable_desc'
                                ],
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()

        for i, m in enumerate(Measurement, start=1):
            if args.verbose:
                print(f'{i:6}: {m.variable.variable} {m.value}')

            writer.writerow({
                'source': m.variable.source.source,
                'unit': m.variable.unit,
                'variable_name': m.variable.variable,
                'variable_desc': m.variable.description,
                'location_name': str(m.location.location_name),
                'location_type': m.location.location_type.location_type,
                'value': m.value,
                'collected_on': m.collected_on,
                'medium': m.medium.medium,
            })

            variables.add((m.variable.variable, m.variable.description))

    variables_file = os.path.join(args.outdir, 'variables.csv')
    with open(variables_file, 'wt') as variables_fh:
        writer = csv.DictWriter(variables_fh, fieldnames=['name', 'desc'])
        writer.writeheader()
        for key, val in dict(variables).items():
            writer.writerow({'name': key, 'desc': val})

    print(f'Done, see outdir "{args.outdir}".')


# --------------------------------------------------
if __name__ == '__main__':
    main()
