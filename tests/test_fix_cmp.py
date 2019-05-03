from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_cmp(FixerTestCase):
    fixer = "cmp_inline"

    def test_cmp(self):
        b = """cmp(a, b)"""
        a = """((a > b) - (a < b))"""
        self.check(b, a)

    def test_cmp2(self):
        b = """return cmp(self.date(), Time(other).date())"""
        a = """return ((self.date() > Time(other).date()) - """\
            """(self.date() < Time(other).date()))"""
        self.check(b, a)
