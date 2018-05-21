import requests
from urlparse import urljoin
from pprint import pprint

from oslo_serialization import jsonutils
from oslo_log import log


from bright.sinnetcloud.base import get_admin_auth_session
from bright.sinnetcloud.base import get_auth_session

LOG = log.getLogger(__name__)



# print auth_session.get('http://2.3.3.9:5000/v3/endpoints').json()
host = '2.3.3.9'
port = 8041

END_POINT = 'http://2.3.3.9:8041'

service_name = 'gnocchi'





def get_aggregations(session):
    path = 'v1/aggregates'
    endpoint = 'http://{host}:{port}/{path}'.format(host=host,
                                                    port=port,
                                                    path=path)
    resource = 'f6ffcbb1-9ba8-433e-b839-2fcba2c69a26'

    # data = "(metric cpu_util mean)"
    param = {"start": "2018-03-20T02:35:00"}
    data = {"operations": "(metric cpu_util mean)",
            "search": "id=f6ffcbb1-9ba8-433e-b839-2fcba2c69a26",
            "resource_type": "instance"}

    data = {
        'operations': [
            'metric',
            'cpu_util',
            'mean'
        ],
        'resource_type': 'instance',
        'search': {
            '=': {
                'id': resource
            }
        }
    }
    import pprint
    try:
        # data='{"operations": "(metric cpu_util mean)", "search": "id=f6ffcbb1-9ba8-433e-b839-2fcba2c69a26", "resource_type": "instance"}'
        import requests
        # rq = session.post(endpoint,data=jsonutils.dumps(data))
        headers = {"Content-Type": "application/json", }
        session.additional_headers.update(headers)
        rq = session.post(endpoint, data=jsonutils.dumps(data))
        pprint.pprint(rq.json())
    except Exception as e:
        print endpoint
        print e.message

def _create_resource(resource):
    session = get_admin_auth_session()
    path = 'v1/resource'

def create_resoruces(resources):
    for resource in resources:
        _create_resource(resource)




def create_metric():
    path = '/v1/metric'
    url = urljoin(END_POINT, path)
    data = {"archive_policy_name": "lancer"}
    auth_session = get_admin_auth_session()
    pprint(auth_session.post(url, data=jsonutils.dumps(data)).json())


def push_measures():
    auth_session = get_admin_auth_session()
    path = '/v1/metric/{metric}/measures'
    metric = 'e9a002ea-247d-4f47-99ec-6437bc3963a3'
    url = urljoin(END_POINT, path.format(metric=metric))
    data = [
        {
            "timestamp": "2014-10-06T14:33:57",
            "value": 43.1
        },
        {
            "timestamp": "2014-10-06T14:34:12",
            "value": 12
        },
        {
            "timestamp": "2014-10-06T14:34:20",
            "value": 2
        }
    ]
    print url
    pprint(auth_session.post(url, data=jsonutils.dumps(data)))


def show_aggregations():
    auth_session = get_auth_session()
    get_aggregations(auth_session)


# def test_get_aggrates():
#    import requests
#    headers = {"Content-Type":"application/json",
#              "X-Auth-Token":"28a18217549a481b9c621a446866677b",
#              "Accept":"application/json, */*"}
#    import pprint
#    data = requests.post("http://2.3.3.9:8041/v1/aggregates",
#                         headers=headers,
#                         data='{"operations": "(metric cpu_util mean)", "search": "id=f6ffcbb1-9ba8-433e-b839-2fcba2c69a26", "resource_type": "instance"}'
#                         ).json()
#    pprint.pprint(data)



def main():
    pass


if __name__ == '__main__':
    main()
