import json
from jsonschema import validate
from kongrequests import make_request


def add_ca_certificate(ca_cert_json_filename):
    api = '/ca_certificates'

    # Open JSON schema for service endpoint
    with open('json_schema/ca-cert-schema.json') as ca_cert_schema:
        schema = json.load(ca_cert_schema)

    # Open JSON file for new or existing service endpoint as defined by user
    with open(ca_cert_json_filename) as json_file:
        payload = json.load(json_file)

    # Validate user JSON file against schema
    validate(instance=payload, schema=schema)

    create_ca_cert = make_request('POST', api, payload)

    print(json.dumps(create_ca_cert, indent=2))

    return create_ca_cert


def list_ca_certificates():
    api = '/ca_certificates'

    payload = {}

    ca_certificates = make_request('GET', api, payload)

    print(json.dumps(ca_certificates, indent=2))

    return ca_certificates


def retrieve_ca_certificate_by_id(ca_certificate_id):
    api = '/ca_certificates/'
    payload = {}

    if ca_certificate_id is None:
        print('No CA Certificate found with this ID...')
        exit(1)

    ca_certificate_id_request = make_request('GET', api + ca_certificate_id, payload)

    print(json.dumps(ca_certificate_id_request, indent=2))

    return ca_certificate_id_request
