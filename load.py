#!/usr/bin/env python
'''
TODO

* Related items
* US dataset
'''
import optparse
import csv
import urllib
import json

import ckanapi

demodata = json.load(open('data.json'))


def create_demo_data(client):
    for name, dataset in demodata['datasets'].items():
        create_dataset(client, dataset)
    for name, group in demodata['groups'].items():
        print 'Creating group: %s' % name
        try:
            client.action.group_create(**group)
        except Exception as e:
            print "Error creating group `{0}`: {1}".format(name, unicode(e))



def create_dataset(client, dataset):
    print 'Uploading dataset: %s' % dataset['name']
    try:
        client.action.package_create(**dataset)
    except Exception as e:
        print "Error uploading dataset `{0}`: {1}".format(dataset['name'], unicode(e))
    #TODO: Upload resources directly


def main():
    parser = optparse.OptionParser()
    parser.add_option("-b", "--base", default="http://localhost:5000",
            help="Base URL for CKAN API to post to [default: '%default']")
    parser.add_option("-a", "--apikey", default="tester",
            help="API key to post with [default: '%default']")
    options, args = parser.parse_args()
    client = ckanapi.RemoteCKAN(options.base, apikey=options.apikey,
            user_agent='ckanapi/ckandemodata')
    create_demo_data(client)


if __name__ == '__main__':
    main()
