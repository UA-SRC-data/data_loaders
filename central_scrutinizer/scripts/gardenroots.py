#!/usr/bin/env python3
"""
Author : Ken Youens-Clark<kyclark@gmail.com>
Date   : 2020-04-21
Purpose: Rock the Casbah
"""

import argparse
import os
import re
import sys
from datapackage import Package
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        help='GardenRoots "datapackage.json" file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+',
                        required=True)

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    parser.add_argument('-v',
                        '--verbose',
                        help='Talk loudly',
                        action='store_true')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    for fh in args.file:
        fh.close()
        process(fh.name, args.outdir, args.verbose)

    print('Done.')


# --------------------------------------------------
def process(pkg_name, out_dir, verbose):
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
        out_file = os.path.join(out_dir, resource.name + '.csv')
        out_fh = open(out_file, 'wt')
        delim = ','
        out_fh.write(
            delim.join([
                'location_name', 'location_type', 'variable_name',
                'variable_desc', 'collected_on', 'medium', 'value'
            ]) + '\n')

        data = []
        for row in resource.iter(keyed=True):
            if verbose:
                pprint(row)
            sampling_year = row.get('sampling_year')
            match = re.match(r'(20\d{2})', sampling_year)
            collected_on = '{}-01-01'.format(match.group(1)) if match else None

            if not collected_on:
                continue

            medium = row.get('type')
            location_name = row.get('geoid')
            location_type = row.get('geoid_type')

            for variable_name in contaiminants:
                value = row.get(variable_name)
                try:
                    value = float(value)
                except Exception:
                    value = None

                if value is None:
                    continue

                out_fh.write(
                    delim.join(
                        map(
                            str,
                            [
                                location_name,
                                location_type,
                                variable_name,
                                '',  # variable_desc
                                collected_on,
                                medium,
                                value
                            ])) + '\n')


# --------------------------------------------------
if __name__ == '__main__':
    main()
