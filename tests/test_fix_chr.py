from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_char(FixerTestCase):
    fixer = "chr"

    def test_chr(self):
        b = "chr(i)"
        a = "import six\nsix.int2byte(i)"
        self. check(b, a)

        s = "unichr(i)"
        self.unchanged(s)
