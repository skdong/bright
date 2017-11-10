import requests
import pprint
import json

DATA = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "id": "8e3ba4472c434959a7619378ce657c9f",
                    "password": "sinnet6418"
                }
            }
        },
        "scope": {
            "project": {
                "id": "1a7008d45cbd45fa8454b952d0bade2b"
            }
        }
    }
}

headers = {'Content-Type': 'application/json'}
url = u'http://identity.api.ghyun.com.cn/v3/auth/tokens'

# req = requests.post(url, headers=headers, data=json.dumps(DATA))
# print req.headers

_session = requests.Session()
# rq = _session.post(url, data=json.dumps(DATA), headers=headers)
# headers['X-Auth-Token'] = rq.headers['X-Subject-Token']
headers['X-Auth-Token'] = '4af64b72d6d74d13bfa0199e0c559d1a'
_session.headers.update(**headers)

server_host = 'regionone.compute.api.ghyun.com.cn'
server_url = 'http://{host}/v2/{project_id}/servers/{server_id}/os-volume_attachments'
project_id = '1a7008d45cbd45fa8454b952d0bade2b'
server_id = '6d18f0f4-35b0-448b-bef3-632a6729cf1e'
volume_id = '233ff0e3-7d79-4ed2-99b5-1ace7febde70'

ATTACH_DATA = {
    "volumeAttachment": {
        "volumeId": volume_id,
        "device": "/dev/vdc"
    }
}
print server_url.format(host=server_host,
                        project_id=project_id,
                        server_id=server_id)
# url = 'http://console.ghyun.com.cn/os/compute/v2/1a7008d45cbd45fa8454b952d0bade2b/servers/6d18f0f4-35b0-448b-bef3-632a6729cf1e/os-volume_attachments'
url = 'http://regionone.compute.api.ghyun.com.cn/v2/1a7008d45cbd45fa8454b952d0bade2b/servers/6d18f0f4-35b0-448b-bef3-632a6729cf1e/os-volume_attachments'
req = _session.post(server_url.format(host=server_host,
                                      project_id=project_id,
                                      server_id=server_id),
                    data=json.dumps(ATTACH_DATA)
                    )

# req = _session.post(url, data=json.dumps(ATTACH_DATA))
# req = _session.get('http://regionone.compute.api.ghyun.com.cn/v2/1a7008d45cbd45fa8454b952d0bade2b/servers')
pprint.pprint(req.json())
