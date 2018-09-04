from fixertestcase import FixerTestCase


class Test_unicode_literals(FixerTestCase):
    fixer = "unicode"

    def test_unicode_literal_1(self):
        b = '''s = u"x"'''
        a = '''import six\ns = six.u("x")'''
        self.check(b, a)

    def test_unicode_literal_2(self):
        b = """s = ur'x'"""
        a = """import six\ns = six.u(r'x')"""
        self.check(b, a)

    def test_unicode_literal_3(self):
        b = """s = UR'''x''' """
        a = """import six\ns = six.u(R'''x''') """
        self.check(b, a)

    def test_u(self):
        b = """a = u'test' in b"""
        a = """import six\na = six.u('test') in b"""
        self.check(b, a)

        b = """s = u'test'"""
        a = """import six\ns = six.u('test')"""
        self.check(b, a)

    def test_unchanged(self):
        s = """r'test'"""
        self.unchanged(s)
