import json
from services import get_service_id_from_name
from kongrequests import make_request


def get_ip_restriction(service_name):
    service_id = get_service_id_from_name(service_name)

    api = '/services/' + service_id + '/plugins'
    payload = {}

    ip_restriction = make_request('GET', api, payload)

    print("\nDisplaying IP restrictions for service...\n")
    print(json.dumps(ip_restriction, indent=2))

    return json.dumps(ip_restriction)


def add_ip_restriction(service_name, ip_json_filename):
    service_id = get_service_id_from_name(service_name)
    api = '/services/' + service_id + '/plugins'

    with open(ip_json_filename) as json_file:
        payload = json.load(json_file)

    add_request = make_request('POST', api, payload)

    print("\nAdding IP restrictions for service...\n")
    print(json.dumps(add_request, indent=2))

    return add_request


def amend_ip_restriction(service_name, ip_json_filename):
    service_id = get_service_id_from_name(service_name)

    whitelist = get_ip_restriction(service_name)
    whitelist_id = json.loads(whitelist)
    id = whitelist_id['data'][0]['id']

    api = '/services/' + service_id + '/plugins/' + id
    with open(ip_json_filename) as json_file:
        payload = json.load(json_file)

    amend_request = make_request('PATCH', api, payload)

    print("\nAmending IP restrictions for service...\n")
    print(json.dumps(amend_request, indent=2))

    return amend_request


