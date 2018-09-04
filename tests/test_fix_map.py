""" Test for fix_map  """

# Local imports
from fixertestcase import FixerTestCase


class Test_map(FixerTestCase):
    fixer = "map"

    def check(self, b, a):
        self.unchanged("from future_builtins import map\n" + b)
        super(Test_map, self).check(b, a)

    def test_prefix_preservation(self):
        b = """x =    map(   f,    'abc'   )"""
        a = """import six\n""" \
            """x =    list(six.moves.map(   f,    'abc'   ))"""
        self.check(b, a)

    def test_trailing_comment(self):
        b = """x = map(f, 'abc')   #   foo"""
        a = """import six\nx = list(six.moves.map(f, 'abc'))   #   foo"""
        self.check(b, a)

    def test_None_with_multiple_arguments(self):
        s = """x = map(None, a, b, c)"""
        self.warns_unchanged(s, "cannot convert map(None, ...) with "
                             "multiple arguments")

    def test_map_basic(self):
        b = """x = map(f, 'abc')"""
        a = """import six\nx = list(six.moves.map(f, 'abc'))"""
        self.check(b, a)

        b = """x = len(map(f, 'abc', 'def'))"""
        a = """import six\n"""\
            """x = len(list(six.moves.map(f, 'abc', 'def')))"""
        self.check(b, a)

        b = """x = map(None, 'abc')"""
        a = """x = list('abc')"""
        self.check(b, a)

        b = """x = map(lambda x: x+1, range(4))"""
        a = """x = [x+1 for x in range(4)]"""
        self.check(b, a)

        # Note the parens around x
        b = """x = map(lambda (x): x+1, range(4))"""
        a = """x = [x+1 for x in range(4)]"""
        self.check(b, a)

        # XXX This (rare) case is not supported
        b = """x = map(f, 'abc')[0]"""
        a = """import six\nx = list(six.moves.map(f, 'abc'))[0]"""
        self.check(b, a)

        b = """
            foo()
            # foo
            map(f, x)
            """
        a = """\
            import six

            foo()
            # foo
            list(six.moves.map(f, x))
            """

        self.warns(b, a, "You should use a for loop here")

    def test_map_nochange(self):
        a = """b.join(map(f, 'abc'))"""
        self.unchanged(a)
        a = """(a + foo(5)).join(map(f, 'abc'))"""
        self.unchanged(a)
        a = """iter(map(f, 'abc'))"""
        self.unchanged(a)
        a = """list(map(f, 'abc'))"""
        self.unchanged(a)
        a = """list(map(f, 'abc'))[0]"""
        self.unchanged(a)
        a = """set(map(f, 'abc'))"""
        self.unchanged(a)
        a = """set(map(f, 'abc')).pop()"""
        self.unchanged(a)
        a = """tuple(map(f, 'abc'))"""
        self.unchanged(a)
        a = """any(map(f, 'abc'))"""
        self.unchanged(a)
        a = """all(map(f, 'abc'))"""
        self.unchanged(a)
        a = """sum(map(f, 'abc'))"""
        self.unchanged(a)
        a = """sorted(map(f, 'abc'))"""
        self.unchanged(a)
        a = """sorted(map(f, 'abc'), key=blah)"""
        self.unchanged(a)
        a = """sorted(map(f, 'abc'), key=blah)[0]"""
        self.unchanged(a)
        a = """enumerate(map(f, 'abc'))"""
        self.unchanged(a)
        a = """enumerate(map(f, 'abc'), start=1)"""
        self.unchanged(a)
        a = """for i in map(f, 'abc'): pass"""
        self.unchanged(a)
        a = """[x for x in map(f, 'abc')]"""
        self.unchanged(a)
        a = """(x for x in map(f, 'abc'))"""
        self.unchanged(a)

    def test_future_builtins(self):
        a = "from future_builtins import spam, map, eggs; map(f, 'ham')"
        self.unchanged(a)

        b = """from future_builtins import spam, eggs\nx = map(f, 'abc')"""
        a = """from future_builtins import spam, eggs\nimport six\n"""\
            """x = list(six.moves.map(f, 'abc'))"""
        self.check(b, a)

        a = "from future_builtins import *; map(f, 'ham')"
        self.unchanged(a)
