from fixertestcase import FixerTestCase


class Test_zip(FixerTestCase):
    fixer = "zip"

    def check(self, b, a):
        self.unchanged("from six.moves import zip; " + b, a)
        super(Test_zip, self).check(b, a)

    def test_zip_basic(self):
        b = """x = zip(a, b, c)"""
        a = """import six\nx = list(six.moves.zip(a, b, c))"""
        self.check(b, a)

        b = """x = len(zip(a, b))"""
        a = """import six\nx = len(list(six.moves.zip(a, b)))"""
        self.check(b, a)

    def test_zip_nochange(self):
        a = """b.join(zip(a, b))"""
        self.unchanged(a)
        a = """(a + foo(5)).join(zip(a, b))"""
        self.unchanged(a)
        a = """iter(zip(a, b))"""
        self.unchanged(a)
        a = """list(zip(a, b))"""
        self.unchanged(a)
        a = """list(zip(a, b))[0]"""
        self.unchanged(a)
        a = """set(zip(a, b))"""
        self.unchanged(a)
        a = """set(zip(a, b)).pop()"""
        self.unchanged(a)
        a = """tuple(zip(a, b))"""
        self.unchanged(a)
        a = """any(zip(a, b))"""
        self.unchanged(a)
        a = """all(zip(a, b))"""
        self.unchanged(a)
        a = """sum(zip(a, b))"""
        self.unchanged(a)
        a = """sorted(zip(a, b))"""
        self.unchanged(a)
        a = """sorted(zip(a, b), key=blah)"""
        self.unchanged(a)
        a = """sorted(zip(a, b), key=blah)[0]"""
        self.unchanged(a)
        a = """enumerate(zip(a, b))"""
        self.unchanged(a)
        a = """enumerate(zip(a, b), start=1)"""
        self.unchanged(a)
        a = """for i in zip(a, b): pass"""
        self.unchanged(a)
        a = """[x for x in zip(a, b)]"""
        self.unchanged(a)
        a = """(x for x in zip(a, b))"""
        self.unchanged(a)

    def test_six_import(self):
        a = "from six.moves import spam, zip, eggs; zip(a, b)"
        self.unchanged(a)

        b = """from six.moves import spam, eggs\nx = zip(a, b)"""
        a = """from six.moves import spam, eggs\nimport six\n""" \
            """x = list(six.moves.zip(a, b))"""
        self.check(b, a)

        a = "from six.moves import *; zip(a, b)"
        self.unchanged(a)
