#!/usr/bin/env python3
"""
Author : Ken Youens-Clark<kyclark@gmail.com>
Date   : 2020-04-01
Purpose: Load AZEPHT data
"""

import argparse
import csv
import os
import re
import sys
from typing import TextIO, NamedTuple, Dict, List
from collections import defaultdict


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[TextIO]
    outfile: TextIO
    variables: TextIO
    location_type: str
    medium: str
    source: str
    units: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Load AZEPHT data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--files',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+',
                        help='Input file(s)')

    parser.add_argument('-v',
                        '--variables',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='ArizonaEPHT_Variables.csv',
                        help='Variables file')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='scrutinizer.csv',
                        help='Output file')

    parser.add_argument('-l',
                        '--location_type',
                        metavar='location type',
                        type=str,
                        required=True,
                        choices=['county', 'municipality'],
                        help='Location type')

    parser.add_argument('-m',
                        '--medium',
                        metavar='medium',
                        type=str,
                        default='population',
                        help='Medium for data')

    parser.add_argument('-s',
                        '--source',
                        metavar='source',
                        type=str,
                        default='AZEPHT',
                        help='Source for data')

    parser.add_argument('-u',
                        '--units',
                        metavar='units',
                        type=str,
                        default='Cases per 100,000 people per year',
                        help='Units for data')

    args = parser.parse_args()

    return Args(files=args.files,
                outfile=args.outfile,
                variables=args.variables,
                location_type=args.location_type,
                medium=args.medium,
                source=args.source,
                units=args.units)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    variables = get_variables(args.variables)
    writer = csv.DictWriter(args.outfile,
                            fieldnames=[
                                'source', 'unit', 'location_name',
                                'location_type', 'variable_name',
                                'variable_desc', 'collected_on', 'medium',
                                'value'
                            ])
    writer.writeheader()
    num_exported = 0

    for fh in args.files:
        reader = csv.DictReader(fh, delimiter=',')

        # Cannot normalize names b/c some have "Name" and "NAME" fields!
        # reader.fieldnames = list(map(normalize, reader.fieldnames))

        if 'Name' not in reader.fieldnames:
            print(f'"{fh.name}" missing county "Name" field', file=sys.stderr)
            print("\n".join(map(lambda f: f'"{f}"', reader.fieldnames)))
            print(reader.fieldnames)
            continue

        counties = [
            'Apache', 'Cochise', 'Coconino', 'Gila', 'Graham', 'Greenlee',
            'La Paz', 'Maricopa', 'Mohave', 'Navajo', 'Pima', 'Pinal',
            'Santa Cruz', 'Yavapai', 'Yuma'
        ]

        basename = os.path.basename(fh.name)
        for rec in reader:
            loc_name = ' '.join(map(str.title, rec.get('Name', '').split()))
            if args.location_type == 'county' and loc_name not in counties:
                print(f'{basename}: unknown county "{loc_name}"',
                      file=sys.stderr)
                continue

            indicator_name = rec.get('indicatorName')
            if not indicator_name:
                print(f'{basename}: missing indicator name', file=sys.stderr)
                continue

            vars_ = variables.get(normalize(indicator_name))
            if not vars_:
                print(f'{basename}: unknown indicator "{indicator_name}"',
                      file=sys.stderr)
                continue

            if len(vars_) > 1:
                print(f'{basename}: multiple variables for "{indicator_name}"',
                      file=sys.stderr)
                continue

            variable = vars_[0]

            value = rec.get('Value')
            if not value:
                print(f'{basename}: missing value', file=sys.stderr)
                continue

            num_exported += 1
            writer.writerow({
                'source':
                args.source,
                'unit':
                args.units,
                'location_name':
                loc_name,
                'location_type':
                args.location_type,
                'variable_name':
                variable['Code'],
                'variable_desc':
                '{}: {}'.format(indicator_name, variable['Measure']),
                'medium':
                args.medium,
                'collected_on':
                rec.get('Year') or '',
                'value':
                value,
            })

    print(f'Done, exported {num_exported:,} to "{args.outfile.name}"')


# --------------------------------------------------
def normalize(s: str) -> str:
    """ Normalize a string """

    return re.sub('[^a-z0-9_]', '_', re.sub('[()]', '', s.lower()))


# --------------------------------------------------
def get_variables(fh: TextIO) -> Dict[str, Dict[str, str]]:
    """ Read variables file """

    reader = csv.DictReader(fh)
    ret = defaultdict(list)
    for rec in reader:
        indicator = normalize(rec['Indicator'])
        ret[indicator].append(rec)

    return ret


# --------------------------------------------------
if __name__ == '__main__':
    main()
