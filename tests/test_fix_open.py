from __future__ import absolute_import

from .fixertestcase import FixerTestCase


class Test_open(FixerTestCase):
    fixer = "open"

    def test_open(self):
        b = "open('some/path')"
        a = """\
        from io import open
        open('some/path')"""
        self.check(b, a)
