#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-01-24
Purpose: Create input for Central Scrutinizer
"""

import argparse
import csv
import os
import dateparser
import datetime
from typing import Dict, List, NamedTuple, Optional, TextIO

STATION_LOCATION = {
    'ABOVE_RUSSEL': (39.764606, -105.446683),
    'CC_MAIN_ABOVE_NFCC': (39.740397, -105.411517),
    'CONFLUENCE': (39.742069, -105.390567),
    'PUMPHOUSE': (39.812636, -105.498117),
    'RAIL_LESS': (39.792289, -105.472406),
    'RIVIERA': (39.798722, -105.483097),
    'UPPER_REFERENCE': (39.815519, -105.500403),
    'USGS_GAUGE_STATION': (39.749308, -105.399631),
}

STATION_ALIAS = {
    'RIVIERA': ['RIVERA'],
    'USGS_GAUGE_STATION': ['GUAGE'],
}


class Args(NamedTuple):
    file: List[TextIO]
    headers: Optional[TextIO]
    outfile: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Create input for Central Scrutinizer',
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
                        metavar='FILE',
                        type=argparse.FileType('w'),
                        default='scrutinizer.csv',
                        help='Output file')

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

        expected = 'header order family genus'.split()
        missing = list(filter(lambda f: f not in flds, expected))

        if missing:
            msg = f'"{fh.name}" missing fields: {", ".join(missing)}'
            raise Exception(msg)

        for rec in reader:
            hdr = rec['header']
            if hdr:
                order, family, genus = map(lambda h: rec[h].strip(),
                                           'order family genus'.split())
                if all([order, family, genus]):
                    headers[hdr.upper()] = ' '.join([order, family, genus])
                elif order:
                    headers[hdr.upper()] = order
                else:
                    headers[hdr.upper()] = hdr

    return headers


# --------------------------------------------------
def process(fh: TextIO, headers: Optional[Dict[str, str]],
            outfile: TextIO) -> int:
    """Process the file into Mongo (client)"""

    reader = csv.DictReader(fh, delimiter=',')
    flds = reader.fieldnames
    num_inserted = 0

    for i, row in enumerate(reader, start=1):
        if not row.get('STREAM'):
            continue

        for fld in flds[5:-8]:
            if fld.strip() == '':
                continue

            date = dateparser.parse(row['DATE'])
            if not date:
                continue

            variable = headers.get(fld.upper(), fld) if headers else fld

            # Handle aliases, misspelling
            # Covert spaces and dashes to underscores
            station = row['STATION'].strip().upper().replace(' ', '_')
            for name, aliases in STATION_ALIAS.items():
                if any(map(lambda s: station == s, [name] + aliases)):
                    station = name

            # Base record has station/date
            date = datetime.datetime.utcfromtimestamp(date.timestamp())

            # Remove leading "="?
            val = row[fld].strip()
            if val.startswith('='):
                val = val[1:]

            # Try to convert value to float
            try:
                val = float(val)
            except Exception:
                continue

            print(f'{i:4}: {fld} => {val}')
            outfile.write(','.join(
                map(quote, [station, 'station', fld, variable, date, val])) +
                         '\n')

    return num_inserted


# --------------------------------------------------
def quote(s):
    """ Quote a string """

    return f'"{s}"'


# --------------------------------------------------
if __name__ == '__main__':
    main()
