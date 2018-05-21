from urlparse import urljoin
from oslo_serialization import jsonutils
from pprint import pprint
from bright.sinnetcloud.base import get_admin_auth_session
from bright.sinnetcloud.base import HOST


PORT = 8777
END_POINT = 'http://{host}:{port}'.format(host=HOST, port=PORT)

field = ['resource_id', 'project_id', 'user_id']
def get_url(path):
    return urljoin(END_POINT, path)

def get_resources():
    path = 'v2/resources'
    session = get_admin_auth_session()
    resources = session.get(get_url(path)).json()
    pprint(resources)
    return [{"id":resource['resource_id'],
             "project_id":resource['project_id'],
             "user_id":resource['user_id']}
            for resource in resources]


#get_resources()

from oslo_utils import timeutils
print timeutils.isotime()
