import re
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, Attr, Leaf
from lib2to3.fixer_util import touch_import
from lib2to3.pytree import Node
from lib2to3.pgen2 import token

_literal_re = re.compile(u"[uU][rR]?[\\'\\\"]")


class FixUnicode(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """STRING"""

    def transform(self, node, results):
        if _literal_re.match(node.value):
            touch_import(None, u'six', node)
            new = Name(node.value[1:], prefix=u'')
            new = self.createNewNode(new)
            new.prefix = node.prefix
            node.replace(new)

    def createNewNode(self, node):
        lpar = Leaf(token.LPAR, u'(')
        rpar = Leaf(token.RPAR, u')')
        new = Node(self.syms.power,
                   Attr(Name(u"six"), Name(u"u")) +
                   [Node(self.syms.trailer, [lpar, node, rpar])]
                   )
        return new
