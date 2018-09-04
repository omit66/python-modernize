# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.
# Extended by CONTACT Software GmbH
"""
Fixer that changes xrange(...) into six.moves.range(...).
range() -> list(six.moves.range())
"""

from lib2to3 import fixer_base, patcomp
from lib2to3.fixer_util import Name, Call, consuming_calls
from lib2to3.fixer_util import touch_import


class FixRangeSix(fixer_base.ConditionalFix, fixer_base.BaseFix):
    skip_on = 'six.moves.range'

    BM_compatible = True
    PATTERN = """
              power<
                 (name='range'|name='xrange') trailer< '(' args=any ')' >
              rest=any* >
              """

    def start_tree(self, tree, filename):
        super(FixRangeSix, self).start_tree(tree, filename)
        self.transformed_xranges = set()

    def finish_tree(self, tree, filename):
        self.transformed_xranges = None

    def transform(self, node, results):
        name = results["name"]
        touch_import(None, u'six', node)
        if name.value == u"xrange":
            return self.transform_xrange(node, results)
        elif name.value == u"range":
            return self.transform_range(node, results)
        else:
            raise ValueError(repr(name))

    def transform_xrange(self, node, results):
        name = results["name"]
        name.replace(Name(u"six.moves.range", prefix=name.prefix))
        # This prevents the new range call from being wrapped in a list later.
        self.transformed_xranges.add(id(node))

    def transform_range(self, node, results):
        range_call = Call(Name(u"six.moves.range"), [results["args"].clone()])
        if (id(node) not in self.transformed_xranges and
           not self.in_special_context(node)):
            # Encase the range call in list().
            list_call = Call(Name(u"list"), [range_call],
                             prefix=node.prefix)
            # Put things that were after the range() call after the list call.
            for n in results["rest"]:
                list_call.append_child(n)
            return list_call
        range_call.prefix = results['name'].prefix
        return range_call

    P1 = "power< func=NAME trailer< '(' node=any ')' > any* >"
    p1 = patcomp.compile_pattern(P1)

    P2 = """for_stmt< 'for' any 'in' node=any ':' any* >
            | comp_for< 'for' any 'in' node=any any* >
            | comparison< any 'in' node=any any*>
         """
    p2 = patcomp.compile_pattern(P2)

    def in_special_context(self, node):
        if node.parent is None:
            return False
        results = {}
        if (node.parent.parent is not None and
           self.p1.match(node.parent.parent, results) and
           results["node"] is node):
            # list(range()) -> list(six.moves.range()), etc.
            return results["func"].value in consuming_calls
        # for ... in range(...) -> for ... in range(...), etc.
        return self.p2.match(node.parent, results) and results["node"] is node
