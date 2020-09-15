import json
from jsonschema import validate, exceptions
from deepdiff import DeepDiff
from pprint import pprint
from kongrequests import make_request
from services import get_service_id_from_name


def get_route_id_from_name(route_name):
    api = '/routes'
    payload = {}

    get_route_id = make_request('GET', api, payload)

    for data in get_route_id['data']:
        if data['name'] == route_name:
            route_id = data['id']
            return route_id


def create_route_on_service(service_name, route_json_filename):
    if get_service_id_from_name(service_name) is not None:
        service_id = get_service_id_from_name(service_name)
        api = '/services/' + service_id + '/routes'
    else:
        print("Service doesn't exist, please check name...")
        exit(1)

    # Open JSON schema for route
    with open('json_schema/route-schema.json') as route_schema:
        schema = json.load(route_schema)

    # Open JSON file for new or existing route as defined by user
    with open(route_json_filename) as json_file:
        payload = json.load(json_file)

    # Validate user JSON file against schema
    try:
        validate(instance=payload, schema=schema)
    except (exceptions.ValidationError, exceptions.SchemaError) as err:
        print(err)
        exit(1)

    create_route = make_request('POST', api, payload)

    print(json.dumps(create_route, indent=2))

    return create_route


def amend_route(route_name, route_json_filename):
    if get_route_id_from_name(route_name) is not None:
        route_id = get_route_id_from_name(route_name)
        api = '/routes/' + route_id
    else:
        print("Route doesn't exist, please check name...")
        exit(1)

    # Open JSON schema for route
    with open('json_schema/route-schema.json') as route_schema:
        schema = json.load(route_schema)

    # Open JSON file for new or existing route as defined by user
    with open(route_json_filename) as json_file:
        payload = json.load(json_file)

    # Validate user JSON file against schema
    try:
        validate(instance=payload, schema=schema)
    except (exceptions.ValidationError, exceptions.SchemaError) as err:
        print(err)
        exit(1)

    # Get route by ID and diff existing route and proposed route
    existing_route = get_route_by_id(route_id)
    ddiff = DeepDiff(existing_route, payload, ignore_order=True,
                     exclude_paths=["root['id']", "root['created_at']", "root['updated_at']", "root['service']"])
    if bool(ddiff) is False:
        print('No changes, nothing to do!')
        exit(0)

    create_route = make_request('PATCH', api, payload)

    try:
        ddiff
    except NameError:
        ddiff = None

    if ddiff is not None:
        pprint(ddiff, indent=2)
    else:
        print(json.dumps(create_route, indent=2))
        return create_route


def get_routes_on_service(service_name):
    payload = {}

    service_id = get_service_id_from_name(service_name)

    api = '/services/' + service_id + '/routes'

    service_routes = make_request('GET', api, payload)

    print(json.dumps(service_routes, indent=2))

    return service_routes


def get_route_by_id(route_id):
    api = '/routes/'
    payload = {}

    get_route = make_request('GET', api + route_id, payload)

    return get_route


def delete_route_by_id(route_id):
    api = '/routes/'
    payload = {}

    delete_route = make_request('DELETE', api + route_id, payload)

    return delete_route
