# Copyright 2006 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.
# Extended by CONTACT Software GmbH

"""Fixer that turns 'long' into 'int' everywhere.
"""

# Local imports
from lib2to3.fixes import fix_long


class FixLong(fix_long.FixLong):
        run_order = 6
