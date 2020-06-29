import requests
import configparser


def make_request(method, api, params):
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_url = config['Kong']['API_URL']
    url = api_url

    headers = {
        'cache-control': "no-cache"
    }

    if (method == 'POST') or (method == 'PATCH') or (method == 'PUT'):
        resp = requests.request(method, url + api, headers=headers, data=params)
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
        resp = requests.request(method, url + api, headers=headers, params=params)
        if resp.status_code == 200:
            return resp.json()
    elif method == 'DELETE':
        resp = requests.request(method, url + api, headers=headers, data=params)
        if resp.status_code == 204:
            print('Deletion successful')
