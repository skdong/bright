import requests
import json
import copy

SESSION = None

url = 'http://identity.api.ghyun.com.cn/v3/auth/tokens'
DATA = {
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
        rq = SESSION.post(url, data=json.dumps(DATA), headers=headers)
        headers['X-Auth-Token'] = rq.headers['X-Subject-Token']
        # headers = {'X-Auth-Token': 'dd1695d652104a5abc7cc2b124be16c2', 'Content-Type': 'application/json',}

        SESSION.headers.update(**headers)
    return SESSION

class Context(dict):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self[key] = Context(**value)
            else:
                self[key] = value

    def __getattr__(self, item):
        return self.get(item, None)

    def __setattr__(self, key, value):
        self[key] = value


class OceanClient(object):
    def __init__(self, url, user=None):
        self.url = url
        self.data = Context(**DATA)
        self.data.auth.identity.password.user.password = 'admin'
        self._session = None

    def get_auth_session(self):
        if not self._session:
            self._session = requests.Session()
            rq = self._session.post(self.url, data=json.dumps(self.data), headers=headers)
            headers['X-Auth-Token'] = rq.headers['X-Subject-Token']
            self._session.headers.update(**headers)
        return self._session

    @property
    def user_url(self):
        return 'http://console.dev.oceanstack.slancer.com/us/bill/v2/projects'

    def list_users(self):
        if self._session:
            if self._session.get(self.user_url).statu_code > 300:
                self._session = None


    def check_session(self):
        try:
            self.list_users()
        except Exception as e:
            self._session = None


def main():
    client = OceanClient('http://console.dev.oceanstack.slancer.com/os/identity/v3/auth/tokens')
    session = client.get_auth_session()
    rp = session.get('http://console.dev.oceanstack.slancer.com/us/bill/v2/projects')
    print rp.json()


if __name__ == "__main__":
    main()