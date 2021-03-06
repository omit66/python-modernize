# This file is taken from python-future

# test case for fixers, taken from future
from __future__ import absolute_import
import os
import os.path
from itertools import chain
from textwrap import dedent
from lib2to3 import refactor

# Local imports
from future.tests.base import unittest

test_dir = os.path.dirname(__file__)
proj_dir = os.path.normpath(os.path.join(test_dir, ".."))


def run_all_tests(test_mod=None, tests=None):
    if tests is None:
        tests = unittest.TestLoader().loadTestsFromModule(test_mod)
    unittest.TextTestRunner(verbosity=2).run(tests)


def reformat(string):
    return dedent(string) + u"\n\n"


def get_refactorer(fixer_pkg="lib2to3", fixers=None, options=None):
    """
    A convenience function for creating a RefactoringTool for tests.

    fixers is a list of fixers for the RefactoringTool to use. By default
    "lib2to3.fixes.*" is used. options is an optional dictionary of options to
    be passed to the RefactoringTool.
    """
    if fixers is not None:
        fixers = [fixer_pkg + ".fixes.fix_" + fix for fix in fixers]
    else:
        fixers = refactor.get_fixers_from_package(fixer_pkg + ".fixes")
    options = options or {}
    return refactor.RefactoringTool(fixers, options, explicit=True)


def all_project_files():
    for dirpath, dirnames, filenames in os.walk(proj_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                yield os.path.join(dirpath, filename)


class FixerTestCase(unittest.TestCase):

    # Other test cases can subclass this class and replace "fixer_pkg" with
    # their own.
    def setUp(self, fix_list=None, fixer_pkg="libmodernize", options=None):
        if fix_list is None:
            fix_list = [self.fixer]
        self.refactor = get_refactorer(fixer_pkg, fix_list, options)
        self.fixer_log = []
        self.filename = u"<string>"

        for fixer in chain(self.refactor.pre_order,
                           self.refactor.post_order):
            fixer.log = self.fixer_log

    def _check(self, before, after):
        before = reformat(before)
        after = reformat(after)
        tree = self.refactor.refactor_string(before, self.filename)
        self.assertEqual(after, str(tree))
        return tree

    def check(self, before, after, ignore_warnings=False):
        tree = self._check(before, after)
        self.assertTrue(tree.was_changed)
        if not ignore_warnings:
            self.assertEqual(self.fixer_log, [])

    def warns(self, before, after, message, unchanged=False):
        tree = self._check(before, after)
        self.assertTrue(message in "".join(self.fixer_log))
        if not unchanged:
            self.assertTrue(tree.was_changed)

    def warns_unchanged(self, before, message):
        self.warns(before, before, message, unchanged=True)

    def unchanged(self, before, ignore_warnings=False):
        self._check(before, before)
        if not ignore_warnings:
            self.assertEqual(self.fixer_log, [])

    def assert_runs_after(self, *names):
        fixes = [self.fixer]
        fixes.extend(names)
        # fixer is in lib2to3 or in libfutuirze
        try:
            r = get_refactorer("lib2to3", fixes)
        except ImportError:
            r = get_refactorer("libmodernize", fixes)
        (pre, post) = r.get_fixers()
        n = "fix_" + self.fixer
        if post and post[-1].__class__.__module__.endswith(n):
            # We're the last fixer to run
            return
        if pre and pre[-1].__class__.__module__.endswith(n) and not post:
            # We're the last in pre and post is empty
            return
        self.fail("Fixer run order (%s) is incorrect; %s should be last."
                  % (", ".join([x.__class__.__module__ for x in (pre + post)]),
                     n))
