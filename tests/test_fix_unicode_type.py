from fixertestcase import FixerTestCase


class Test_unicode(FixerTestCase):
    fixer = "unicode_type"

    def test_whitespace(self):
        b = """unicode( x)"""
        a = """import six\nsix.text_type( x)"""
        self.check(b, a)

        b = """ unicode(x )"""
        a = """import six\nsix.text_type(x )"""
        self.check(b, a)

    def test_unicode_call(self):
        b = """unicode(x, y, z)"""
        a = """import six\nsix.text_type(x, y, z)"""
        self.check(b, a)
