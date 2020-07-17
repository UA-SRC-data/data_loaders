#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-03-09
Purpose: Scrutinizer to Mongo
"""

import argparse
import os
import sys
import sqlite3
from scrutinizer import database, Measurement
from pymongo import MongoClient, GEO2D
from typing import Dict, List, Tuple, NamedTuple, Optional, TextIO


class Args(NamedTuple):
    mongo_uri: str
    mongo_db: str
    mongo_collection: str
    location_type: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Scrutinizer to Mongo',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-m',
                        '--mongo_uri',
                        help='Mongo URI',
                        metavar='str',
                        type=str,
                        default='mongodb://localhost:27017/')

    parser.add_argument('-d',
                        '--db',
                        help='Mongo DB name',
                        metavar='str',
                        type=str,
                        default='uasrc')

    parser.add_argument('-c',
                        '--collection',
                        help='Mongo collection name',
                        metavar='str',
                        type=str,
                        default='scrutinizer')

    parser.add_argument('-l',
                        '--location_type',
                        help='Restrict to location_type',
                        metavar='str',
                        type=str,
                        default='')

    args = parser.parse_args()

    return Args(args.mongo_uri, args.db, args.collection, args.location_type)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    client = MongoClient(args.mongo_uri)
    db = client[args.mongo_db]
    coll = db[args.mongo_collection]
    variables = set()

    for i, m in enumerate(Measurement, start=1):
        if args.location_type:
            if m.location.location_type.location_type != args.location_type:
                continue

        print(f'{i:6}: {m.variable.variable} {m.value}')
        qry = {'variable_name': m.variable.variable,
               'location_name': m.location.location_name,
               'location_type': m.location.location_type.location_type}

        exists = coll.find_one(qry)

        value = None
        try:
            value = float(m.value)
        except Exception:
            pass

        # If we need to insert, add the value, maybe float or str
        if exists:
            coll.update_one(
                qry, {
                    "$set": {
                        'value': value,
                        'collected_on': m.collected_on,
                        'medium': m.medium.medium,
                        'variable_desc': m.variable.description
                    }
                })
        else:
            qry['value'] = value
            qry['collected_on'] = m.collected_on
            qry['medium'] = m.medium.medium
            qry['variable_desc'] = m.variable.description
            coll.insert_one(qry)

        variables.add((m.variable.variable, m.variable.description))

    var_collection = db['variables']
    for name, desc in variables:
        var = {'name': name, 'desc': desc}
        exists = var_collection.find_one(var)
        if not exists:
            var_collection.insert_one(var)


# --------------------------------------------------
if __name__ == '__main__':
    main()
