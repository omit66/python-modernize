# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.
# This work has been extended by CONTACT Software GmbH.

"""Fixer for dict methods.

d.keys() -> list(d)
d.items() -> import six\nlist(six.iteritems(d))
d.values() -> import six\nlist(six.itervalues(d))

d.iterkeys() ->  import six\nsix.iterkeys(d)
d.iteritems() ->  import six\nsix.iteritems(d)
d.itervalues() ->  import six\nsix.itervalues(d)

d.viewkeys() ->  import six\nsix.viewkeys(d)
d.viewitems() ->  import six\nsix.viewitems(d)
d.viewvalues() ->  import six\nsix.viewvalues(d)

Except in certain very specific contexts: the iter() can be dropped
when the context is list(), sorted(), iter() or for...in; the list()
can be dropped when the context is list() or sorted() (but not iter()
or for...in!). Special contexts that apply to both: list(), sorted(), tuple()
set(), any(), all(), sum().
"""

# Local imports
from lib2to3 import patcomp, pytree, fixer_base
from lib2to3.fixer_util import Name, Call
from lib2to3 import fixer_util
from lib2to3.fixer_util import touch_import


iter_exempt = fixer_util.consuming_calls | set(["iter"])


class FixDictSix(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = """
    power< head=any+
         trailer< '.' method=('keys'|'items'|'values'|
                              'iterkeys'|'iteritems'|'itervalues'|
                              'viewkeys'|'viewitems'|'viewvalues') >
         parens=trailer< '(' ')' >
         tail=any*
    >
    """

    def transform(self, node, results):
        head = results["head"]
        method = results["method"][0]  # Extract node for method name
        tail = results["tail"]
        syms = self.syms
        method_name = method.value
        isiter = method_name.startswith(u"iter")
        isview = method_name.startswith(u"view")
        head = [n.clone() for n in head]
        tail = [n.clone() for n in tail]
        # no changes neccessary if the call is in a special context
        self.parentIsList = False
        special = not tail and self.in_special_context(node, isiter or isview)
        new = pytree.Node(syms.power, head)
        new.prefix = u""
        if isiter or isview:
            # replace the method with the six function
            # e.g. d.iteritems() -> from six import iteritems\n iteritems(d)
            new = Call(Name('six.' + method_name), [new])
            touch_import(None, 'six', node)
        elif special:
            # it is not neccessary to change this case
            return node
        elif method_name in ("items", "values"):
            # ensure to return a list in python 3
            new = Call(Name(u"six.iter" + method_name), [new])
            new = Call(Name('list'), [new])
            touch_import(None, 'six', node)
        else:
            # method_name is "keys"; removed it and cast the dict to list
            new = Call(Name(u"list"), [new])

        if tail:
            new = pytree.Node(syms.power, [new] + tail)
        new.prefix = node.prefix
        return new

    P1 = "parent=power< func=NAME trailer< '(' node=any ')' > any* >"
    p1 = patcomp.compile_pattern(P1)

    def in_special_context(self, node, isiter):
        # it is not wrapped
        if node.parent is None:
            return False
        results = {}
        if (node.parent.parent is not None and
           self.p1.match(node.parent.parent, results) and
           results["node"] is node):

            # list(d.keys()) -> list(d), etc.
            # py2 keys() return a list and list(d.keys()) would be inefficcient
            if results['func'].value == 'list' and not isiter:
                # remove the call list if the child is not an iterator
                results['parent'].replace([node])
                return False
            return results["func"].value in fixer_util.consuming_calls
        return False
