# coding: utf-8
"""
Fixer for the cmp() function on Py2, which was removed in Py3.

Replace cmp(a, b) with (a > b) - (a < b)
"""

from lib2to3 import fixer_base
from lib2to3.pgen2 import token
from lib2to3.pytree import Node, Leaf


class FixCmpInline(fixer_base.BaseFix):
    BM_compatible = True
    run_order = 9

    PATTERN = """
              power<
                 'cmp' trailer< '(' arglist<x=any ',' y=any> ')' >
              >
              """

    def transform(self, node, results):
        x = results['x']
        y = results['y']
        gt = Leaf(token.GREATER, u'>', prefix=u' ')
        lt = Leaf(token.LESS, u'<', prefix=u' ')
        # left node
        left_n = Node(self.syms.comparison, [x.clone(), gt, y.clone()])
        left_n = self.trailer(left_n)
        # right node
        right_n = Node(self.syms.comparison,
                       [x.clone(), lt, y.clone()])
        right_n = self.trailer(right_n)
        right_n.prefix = u' '
        minus = Leaf(token.MINUS, u'-', prefix=u' ')
        new = Node(self.syms.arith_expr, [left_n, minus, right_n])
        new = self.trailer(new)
        new.prefix = node.prefix
        return new

    def trailer(self, node):
        # wrap into parenthesis
        lpar = Leaf(token.LPAR, u'(')
        rpar = Leaf(token.RPAR, u')')
        return Node(self.syms.trailer, [lpar, node, rpar])
