from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_nonzero(FixerTestCase):
    fixer = "nonzero"

    def test_1(self):
        b = """
            class A:
                def __nonzero__(self):
                    pass
            """
        a = """
            class A:
                def __nonzero__(self):
                    return self.__bool__()

                def __bool__(self):
                    pass
            """
        self.check(b, a)

    def test_2(self):
        b = """
            class A(object):
                def __nonzero__(self):
                    pass
            """
        a = """
            class A(object):
                def __nonzero__(self):
                    return self.__bool__()

                def __bool__(self):
                    pass
            """
        self.check(b, a)

    def test_3(self):
        b = """
            class A(object):
                def __nonzero__(self): pass
            """
        a = """
            class A(object):
                def __nonzero__(self):
                    return self.__bool__()

                def __bool__(self): pass
            """
        self.check(b, a)

    def test_unchanged_1(self):
        s = """
            class A(object):
                def __bool__(self):
                    pass
            """
        self.unchanged(s)

    def test_unchanged_2(self):
        s = """
            class A(object):
                def __nonzero__(self, a):
                    pass
            """
        self.unchanged(s)

    def test_unchanged_func(self):
        s = """
            def __nonzero__(self):
                pass
            """
        self.unchanged(s)
