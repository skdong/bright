import os

from workflow import workflow
import add_nodes
import update_controllers

WORKFLOW_PAHT = "C:\Users\shika\Downloads"

WORKFLOW_FILE = os.path.join(WORKFLOW_PAHT, "default-release.json")


def gen_add_controller_workflow():
    add_info = dict(workflow=dict(tasks_file=WORKFLOW_FILE,
                                  skip_ids=add_nodes.SKIP_TASKS),
                    target_file=os.path.join(WORKFLOW_PAHT, "add_controller.json"))
    add_controller = workflow.WorkFlow(**add_info['workflow'])
    add_controller.gen_target_task(add_info['target_file'])


def gen_update_controller_workflow():
    update_info = dict(workflow=dict(tasks_file=WORKFLOW_FILE,
                                     skip_ids=update_controllers.SKIP_TASKS),
                       target_file=os.path.join(WORKFLOW_PAHT, "update_controller.json"))
    update_controller = workflow.WorkFlow(**update_info['workflow'])
    update_controller.gen_target_task(update_info['target_file'])


def generate_tasks():
    gen_update_controller_workflow()
    gen_add_controller_workflow()


def main():
    generate_tasks()


if __name__ == '__main__':
    main()
