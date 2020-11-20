#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-11-20
Purpose: Create input for Central Scrutinizer
"""

import argparse
import csv
import os
import dateparser
import datetime
import re
from collections import defaultdict
from typing import Dict, List, NamedTuple, Optional, TextIO
from numpy import mean

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


class Args(NamedTuple):
    file: List[TextIO]
    outfile: TextIO
    source: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Create input for Central Scrutinizer',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        nargs='+',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Input file(s)')

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='scrutinizer.csv',
                        help='Output file')

    parser.add_argument('-s',
                        '--source',
                        metavar='source',
                        type=str,
                        default='CO School of Mines',
                        help='Data source')

    args = parser.parse_args()

    return Args(file=args.file, outfile=args.outfile, source=args.source)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    # Create writer for outfile
    out_flds = [
        'source', 'unit', 'location_name', 'location_type', 'variable_name',
        'variable_desc', 'collected_on', 'value', 'medium'
    ]
    writer = csv.DictWriter(args.outfile, out_flds)
    writer.writeheader()

    dispatch = {
        'field_data': process_field_data,
        'icp_aes': process_icp_aes,
        'doc_toc': process_doc_toc,
        'ic': process_ic,
    }

    num_written = 0
    for i, fh in enumerate(args.file, start=1):
        basename = os.path.splitext(os.path.basename(fh.name))[0]
        if match := re.match('(\d{4})(\d{2})(\d{2})_(.+)', basename):
            year, month, day, data_type = match.groups()
            collected_on = '-'.join([year, month, day])
            print(f'{i:3}: {basename} -> {data_type}')
            if f := dispatch.get(data_type):
                num_written += f(fh, collected_on, writer, args)
            else:
                print(f'No dispatch for data type "{data_type}"')
        else:
            print(f'Unexpected file name "{basename}"')

    print(f'Done, wrote {num_written:,}.')


# --------------------------------------------------
def process_field_data(fh: TextIO, collected_on: str, writer: csv.DictWriter,
                       args: Args) -> int:
    """ Process the file into CSV """

    reader = csv.DictReader(fh, delimiter=',')
    flds = reader.fieldnames
    stations = 'ant arg railless rap rbp ref1 ref2 tp usgs'.split()
    num_written = 0

    # Parse file into values for each variable, station, and date
    for i, row in enumerate(reader, start=1):
        if 'measurement' not in row:
            continue

        variable = normalize(row.get('measurement'))
        unit = row.get('uom', '')

        if unit.lower() == 'kathy':
            unit = ''

        for station in stations:
            if station in row:
                writer.writerow({
                    'source': 'csm_field_data',
                    'unit': unit,
                    'location_name': station,
                    'location_type': 'station',
                    'variable_name': variable,
                    'variable_desc': variable,
                    'collected_on': collected_on,
                    'value': row.get(station),
                    'medium': 'water',
                })
                num_written += 1

    return num_written


# --------------------------------------------------
def process_icp_aes(fh: TextIO, collected_on: str, writer: csv.DictWriter,
                    args: Args) -> int:
    """ Process the file into CSV """

    reader = csv.DictReader(fh, delimiter=',')
    flds = reader.fieldnames
    num_written = 0

    # Parse file into values for each variable, station, and date
    for i, row in enumerate(reader, start=1):
        if 'measurement' not in row:
            continue

        variable = normalize(row.get('measurement'))
        unit = row.get('dl_mg_l', '')

        for fld in flds:
            if fld in ('measurement', 'dl_mg_l'):
                continue

            writer.writerow({
                'source': 'csm_icp_aes',
                'unit': unit,
                'location_name': fld,
                'location_type': 'station',
                'variable_name': variable,
                'variable_desc': variable,
                'collected_on': collected_on,
                'value': row.get(fld),
                'medium': 'water',
            })
            num_written += 1

    return num_written


# --------------------------------------------------
def process_doc_toc(fh: TextIO, collected_on: str, writer: csv.DictWriter,
                    args: Args) -> int:
    """ Process the file into CSV """

    reader = csv.DictReader(fh, delimiter=',')
    flds = reader.fieldnames
    num_written = 0

    # Parse file into values for each variable, station, and date
    for i, row in enumerate(reader, start=1):
        if 'measurement' not in row:
            continue

        variable = normalize(row.get('measurement'))
        unit = ''

        if variable == 'npoc_(ppm)':
            variable = 'npoc'
            unit = 'ppm'

        for fld in flds:
            if fld == 'measurement':
                continue

            writer.writerow({
                'source': 'csm_doc_toc',
                'unit': unit,
                'location_name': fld,
                'location_type': 'station',
                'variable_name': variable,
                'variable_desc': variable,
                'collected_on': collected_on,
                'value': row.get(fld),
                'medium': 'water',
            })
            num_written += 1

    return num_written


# --------------------------------------------------
def process_ic(fh: TextIO, collected_on: str, writer: csv.DictWriter,
               args: Args) -> int:
    """ Process the file into CSV """

    reader = csv.DictReader(fh, delimiter=',')
    flds = reader.fieldnames
    num_written = 0

    # Parse file into values for each variable, station, and date
    for i, row in enumerate(reader, start=1):
        if 'measurement' not in row:
            continue

        variable = normalize(row.get('measurement'))
        unit = ''

        for fld in flds:
            if fld == 'measurement':
                continue

            writer.writerow({
                'source': 'csm_ic',
                'unit': unit,
                'location_name': fld,
                'location_type': 'station',
                'variable_name': variable,
                'variable_desc': variable,
                'collected_on': collected_on,
                'value': row.get(fld),
                'medium': 'water',
            })
            num_written += 1

    return num_written


# --------------------------------------------------
def normalize(text: str) -> str:
    """Remove whitespace, lowercase, convert spaces to underscores"""

    return text.strip().lower().replace(' ', '_')


# --------------------------------------------------
def test_normalize() -> None:
    """Test normalize"""

    assert normalize('') == ''
    assert normalize('foo') == 'foo'
    assert normalize('foo BAR ') == 'foo_bar'
    assert normalize('foo Bar BAZ') == 'foo_bar_baz'


# --------------------------------------------------
def get_date(raw_date: str) -> Optional[str]:
    """Convert date"""

    date = None
    if raw_date:
        dp = dateparser.parse(raw_date)
        date = str(datetime.datetime.utcfromtimestamp(dp.timestamp()))

    return date


# --------------------------------------------------
if __name__ == '__main__':
    main()
