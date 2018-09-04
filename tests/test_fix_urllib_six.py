from fixertestcase import FixerTestCase


class Test_urllib(FixerTestCase):
    fixer = "urllib_six"
    from libfuturize.fixes.fix_urllib import MAPPING as modules

    def test_import_module(self):
        for old, changes in self.modules.items():
            b = "import %s" % old
            a = "import six"
            self.check(b, a)

    def test_import_from(self):
        for old, changes in self.modules.items():
            all_members = []
            for new, members in changes:
                for member in members:
                    all_members.append(member)
                    b = "from %s import %s" % (old, member)
                    a = "from %s import %s" % (new, member)
                    self.check(b, a)

                    s = "from foo import %s" % member
                    self.unchanged(s)

                b = "from %s import %s" % (old, ", ".join(members))
                a = "from %s import %s" % (new, ", ".join(members))
                self.check(b, a)

                s = "from foo import %s" % ", ".join(members)
                self.unchanged(s)

            # test the breaking of a module into multiple replacements
            b = "from %s import %s" % (old, ", ".join(all_members))
            a = "\n".join(["from %s import %s" % (new, ", ".join(members))
                          for (new, members) in changes])
            self.check(b, a)

    def test_import_module_as(self):
        for old in self.modules:
            s = "import %s as foo" % old
            self.warns_unchanged(s, "This module is now multiple modules")

    def test_import_from_as(self):
        for old, changes in self.modules.items():
            for new, members in changes:
                for member in members:
                    b = "from %s import %s as foo_bar" % (old, member)
                    a = "from %s import %s as foo_bar" % (new, member)
                    self.check(b, a)
                    b = "from %s import %s as blah, %s" % (old, member, member)
                    a = "from %s import %s as blah, %s" % (new, member, member)
                    self.check(b, a)

    def test_star(self):
        for old in self.modules:
            s = "from %s import *" % old
            self.warns_unchanged(s, "Cannot handle star imports")

    def test_indented(self):
        b = """
def foo():
    from urllib import urlencode, urlopen
"""
        a = """
def foo():
    from six.moves.urllib.parse import urlencode
    from six.moves.urllib.request import urlopen
"""
        self.check(b, a)

        b = """
def foo():
    other()
    from urllib import urlencode, urlopen
"""
        a = """
def foo():
    other()
    from six.moves.urllib.parse import urlencode
    from six.moves.urllib.request import urlopen
"""
        self.check(b, a)

    def test_import_module_usage(self):
        for old, changes in self.modules.items():
            for new, members in changes:
                for member in members:
                    b = """
                        import %s
                        foo(%s.%s)
                        """ % (old, old, member)
                    a = """
                        import six
                        foo(%s.%s)
                        """ % (new, member)
                    self.check(b, a)
                    b = """
                        import %s
                        %s.%s(%s.%s)
                        """ % (old, old, member, old, member)
                    a = """
                        import six
                        %s.%s(%s.%s)
                        """ % (new, member, new, member)
                    self.check(b, a)
