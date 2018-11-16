from __future__ import absolute_import

from .fixertestcase import FixerTestCase


PRINT_BARE = ("""\
print
""", """\
from __future__ import print_function
print()
""")

PRINT_SIMPLE = ("""\
print 'Hello'
""", """\
from __future__ import print_function
print('Hello')
""")

PRINT_MULTIPLE = ("""\
print 'Hello', 'world'
""", """\
from __future__ import print_function
print('Hello', 'world')
""")

PRINT_WITH_PARENS = ("""\
print('Hello')
""", """\
from __future__ import print_function
print('Hello')
""")

PRINT_WITH_COMMA = ("""\
print 'Hello',
""", """\
from __future__ import print_function
print('Hello', end=' ')
""")

PRINT_TO_STREAM = ("""\
print >>x, 'Hello'
""", """\
from __future__ import print_function
print('Hello', file=x)
""")

PRINT_TO_STREAM_WITH_COMMA = ("""\
print >>x, 'Hello',
""", """\
from __future__ import print_function
print('Hello', end=' ', file=x)
""")


class Test_print(FixerTestCase):
    fixer = "print"

    def test_print_bare(self):
        self.check(*PRINT_BARE)

    def test_print_simple(self):
        self.check(*PRINT_SIMPLE)

    def test_print_multiple(self):
        self.check(*PRINT_MULTIPLE)

    def test_print_with_parens(self):
        self.check(*PRINT_WITH_PARENS)

    def test_print_with_comma(self):
        self.check(*PRINT_WITH_COMMA)

    def test_print_to_stream(self):
        self.check(*PRINT_TO_STREAM)

    def test_print_to_stream_with_comma(self):
        self.check(*PRINT_TO_STREAM_WITH_COMMA)
