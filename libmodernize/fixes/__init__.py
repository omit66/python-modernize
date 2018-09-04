
lib2to3_fix_names = set([
    'lib2to3.fixes.fix_apply',
    'lib2to3.fixes.fix_except',
    'lib2to3.fixes.fix_exec',
    'lib2to3.fixes.fix_execfile',
    'lib2to3.fixes.fix_exitfunc',
    'lib2to3.fixes.fix_funcattrs',
    'lib2to3.fixes.fix_has_key',
    'lib2to3.fixes.fix_idioms',
    'lib2to3.fixes.fix_long',
    'lib2to3.fixes.fix_methodattrs',
    'lib2to3.fixes.fix_ne',
    'lib2to3.fixes.fix_numliterals',
    'lib2to3.fixes.fix_operator',
    'lib2to3.fixes.fix_paren',
    'lib2to3.fixes.fix_reduce',
    'lib2to3.fixes.fix_renames',
    'lib2to3.fixes.fix_repr',
    'lib2to3.fixes.fix_set_literal',
    'lib2to3.fixes.fix_standarderror',
    'lib2to3.fixes.fix_sys_exc',
    'lib2to3.fixes.fix_throw',
    'lib2to3.fixes.fix_tuple_params',
    'lib2to3.fixes.fix_types',
    'lib2to3.fixes.fix_ws_comma',
    'lib2to3.fixes.fix_xreadlines'
])

# This fixers may not be safe
lib2to3_fix_names_stage2 = set([
    'lib2to3.fixes.fix_numliterals',    # turns 1L into 1, 0755 into 0o755
    'lib2to3.fixes.fix_operator',    # we will need support for this by e.g.
    # extending the Py2 operator module to

])

# fixes that involve using six
six_fix_names = set([
    'libmodernize.fixes.fix_basestring',
    'libmodernize.fixes.fix_chr',
    'libmodernize.fixes.fix_dict_six',
    'libmodernize.fixes.fix_filter',
    'libmodernize.fixes.fix_getcwdu',
    'libmodernize.fixes.fix_imports_six',
    'libmodernize.fixes.fix_input_six',
    'libmodernize.fixes.fix_int_long_tuple',
    'libmodernize.fixes.fix_itertools_six',
    'libmodernize.fixes.fix_itertools_imports_six',
    'libmodernize.fixes.fix_long',
    'libmodernize.fixes.fix_long_typechecks',
    'libmodernize.fixes.fix_map',
    'libmodernize.fixes.fix_metaclass',
    'libmodernize.fixes.fix_methodattrs',  # is not complete (im_class is skipped)
    'libmodernize.fixes.fix_next',
    'libmodernize.fixes.fix_nonzero',
    'libmodernize.fixes.fix_raise_six',
    'libmodernize.fixes.fix_range_six',
    'libmodernize.fixes.fix_reduce',
    'libmodernize.fixes.fix_types',
    'libmodernize.fixes.fix_unichr',
    'libmodernize.fixes.fix_unicode',
    'libmodernize.fixes.fix_unicode_type',
    'libmodernize.fixes.fix_urllib_six',
    'libmodernize.fixes.fix_unichr',
    'libmodernize.fixes.fix_xrange_six',
    'libmodernize.fixes.fix_zip',
])

# Fixes that are opt-in only.
opt_in_fix_names = set([
    'libmodernize.fixes.fix_classic_division',
    'libmodernize.fixes.fix_open',
])


# The following fixers are "safe": they convert Python 2 code to more
# modern Python 2 code. They should be uncontroversial to apply to most
# projects that are happy to drop support for Py2.5 and below. Applying
# them first will reduce the size of the patch set for the real porting.
lib2to3_fix_names_stage1 = set([
    'lib2to3.fixes.fix_apply',
    'lib2to3.fixes.fix_except',
    'lib2to3.fixes.fix_exec',
    'lib2to3.fixes.fix_exitfunc',
    'lib2to3.fixes.fix_funcattrs',
    'lib2to3.fixes.fix_has_key',  # not safe if you have method has_key
    'lib2to3.fixes.fix_ne',
    'lib2to3.fixes.fix_paren',
    'lib2to3.fixes.fix_renames',        # sys.maxint -> sys.maxsize
    'lib2to3.fixes.fix_repr',
    'lib2to3.fixes.fix_standarderror',
    'lib2to3.fixes.fix_sys_exc',
    'lib2to3.fixes.fix_throw',
    'lib2to3.fixes.fix_tuple_params',
    'lib2to3.fixes.fix_xreadlines',
])

# This fixers may not be safe
lib2to3_fix_names_stage2 = set([
    'lib2to3.fixes.fix_numliterals',    # turns 1L into 1, 0755 into 0o755
    'lib2to3.fixes.fix_operator',    # we will need support for this by e.g.
    # extending the Py2 operator module to
])

libmodernize_fix_names_stage1 = set([
    'libmodernize.fixes.fix_intern',
    'libmodernize.fixes.fix_print',
    'libmodernize.fixes.fix_raise',
])

libmodernize_fix_names_stage2 = set([
    'libmodernize.fixes.fix_basestring',
    'libmodernize.fixes.fix_chr',
    'libmodernize.fixes.fix_cmp_inline',
    'libmodernize.fixes.fix_dict_six',
    'libmodernize.fixes.fix_filter',
    'libmodernize.fixes.fix_getcwdu',
    'libmodernize.fixes.fix_imports_six',
    'libmodernize.fixes.fix_input_six',
    'libmodernize.fixes.fix_itertools_six',
    'libmodernize.fixes.fix_itertools_imports_six',
    'libmodernize.fixes.fix_long',
    'libmodernize.fixes.fix_long_typechecks',
    'libmodernize.fixes.fix_metaclass',
    'libmodernize.fixes.fix_methodattrs',  # is not complete (im_class is skipped)
    'libmodernize.fixes.fix_map',
    # 'libmodernize.fixes.fix_newstyle', this is not safe
    'libmodernize.fixes.fix_next',
    'libmodernize.fixes.fix_nonzero',
    'libmodernize.fixes.fix_range_six',
    'libmodernize.fixes.fix_reduce',
    'libmodernize.fixes.fix_types',
    'libmodernize.fixes.fix_unichr',
    'libmodernize.fixes.fix_unicode_type',
    'libmodernize.fixes.fix_urllib_six',
    'libmodernize.fixes.fix_zip',
])
