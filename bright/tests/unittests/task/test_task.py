import unittest
import fixtures
import os
import mock

from bright.task import task

test=""

class TestTask(fixtures.TestWithFixtures):

    def setUp(self):
        self.task = task.Task('a')

    def tearDown(self):
        self.task = None

    def test_mock(self):
        m = mock.Mock()
        m.some_method.return_value = 42
        self.assertEqual(m.some_mehtod(), 42)

    def test_environ(self):
        self.useFixture(
            fixtures.EnvironmentVariable("FOOBAR","42"))
        self.assertEqual(os.environ.get("FOOBAR"), "42")

    def test_init(self):
        self.assertEqual(self.task.name, 'a')

    @unittest.skipIf(test is not None, "Do not run this")
    def test_range(self):
        for x in range(5):
            if x > 3:
                self.fail("Range returned a too big value: %d"% x)

def test_true():
    assert True