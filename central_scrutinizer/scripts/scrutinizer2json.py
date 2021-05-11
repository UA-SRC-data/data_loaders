#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-03-09
Purpose: Scrutinizer to JSON for Mongo load
"""

import argparse
import json
import os
from scrutinizer import Measurement, Variable
from typing import NamedTuple


class Args(NamedTuple):
    outdir: str


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

    args = parser.parse_args()

    return Args(args.outdir)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    print('Exporting variables...')
    variables_file = os.path.join(args.outdir, 'variables.json')
    with open(variables_file, 'wt') as variables_fh:
        variables = [{
            'name': v.variable,
            'desc': v.description or "",
            'unit': v.unit or "",
            'source': v.source.source or "",
        } for v in Variable]

        json.dump(variables, variables_fh)

    print('Exporting measurements...')
    for i, m in enumerate(Measurement, start=1):
        # TODO use measurement_id
        outfile = os.path.join(args.outdir, f'm-{i:010d}.json')
        if os.path.isfile(outfile):
            continue

        print(f'{i:10d}\r')
        out_fh = open(outfile, 'wt')
        json.dump(
            {
                'source': m.variable.source.source,
                'unit': m.variable.unit,
                'variable_name': m.variable.variable,
                'variable_desc': m.variable.description,
                'location_name': m.location.location_name,
                'location_type': m.location.location_type.location_type,
                'value': m.value,
                'collected_on': m.collected_on,
                'medium': m.medium.medium
            }, out_fh)

    print(f'\nDone, see outdir "{args.outdir}".')


# --------------------------------------------------
if __name__ == '__main__':
    main()
