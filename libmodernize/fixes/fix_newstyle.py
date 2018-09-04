"""
Fixer for "class Foo: ..." -> "class Foo(object): ..."

This fixer changes the method resolution order under python2. It must be
checked if it still works as expected.
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import LParen, RParen, Name


def insert_object(node, idx):
    node.insert_child(idx, RParen())
    node.insert_child(idx, Name(u"object"))
    node.insert_child(idx, LParen())


class FixNewstyle(fixer_base.BaseFix):

    PATTERN = """classdef< 'class' NAME ['(' ')'] colon=':' any >"""

    def transform(self, node, results):
        colon = results[u"colon"]
        idx = node.children.index(colon)
        if (node.children[idx-2].value == '(' and
           node.children[idx-1].value == ')'):
            del node.children[idx-2:idx]
            idx -= 2
        insert_object(node, idx)
