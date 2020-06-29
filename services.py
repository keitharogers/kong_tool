import json
from kongrequests import make_request


def get_service_id_from_name(service_name):
    api = '/services'
    payload = {}

    get_service_id = make_request('GET', api, payload)

    for data in get_service_id['data']:
        if data['name'] == service_name:
            service_id = data['id']
            return service_id


def create_service_endpoint(service_name, service_json_filename):
    if get_service_id_from_name(service_name) is not None:
        service_id = get_service_id_from_name(service_name)
        api = '/services/' + service_id
    else:
        api = '/services'

    with open(service_json_filename) as json_file:
        payload = json.load(json_file)

    if api == '/services':
        msg = "\nCreating service endpoint...\n"
        create_service = make_request('POST', api, payload)
    else:
        msg = "\nAmending service endpoint...\n"
        create_service = make_request('PUT', api, payload)

    print(msg)
    print(json.dumps(create_service, indent=2))

    return create_service


def get_service_endpoint(service_name):
    api = '/services/'
    payload = {}

    service_id = get_service_id_from_name(service_name)

    service_endpoint = make_request('GET', api + service_id, payload)

    print('\nRetrieving service endpoint...\n')
    print(json.dumps(service_endpoint, indent=2))

    return service_endpoint


def delete_service_by_id(service_id):
    api = '/services/'
    payload = {}

    delete_service = make_request('DELETE', api + service_id, payload)

    return delete_service
