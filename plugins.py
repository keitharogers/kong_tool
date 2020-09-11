import json
from jsonschema import validate, exceptions
from services import get_service_id_from_name
from kongrequests import make_request
from deepdiff import DeepDiff


def get_plugins(service_name, display_output=False):
    service_id = get_service_id_from_name(service_name)

    if service_id is not None:
        api = '/services/' + service_id + '/plugins'
    else:
        print('No plugins to display...')
        exit(1)

    payload = {}

    plugins = make_request('GET', api, payload)

    if display_output:
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

        if "allow" in json1_file["config"] and ip_whitelist_2 is None:
            json1_file["config"]["allow"].extend(json2_file["config"]["allow"])
        elif "allow" in json1_file["config"] and ip_whitelist_3 is None:
            json1_file["config"]["allow"].extend(json2_file["config"]["allow"])
            json1_file["config"]["allow"].extend(json3_file["config"]["allow"])
        elif "allow" in json1_file["config"] and ip_whitelist_3 is not None:
            json1_file["config"]["allow"].extend(json2_file["config"]["allow"])
            json1_file["config"]["allow"].extend(json3_file["config"]["allow"])
            json1_file["config"]["allow"].extend(json4_file["config"]["allow"])
        else:
            print("Merging of JSON plugin files only supports the IP restriction plugin...")
            exit(1)

        payload = json1_file

        # Validate user JSON file against schema
        try:
            validate(instance=payload, schema=schema)
        except (exceptions.ValidationError, exceptions.SchemaError) as err:
            print(err)
            exit(1)

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
        try:
            validate(instance=payload, schema=schema)
        except (exceptions.ValidationError, exceptions.SchemaError) as err:
            print(err)
            exit(1)

        ddiff = None
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

        if "allow" in json1_file["config"] and ip_whitelist_2 is None:
            json1_file["config"]["allow"].extend(json2_file["config"]["allow"])
        elif "allow" in json1_file["config"] and ip_whitelist_3 is None:
            json1_file["config"]["allow"].extend(json2_file["config"]["allow"])
            json1_file["config"]["allow"].extend(json3_file["config"]["allow"])
        elif "allow" in json1_file["config"] and ip_whitelist_3 is not None:
            json1_file["config"]["allow"].extend(json2_file["config"]["allow"])
            json1_file["config"]["allow"].extend(json3_file["config"]["allow"])
            json1_file["config"]["allow"].extend(json4_file["config"]["allow"])
        else:
            print("Merging of JSON plugin files only supports the IP restriction plugin...")
            exit(1)

        payload = json1_file

        # Validate user JSON file against schema
        try:
            validate(instance=payload, schema=schema)
        except (exceptions.ValidationError, exceptions.SchemaError) as err:
            print(err)
            exit(1)

        if ip_whitelist is not None:
            existing_whitelist = make_request('GET', api, params=None)
            existing_whitelist_json = json.dumps(existing_whitelist, indent=2)
            if "ip-restriction" in existing_whitelist_json:
                ddiff = DeepDiff(existing_whitelist, payload, ignore_order=True,
                                 exclude_paths=["root['id']", "root['created_at']", "root['service']", "root['route']",
                                                "root['enabled']", "root['consumer']", "root['protocols']"])
                if bool(ddiff) is False:
                    print('No changes, nothing to do!')
                    exit(0)

    amend_request = make_request('PATCH', api, payload)

    try:
        ddiff
    except NameError:
        ddiff = None

    if ddiff is not None:
        print(ddiff)
    else:
        print(json.dumps(amend_request, indent=2))
        return amend_request


def delete_plugin(plugin_id):
    api = '/plugins/' + plugin_id

    payload = {}

    delete_plugin_with_id = make_request('DELETE', api, payload)

    return delete_plugin_with_id

