import os

from workflow import api
import update_computes
import add_controllers
import update_controllers

WORKFLOW_PAHT = "C:\Users\cgj\Downloads"

WORKFLOW_FILE = os.path.join(WORKFLOW_PAHT, "default-release.json")


def gen_add_controller_workflow():
    api.gen_workflow(WORKFLOW_FILE, add_controllers)


def gen_update_controller_workflow():
    api.gen_workflow(WORKFLOW_FILE, update_controllers)


def gen_update_compute_workflow():
    api.gen_workflow(WORKFLOW_FILE, update_computes)


def generate_tasks():
    gen_update_compute_workflow()
    # gen_update_controller_workflow()
    # gen_add_controller_workflow()


def main():
    generate_tasks()


if __name__ == '__main__':
    main()
