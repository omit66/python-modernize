from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_basestring(FixerTestCase):
    fixer = "basestring"

    def test_basestring(self):
        b = """isinstance(x, basestring)"""
        a = """import six\nisinstance(x, six.string_types)"""
        self.check(b, a)


