# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.
# Extended by CONTACT Software GmbH

"""Fixer that changes filter(F, X) into list(six.moves.filter(F, X)).

We avoid the transformation if the filter() call is directly contained
in iter(<>), list(<>), tuple(<>), sorted(<>), ...join(<>), or
for V in <>:.

NOTE: This is still not correct if the original code was depending on
filter(F, X) to return a string if X is a string and a tuple if X is a
tuple.  That would require type inference, which we don't do.  Let
Python 2.6 figure it out.
"""

# Local imports
from lib2to3 import fixer_base, pytree
from lib2to3.fixer_util import Name, Call, ListComp, in_special_context
from lib2to3.fixer_util import touch_import


class FixFilter(fixer_base.ConditionalFix):
    skip_on = "six.moves.filter"
    BM_compatible = True

    PATTERN = """
    filter_lambda=power<
        func='filter'
        trailer<
            '('
            arglist<
                lambdef< 'lambda'
                         (fp=NAME | vfpdef< '(' fp=NAME ')'> ) ':' xp=any
                >
                ','
                it=any
            >
            ')'
        >
    >
    |
    power<
        func='filter'
        args=trailer< '(' arglist< none='None' ',' seq=any > ')' >
        rest=any*
    >
    |
    power<
        func='filter'
        args=trailer< '(' [any] ')' >
        rest=any*
    >
    """

    def transform(self, node, results):
        if self.should_skip(node):
            return

        if "filter_lambda" in results:
            new = ListComp(results.get("fp").clone(),
                           results.get("fp").clone(),
                           results.get("it").clone(),
                           results.get("xp").clone())

        elif "none" in results:
            new = ListComp(Name(u"_f"),
                           Name(u"_f"),
                           results["seq"].clone(),
                           Name(u"_f"))

        else:
            if in_special_context(node):
                return None
            func = results['func']
            touch_import(None, u'six', node)
            new = pytree.Node(self.syms.power,
                              [Name(u"six.moves.filter", func.prefix),
                               results['args'].clone()])
            new.prefix = u""
            new = Call(Name(u"list"), [new])
            if "rest" in results:
                for child in results["rest"]:
                    new.append_child(child)
        new.prefix = node.prefix
        return new
