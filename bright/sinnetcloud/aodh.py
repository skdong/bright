from urlparse import urljoin
from pprint import pprint

from oslo_serialization import jsonutils

from bright.sinnetcloud.base import get_auth_session
from bright.sinnetcloud.base import HOST

session = get_auth_session()

PORT = 8042
PATH = 'ocean/alarms'

BASE_URL = 'http://{host}:{port}'.format(host=HOST, port=PORT)
ALARM_URL = urljoin(BASE_URL, PATH)


def create_alarms():
    data = {"name": "test2", "description": " ", "type": "gnocchi_resources_threshold",
            "gnocchi_resources_threshold_rule":
                {"comparison_operator": "gt",
                 "granularity": 300,
                 "aggregation_method": "mean",
                 "evaluation_periods": 1,
                 "metric": "cpu_util",
                 "resource_id": "f6ffcbb1-9ba8-433e-b839-2fcba2c69a26",
                 "resource_type": "instance",
                 "threshold": 5},
            "alarm_actions": ["http://lotus/3a324482-da90-43ef-97bd-ecf8f6bfecc2"],
            "ok_actions": [], "insufficient_data_actions": []}
    try:
        print session.post(ALARM_URL, data=jsonutils.dumps(data)).json()
    except Exception as e:
        print e.message


def get_alarms():
    pprint( session.get(ALARM_URL).json())




def main():
    get_alarms()


if __name__ == '__main__':
    main()
