# -*- coding: utf-8 -*-
from collections import defaultdict

processes_file = u'E:\work\公有云\稳定性优化\process.log'

PYTHON_PREX = '/usr/bin/python2.7'
BASH_PREX = 'bash'
NEUTRON_KEEP_ALIVE = '/usr/bin/neutron-keepalived-state-change'
DOKCER_KEY = 'extend_start'
SSH_KEY = 'ssh'
PS_KEY = 'ps'
GETTY_KEY = 'getty'
DOCKER_SERVICE = 'docker-containerd'

class Process(object):
    def __init__(self, line):
        items = line.split()
        self.user = items[0]
        self.pid = items[1]
        self.parent = items[2]
        if items[3] == PYTHON_PREX or items[3] == BASH_PREX:
            self.command = ' '.join(items[4:])
        else:
            self.command = ' '.join(items[3:])

def get_processes():
    processes = defaultdict(list)
    with open(processes_file) as fp:
        for line in fp.readlines():
            process = Process(line)
            if process.command.startswith('['):
                continue
            if (process.command.startswith('keepalived') and
                        'neutron' in process.command):
                continue
            if (process.command.startswith(NEUTRON_KEEP_ALIVE)):
                continue
            if process.user.isdigit():
                continue
            if DOKCER_KEY in process.command:
                continue
            if process.command.startswith(SSH_KEY):
                continue
            if process.command.startswith(PS_KEY):
                continue
            if GETTY_KEY in process.command:
                continue
            if process.command.startswith(DOCKER_SERVICE):
                continue
            processes[process.command].append(process)
    return processes

def show_processes():
    processes = get_processes()
    for key in processes.keys():
        print key

    print len(processes)

if __name__ == '__main__':
    show_processes()
