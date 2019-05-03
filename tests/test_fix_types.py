from __future__ import absolute_import
from .fixertestcase import FixerTestCase


class Test_types(FixerTestCase):
    fixer = "types"

    def test_basic_types_convert(self):
        b = """types.StringType"""
        a = """import six\nsix.binary_type"""
        self.check(b, a)

        b = """types.DictType"""
        a = """dict"""
        self.check(b, a)

        b = """types . IntType"""
        a = """int"""
        self.check(b, a)

        b = """types.ListType"""
        a = """list"""
        self.check(b, a)

        b = """types.LongType"""
        a = """import six\nsix.integer_types"""
        self.check(b, a)

        b = """types.NoneType"""
        a = """type(None)"""
        self.check(b, a)

        b = "types.StringTypes"
        a = "import six\nsix.string_types"
        self.check(b, a)

        b = "types.UnicodeType"
        a = "import six\nsix.text_type"
        self.check(b, a)

        b = "types.ClassType"
        a = "import six\nsix.class_types"
        self.check(b, a)
