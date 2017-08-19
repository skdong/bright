import requests

SESSION = None

url = 'http://identity.api.ghyun.com.cn/v3/auth/tokens'
data = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": "admin",
                    "domain": {
                        "name": "Default"
                    },
                    "password": "6bc37d3718363bee03ef"
                }
            }
        }
    }
}
headers = {'Content-Type': 'application/json'}


def get_auth_session():
    global SESSION
    if not SESSION:
        SESSION = requests.Session()
        rq = SESSION.post(url, data=json.dumps(data), headers=headers)
        headers['X-Auth-Token'] = rq.headers['X-Subject-Token']
        # headers = {'X-Auth-Token': 'dd1695d652104a5abc7cc2b124be16c2', 'Content-Type': 'application/json',}

        SESSION.headers.update(**headers)
    return SESSION
