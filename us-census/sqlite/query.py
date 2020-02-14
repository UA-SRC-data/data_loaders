#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-02-13
Purpose: Rock the Casbah
"""

import argparse
import os
import sys
import sqlite3
from tabulate import tabulate


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d',
                        '--db',
                        help='DB name',
                        metavar='str',
                        type=str,
                        default='census.db')

    parser.add_argument('--location',
                        help='Location name',
                        metavar='str',
                        type=str,
                        default='Tucson city, Arizona')

    parser.add_argument('-l',
                        '--limit',
                        help='Limit records',
                        metavar='int',
                        type=int,
                        default=100)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    select = """
        select l.name, t.attr_type, a.value
        from   location l, attr_type t, attr a
        where  l.location_id=a.location_id
        and    a.attr_type_id=t.attr_type_id
    """

    qry_args = []
    if args.location:
        select += 'and l.name=? '
        qry_args.append(args.location)

    if args.limit:
        select += f'limit {args.limit}'

    cur.execute(select, qry_args)
    res = cur.fetchall()
    print(tabulate(res, headers=['name', 'type', 'value']))


# --------------------------------------------------
if __name__ == '__main__':
    main()
