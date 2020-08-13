#!/usr/bin/python3
import json
import sys


def route_transform(input_filename, output_filename):
    with open(input_filename, 'r') as data_file:
        data = json.load(data_file)

    print('\nJSON as presented by API before transformation...\n')
    print(json.dumps(data['data'][0], indent=4, sort_keys=True))

    if 'created_at' in data['data'][0]:
        del data['data'][0]['created_at']

    if 'id' in data['data'][0]:
        del data['data'][0]['id']

    if 'service' in data['data'][0]:
        del data['data'][0]['service']

    if 'updated_at' in data['data'][0]:
        del data['data'][0]['updated_at']

    print('\nJSON after transformation...\n')
    print(json.dumps(data['data'][0], indent=4, sort_keys=True))

    with open(output_filename, 'w') as output_file:
        json.dump(data['data'][0], output_file, indent=4, sort_keys=True)


def service_transform(input_filename, output_filename):
    with open(input_filename, 'r') as data_file:
        data = json.load(data_file)

    print('\nJSON as presented by API before transformation...\n')
    print(json.dumps(data, indent=4, sort_keys=True))

    if 'created_at' in data:
        del data['created_at']

    if 'id' in data:
        del data['id']

    if 'updated_at' in data:
        del data['updated_at']

    print('\nJSON after transformation...\n')
    print(json.dumps(data, indent=4, sort_keys=True))

    with open(output_filename, 'w') as output_file:
        json.dump(data, output_file, indent=4, sort_keys=True)


def plugin_transform(input_filename, output_filename):
    with open(input_filename, 'r') as data_file:
        data = json.load(data_file)

    print('\nJSON as presented by API before transformation...\n')
    print(json.dumps(data['data'], indent=4, sort_keys=True))

    for d in data["data"]:
        if 'id' in d:
            del d["id"]
        if 'updated_at' in d:
            del d["updated_at"]
        if 'created_at' in d:
            del d["created_at"]
        if 'service' in d:
            del d["service"]

    print('\nJSON after transformation...\n')
    print(json.dumps(data["data"], indent=4, sort_keys=True))

    for plugin in data["data"]:
        if 'name' in plugin:
            plugin_output_filename = plugin["name"] + '_' + output_filename
            with open(plugin_output_filename, 'w') as output_file:
                json.dump(plugin, output_file, indent=4, sort_keys=True)


if len(sys.argv) > 2:
    if sys.argv[1] == "--route-transform":
        route_transform(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "--service-transform":
        service_transform(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "--plugin-transform":
        plugin_transform(sys.argv[2], sys.argv[3])
else:
    print("\nUsage:\n"
          "./transform.py --route-transform <input_filename> <output_filename>\n"
          "./transform.py --service-transform <input_filename> <output_filename>\n"
          "./transform.py --plugin-transform <input_filename> <output_filename>\n"
          "\nNote: In the case of 'plugin-transform' the output_filename is prepended with the name of the plugin "
          "you're transforming. If multiple plugins exist, multiple prepended files will be output.")
