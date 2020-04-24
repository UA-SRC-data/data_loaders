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

    args = parser.parse_args()

    return Args(args.mongo_uri, args.db, args.collection)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()
    client = MongoClient(args.mongo_uri)
    db = client[args.mongo_db]
    coll = db[args.mongo_collection]

    for i, m in enumerate(Measurement, start=1):
        print(f'{i:6}: {m.variable.variable} {m.value}')
        qry = {'variable': m.variable.variable,
               'location_name': m.location.location_name,
               'location_type': m.location.location_type.location_type}

        exists = coll.find_one(qry)

        value = m.value
        try:
            value = float(value)
        except Exception:
            pass

        # If we need to insert, add the value, maybe float or str
        if exists:
            coll.update_one(
                qry, {
                    "$set": {
                        'value': value,
                        'collected_on': m.collected_on,
                        'medium': m.medium.medium
                    }
                })
        else:
            qry['value'] = value
            qry['collected_on'] = m.collected_on
            qry['medium'] = m.medium.medium
            coll.insert_one(qry)

    # cursor = database.cursor()
    # sql = """
    #     select v.variable,
    #            l.location_name,
    #            lt.location_type,
    #            m.collected_on,
    #            m.value
    #     from   variable v, location l, location_type lt, measurement m
    #     where  m.variable_id=v.variable_id
    #     and    m.location_id=l.location_id
    #     and    l.location_type_id=lt.location_type_id
    # """

    # cursor.execute(sql)
    # for rec in cursor.fetchall():
    #     print(rec)
    #     break

    # coll.create_index([("location", GEO2D)])

    # Look for the base record w/o the value

# --------------------------------------------------
if __name__ == '__main__':
    main()
