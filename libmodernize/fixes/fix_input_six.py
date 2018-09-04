# This is a derived work of Lib/lib2to3/fixes/fix_input.py and
# Lib/lib2to3/fixes/fix_raw_input.py. Those files are under the
# copyright of the Python Software Foundation and licensed under the
# Python Software Foundation License 2.
#
# Copyright notice:
#
#     Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
#     2011, 2012, 2013, 2014 Python Software Foundation. All rights reserved.
# This work has been extended by CONTACT Software GmbH
from __future__ import absolute_import

from lib2to3 import patcomp, fixer_base
from lib2to3.fixer_util import Call, Name
from lib2to3.fixer_util import touch_import


class FixInputSix(fixer_base.ConditionalFix):

    BM_compatible = True
    order = 'pre'
    skip_on = 'six.moves.input'

    PATTERN = """
              power< (name='input' | name='raw_input')
                trailer< '(' [any] ')' > any* >
              """

    def transform(self, node, results):
        if self.should_skip(node):
            return

        touch_import(None, u'six', node)
        name = results['name']
        old_name = name.value
        name.replace(Name('six.moves.input', prefix=name.prefix))
        if old_name == 'input':
            # if the node is wrapped in eval it not necessary to wrap again
            if not self.in_special_context(node):
                new_node = node.clone()
                new_node.prefix = ''
                return Call(Name('eval'), [new_node], prefix=node.prefix)

    P1 = "parent=power< func=NAME trailer< '(' node=any ')' > any* >"
    p1 = patcomp.compile_pattern(P1)

    def in_special_context(self, node):
        # it is not wrapped
        if node.parent is None:
            return False
        results = {}
        if (node.parent.parent is not None and
           self.p1.match(node.parent.parent, results) and
           results["node"] is node):

            # eval(input) -> eval(six.moves.input)
            if results['func'].value == 'eval':
                return True
        return False
