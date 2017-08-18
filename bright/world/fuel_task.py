import json
import pprint

from workflow import workflow
from workflow import fix_workflow

tasks_file = "C:\Users\cgj\Downloads\default-release.json"

skip_keys = ['primary', 'ceph', 'nova', 'rabbitmq', 'firewall', 'vmware', 'virtual_ips',
             'db', 'cirros', 'ironic', 'apache', 'cinder', 'heat', 'keystone', 'network']

need_tasks = ['ceph-mon', 'openstack-haproxy-nova', 'openstack-haproxy-cinder',
              'openstack-haproxy-keystone']


def cehck_skip(task, skip_keys, need_tasks=[]):
    if task not in need_tasks:
        for skip in skip_keys:
            if skip in task:
                return None
    return task


def print_key_tasks(tasks, key):
    for task in tasks:
        if key in task['id']:
            print task['id']


def over_skip_tasks(default_tasks, skip_keys, need_tasks):
    tasks = set()
    for task in default_tasks:
        if cehck_skip(task['id'], skip_keys, need_tasks):
            tasks.add(task['id'])
    for task in tasks:
        print task
    return tasks


def show_task(default_tasks, task):
    for default_task in default_tasks:
        if default_task['id'] == task:
            pprint.pprint(default_task)


def generate_tasks():
    update_info = dict( workflow= dict(tasks_file="C:\Users\cgj\Downloads\default-release.json",

                       skip_keys=['primary', 'ceph', 'nova', 'rabbitmq', 'firewall', 'vmware', 'virtual_ips',
                                  'db', 'cirros', 'ironic', 'apache', 'cinder', 'heat', 'keystone', 'network',
                                  'api-proxy'],

                       need_tasks=['ceph-mon', 'openstack-haproxy-nova', 'openstack-haproxy-cinder',
                                   'openstack-haproxy-keystone'],),
                       target_file="C:\Users\cgj\Downloads\update_workflow.json")
    update_info['workflow']['need_tasks'] = ['health', 'database', 'cluster-vroute', 'virtual_ips',
                                             'conntrackd', 'cluster-haproxy', 'ntp-server',
                                             'dns-server']
    #update_workflow = fix_workflow.FixWorkFlow(**update_info['workflow'])
    update_workflow = workflow.WorkFlow(**update_info['workflow'])
    #update_workflow.get_task('ceilometer-controller', show=True)
    #update_workflow.gen_target_task(target_file=update_info['target_file'])
    #update_workflow.gen_target_task(target_file=update_info['target_file'])
    update_workflow.show_key_tasks('api-proxy')


def main():
    generate_tasks()


if __name__ == '__main__':
    main()
