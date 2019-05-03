from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_long_typechecks(FixerTestCase):
    fixer = "long_typechecks"

    def test_1(self):
        s = """x = long(x)"""
        self.unchanged(s)

    def test_isinstance(self):
        b = """y = isinstance(x, long)"""
        a = """import six\ny = isinstance(x, six.integer_types)"""
        self.check(b, a)

        b = """isinstance(x, long)"""
        a = """import six\nisinstance(x, six.integer_types)"""
        self.check(b, a)

        b = """isinstance(x, (long,))"""
        a = """import six\nisinstance(x, six.integer_types)"""
        self.check(b, a)

        b = """isinstance(x, (long, int))"""
        a = """import six\nisinstance(x, six.integer_types)"""
        self.check(b, a)

        b = """isinstance(x, (int, long))"""
        a = """import six\nisinstance(x, six.integer_types)"""
        self.check(b, a)

        b = """isinstance(x, (int, long, bool))"""
        a = """import six\nisinstance(x, (bool,) + six.integer_types)"""
        self.check(b, a)

        b = """isinstance(x, (y, long, bool))"""
        a = """import six\nisinstance(x, (y, bool) + six.integer_types)"""
        self.check(b, a)

    def test_type_in(self):
        b = """z = type(x) in (int, long)"""
        a = """import six\nz = type(x) in six.integer_types"""
        self.check(b, a)

        b = """z = type(x) in (y, long)"""
        a = """import six\nz = type(x) in (y,) + six.integer_types"""
        self.check(b, a)

        b = """z = type(x) in (long, int)"""
        a = """import six\nz = type(x) in six.integer_types"""
        self.check(b, a)

    def test_type_is(self):
        b = """z = type(x) is long"""
        a = """import six\nz = type(x) in six.integer_types"""
        self.check(b, a)

    def test_type_eq(self):
        b = """type(x) == long"""
        a = """import six\ntype(x) in six.integer_types"""
        self.check(b, a)

    def test_unchanged(self):
        s = """long = True"""
        self.unchanged(s)

        s = """s.long = True"""
        self.unchanged(s)

        s = """def long(): pass"""
        self.unchanged(s)

        s = """class long(): pass"""
        self.unchanged(s)

        s = """def f(long): pass"""
        self.unchanged(s)

        s = """def f(g, long): pass"""
        self.unchanged(s)

        s = """def f(x, long=True): pass"""
        self.unchanged(s)

    def test_prefix_preservation(self):
        s = """x =   long(  x  )"""
        self.unchanged(s)

    def test_single_long(self):
        s = """long"""
        self.unchanged(s)
