import pprint
import json
import sys

def dump_pretty_json(data, stream):
    json.dump(data, stream, sort_keys=True, indent=4)

class WorkFlow(object):
    skippe_key = 'skipped'

    def __init__(self, tasks_file=None, skip_keys=[], need_tasks=[], skip_ids=[]):
        self.default_file = tasks_file
        self.default_tasks = None
        self.skip_keys = skip_keys
        self.need_tasks = need_tasks
        self.skip_ids = skip_ids
        self.gen_default_tasks()

    def gen_default_tasks(self):
        with open(self.default_file) as fp:
            self.default_tasks = json.load(fp)

    def cehck_skip(self, id):
        if id not in self.need_tasks:
            if id in self.skip_ids:
                self.skip_task(id)
                return None
            for skip in self.skip_keys:
                if skip in id:
                    self.skip_task(id)
                    return None
        return id

    def skip_task(self, id=None):
        if id:
            for task in self.default_tasks:
                if id == task['id']:
                    task['type'] = self.skippe_key

    def show_key_tasks(self, key):
        for task in self.default_tasks:
            if key in task['id']:
                print task['id']

    def over_skip_tasks(self, show=False):
        tasks = set()
        for task in self.default_tasks:
            if self.cehck_skip(task['id']):
                tasks.add(task['id'])
        if show:
            for task in tasks:
                print task
        return tasks

    def get_task(self, id, show=False):
        for task in self.default_tasks:
            if task['id'] == id:
                if show:
                    pprint.pprint(task)
                return task

    def gen_target_task(self, target_file=None):
        tasks=list()
        ids = self.over_skip_tasks()
        for task in self.default_tasks:
            if task['id'] in ids:
                tasks.append(task)
        if target_file:
            with open(target_file, 'w') as fp:
                dump_pretty_json(self.default_tasks, fp)
        else:
            dump_pretty_json(tasks, sys.stdout)

