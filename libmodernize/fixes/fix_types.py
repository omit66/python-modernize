# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.
# Extended by Contact Software GmbH

"""Fixer for removing uses of the types module.

These work for only the known names in the types module.  The forms above
can include types. or not.  ie, It is assumed the module is imported either as:

    import types
    from types import ... # either * or specific types

The import statements are not modified.

There should be another fixer that handles at least the following constants:

   type([]) -> list
   type(()) -> tuple
   type('') -> str

"""

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name
from lib2to3.fixer_util import touch_import

_TYPE_MAPPING = {
        'BooleanType': 'bool',
        'BufferType': 'memoryview',
        'ClassType': 'six.class_types',
        'ComplexType': 'complex',
        'DictType': 'dict',
        'DictionaryType': 'dict',
        'EllipsisType': 'type(Ellipsis)',
        # 'FileType': 'io.IOBase',
        'FloatType': 'float',
        'IntType': 'int',
        'ListType': 'list',
        'LongType': 'six.integer_types',
        'ObjectType': 'object',
        'NoneType': 'type(None)',
        'NotImplementedType': 'type(NotImplemented)',
        'SliceType': 'slice',
        'StringType': 'six.binary_type',
        'StringTypes': 'six.string_types',
        'TupleType': 'tuple',
        'TypeType': 'type',
        'UnicodeType': 'six.text_type',
        'XRangeType': 'six.moves.range',
    }

_pats = ["power< 'types' trailer< '.' name='%s' > >"
         % t for t in _TYPE_MAPPING]


class FixTypes(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = '|'.join(_pats)

    def transform(self, node, results):
        new_value = unicode(_TYPE_MAPPING.get(results["name"].value))
        if new_value:
            if u'six' in new_value:
                touch_import(None, u'six', node)
            return Name(new_value, prefix=node.prefix)
        return None
