import unittest

from rope.contrib import finderrors
from ropetest import testutils


class FindErrorsTest(unittest.TestCase):

    def setUp(self):
        super(FindErrorsTest, self).setUp()
        self.project = testutils.sample_project()
        self.mod = self.project.root.create_file('mod.py')

    def tearDown(self):
        testutils.remove_project(self.project)
        super(FindErrorsTest, self).tearDown()

    def test_unresolved_variables(self):
        self.mod.write('print(var)\n')
        result = finderrors.find_errors(self.project, self.mod)
        self.assertEquals(1, len(result))
        self.assertEquals(1, result[0].lineno)

    def test_defined_later(self):
        self.mod.write('print(var)\nvar = 1\n')
        result = finderrors.find_errors(self.project, self.mod)
        self.assertEquals(1, len(result))
        self.assertEquals(1, result[0].lineno)

    def test_ignoring_builtins(self):
        self.mod.write('range(2)\n')
        result = finderrors.find_errors(self.project, self.mod)
        self.assertEquals(0, len(result))


if __name__ == '__main__':
    unittest.main()
