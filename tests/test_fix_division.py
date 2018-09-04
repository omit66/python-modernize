from fixertestcase import FixerTestCase


class Test_division(FixerTestCase):
    fixer = "classic_division"

    def test_division(self):
        b = """c = a / b"""
        a = """from __future__ import division\nc = a // b"""
        self.check(b, a)

        b = """c = (42 * a) / b"""
        a = """from __future__ import division\nc = (42 * a) // b"""
        self.check(b, a)

    def test_unchange(self):
        s = """from __future__ import division\nc = a / b"""
        self.unchanged(s)

        s = """c = a // b"""
        self.unchanged(s)
