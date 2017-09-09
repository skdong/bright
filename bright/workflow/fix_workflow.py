from workflow import WorkFlow
from workflow import dump_pretty_json
import sys


class FixWorkFlow(WorkFlow):
    def gen_target_task(self, target_file=None):
        tasks = list()
        for task in self.default_tasks:
            if task['id'] in self.need_tasks:
                tasks.append(task)
        if target_file:
            with open(target_file, 'w') as fp:
                dump_pretty_json(tasks, fp)
        else:
            dump_pretty_json(tasks, sys.stdout)
