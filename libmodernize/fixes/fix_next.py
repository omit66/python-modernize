"""
Based on fix_next.py by Collin Winter.

Replaces it.next() -> next(it), per PEP 3114.

Like fix_next.py from lib2to3, this fixer replaces the name of a next method
with __next__. Additionally it adds six.iterator as subclass. This is
neccessary to keep the Python 2 compatibility.

Shadowed next will be changed all the same. But the user will be warned.
"""

# Local imports
from lib2to3.pygram import token, python_symbols as syms
from lib2to3 import fixer_base
from lib2to3.fixer_util import (Name, Call, find_binding, LParen, RParen,
                                touch_import, Leaf)

bind_warning = "Calls to builtin next() possibly shadowed by global binding"


class FixNext(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """
    power< base=any+ trailer< '.' attr='next' > trailer< '(' ')' > >
    |
    power< head=any+ trailer< '.' attr='next' > not trailer< '(' ')' > >
    |
    classdef< 'class' any+ colon=':'
        suite< any*
            func=funcdef< 'def' name='next'
                parameters< '(' NAME ')' > any+ >
            any* > >
    |
    global=global_stmt< 'global' any* 'next' any* >
    """
    order = "pre"  # Pre-order tree traversal

    def start_tree(self, tree, filename):
        super(FixNext, self).start_tree(tree, filename)

        n = find_binding('next', tree)
        if n:
            self.warning(n, bind_warning)
            self.shadowed_next = True
        else:
            self.shadowed_next = False

    def transform(self, node, results):
        assert results

        base = results.get("base")
        attr = results.get("attr")
        name = results.get("name")

        if base:
            base = [n.clone() for n in base]
            base[0].prefix = ""
            node.replace(Call(Name("next", prefix=node.prefix), base))
        elif name:
            # rename next -> __next__
            # add next method which calls __next__ (for python2)

            name = results['name']
            # rename old function
            new_name = "__{}__".format(name.value)
            new = Name(new_name, prefix=name.prefix)
            name.replace(new)
            add_iterator_subclass(node, results)
        elif attr:
            # We don't do this transformation if we're assigning to "x.next".
            # Unfortunately, it doesn't seem possible to do this in PATTERN,
            #  so it's being done here.
            if is_assign_target(node):
                head = results["head"]
                if "".join([str(n) for n in head]).strip() == '__builtin__':
                    self.warning(node, bind_warning)
                return
            # Omit this:
            # attr.replace(Name("__next__"))
        elif "global" in results:
            self.warning(node, bind_warning)
            self.shadowed_next = True


# The following functions help test if node is part of an assignment
#  target.
def is_assign_target(node):
    assign = find_assign(node)
    if assign is None:
        return False

    for child in assign.children:
        if child.type == token.EQUAL:
            return False
        elif is_subtree(child, node):
            return True
    return False


def find_assign(node):
    if node.type == syms.expr_stmt:
        return node
    if node.type == syms.simple_stmt or node.parent is None:
        return None
    return find_assign(node.parent)


def is_subtree(root, node):
    if root == node:
        return True
    return any(is_subtree(c, node) for c in root.children)


def insert_object(node, idx, subs=[]):
    node.insert_child(idx, RParen())
    for sub in subs:
        sub.prefix = u' '
        node.insert_child(idx, sub)
        node.insert_child(idx, Leaf(token.COMMA, ','))
    node.insert_child(idx, Name(u"six.Iterator"))
    node.insert_child(idx, LParen())


def add_iterator_subclass(node, results):
    colon = results[u"colon"]
    idx = node.children.index(colon)

    subs = []
    if (node.children[idx-1].value == ')'):
        pos = 2
        while idx - pos >= 0 and not node.children[idx-pos].type == token.LPAR:
            subs.append(node.children[idx - pos])
            pos += 1
        del node.children[idx-pos:idx]
        idx -= pos
    insert_object(node, idx, subs)
    touch_import(None, u'six', node)
