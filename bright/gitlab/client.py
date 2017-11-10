import requests
import pprint

GIT_LAB_HOST = '10.0.44.51'
headers = """Host: 10.0.44.51
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://10.0.44.51/projects/new?namespace_id=5
Cookie: _gitlab_session=e657f192755271fe7846a40e967854bf
Connection: keep-alive
Upgrade-Insecure-Requests: 1 """

headers = """Host: 10.0.44.51
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://10.0.44.51/projects/new?namespace_id=4
Content-Type: application/x-www-form-urlencoded
Content-Length: 301
Cookie: _gitlab_session=ed07f66ac8d69a73b7e7a6b12cc2a22a
Connection: keep-alive
Upgrade-Insecure-Requests: 1"""
headers = headers.splitlines()
headers = {header.split(':', 1)[0].strip(): header.split(':', 1)[1].strip() for header in headers}
pprint.pprint(headers)

session = requests.Session()
session.headers.update(**headers)
# rq = requests.get('https://10.0.44.51', headers=headers, verify=False)


projects = ['python-cinderclient', 'python-openstackclient', 'python-designateclient', 'python-oslo-messaging',
            'python-designateclient', 'python-oslo-messaging', 'python-glanceclient', 'python-troveclient',
            'ustack_www', 'cinder', 'gringotts', 'lotus', 'placebo_extras', 'python-keystoneclient', 'shire',
            'vm_manager', 'crystal', 'manila', 'ppp', 'python-manilaclient', 'ssdb', 'zabbix', 'designate', 'inkfish',
            'neutron', 'python-amqp', 'python-neutronclient', 'tars', 'dispatcher', 'keystone', 'nova',
            'python-ceilometerclient', 'python-novaclient', 'ticket']

projects = ['dispatcher', 'leopard', 'marmot', 'rate_limit', 'sinnet_www', 'trochilus', 'crystal', 'doctor',
            'lotus', 'marmot_extras', 'novnc', 'script', 'sloth', 'vm_manager', 'designate', 'hedwig', 'manila',
            'millet', 'ppp', 'shire']


def create_gitlab_project(project):
    data = 'utf8=%E2%9C%93&authenticity_token=0YEq02CRxu%2BPFZwduIQjeVdxGCyk2bvvkJ3JIfI0jEDuygHhubn%2Fs%2FDsflNspe4xdXmTW1pHmy9d4xfzxP%2FskA%3D%3D&project%5Btemplate_name%5D=&project%5Bimport_url%5D=&project%5Bnamespace_id%5D=5&project%5Bpath%5D={project}&project%5Bdescription%5D=&project%5Bvisibility_level%5D=0'
    data = 'utf8=%E2%9C%93&authenticity_token=a%2BduJiVm6M%2BS9MvLijebEOpZN%2FW%2F%2BTnLK9vOJ9DVIFbUHvjwSTAmqFCHBCkxRJlxNKo97XY%2BrkKSHiPzZAGDGA%3D%3D&project%5Btemplate_name%5D=&project%5Bimport_url%5D=&project%5Bnamespace_id%5D=4&project%5Bpath%5D={project}&project%5Bdescription%5D=&project%5Bvisibility_level%5D=0'
    rq = requests.post('https://{host}/projects'.format(host=GIT_LAB_HOST), headers=headers,
                       data=data.format(project=project), verify=False)
    print rq


def creat_gitlab_projects():
    for project in projects:
        create_gitlab_project(project)


def main():
    creat_gitlab_projects()


if __name__ == "__main__":
    main()
