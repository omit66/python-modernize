"""
Fixer that changes zip(seq0, seq1, ...) into
list(six.moves.zip(seq0, seq1, ...) unless there exists a
'from six.moves import zip' statement in the top-level namespace.

We avoid the transformation if the zip() call is directly contained in
iter(<>), list(<>), tuple(<>), sorted(<>), ...join(<>), or for V in <>:.
Extended by CONTACT Software GmbH
"""

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, Call, in_special_context

from lib2to3.fixer_util import touch_import


class FixZip(fixer_base.ConditionalFix):

    BM_compatible = True
    PATTERN = """
    power< name='zip' args=trailer< '(' [any] ')' >
    >
    """

    skip_on = "six.moves.zip"

    def transform(self, node, results):
        if self.should_skip(node):
            return

        if in_special_context(node):
            return None

        touch_import(None, u'six', node)
        name = results['name']
        name.replace(Name(u'six.moves.zip', name.prefix))
        new = node.clone()
        new.prefix = u""
        new = Call(Name(u"list"), [new])
        new.prefix = node.prefix
        return new
