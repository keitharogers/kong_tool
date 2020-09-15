from kongrequests import make_request


def get_kong_version():
    api = ''
    payload = {}
    resp = make_request('GET', api, payload)
    version = resp['version']

    return version
