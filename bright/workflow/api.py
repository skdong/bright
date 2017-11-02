from workflow import WorkFlow


def gen_workflow(default, action):
    workflow = WorkFlow(tasks_file=default, skip_ids=action.SKIP_TASKS)
    workflow.gen_target_task(action.workflow)
