""" Test for fix_range  """

from fixertestcase import FixerTestCase
from lib2to3 import fixer_util


class Test_range(FixerTestCase):
    fixer = "range_six"

    def test_prefix_preservation(self):
        b = """x =    xrange(  10  )"""
        a = """import six\nx =    six.moves.range(  10  )"""
        self.check(b, a)

        b = """x = xrange(  1  ,  10   )"""
        a = """import six\nx = six.moves.range(  1  ,  10   )"""
        self.check(b, a)

        b = """x = xrange(  0  ,  10 ,  2 )"""
        a = """import six\nx = six.moves.range(  0  ,  10 ,  2 )"""
        self.check(b, a)

    def test_single_arg(self):
        b = """x = xrange(10)"""
        a = """import six\nx = six.moves.range(10)"""
        self.check(b, a)

    def test_two_args(self):
        b = """x = xrange(1, 10)"""
        a = """import six\nx = six.moves.range(1, 10)"""
        self.check(b, a)

    def test_three_args(self):
        b = """x = xrange(0, 10, 2)"""
        a = """import six\nx = six.moves.range(0, 10, 2)"""
        self.check(b, a)

    def test_wrap_in_list(self):
        b = """x = range(10, 3, 9)"""
        a = """import six\nx = list(six.moves.range(10, 3, 9))"""
        self.check(b, a)

        b = """x = foo(range(10, 3, 9))"""
        a = """import six\nx = foo(list(six.moves.range(10, 3, 9)))"""
        self.check(b, a)

        b = """x = range(10, 3, 9) + [4]"""
        a = """import six\nx = list(six.moves.range(10, 3, 9)) + [4]"""
        self.check(b, a)

        b = """x = range(10)[::-1]"""
        a = """import six\nx = list(six.moves.range(10))[::-1]"""
        self.check(b, a)

        b = """x = range(10)  [3]"""
        a = """import six\nx = list(six.moves.range(10))  [3]"""
        self.check(b, a)

    def test_xrange_in_for(self):
        b = """for i in xrange(10):\n    j=i"""
        a = """import six\nfor i in six.moves.range(10):\n    j=i"""
        self.check(b, a)

        b = """[i for i in xrange(10)]"""
        a = """import six\n[i for i in six.moves.range(10)]"""
        self.check(b, a)

    # replace range with xrange -> i guess it is faster (python2)
    def test_range_in_for(self):
        b = "for i in range(10): pass"
        a = "import six\nfor i in six.moves.range(10): pass"
        self.check(b, a)
        b = "[i for i in range(10)]"
        a = "import six\n[i for i in six.moves.range(10)]"
        self.check(b, a)

    # replace range with xrange -> i guess it is faster (python2)
    def test_in_contains_test(self):
        b = "x in range(10, 3, 9)"
        a = "import six\nx in six.moves.range(10, 3, 9)"
        self.check(b, a)

    # replace range with xrange -> i guess it is faster (python2)
    def test_in_consuming_context(self):
        for call in fixer_util.consuming_calls:
            b = "a = %s(range(10))" % call
            a = "import six\na = %s(six.moves.range(10))" % call
            self.check(b, a)
