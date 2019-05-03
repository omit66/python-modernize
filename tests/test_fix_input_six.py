
from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_input(FixerTestCase):
    fixer = "input_six"

    def test_prefix_preservation(self):
        b = """x =    raw_input(   )"""
        a = """import six\nx =    six.moves.input(   )"""
        self.check(b, a)

        b = """x = raw_input(   ''   )"""
        a = """import six\nx = six.moves.input(   ''   )"""
        self.check(b, a)

        b = """x =   input(   )"""
        a = """import six\nx =   eval(six.moves.input(   ))"""
        self.check(b, a)

        b = """x = input(   ''   )"""
        a = """import six\nx = eval(six.moves.input(   ''   ))"""
        self.check(b, a)

    def test_1(self):
        b = """x = raw_input()"""
        a = """import six\nx = six.moves.input()"""
        self.check(b, a)

        b = """x = input()"""
        a = """import six\nx = eval(six.moves.input())"""
        self.check(b, a)

    def test_2(self):
        b = """x = raw_input('')"""
        a = """import six\nx = six.moves.input('')"""
        self.check(b, a)

        b = """x = input('')"""
        a = """import six\nx = eval(six.moves.input(''))"""
        self.check(b, a)

    def test_3(self):
        b = """x = raw_input('prompt')"""
        a = """import six\nx = six.moves.input('prompt')"""
        self.check(b, a)

        b = """x = input('prompt')"""
        a = """import six\nx = eval(six.moves.input('prompt'))"""
        self.check(b, a)

    def test_4(self):
        b = """x = raw_input(foo(a) + 6)"""
        a = """import six\nx = six.moves.input(foo(a) + 6)"""
        self.check(b, a)

        b = """x = input(foo(5) + 9)"""
        a = """import six\nx = eval(six.moves.input(foo(5) + 9))"""
        self.check(b, a)

    def test_5(self):
        b = """x = raw_input(invite).split()"""
        a = """import six\nx = six.moves.input(invite).split()"""
        self.check(b, a)

    def test_6(self):
        b = """x = raw_input(invite) . split ()"""
        a = """import six\nx = six.moves.input(invite) . split ()"""
        self.check(b, a)

    def test_8(self):
        b = "x = int(raw_input())"
        a = "import six\nx = int(six.moves.input())"
        self.check(b, a)

    def test_trailing_comment(self):
        b = """x = input()  #  foo"""
        a = """import six\nx = eval(six.moves.input())  #  foo"""
        self.check(b, a)

    def test_wrapped_input(self):
        b = """x = eval(input())"""
        a = """import six\nx = eval(six.moves.input())"""
        self.check(b, a)

        b = """x = eval(input(''))"""
        a = """import six\nx = eval(six.moves.input(''))"""
        self.check(b, a)

        b = """x = eval(input(foo(5) + 9))"""
        a = """import six\nx = eval(six.moves.input(foo(5) + 9))"""
        self.check(b, a)
