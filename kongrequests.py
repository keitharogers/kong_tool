import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import configparser


def make_request(method, api, params):
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_url = config['Kong']['API_URL']
    api_url_verify_cert = config['Kong']['API_VERIFY_CERTIFICATE']
    url = api_url

    headers = {
        'cache-control': "no-cache"
    }

    if api_url_verify_cert == 'false':
        verify_cert = False
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    elif api_url_verify_cert == 'true':
        verify_cert = True
    else:
        print("Please set API_URL_VERIFY_CERT to 'true' or 'false' in config.ini")
        exit(1)

    if (method == 'POST') or (method == 'PATCH') or (method == 'PUT'):
        resp = requests.request(method, url + api, headers=headers, data=params, verify=verify_cert)
        if resp.status_code == 409:
            print('Object already exists please amend instead')
            exit(1)
        elif resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 201:
            return resp.json()
        else:
            print('Request failed...')
            return resp.json()
    elif method == 'GET':
        resp = requests.request(method, url + api, headers=headers, params=params, verify=verify_cert)
        if resp.status_code == 200:
            return resp.json()
    elif method == 'DELETE':
        resp = requests.request(method, url + api, headers=headers, data=params, verify=verify_cert)
        if resp.status_code == 204:
            print('Deletion successful')
        else:
            print('Deletion not successful, object has dependencies still attached. Please delete these first.')
            return resp.json()

