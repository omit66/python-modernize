from fixertestcase import FixerTestCase


class Test_itertools_imports(FixerTestCase):
    fixer = "itertools_imports_six"

    def test_reduced(self):
        b = "from itertools import imap, izip, foo"
        a = "from itertools import foo\nimport six"
        self.check(b, a)

        b = "from itertools import bar, imap, izip, foo"
        a = "from itertools import bar, foo\nimport six"
        self.check(b, a)

        b = "from itertools import chain, imap, izip"
        a = "from itertools import chain\nimport six"
        self.check(b, a)

    def test_comments(self):
        b = "#foo\nfrom itertools import imap, izip"
        a = "#foo\n\nimport six"
        self.check(b, a)

    def test_none(self):
        b = "from itertools import imap, izip"
        a = "\nimport six"
        self.check(b, a)

        b = "from itertools import izip"
        a = "\nimport six"
        self.check(b, a)

    def test_import_as(self):
        b = "from itertools import izip, bar as bang, imap"
        a = "from itertools import bar as bang\nimport six"
        self.check(b, a)

        b = "from itertools import izip as _zip, imap, bar"
        a = "from itertools import bar\nfrom six.moves import zip as _zip\n"\
            "import six"
        self.check(b, a)

        b = "from itertools import imap as _map"
        a = "\nfrom six.moves import map as _map"
        self.check(b, a)

        b = "from itertools import imap as _map, izip as _zip"
        a = "\nfrom six.moves import map as _map\n"\
            "from six.moves import zip as _zip"
        self.check(b, a)

        s = "from itertools import bar as bang"
        self.unchanged(s)

    def test_ifilter_and_zip_longest(self):
        for name in "filterfalse", "zip_longest":
            b = "from itertools import i%s" % (name,)
            a = "\nimport six"
            self.check(b, a)

            b = "from itertools import imap, i%s, foo" % (name,)
            a = "from itertools import foo\nimport six"
            self.check(b, a)

            b = "from itertools import bar, i%s, foo" % (name,)
            a = "from itertools import bar, foo\nimport six"
            self.check(b, a)

    def test_import_star(self):
        s = "from itertools import *"
        self.unchanged(s)

    def test_unchanged(self):
        s = "from itertools import foo"
        self.unchanged(s)

    def test_izip(self):
        # fixer_tools will replace izip(...)
        b = "from itertools import izip\nizip([1, 2], [1])"""
        a = "\nimport six\nizip([1, 2], [1])"
        self.check(b, a)

    def test_imap(self):
        # fixer_tools will replace imap(...)
        s = """import itertools\nitertools.imap(lambda x: x * 2, [1, 2])"""
        self.unchanged(s)
