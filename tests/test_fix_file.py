from __future__ import absolute_import

from .fixertestcase import FixerTestCase


class Test_file(FixerTestCase):
    fixer = "file"

    def test_file(self):
        b = "file('some/path')"
        a = """\
        open('some/path')"""
        self.check(b, a)
