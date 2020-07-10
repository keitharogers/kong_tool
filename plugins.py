import json
from jsonschema import validate
from services import get_service_id_from_name
from kongrequests import make_request


def get_plugins(service_name):
    service_id = get_service_id_from_name(service_name)

    if service_id is not None:
        api = '/services/' + service_id + '/plugins'
    else:
        print('No plugins to display...')
        exit(1)

    payload = {}

    plugins = make_request('GET', api, payload)

    print("\nDisplaying plugin(s) for service...\n")
    print(json.dumps(plugins, indent=2))

    return json.dumps(plugins)


def add_plugins(service_name, plugin_json_filename, ip_whitelist=None):
    service_id = get_service_id_from_name(service_name)

    if service_id is not None:
        api = '/services/' + service_id + '/plugins'
    else:
        print('Service not found...')
        exit(1)

    if ip_whitelist is None:
        # Open JSON schema for service endpoint
        with open('json_schema/plugin-schema.json') as plugin_schema:
            schema = json.load(plugin_schema)

        # Open JSON file for new or existing service endpoint as defined by user
        with open(plugin_json_filename) as json_file:
            payload = json.load(json_file)

        # Validate user JSON file against schema
        validate(instance=payload, schema=schema)
    else:
        with open('json_schema/plugin-schema.json') as plugin_schema:
            schema = json.load(plugin_schema)

        with open(plugin_json_filename) as json_file1:
            json1_file = json.load(json_file1)

        with open(ip_whitelist) as json_file2:
            json2_file = json.load(json_file2)

        if "config.whitelist" in json1_file:
            json1_file["config.whitelist"].extend(json2_file["config.whitelist"])
        else:
            print("Merging of JSON plugin files only supports the IP restriction plugin...")
            exit(1)

        payload = json1_file

        # Validate user JSON file against schema
        validate(instance=payload, schema=schema)

    add_request = make_request('POST', api, payload)

    print("\nAdding plugin(s) for service...\n")
    print(json.dumps(add_request, indent=2))

    return add_request


def amend_plugin(plugin_id, plugin_json_filename, ip_whitelist=None):
    api = '/plugins/' + plugin_id

    if ip_whitelist is None:
        # Open JSON schema for service endpoint
        with open('json_schema/plugin-schema.json') as plugin_schema:
            schema = json.load(plugin_schema)

        # Open JSON file for new or existing service endpoint as defined by user
        with open(plugin_json_filename) as json_file:
            payload = json.load(json_file)

        # Validate user JSON file against schema
        validate(instance=payload, schema=schema)
    else:
        with open('json_schema/plugin-schema.json') as plugin_schema:
            schema = json.load(plugin_schema)

        with open(plugin_json_filename) as json_file1:
            json1_file = json.load(json_file1)

        with open(ip_whitelist) as json_file2:
            json2_file = json.load(json_file2)

        if "config.whitelist" in json1_file:
            json1_file["config.whitelist"].extend(json2_file["config.whitelist"])
        else:
            print("Merging of JSON plugin files only supports the IP restriction plugin...")
            exit(1)

        payload = json1_file

        # Validate user JSON file against schema
        validate(instance=payload, schema=schema)

    amend_request = make_request('PATCH', api, payload)

    print("\nAmending plugin(s)...\n")
    print(json.dumps(amend_request, indent=2))

    return amend_request


def delete_plugin(plugin_id):
    api = '/plugins/' + plugin_id

    payload = {}

    delete_plugin_with_id = make_request('DELETE', api, payload)

    print(json.dumps(delete_plugin_with_id, indent=2))

    return delete_plugin

