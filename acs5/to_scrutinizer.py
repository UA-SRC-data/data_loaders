#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-07-16
Purpose: Create Scrutinizer format
"""

import argparse
import csv
import os
import sys
import re
import unicodedata
from typing import Any, NamedTuple, TextIO, List, Dict, Callable, Iterable, Optional
from pprint import pprint


class Args(NamedTuple):
    file: List[str]  # Too many open files error!
    variables: TextIO
    outfile: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Create Scrutinizer format',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        help='A readable file',
                        metavar='FILE',
                        type=str,
                        nargs='+')

    parser.add_argument('-v',
                        '--variables',
                        help='Variable description file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='acs_variables_to_download.csv')

    parser.add_argument('-o',
                        '--outfile',
                        help='Output file',
                        metavar='FILE',
                        type=argparse.FileType('wt'),
                        default='scrutinizer.csv')

    args = parser.parse_args()

    if bad := list(filter(lambda f: not os.path.isfile(f), args.file)):
        parser.error('The following are not files:\n{}'.format("\n".join(bad)))

    return Args(args.file, args.variables, args.outfile)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()

    variables = read_variables(args.variables)

    writer = csv.DictWriter(args.outfile,
                            delimiter=',',
                            fieldnames=[
                                'location_name', 'location_type',
                                'variable_name', 'variable_desc',
                                'collected_on', 'value', 'medium'
                            ])
    writer.writeheader()

    num_written = 0
    for file_num, file in enumerate(args.file, start=1):
        print('{:3}: {}'.format(file_num, os.path.basename(file)))
        reader = csv.DictReader(open(file, 'rt'), delimiter=',')

        for line_num, row in enumerate(reader, start=1):
            if value := get_value(row.get('value')):
                if var_name := row.get('variable'):
                    if var_desc := variables.get(var_name):
                        num_written += 1
                        writer.writerow({
                            'location_name': row['block_group'],
                            'location_type': 'block_group',
                            'variable_name': var_name,
                            'variable_desc': f'{var_desc} ({var_name})',
                            'collected_on': '01-01-2018',
                            'value': value,
                            'medium': 'population',
                        })
                    else:
                        warn(
                            f'{file}/{line_num}: Unknown variable "{var_name}"'
                        )
                else:
                    warn(f'{file}/{line_num}: Missing "variable" field')

    print(f'Done, wrote {num_written:,} to "{args.outfile.name}"')


# --------------------------------------------------
def get_value(raw: Optional[str]) -> Optional[float]:
    """Try to convert a string to a float"""

    try:
        return float(raw)
    except:
        pass


# --------------------------------------------------
def test_get_value() -> None:
    """Test get_value"""

    assert get_value('') == None
    assert get_value(None) == None
    assert get_value('foo') == None
    assert get_value('0') == 0.
    assert get_value('1.23') == 1.23


# --------------------------------------------------
def warn(msg: str) -> None:
    """Print a message to STDERR"""

    print(msg, file=sys.stderr)


# --------------------------------------------------
def read_variables(fh: TextIO) -> Dict[str, str]:
    """Read variables from file"""

    reader = csv.reader(fh, delimiter=',')
    headers = filter_map(normalize, next(reader))

    assert 'variable_id' in headers
    assert 'label_in_vars_csv' in headers

    num_headers = len(headers)

    def norm(name):
        name = re.sub('^["]|["]$', '', name).strip()
        name = unicodedata.normalize("NFKD", name)
        return name.replace('!!', ' ')

    def mk_row(row):
        rec = dict(zip(headers, map(norm, row[:num_headers])))
        return (rec['variable_id'], rec['label_in_vars_csv'])

    return dict(mk_row(row) for row in reader)


# --------------------------------------------------
def normalize(name: str) -> Optional[str]:
    """Make identifiers sane"""

    name = re.sub('[\'"()]', '', name.lower().strip())
    return re.sub('[^a-z_]+', '_', name) or None


# --------------------------------------------------
def test_normalize() -> None:
    """Test normalize"""

    assert normalize('""Foo - Bar (Baz)"""') == 'foo_bar_baz'


# --------------------------------------------------
def filter_map(f: Callable, xs: Iterable[Any]) -> Iterable[Any]:
    """Remove false elements"""

    return list(filter(lambda v: v, map(f, xs)))


# --------------------------------------------------
def test_filter_map() -> None:
    """Test filter_map"""

    recip = filter_map(lambda v: 1 / v if v != 0 else None, range(-2, 3))
    assert recip == [-0.5, -1, 1, .5]

    joins = filter_map(lambda xs: ', '.join(xs)
                       if xs else '', ['', 'ab', None, 'cde'])
    assert joins == ['a, b', 'c, d, e']


# --------------------------------------------------
if __name__ == '__main__':
    main()
