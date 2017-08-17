import json
import pprint


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


def generate_tasks():
    tasks_file = "C:\Users\shika\Downloads\default.json"
    with open(tasks_file) as fp:
        default_tasks = json.load(fp)
    skip_keys = ['primary', 'ceph', 'nova', 'rabbitmq', 'firewall', 'vmware', 'virtual_ips',
                 'db', 'cirros', 'ironic', 'apache', 'cinder', 'heat', 'keystone', 'network']

    need_tasks = ['ceph-mon', 'openstack-haproxy-nova', 'openstack-haproxy-cinder',
                  'openstack-haproxy-keystone']

    # print_key_tasks(default_tasks, 'keystone')
    over_skip_tasks(default_tasks, skip_keys, need_tasks)


def main():
    generate_tasks()


if __name__ == '__main__':
    main()
