# Test code for fix_getcwdu.py

# Python imports
from fixertestcase import FixerTestCase


class Test_getcwdu(FixerTestCase):

    fixer = 'getcwdu'

    def test_basic(self):
        b = """os.getcwdu"""
        a = """import six\nsix.moves.getcwdu"""
        self.check(b, a)

        b = """os.getcwdu()"""
        a = """import six\nsix.moves.getcwdu()"""
        self.check(b, a)

        b = """meth = os.getcwdu"""
        a = """import six\nmeth = six.moves.getcwdu"""
        self.check(b, a)

        b = """os.getcwdu(args)"""
        a = """import six\nsix.moves.getcwdu(args)"""
        self.check(b, a)

    def test_comment(self):
        b = """os.getcwdu() # Foo"""
        a = """import six\nsix.moves.getcwdu() # Foo"""
        self.check(b, a)

    def test_unchanged(self):
        s = """os.getcwd()"""
        self.unchanged(s)

        s = """getcwdu()"""
        self.unchanged(s)

        s = """os.getcwdb()"""
        self.unchanged(s)

    def test_indentation(self):
        b = """
            if 1:
                os.getcwdu()
            """
        a = """\
            import six

            if 1:
                six.moves.getcwdu()
            """
        self.check(b, a)

    def test_multilation(self):
        b = """os .getcwdu()"""
        a = """import six\nsix.moves .getcwdu()"""
        self.check(b, a)

        b = """os.  getcwdu"""
        a = """import six\nsix.moves.  getcwdu"""
        self.check(b, a)

        b = """os.getcwdu (  )"""
        a = """import six\nsix.moves.getcwdu (  )"""
        self.check(b, a)

    def test_imported_getcwdu(self):
        b = """from os import getcwdu\ngetcwdu()"""
        a = """from os import getcwdu\nimport six\nsix.moves.getcwdu()"""
        self.check(b, a)

        # cannot remove the import
        b = """import os.getcwdu\nos.getcwdu()"""
        a = """import os.getcwdu\nimport six\nsix.moves.getcwdu()"""
        self.check(b, a)

        b = """from os import *\ngetcwdu()"""
        a = """from os import *\nimport six\nsix.moves.getcwdu()"""
        self.check(b, a)
