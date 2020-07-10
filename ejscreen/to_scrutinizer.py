#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-24
Purpose: Convert EJSCREEN data to Scrutinizer format
"""

import argparse
import csv
import os
import re
from typing import Dict, List, NamedTuple, Optional, TextIO


class Args(NamedTuple):
    file: List[TextIO]
    headers: Optional[TextIO]
    collected_on: str
    medium: str
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
                        type=argparse.FileType('rt'),
                        help='Input file(s)')

    parser.add_argument('-H',
                        '--headers',
                        help='Headers file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        required=True)

    parser.add_argument('-c',
                        '--collected_on',
                        help='Date for "collected_on" field',
                        metavar='str',
                        type=str,
                        required=True)

    parser.add_argument('-m',
                        '--medium',
                        help='Dummy value for "medium"',
                        metavar='str',
                        type=str,
                        default='Population')

    parser.add_argument('-o',
                        '--outfile',
                        help='Output filename',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='scrutinizer.csv')

    args = parser.parse_args()

    return Args(args.file, args.headers, args.collected_on, args.medium,
                args.outfile)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    num_inserted = 0
    headers = get_headers(args.headers)
    writer = csv.DictWriter(args.outfile,
                            delimiter=',',
                            fieldnames=[
                                'location_name', 'location_type',
                                'variable_name', 'variable_desc',
                                'collected_on', 'medium', 'value'
                            ])
    writer.writeheader()

    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        num_inserted += process(fh, headers, args.collected_on, args.medium,
                                writer)

    print(f'Done, inserted {num_inserted:,}.')


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
def process(in_fh: TextIO, headers: Dict[str, str], collected_on: str,
            medium: str, writer: csv.DictWriter) -> int:
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

            print(f'{i:4}: {block_id} {fld} => {val}')
            writer.writerow({
                'location_name': block_id,
                'location_type': 'census_block',
                'variable_name': fld,
                'variable_desc': desc,
                'collected_on': collected_on,
                'medium': medium,
                'value': val
            })
            num += 1

    return num


# --------------------------------------------------
if __name__ == '__main__':
    main()
