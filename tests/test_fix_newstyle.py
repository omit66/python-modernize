from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_newstyle(FixerTestCase):
    fixer = 'newstyle'

    def test_without_parenthesis(self):
        b = """class A: pass"""
        a = """class A(object): pass"""
        self.check(b, a)

    def test_newstyle(self):
        b = """
        class A:
            pass

        class B():
            attr = 'attr'

        class C(A, B):
            pass"""
        a = """
        class A(object):
            pass

        class B(object):
            attr = 'attr'

        class C(A, B):
            pass"""
        self.check(b, a)

    def test_no_parents(self):
        b = """class A(): pass"""
        a = """class A(object): pass"""
        self.check(b, a)

    def test_unchanged(self):
        s = """class A(object): pass"""
        self.unchanged(s)

        s = """class B(A): pass"""
        self.unchanged(s)
