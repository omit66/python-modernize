from fixertestcase import FixerTestCase


class Test_metaclass(FixerTestCase):
    fixer = 'metaclass'

    def test_unchanged(self):
        self.unchanged("class X(): pass")
        self.unchanged("class X(object): pass")
        self.unchanged("class X(object1, object2): pass")
        self.unchanged("class X(object1, object2, object3): pass")
        self.unchanged("class X(metaclass=Meta): pass")
        self.unchanged("class X(b, arg=23, metclass=Meta): pass")
        self.unchanged("class X(b, arg=23, metaclass=Meta, other=42): pass")

        s = """
        class X:
            def __metaclass__(self): pass
        """
        self.unchanged(s)

        s = """
        class X:
            a[23] = 74
        """
        self.unchanged(s)

    def test_comments(self):
        b = """
        class X:
            # hi
            __metaclass__ = AppleMeta
        """
        a = """\
        import six

        @six.add_metaclass(AppleMeta)
        class X:
            # hi
            pass
        """
        self.check(b, a)

        b = """
        class X:
            __metaclass__ = Meta
            # Bedtime!
        """
        a = """\
        import six

        @six.add_metaclass(Meta)
        class X:
            pass
            # Bedtime!
        """
        self.check(b, a)

    def test_meta_no_parent(self):
        # no-parent class, odd body
        b = """
        class X():
            __metaclass__ = Q
            pass
        """
        a = """\
        import six

        @six.add_metaclass(Q)
        class X():
            pass
        """
        self.check(b, a)

    def test_meta(self):
        # one parent class, no body
        b = """class X(object): __metaclass__ = Q"""
        a = """import six\n@six.add_metaclass(Q)\nclass X(object): pass"""
        self.check(b, a)

        # one parent, simple body
        b = """
        class X(object):
            __metaclass__ = Meta
            bar = 7
        """
        a = """\
        import six

        @six.add_metaclass(Meta)
        class X(object):
            bar = 7
        """
        self.check(b, a)

        b = """
        class X:
            __metaclass__ = Meta; x = 4; g = 23
        """
        a = """\
        import six

        @six.add_metaclass(Meta)
        class X:
            x = 4; g = 23
        """
        self.check(b, a)

    def test_metaclass_last(self):
        # one parent, simple body, __metaclass__ last
        b = """
        class X(object):
            bar = 7
            __metaclass__ = Meta
        """
        a = """\
        import six

        @six.add_metaclass(Meta)
        class X(object):
            bar = 7
        """
        self.check(b, a)

    def test_meta_multiple_inheritance(self):
        # multiple inheritance, simple body
        b = """
        class X(clsA, clsB):
            __metaclass__ = Meta
            bar = 7
        """
        a = """\
        import six

        @six.add_metaclass(Meta)
        class X(clsA, clsB):
            bar = 7
        """
        self.check(b, a)

        # keywords in the class statement
        b = """class m(a, arg=23): __metaclass__ = Meta"""
        a = """import six\n@six.add_metaclass(Meta)\nclass m(a, arg=23): """\
            """pass"""
        self.check(b, a)

        b = """
        class X(expression(2 + 4)):
            __metaclass__ = Meta
        """
        a = """\
        import six

        @six.add_metaclass(Meta)
        class X(expression(2 + 4)):
            pass
        """
        self.check(b, a)

        b = """
        class X(expression(2 + 4), x**4):
            __metaclass__ = Meta
        """
        a = """\
        import six

        @six.add_metaclass(Meta)
        class X(expression(2 + 4), x**4):
            pass
        """
        self.check(b, a)

        b = """
        class X:
            __metaclass__ = Meta
            save.py = 23
        """
        a = """\
        import six

        @six.add_metaclass(Meta)
        class X:
            save.py = 23
        """
        self.check(b, a)

    def test_meta_defefining(self):
        # redefining __metaclass__
        b = """
        class X():
            __metaclass__ = A
            __metaclass__ = B
            bar = 7
        """
        a = """\
        import six

        @six.add_metaclass(B)
        class X():
            bar = 7
        """
        self.check(b, a)
