#!/usr/bin/python3

import argparse

from plugins import get_plugins, add_plugins, amend_plugin
from services import create_service_endpoint, get_service_endpoint, get_all_service_endpoints, delete_service_by_id
from routes import create_route_on_service, amend_route, get_routes_on_service, delete_route_by_id


parser = argparse.ArgumentParser()
parser.add_argument("--create-service-endpoint", nargs='+',
                    help="--create-service-endpoint SERVICE_NAME JSON_FILENAME (creates or amends)")
parser.add_argument("--get-service-endpoint", nargs='+',
                    help="--get-service-endpoint SERVICE_NAME")
parser.add_argument("--get-all-service-endpoints", action='store_true',
                    help="--get-all-service-endpoints")
parser.add_argument("--delete-service", nargs='+',
                    help="--delete-service SERVICE_ID")
parser.add_argument("--add-route-to-service", nargs='+',
                    help="--add-route-to-service SERVICE_NAME JSON_FILENAME")
parser.add_argument("--amend-route-on-service", nargs='+',
                    help="--amend-route-on-service ROUTE_NAME JSON_FILENAME")
parser.add_argument("--get-routes-on-service", nargs='+',
                    help="--get-routes-on-service SERVICE_NAME")
parser.add_argument("--delete-route", nargs='+',
                    help="--delete-route ROUTE_ID")
parser.add_argument("--get-plugins",
                    help="--get-plugins SERVICE_NAME")
parser.add_argument("--add-plugins", nargs='+',
                    help="--add-plugins SERVICE_NAME JSON_FILENAME")
parser.add_argument("--amend-plugin", nargs='+',
                    help="--amend-plugin PLUGIN_ID JSON_FILENAME")
args = parser.parse_args()


if args.create_service_endpoint:
    create_service_endpoint(args.create_service_endpoint[0], args.create_service_endpoint[1])
elif args.get_service_endpoint:
    get_service_endpoint(args.get_service_endpoint[0])
elif args.get_plugins:
    get_plugins(args.get_plugins)
elif args.add_plugins:
    add_plugins(args.add_plugins[0], args.add_plugins[1])
elif args.amend_plugin:
    amend_plugin(args.amend_plugin[0], args.amend_plugin[1])
elif args.add_route_to_service:
    create_route_on_service(args.add_route_to_service[0], args.add_route_to_service[1])
elif args.amend_route_on_service:
    amend_route(args.amend_route_on_service[0], args.amend_route_on_service[1])
elif args.get_routes_on_service:
    get_routes_on_service(args.get_routes_on_service[0])
elif args.delete_route:
    delete_route_by_id(args.delete_route[0])
elif args.delete_service:
    delete_service_by_id(args.delete_service[0])
elif args.get_all_service_endpoints:
    get_all_service_endpoints()
