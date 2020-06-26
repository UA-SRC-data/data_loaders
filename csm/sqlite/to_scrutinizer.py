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
    headers: Optional[TextIO]
    outfile: TextIO
    medium: str


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

    parser.add_argument('-m',
                        '--medium',
                        metavar='medium',
                        type=str,
                        default='water',
                        help='Collection medium')

    args = parser.parse_args()

    return Args(args.file, args.headers, args.outfile, args.medium)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    # Create writer for outfile
    out_flds = [
        'location_name', 'location_type', 'variable_name', 'variable_desc',
        'collected_on', 'value', 'medium'
    ]
    writer = csv.DictWriter(args.outfile, out_flds)
    writer.writeheader()

    num_written = 0
    headers = get_headers(args.headers)
    for i, fh in enumerate(args.file, start=1):
        print(f'{i:3}: {os.path.basename(fh.name)}')
        num_written += process(fh, headers, writer, args.medium)

    print(f'Done, wrote {num_written:,}.')


# --------------------------------------------------
def get_headers(fh: Optional[TextIO]) -> Dict[str, str]:
    """Reader headers (optional)"""

    headers = {}

    if fh:
        reader = csv.DictReader(fh, delimiter=',')
        flds = reader.fieldnames
        expected = ['header', 'order', 'family', 'genus']
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
            writer: csv.DictWriter, medium: str) -> int:
    """
    Process the file into Mongo (client)

    First 5 columns are: STREAM, DATE, STATION, REP, #GRIDS
    Columns after that are the measurements
    """

    reader = csv.DictReader(fh, delimiter=',')
    flds = reader.fieldnames
    values = defaultdict(list)  # to average replicates

    # Parse file into values for each variable, station, and date
    for i, row in enumerate(reader, start=1):
        # Base record has station/date
        station = get_station(row.get('STATION', ''))
        date = get_date(row.get('DATE', ''))

        if not all([date, station]):
            continue

        for fld in filter(lambda f: f != '', flds[5:]):
            raw_val = row[fld].strip()
            if raw_val == '':
                continue

            # Remove leading "="?
            if raw_val.startswith('='):
                raw_val = raw_val[1:]

            # Try to convert value to float
            val = None
            try:
                val = float(raw_val)
            except Exception:
                continue

            if val is not None:
                values[(fld, station, date)].append(val)

    # Write the averages for each variable, station, and date
    num_written = 0
    for key, replicates in values.items():
        fld, station, date = key

        # Maybe convert "ACENTR" -> "Ephemeroptera Baetidae Acentrella spp."
        variable = headers.get(fld.upper(), fld) if headers else fld

        # Take the average of the values
        val = mean(replicates)
        print(f'{fld} {station} {date} => {val}')

        writer.writerow({
            'location_name': station,
            'location_type': 'station',
            'variable_name': fld,
            'variable_desc': variable,
            'collected_on': date,
            'value': val,
            'medium': medium
        })
        num_written += 1

    return num_written


# --------------------------------------------------
def get_station(station):
    """Normalize station name, find aliases"""

    station = normalize(station)
    alias = {
        'RIVIERA': ['RIVERA'],
        'USGS_GAUGE_STATION': ['GUAGE'],
    }

    for name, aliases in alias.items():
        if any(map(lambda s: station == s, [name] + aliases)):
            station = name

    return station


# --------------------------------------------------
def test_get_station() -> None:
    """Test get_station"""

    assert get_station('') == ''
    assert get_station('Above Russel') == 'ABOVE_RUSSEL'
    assert get_station('RIVERA') == 'RIVIERA'
    assert get_station('guage') == 'USGS_GAUGE_STATION'


# --------------------------------------------------
def normalize(text: str) -> str:
    """Remove whitespace, uppercase, convert spaces to underscores"""

    return text.strip().upper().replace(' ', '_')


# --------------------------------------------------
def test_normalize() -> None:
    """Test normalize"""

    assert normalize('') == ''
    assert normalize('foo') == 'FOO'
    assert normalize('foo BAR ') == 'FOO_BAR'
    assert normalize('foo Bar BAZ') == 'FOO_BAR_BAZ'


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
