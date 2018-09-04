# Copyright 2008 Armin Ronacher.
# Licensed to PSF under a Contributor Agreement.
# Extended by CONTACT Software GmbH

"""Fixer for reduce().

reduce() -> six.moves.reduce()
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import touch_import, Name


class FixReduce(fixer_base.BaseFix):

    BM_compatible = True
    order = "pre"

    PATTERN = """
    power< name='reduce'
        trailer< '('
            arglist< (
                (not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any) |
                (not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any)
            ) >
        ')' >
    >
    """

    def transform(self, node, results):
        name = results['name']
        name.replace(Name(u'six.moves.reduce', name.prefix))
        touch_import(None, u'six', node)
