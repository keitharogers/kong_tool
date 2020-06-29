from kongrequests import make_request


def get_kong_major_version():
    api = ''
    payload = {}
    resp = make_request('GET', api, payload)
    version = resp['version']

    major_version = version.replace(".", "")[:1]

    return int(major_version)
