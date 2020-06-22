#!/usr/bin/python3

import requests
import configparser
import argparse
import json

config = configparser.ConfigParser()
config.read('config.ini')

API_URL = config['Kong']['API_URL']

parser = argparse.ArgumentParser()
parser.add_argument("--create-service-endpoint", nargs='+', help="Create Kong service with SERVICE_NAME HOST PORT PROTOCOL")
parser.add_argument("--get-ip-restriction", help="Get IP restriction details for given service name (if exists)")
parser.add_argument("--add-ip-restriction", nargs='+', help="Add IP restriction to service with SERVICE_NAME FILENAME")
parser.add_argument("--amend-ip-restriction", nargs='+', help="Amend IP restriction of service with SERVICE_NAME FILENAME")
args = parser.parse_args()


def create_service_endpoint(service_name, host, port, protocol):
    api = '/services'
    payload = {'name': service_name, 'host': host, 'port': port, 'protocol': protocol}

    return make_request('POST', api, payload)


def get_ip_restriction(service_name):
    api = '/services/' + service_name + '/plugins'
    payload = {}

    print('Show existing IP restrictions for service...\n')

    return make_request('GET', api, payload)


def add_ip_restriction(service_name, ip_json_filename):
    api = '/services/' + service_name + '/plugins'

    with open(ip_json_filename) as json_file:
        payload = json.load(json_file)

    return make_request('POST', api, payload)


def amend_ip_restriction(service_name, ip_json_filename):
    whitelist = json.dumps(get_ip_restriction(service_name))
    whitelist_id = json.loads(whitelist)
    id = whitelist_id['data'][0]['id']

    api = '/services/' + service_name + '/plugins/' + id
    with open(ip_json_filename) as json_file:
        payload = json.load(json_file)

    print('\nAmending IP restrictions for service...\n')

    return make_request('PATCH', api, payload)


def make_request(method, api, params):
    url = API_URL
    headers = {
        'cache-control': "no-cache"
    }

    if (method == 'POST') or (method == 'PATCH'):
        resp = requests.request(method, url + api, headers=headers, data=params)
        if resp.status_code == 409:
            print('Object already exists please amend instead')
        elif resp.status_code == 200:
            print(resp.json())
            print('\nSuccess!')
            return resp.json()
        elif resp.status_code == 201:
            print('Object created successfully')
            return resp.json()
    elif method == 'GET':
        resp = requests.request(method, url + api, headers=headers, params=params)
        if resp.status_code == 200:
            print(resp.json())
            return resp.json()


if args.create_service_endpoint:
    print(args.create_service_endpoint)
    create_service_endpoint(args.create_service_endpoint[0], args.create_service_endpoint[1],
                            args.create_service_endpoint[2], args.create_service_endpoint[3])
elif args.get_ip_restriction:
    get_ip_restriction(args.get_ip_restriction)
elif args.add_ip_restriction:
    add_ip_restriction(args.add_ip_restriction[0], args.add_ip_restriction[1])
elif args.amend_ip_restriction:
    amend_ip_restriction(args.amend_ip_restriction[0], args.amend_ip_restriction[1])
