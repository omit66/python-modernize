# Copyright 2006 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.
# Extended by CONTACT Software GmbH

"""Fixer that turns 'long()' into 'int'().
(int, long) -> six.integer_types
(y, long) -> (y,) + six.integer_types
(int, long, bool) -> (bool,) + six.integer_types



type(..) == long -> type(..) in six.integer_type
type(..) is long -> type(..) in six.integer_type

isinstance(x, long) -> isinstance(x, six.integer_types)

"""

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, token
from lib2to3.pytree import Node, Leaf

from lib2to3.fixer_util import touch_import


class FixLongTypechecks(fixer_base.BaseFix):
    PATTERN = """
                power < 'isinstance'
                    trailer< '(' arglist< any ',' int_type='long' > ')'>
                >
                |
                comparison<
                    power< 'type' trailer< '(' any ')' > >
                    comp=('=='|'is')
                    int_type='long'>
                |
                tup=atom< '('
                    args=testlist_gexp< (any* 'long' any*)  > ')' >
                """

    def transform(self, node, results):
        if 'int_type' in results:
            int_type = results['int_type']
            if 'comp' in results:
                comp = results['comp'][0]
                comp.value = 'in'
                comp.changed()
            int_type.value = u"six.integer_types"
            int_type.changed()
            touch_import(None, u'six', node)
        elif 'tup' in results:
            touch_import(None, u'six', node)
            args = results['args']
            tup = results['tup']

            children = args.children[:]
            num_children = self.removeIntegers(children)
            # there is no item left
            if num_children == 0:
                tup.replace(Name(u'six.integer_types', tup.prefix))
            else:
                children = args.children[:]
                self.removeComma(children)

                # reset the prefix of the first element
                if args.children[0]:
                    args.children[0].prefix = u''

                # add a comma if the tuple has one element
                if args.children[-1].type != token.COMMA and \
                   len(args.children) == 1:
                    args.children.append(Leaf(token.COMMA, u','))

                new = Name(u'six.integer_types', u' ')
                new = Node(self.syms.arith_expr,
                           [tup.clone(),
                            Leaf(token.PLUS, u'+', prefix=u' '),
                            new])
                tup.replace(new)

    def removeComma(self, children):
        remove_comma = True
        for child in children:
            if remove_comma and child.type == token.COMMA:
                child.remove()
            else:
                remove_comma ^= True

    def removeIntegers(self, children):
        # no comma
        num_childs = 0
        for child in children:
            if hasattr(child, 'value'):
                val = child.value
                if val in ('int', 'long'):
                    child.remove()
                    continue
            if child.type != token.COMMA:
                num_childs = num_childs + 1
        return num_childs
