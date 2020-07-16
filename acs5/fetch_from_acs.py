#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-02-21
Purpose: Get US Census data
"""

import argparse
import csv
import os
import sys
import requests
from pprint import pprint
from typing import NamedTuple, TextIO, Optional, List


class Args(NamedTuple):
    file: TextIO
    variable: Optional[str]
    county: List[str]
    outdir: str
    verbose: bool


COUNTIES = {
    'Apache': '001',
    'Cochise': '003',
    'Greenlee': '011',
    'Yavapai': '025'
}


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Get US Census data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Input file of vars')

    parser.add_argument('-v',
                        '--variable',
                        metavar='var',
                        type=str,
                        nargs='*',
                        help='Input variable(s)')

    parser.add_argument('-c',
                        '--county',
                        help='County name(s)',
                        choices=sorted(COUNTIES.keys()),
                        metavar='str',
                        type=str,
                        nargs='+',
                        default=sorted(COUNTIES.keys()))

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='str',
                        default=os.path.join(os.getcwd(), 'data'))

    parser.add_argument('-V',
                        '--verbose',
                        help='Be chatty',
                        action='store_true')

    args = parser.parse_args()

    return Args(args.file, args.variable, args.county, args.outdir,
                args.verbose)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    variables = read_vars(args)
    out_dir = args.outdir
    num_vars = len(variables)

    if not num_vars:
        sys.exit('Must have --file or --variable to fetch')

    def progress(msg):
        if args.verbose:
            print(msg)

    progress(f"Fetching {num_vars} variable{'' if num_vars == 1 else 's'}")

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    tmpl = ('https://api.census.gov/data/2018/acs/acs5?'
            'get=NAME,{}&for=block%20group:*&in=state:04'
            '&in=county:{}&in=tract:*')

    num_vars = len(variables)
    for var_num, var in enumerate(variables, start=1):
        for county in args.county:
            county_num = COUNTIES.get(county)
            if not county_num:
                continue

            progress(f'{var_num:4}/{num_vars:4}: '
                     f'"{var}" for "{county}" ({county_num})')

            out_file = os.path.join(out_dir, f'{var}-{county_num}.csv')
            if os.path.isfile(out_file) and os.path.getsize(out_file):
                progress(f'\tSkipping "{out_file}" exists')
                continue

            url = tmpl.format(var, county_num)
            r = requests.get(url)
            if r.status_code == 429:
                sys.exit(f'Status "{r.status_code}" getting "{url}"')

            data = r.json()
            headers = data.pop(0)
            var_name = headers[1]

            if not data:
                continue

            progress(f'\tWriting "{out_file}"')
            writer = csv.DictWriter(
                open(out_file, 'wt'),
                fieldnames=['variable', 'value', 'block_group'])
            writer.writeheader()

            for i, row in enumerate(data, start=1):
                rec = dict(zip(headers, row))
                val = rec.get(var_name)
                if val is None or val == '':
                    continue

                writer.writerow({
                    'variable':
                    var_name,
                    'value':
                    val,
                    'block_group':
                    ''.join([
                        rec['state'], rec['county'], rec['tract'],
                        rec['block group']
                    ])
                })

    print(f'Done, see output directory "{args.outdir}".')


# --------------------------------------------------
def read_vars(args: Args) -> List[str]:
    """Read variables from input files or args"""

    var_names = []
    if args.file:
        var_names = args.file.read().splitlines()
    elif args.variable:
        var_names = [args.variable]

    return var_names


# --------------------------------------------------
if __name__ == '__main__':
    main()
