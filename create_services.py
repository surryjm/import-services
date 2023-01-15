#!/usr/bin/env python3

import requests
import chardet
import argparse
import csv


def read_rows(args):
    """ Read the rows in CSV file """
    key = args.api_key
    filename = args.filename
    file_data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            service_dict = {"service": {"type": row["type"], "name": row["name"], "description": row["description"],
                                        "auto_resolve_timeout": int(row["auto_resolve_timeout"]),
                                        "escalation_policy": {"id": row["escalation_policy.id"],
                                                              "type": row["escalation_policy.type"]}}}
            file_data.append(service_dict)
    print(file_data)
    import_services(key, file_data)


def import_services(key, file_data):
    """ Import services from CSV file """
    url = 'https://api.pagerduty.com/services'
    headers = {'Accept': 'application/vnd.pagerduty+json;version=2',
               'Content-Type': 'application/json',
               'Authorization': f'Token token={key}'}
    for row in file_data:
        payload = row
        print(payload)
        response = requests.post(url, json=payload, headers=headers)
        print(f'Statuscode: {response.status_code}')
        response_dict = response.json()
        print(response_dict.keys())


def main():
    parser = argparse.ArgumentParser(description='Bulk import of services from CSV file')
    parser.add_argument('-k', '--api-key', required=True, help='Global REST API key')
    parser.add_argument('-f', '--filename', required=True, help='CSV file of services to import')
    args = parser.parse_args()
    read_rows(args)


if __name__ == '__main__':
    main()


