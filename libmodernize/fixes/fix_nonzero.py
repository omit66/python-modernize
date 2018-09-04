"""Fixer for __nonzero__ -> __bool__ methods.
Creates new __nonzero__ for python2 compability.
"""
# Extended by CONTACT Software GmbH
# Author: Collin Winter, Timo Stueber


# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, find_indentation, Call
from lib2to3.pytree import Node, Leaf
from lib2to3.pygram import token


class FixNonzero(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """
    classdef< 'class' any+ ':'
              suite< any*
                     func=funcdef< 'def' name='__nonzero__'
                              parameters< '(' NAME ')' > any+ >
                     any* > >
    """

    def transform(self, node, results):
        name = results["name"]
        func = results['func']
        new = Name(u"__bool__", prefix=name.prefix)
        name.replace(new)
        indentation = find_indentation(results['func'])
        # create a nonzero func
        nonzero = Node(self.syms.funcdef,
                       [Name('def', prefix=func.prefix),
                        Name('__nonzero__', prefix=name.prefix),
                        # (self):
                        Node(self.syms.parameters,
                             [Leaf(token.LPAR, '('),
                              Name('self'),
                              Leaf(token.RPAR, ')'),
                              Leaf(token.COLON, ':'),
                              Leaf(token.NEWLINE, '\n')]),
                        # return __bool__(self)
                        Node(self.syms.simple_stmt,
                             [Node(self.syms.return_stmt,
                                   [Name('return', prefix=indentation + ' '*4),
                                    Node(self.syms.power,
                                         # self.__bool__()
                                         [Call(Name('self.__bool__', u' '))])
                                    ])
                              ]),
                        # insert blank line
                        Leaf(token.NEWLINE, '\n'),
                        Leaf(token.NEWLINE, '\n')
                        ],
                       prefix=func.prefix)
        # __bool__ func
        bool_func = func.clone()
        bool_func.prefix = indentation
        func.replace([nonzero, bool_func])
