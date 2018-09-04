"""Fix bound method attributes (method.im_? -> method.__?__).
Skipping im_class because it not safe.
"""
# Author: Christian Heimes, Timo Stueber

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

MAP = {
    "im_func": "__func__",
    "im_self": "__self__",
    "im_class": "__self__.__class__"
    }


class FixMethodattrs(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """
    power< any+ trailer< '.' attr=('im_func' | 'im_self' | 'im_class') > any* >
    """

    def transform(self, node, results):
        attr = results["attr"][0]
        new = unicode(MAP[attr.value])
        if attr.value == "im_class":
            self.warning(node,
                         """Skipping im_class. This is not safe for unbound """
                         """methods.""")
        else:
            attr.replace(Name(new, prefix=attr.prefix))
