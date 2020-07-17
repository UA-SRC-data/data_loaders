#!/usr/bin/env python3
"""
Author : Ken Youens-Clark<kyclark@gmail.com>
Date   : 2020-04-21
Purpose: Create Scrutinizer import
"""

import argparse
import csv
import os
import re
from datapackage import Package
from pprint import pprint
from typing import List, NamedTuple, TextIO


class Args(NamedTuple):
    file: List[TextIO]
    outdir: str
    source: str
    delimiter: str
    verbose: bool


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Create Scrutinizer import',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        help='GardenRoots "datapackage.json" file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+')

    parser.add_argument('-s',
                        '--source',
                        help='Data source',
                        metavar='src',
                        type=str,
                        default='GardenRoots')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='scrutinizer')

    parser.add_argument('-d',
                        '--delimiter',
                        help='Output file delimiter',
                        metavar='str',
                        type=str,
                        default=',')

    parser.add_argument('-v',
                        '--verbose',
                        help='Talk loudly',
                        action='store_true')

    args = parser.parse_args()

    return Args(file=args.file,
                source=args.source,
                outdir=args.outdir,
                delimiter=args.delimiter,
                verbose=args.verbose)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    for fh in args.file:
        fh.close()
        process(fh.name, args)

    print(f'Done, see output dir "{args.outdir}".')


# --------------------------------------------------
def process(pkg_name: str, args: Args):
    """Process resource into output directory"""

    _, ext = os.path.splitext(pkg_name)
    if ext != '.json':
        raise Exception(f'File "{pkg_name}" not a JSON file')

    reqd_flds = set("""
        geoid geoid_type sample sampling_year type
    """.split())

    contaiminants = """
        aluminum arsenic barium beryllium cadmium chromium
        manganese nickel lead zinc copper
    """.split()

    package = Package(pkg_name)

    for resource in package.resources:
        flds = set(
            map(lambda f: f['name'], resource.descriptor['schema']['fields']))

        if len(flds.intersection(reqd_flds)) != len(reqd_flds):
            continue

        print(f'==> {resource.name} <==')
        ext = '.csv' if args.delimiter == ',' else '.txt'
        out_file = os.path.join(args.outdir, resource.name + ext)
        flds = [
            'source', 'unit', 'location_name', 'location_type',
            'variable_name', 'variable_desc', 'collected_on', 'medium', 'value'
        ]

        with open(out_file, 'wt') as out_fh:
            writer = csv.DictWriter(out_fh,
                                    fieldnames=flds,
                                    delimiter=args.delimiter)
            writer.writeheader()

            for row in resource.iter(keyed=True):
                if args.verbose:
                    pprint(row)

                sampling_year = row.get('sampling_year')
                match = re.match(r'(20\d{2})', sampling_year)
                collected_on = '{}-01-01'.format(
                    match.group(1)) if match else ''

                if not collected_on:
                    continue

                for variable_name in contaiminants:
                    value = None
                    try:
                        value = float(row.get(variable_name))
                    except Exception:
                        pass

                    if value:
                        writer.writerow({
                            'source': args.source,
                            'unit': row.get('units'),
                            'location_name': row.get('geoid'),
                            'location_type': row.get('geoid_type'),
                            'variable_name': variable_name,
                            'variable_desc': '',
                            'collected_on': collected_on,
                            'medium': row.get('type'),
                            'value': value
                        })


# --------------------------------------------------
if __name__ == '__main__':
    main()
