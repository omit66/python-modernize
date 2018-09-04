# This is a derived work of Lib/lib2to3/fixes/fix_itertools_import.py. That
# file is under the copyright of the Python Software Foundation and licensed
# under the Python Software Foundation License 2.
#
# Copyright notice:
#
#     Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
#     2011, 2012, 2013 Python Software Foundation. All rights reserved.
# Extendet by CONTACT Software GmbH

""" Fixer for itertools.(imap|ifilter|izip) -->
    (six.moves.map|six.moves.filter|six.moves.zip) and
    itertools.ifilterfalse --> six.moves.filterfalse (bugs 2360-2363)
    imports from itertools are fixed in fix_itertools_imports_six.py
    If itertools is imported as something else (ie: import itertools as it;
    it.izip(spam, eggs)) method calls will not get fixed.
    """

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

from lib2to3.fixer_util import touch_import


class FixItertoolsSix(fixer_base.BaseFix):
    BM_compatible = True
    it_funcs = "('imap'|'ifilter'|'izip'|'izip_longest'|'ifilterfalse')"
    PATTERN = """
              power< it='itertools'
                  trailer<
                     dot='.' func=%(it_funcs)s > trailer< '(' [any] ')' > >
              |
              power< func=%(it_funcs)s trailer< '(' [any] ')' > >
              """ % (locals())

    # Needs to be run after fix_(map|zip|filter)
    run_order = 6

    def transform(self, node, results):
        touch_import(None, u'six', node)
        func = results['func'][0]
        if 'it' in results:
            dot, it = (results['dot'], results['it'])
            # Remove the 'itertools'
            func.prefix = it.prefix
            it.remove()
            # Replace the node wich contains ('.', 'function') with the
            # function (to be consistant with the second part of the pattern)
            dot.remove()
            func.parent.replace(func)
        func.replace(Name(u'six.moves.' + func.value[1:], prefix=func.prefix))
