#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-24
Purpose: Convert EJSCREEN data to Scrutinizer format
"""

import argparse
import csv
import os
import dateparser
import datetime
import re
from pprint import pprint
from typing import Dict, List, Tuple, NamedTuple, Optional, TextIO


class Args(NamedTuple):
    file: List[TextIO]
    headers: Optional[TextIO]
    outfile: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Convert EJSCREEN data to Scrutinizer format',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        nargs='+',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        help='Input file(s)')

    parser.add_argument('-H',
                        '--headers',
                        help='Headers file',
                        metavar='FILE',
                        type=argparse.FileType('r'),
                        default=None)

    parser.add_argument('-o',
                        '--outfile',
                        help='Mongo URI',
                        metavar='FILE',
                        type=argparse.FileType('w'),
                        default='scrutinizer.csv')

    args = parser.parse_args()

    return Args(args.file, args.headers, args.outfile)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    num_inserted = 0
    headers = get_headers(args.headers)

    out_flds = ('location_name location_type variable_name '
                'variable_desc collected_on value'.split())
    args.outfile.write(','.join(map(quote, out_flds)) + '\n')

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        num_inserted += process(fh, headers, args.outfile)

    print(f'Done, inserted {num_inserted}.')


# --------------------------------------------------
def get_headers(fh: Optional[TextIO]) -> Dict[str, str]:
    """Reader headers (optional)"""

    headers = {}

    if fh:
        reader = csv.DictReader(fh, delimiter=',')
        flds = reader.fieldnames
        expected = 'FIELD_NAME,DESCRIPTION,CATEGORY'.split(',')
        missing = list(filter(lambda f: f not in flds, expected))

        if missing:
            msg = f'"{fh.name}" missing fields: {", ".join(missing)}'
            raise Exception(msg)

        for rec in reader:
            headers[rec['FIELD_NAME']] = rec['DESCRIPTION']

    return headers


# --------------------------------------------------
def quote(s):
    """ Quote a string """

    return f'"{s}"'


# --------------------------------------------------
def process(in_fh: TextIO, headers: Optional[Dict[str, str]],
            out_fh: TextIO) -> int:
    """Process the file into Mongo (client)"""

    reader = csv.DictReader(in_fh, delimiter=',')
    flds = reader.fieldnames
    num = 0

    counties = {
        '001': 'Apache',
        '003': 'Cochise',
        '011': 'Greenlee',
        '025': 'Yavapai'
    }

    for i, row in enumerate(reader, start=1):
        block_id = row['ID']
        if not block_id:
            continue

        match = re.search(r'^(\d{2})(\d{3})(\d+)$', block_id)
        if not match:
            continue

        state_code, county_code = match.group(1), match.group(2)
        if state_code != '04' or county_code not in counties:
            continue
            print("Skipping")

        print(f'state "{state_code}" county "{county_code}"')

        for fld in filter(lambda f: f != 'ID', flds):
            desc = headers.get(fld)
            if not desc:
                continue

            val = row.get(fld)
            if val == "":
                continue

            val_match = re.search(r'(\d{1,3})%ile', val)
            if val_match:
                val = val_match.group(1)

            # Try to convert value to float
            try:
                val = float(val)
            except Exception:
                pass

            collected_on = ""  # TODO: what goes here?
            print(f'{i:4}: {block_id} {fld} => {val}')
            out_fh.write(','.join(
                map(quote,
                    [block_id, 'census_block', fld, desc, collected_on, val]))
                         + '\n')
            num += 1

    return num


# --------------------------------------------------
if __name__ == '__main__':
    main()
