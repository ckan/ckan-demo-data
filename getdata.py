#!/usr/bin/env python
import urllib
import sys
import json

base = 'http://datahub.io/api'
demodatafile = 'data.json'
current = json.load(open(demodatafile))

datasets = [
    'adur_district_spending',
    "afghanistan-election-data",
    'afterfibre',
    "gold-prices",
    "italyregionalaccounts",
    'malawi-aid-projects',
    "newcastle-city-council-payments-over-500", 
    "us-national-foreclosure-statistics-january-2012"
    ]

def sync():
    for name in datasets:
        print 'Retrieving: %s' % name
        out = get_dataset(name)
        current['datasets'][name] = out

    outfo = open(demodatafile, 'w')
    json.dump(current, outfo, indent=2, sort_keys=True)

def get_dataset(name):
    url = base + '/rest/dataset/' + name
    fo = urllib.urlopen(url)
    parsed = json.load(fo)
    for resource in parsed['resources']:
        for key in ['webstore_url', 'webstore_last_updated',
                'resource_group_id', 'package_id', 'position',
                'tracking_summary', 'cache_url']:
            del resource[key]
    for key in ['isopen', 'groups', 'ckan_url', 'download_url',
        'notes_rendered', 'ratings_average', 'ratings_count', 'revision_id',
        'tracking_summary', 'type', 'metadata_modified', 'metadata_created',
        'id'
        ]:
        del parsed[key]
    return parsed

if __name__ == '__main__':
    sync()
