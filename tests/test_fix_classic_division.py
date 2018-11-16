from __future__ import absolute_import

from .fixertestcase import FixerTestCase


CLASSIC_DIVISION = ("""\
1 / 2
""",
"""\
from __future__ import division
1 // 2
""")

NEW_DIVISION = """\
from __future__ import division
1 / 2
"""



class Test_classical_devision(FixerTestCase):
    fixer = "classic_division"

    def test_fix_classic_division(self):
        self.check(*CLASSIC_DIVISION)

    def test_new_division(self):
        self.unchanged(NEW_DIVISION, NEW_DIVISION)
