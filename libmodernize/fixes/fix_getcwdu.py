"""
Fixer that changes os.getcwdu() to six.getcwdu().
And changes getcwdu to six.getcwdu if an 'from os import getcwdu' statement
was found.
This is still not safe. The imports should be checked and removed.
"""
# Author: Victor Stinner, Timo Stueber

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, find_binding, find_root
from lib2to3.fixer_util import touch_import


class FixGetcwdu(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = """
              power< mod='os' trailer< dot='.' name='getcwdu' > any* >
              |
              power< name='getcwdu' trailer< '(' ')' > >
              """

    def transform(self, node, results):
        os_import = find_binding("getcwdu", find_root(node), "os")
        new_mod = u"six"
        name = results["name"]
        if os_import:
            # we can find only from imports...
            # TODO: remove import and change getcwdu
            # os_import.parent.remove()
            touch_import(None, new_mod, node)
            new_name = new_mod + '.moves.' + name.value
            name.replace(Name(new_name, prefix=name.prefix))
        elif "mod" in results:
            touch_import(None, new_mod, node)
            mod = results["mod"]
            mod.replace(Name(new_mod + '.moves', prefix=mod.prefix))

        return node
