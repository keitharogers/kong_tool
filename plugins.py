import json
from jsonschema import validate, exceptions
from services import get_service_id_from_name
from kongrequests import make_request
from deepdiff import DeepDiff
from version import get_kong_version
from packaging import version
from pprint import pprint


def kong_version_check():
    kong_version = get_kong_version()

    # Kong 2.1.0 changes whitelisting/blacklisting
    # terms: https://github.com/Kong/kong/commit/6517f2adbafaa202a530b620e5fb04f33fbbf33e
    # So compare version to change behaviour when adding an ip restriction plugin

    version_comparison = version.parse(kong_version) < version.parse('2.1.0')

    if version_comparison:
        whitelist = "whitelist"
    else:
        whitelist = "allow"

    return whitelist


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

        iprestriction_config_key = kong_version_check()

        if iprestriction_config_key in json1_file["config"] and ip_whitelist_2 is None:
            json1_file["config"][iprestriction_config_key].extend(json2_file["config"][iprestriction_config_key])
        elif iprestriction_config_key in json1_file["config"] and ip_whitelist_3 is None:
            json1_file["config"][iprestriction_config_key].extend(json2_file["config"][iprestriction_config_key])
            json1_file["config"][iprestriction_config_key].extend(json3_file["config"][iprestriction_config_key])
        elif iprestriction_config_key in json1_file["config"] and ip_whitelist_3 is not None:
            json1_file["config"][iprestriction_config_key].extend(json2_file["config"][iprestriction_config_key])
            json1_file["config"][iprestriction_config_key].extend(json3_file["config"][iprestriction_config_key])
            json1_file["config"][iprestriction_config_key].extend(json4_file["config"][iprestriction_config_key])
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

        existing_plugin = make_request('GET', api, params=None)
        ddiff = DeepDiff(existing_plugin, payload, ignore_order=True, report_repetition=True,
                         exclude_paths=["root['id']", "root['created_at']", "root['service']", "root['route']",
                                        "root['enabled']", "root['consumer']", "root['protocols']",
                                        "root['run_on']", "root['config']['blacklist']", "root['config']['deny']"])
        if bool(ddiff) is False:
            print('No changes, nothing to do!')
            exit(0)
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

        iprestriction_config_key = kong_version_check()

        if iprestriction_config_key in json1_file["config"] and ip_whitelist_2 is None:
            json1_file["config"][iprestriction_config_key].extend(json2_file["config"][iprestriction_config_key])
        elif iprestriction_config_key in json1_file["config"] and ip_whitelist_3 is None:
            json1_file["config"][iprestriction_config_key].extend(json2_file["config"][iprestriction_config_key])
            json1_file["config"][iprestriction_config_key].extend(json3_file["config"][iprestriction_config_key])
        elif iprestriction_config_key in json1_file["config"] and ip_whitelist_3 is not None:
            json1_file["config"][iprestriction_config_key].extend(json2_file["config"][iprestriction_config_key])
            json1_file["config"][iprestriction_config_key].extend(json3_file["config"][iprestriction_config_key])
            json1_file["config"][iprestriction_config_key].extend(json4_file["config"][iprestriction_config_key])
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
                ddiff = DeepDiff(existing_whitelist, payload, ignore_order=True, report_repetition=True,
                                 exclude_paths=["root['id']", "root['created_at']", "root['service']", "root['route']",
                                                "root['enabled']", "root['consumer']", "root['protocols']",
                                                "root['run_on']", "root['config']['blacklist']",
                                                "root['config']['deny']"])
                if bool(ddiff) is False:
                    print('No changes, nothing to do!')
                    exit(0)

    amend_request = make_request('PATCH', api, payload)

    try:
        ddiff
    except NameError:
        ddiff = None

    if ddiff is not None:
        pprint(ddiff, indent=2)
    else:
        print(json.dumps(amend_request, indent=2))
        return amend_request


def delete_plugin(plugin_id):
    api = '/plugins/' + plugin_id

    payload = {}

    delete_plugin_with_id = make_request('DELETE', api, payload)

    return delete_plugin_with_id

