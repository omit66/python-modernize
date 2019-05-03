# Taken from libmodernize
from lib2to3.fixes import fix_imports
from lib2to3.fixer_util import Name

MAPPING = {
    '__builtin__': 'six.moves.builtins',
    '_winreg': 'six.moves.winreg',
    'BaseHTTPServer': 'six.moves.BaseHTTPServer',
    'CGIHTTPServer': 'six.moves.CGIHTTPServer',
    'ConfigParser': 'six.moves.configparser',
    'copy_reg': 'six.moves.copyreg',
    'Cookie': 'six.moves.http_cookies',
    'cookielib': 'six.moves.http_cookiejar',
    'cPickle': 'six.moves.cPickle',
    'Dialog': 'six.moves.tkinter_dialog',
    'dummy_thread': 'six.moves._dummy_thread',
    'cStringIO.StringIO': 'six.moves.cStringIO',
    # email.MIMEBase
    # email.MIMEMultipart
    # email.MIMENonMultipart
    # email.MIMEText
    'email.MIMEMultipart': 'email_mime_multipart',
    'email.MIMENonMultipart':  'email_mime_nonmultipart',
    'email.MIMEText':  'email_mime_text',
    'email.MIMEBASE': 'email_mime_base',

    'FileDialog': 'six.moves.tkinter_filedialog',
    'gdbm': 'six.moves.dbm_gnu',
    'htmlentitydefs': 'six.moves.html_entities',
    'HTMLParser': 'six.moves.html_parser',
    'httplib': 'six.moves.http_client',
    # intern()
    # itertools.ifilter()
    # itertools.ifilterfalse()
    # itertools.imap()
    # itertools.izip()
    # itertools.zip_longest()
    # pipes.quote
    'Queue': 'six.moves.queue',
    # reduce()
    # reload()
    'repr': 'six.moves.reprlib',
    'robotparser': 'six.moves.urllib_robotparser',
    'ScrolledText': 'six.moves.tkinter_scrolledtext',
    'SimpleDialog': 'six.moves.tkinter_simpledialog',
    'SimpleHTTPServer': 'six.moves.SimpleHTTPServer',
    'SimpleXMLRPCServer': 'six.moves.xmlrpc_server',
    'SocketServer': 'six.moves.socketserver',
    'thread': 'six.moves._thread',
    'Tix': 'six.moves.tkinter_tix',
    'tkColorChooser': 'six.moves.tkinter_colorchooser',
    'tkCommonDialog': 'six.moves.tkinter_commondialog',
    'Tkconstants': 'six.moves.tkinter_constants',
    'Tkdnd': 'six.moves.tkinter_dnd',
    'tkFileDialog': 'six.moves.tkinter_filedialog',
    'tkFont': 'six.moves.tkinter_font',
    'Tkinter': 'six.moves.tkinter',
    'tkMessageBox': 'six.moves.tkinter_messagebox',
    'tkSimpleDialog': 'six.moves.tkinter_tksimpledialog',
    'ttk': 'six.moves.tkinter_ttk',
    # urllib
    'urlparse': 'six.moves.urllib.parse',
    # UserDict.UserDict
    # UserList.UserList
    # UserString.UserString
    'xmlrpclib': 'six.moves.xmlrpc_client',
}


def alternates(members):
    return "(" + "|".join(map(add_trailer, members)) + ")"


def build_pattern(mapping=MAPPING):
    mod_list = ' | '.join(["module_name={}".format(add_dotted_names(key)) for key in mapping])
    bare_names = alternates(mapping.keys())

    yield """name_import=import_name< 'import' ((%s) |
               multiple_imports=dotted_as_names< any* (%s) any* >) >
          """ % (mod_list, mod_list)
    yield """import_from< 'from' (%s) 'import' ['(']
              ( any | import_as_name< any 'as' any > |
                import_as_names< any* >)  [')'] >
          """ % mod_list
    yield """import_name< 'import' (dotted_as_name< (%s) 'as' any > |
               multiple_imports=dotted_as_names<
                 any* dotted_as_name< (%s) 'as' any > any* >) >
          """ % (mod_list, mod_list)

    # Find usages of module members in code e.g. thread.foo(bar)
    yield "power< bare_with_attr=(%s) trailer<'.' any > any* >" % bare_names


def add_dotted_names(full_name):
    if '.' in full_name:
        name, attr = full_name.split('.', 1)
        return "dotted_name< name='{}' '.' attr='{}' >".format(name, attr)
    return "'{}'".format(full_name)


def add_trailer(full_name):
    if '.' in full_name:
        name, attr = full_name.split('.', 1)
        return "(name='{}' trailer<'.' attr='{}' >)".format(name, attr)
    return repr(full_name)


class FixImportsSix(fix_imports.FixImports):
    mapping = MAPPING

    def build_pattern(self):
        return "|".join(build_pattern(self.mapping))

    def transform(self, node, results):
        import_mod = results.get("module_name")
        if import_mod:
            if not hasattr(import_mod, "value"):
                mod_name = str(import_mod).strip()
            else:
                mod_name = import_mod.value
            new_name = self.mapping[mod_name]
            import_mod.replace(Name(new_name, prefix=import_mod.prefix))
            if "name_import" in results:
                # If it's not a "from x import x, y" or "import x as y" import,
                # marked its usage to be replaced.
                self.replace[mod_name] = new_name
            if "multiple_imports" in results:
                # This is a nasty hack to fix multiple imports on a line (e.g.,
                # "import StringIO, urlparse"). The problem is that I can't
                # figure out an easy way to make a pattern recognize the keys of
                # MAPPING randomly sprinkled in an import statement.
                results = self.match(node)
                if results:
                    self.transform(node, results)
        else:
            # Replace usage of the module.
            bare_name = results["bare_with_attr"]
            bare_name_str = ''.join(map(str, bare_name))

            new_name = self.replace.get(bare_name_str)
            if new_name:
                # clear list
                if len(bare_name) > 1:
                    for x in bare_name[1:]:
                        x.remove()

                bare_name = bare_name[0]
                prefix = bare_name.prefix
                bare_name.replace(Name(new_name, prefix=prefix))
