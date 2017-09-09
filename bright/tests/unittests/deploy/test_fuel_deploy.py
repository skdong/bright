import unittest
from deploy import fuel_deploy


class DeployTest(unittest.TestCase):
    def test_gen_add_controller_workflow(self):
        fuel_deploy.gen_add_controller_workflow()

    def test_gen_update_controller_workflow(self):
        fuel_deploy.gen_update_controller_workflow()
