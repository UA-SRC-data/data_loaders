#!/usr/bin/env python3

import dateparser
import datetime
from pprint import pprint
from pymongo import MongoClient

def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['uasrc']
    coll = db['csm']

    #print(sorted(coll.distinct('measurement')))

    qry = {}
    qry['measurement'] = 'Ephemeroptera Baetidae Acentrella'

    start = convert_date('2011-01-01')
    end = convert_date('2011-12-31')

    qry['collection_date'] = {'$gte': start , '$lte': end}

    print(f'qry = "{qry}"')
    pprint(list(coll.find(qry)))


def convert_date(date):
    """Convert a date"""

    if date:
        dt = dateparser.parse(date)
        if dt:
            return datetime.datetime.utcfromtimestamp(dt.timestamp())

main()
