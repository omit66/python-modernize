from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_imports_six(FixerTestCase):
    fixer = "imports_six"
    # from libmodernize.fixes.fix_imports_six import FixImportsSix
    from libmodernize.fixes import fix_imports_six
    MAPPING = fix_imports_six.MAPPING

    def test_import_module(self):
        for old, new in self.MAPPING.items():
            b = "import %s" % old
            a = "import %s" % new
            self.check(b, a)

            b = "import foo, %s, bar" % old
            a = "import foo, %s, bar" % new
            self.check(b, a)

    def test_import_from(self):
        for old, new in self.MAPPING.items():
            b = "from %s import foo" % old
            a = "from %s import foo" % new
            self.check(b, a)

            b = "from %s import foo, bar" % old
            a = "from %s import foo, bar" % new
            self.check(b, a)

            b = "from %s import (yes, no)" % old
            a = "from %s import (yes, no)" % new
            self.check(b, a)

    def test_import_module_as(self):
        for old, new in self.MAPPING.items():
            b = "import %s as foo_bar" % old
            a = "import %s as foo_bar" % new
            self.check(b, a)

            b = "import %s as foo_bar" % old
            a = "import %s as foo_bar" % new
            self.check(b, a)

    def test_import_from_as(self):
        for old, new in self.MAPPING.items():
            b = "from %s import foo as bar" % old
            a = "from %s import foo as bar" % new
            self.check(b, a)

    def test_star(self):
        for old, new in self.MAPPING.items():
            b = "from %s import *" % old
            a = "from %s import *" % new
            self.check(b, a)

    def test_import_module_usage(self):
        for old, new in self.MAPPING.items():
            b = """
                import %s
                foo(%s.bar)
                """ % (old, old)
            a = """
                import %s
                foo(%s.bar)
                """ % (new, new)
            self.check(b, a)

            b = """
                from %s import x
                %s = 23
                """ % (old, old)
            a = """
                from %s import x
                %s = 23
                """ % (new, old)
            self.check(b, a)

            s = """
                def f():
                    %s.method()
                """ % (old,)
            self.unchanged(s)

            # test nested usage
            b = """
                import %s
                %s.bar(%s.foo)
                """ % (old, old, old)
            a = """
                import %s
                %s.bar(%s.foo)
                """ % (new, new, new)
            self.check(b, a)

            b = """
                import %s
                x.%s
                """ % (old, old)
            a = """
                import %s
                x.%s
                """ % (new, old)
            self.check(b, a)
