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

import ckanclient


demodata = json.load(open('data.json'))


def create_demo_data(client):
    for name, dataset in demodata['datasets'].items():
        create_dataset(client, dataset)
    for name, group in demodata['groups'].items():
        print 'Creating group: %s' % name
        try:
            client.group_register_post(group)
        except ckanclient.CkanApiError:
            client.group_entity_put(group)


def create_dataset(client, dataset):
    print 'Uploading dataset: %s' % dataset['name']
    try:
        client.package_register_post(dataset)
    except ckanclient.CkanApiError:
        client.package_entity_put(dataset)
    for resource in dataset['resources']:
        # lookupname = '%s::%s' % (dataset['name'], resource['description'])
        lookupname = resource['url']
        if lookupname in demodata['schemas']:
            print 'Updating datastore for %s' % lookupname
            fields = demodata['schemas'][lookupname]
            fmt = resource['format']
            if fmt.lower() == 'csv':
                data = [row for row in
                        csv.DictReader(urllib.urlopen(resource['url']))
                        ]
            elif fmt == 'json':
                data = urllib.urlopen(resource['url']).read()
            else:
                print 'Cannot upload data from resource with format: %s' % resource['format']
                continue
            try:
                client.action('datastore_create',
                    resource_id=resource['id'],
                    fields=fields,
                    records=data
                )
            except:
                print client.last_message


def main():
    parser = optparse.OptionParser()
    parser.add_option("-b", "--base", default="http://localhost:5000/api",
            help="Base URL for CKAN API to post to [default: '%default']")
    parser.add_option("-a", "--apikey", default="tester",
            help="API key to post with [default: '%default']")
    options, args = parser.parse_args()
    client = ckanclient.CkanClient(options.base, options.apikey)
    create_demo_data(client)


if __name__ == '__main__':
    main()
