from fixertestcase import FixerTestCase


class Test_intern(FixerTestCase):
    fixer = "intern"

    def test_prefix_preservation(self):
        b = """x =   intern(  a  )"""
        a = """import six\nx =   six.intern(  a  )"""
        self.check(b, a)

        b = """y = intern("b" # test
              )"""
        a = """import six\ny = six.intern("b" # test
              )"""
        self.check(b, a)

        b = """z = intern(a+b+c.d,   )"""
        a = """import six\nz = six.intern(a+b+c.d,   )"""
        self.check(b, a)

    def test(self):
        b = """x = intern(a)"""
        a = """import six\nx = six.intern(a)"""
        self.check(b, a)

        b = """z = intern(a+b+c.d,)"""
        a = """import six\nz = six.intern(a+b+c.d,)"""
        self.check(b, a)

        b = """intern("y%s" % 5).replace("y", "")"""
        a = """import six\nsix.intern("y%s" % 5).replace("y", "")"""
        self.check(b, a)

    # These should not be refactored

    def test_unchanged(self):
        s = """intern(a=1)"""
        self.unchanged(s)

        s = """intern(f, g)"""
        self.unchanged(s)

        s = """intern(*h)"""
        self.unchanged(s)

        s = """intern(**i)"""
        self.unchanged(s)

        s = """intern()"""
        self.unchanged(s)
