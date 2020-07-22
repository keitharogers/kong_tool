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

    print(json.dumps(plugins, indent=2))

    return json.dumps(plugins)


def add_plugins(service_name, plugin_json_filename, ip_whitelist=None, ip_whitelist_2=None, ip_whitelist_3=None):
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

        if ip_whitelist_2 is not None:
            with open(ip_whitelist_2) as json_file3:
                json3_file = json.load(json_file3)

        if ip_whitelist_3 is not None:
            with open(ip_whitelist_3) as json_file4:
                json4_file = json.load(json_file4)

        if "config.whitelist" in json1_file and ip_whitelist_2 is None:
            json1_file["config.whitelist"].extend(json2_file["config.whitelist"])
        elif "config.whitelist" in json1_file and ip_whitelist_3 is None:
            json1_file["config.whitelist"].extend(json2_file["config.whitelist"])
            json1_file["config.whitelist"].extend(json3_file["config.whitelist"])
        elif "config.whitelist" in json1_file and ip_whitelist_3 is not None:
            json1_file["config.whitelist"].extend(json2_file["config.whitelist"])
            json1_file["config.whitelist"].extend(json3_file["config.whitelist"])
            json1_file["config.whitelist"].extend(json4_file["config.whitelist"])
        else:
            print("Merging of JSON plugin files only supports the IP restriction plugin...")
            exit(1)

        payload = json1_file

        # Validate user JSON file against schema
        validate(instance=payload, schema=schema)

    add_request = make_request('POST', api, payload)

    print(json.dumps(add_request, indent=2))

    return add_request


def amend_plugin(plugin_id, plugin_json_filename, ip_whitelist=None, ip_whitelist_2=None, ip_whitelist_3=None):
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

        if ip_whitelist_2 is not None:
            with open(ip_whitelist_2) as json_file3:
                json3_file = json.load(json_file3)

        if ip_whitelist_3 is not None:
            with open(ip_whitelist_3) as json_file4:
                json4_file = json.load(json_file4)

        if "config.whitelist" in json1_file and ip_whitelist_2 is None:
            json1_file["config.whitelist"].extend(json2_file["config.whitelist"])
        elif "config.whitelist" in json1_file and ip_whitelist_3 is None:
            json1_file["config.whitelist"].extend(json2_file["config.whitelist"])
            json1_file["config.whitelist"].extend(json3_file["config.whitelist"])
        elif "config.whitelist" in json1_file and ip_whitelist_3 is not None:
            json1_file["config.whitelist"].extend(json2_file["config.whitelist"])
            json1_file["config.whitelist"].extend(json3_file["config.whitelist"])
            json1_file["config.whitelist"].extend(json4_file["config.whitelist"])
        else:
            print("Merging of JSON plugin files only supports the IP restriction plugin...")
            exit(1)

        payload = json1_file

        # Validate user JSON file against schema
        validate(instance=payload, schema=schema)

    amend_request = make_request('PATCH', api, payload)

    print(json.dumps(amend_request, indent=2))

    return amend_request


def delete_plugin(plugin_id):
    api = '/plugins/' + plugin_id

    payload = {}

    delete_plugin_with_id = make_request('DELETE', api, payload)

    return delete_plugin_with_id

