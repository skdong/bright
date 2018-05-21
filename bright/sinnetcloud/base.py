from keystoneauth1 import session
from keystoneauth1 import loading

HOST = '2.3.3.9'

auth_info = dict(
    username='bright',
    password='abc123',
    project_name='bright_project',
    project_domain_name='60f10361382d4d77851f26a63bb9763a',
    user_domain_name='60f10361382d4d77851f26a63bb9763a',
    auth_url='http://2.3.3.9:5000/v3'

)

admin_auth_info = dict(
    username='admin',
    password='admin',
    project_name='admin',
    project_domain_name='Default',
    user_domain_name='Default',
    auth_url='http://2.3.3.9:5000/v3'

)

SESSION = None
ADMIN_SESSION = None
def get_auth_session():
    global SESSION
    if not SESSION:
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(**auth_info)
        SESSION = session.Session(auth=auth)
        headers = {"Content-Type": "application/json", }
        SESSION.additional_headers.update(headers)
    return SESSION


def get_admin_auth_session():
    global ADMIN_SESSION
    if not ADMIN_SESSION:
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(**admin_auth_info)
        ADMIN_SESSION = session.Session(auth=auth)
        headers = {"Content-Type": "application/json", }
        ADMIN_SESSION.additional_headers.update(headers)
    return ADMIN_SESSION