This project is based on
`Python-Modernize <https://github.com/python-modernize/python-modernize>`_.
We added serveral new fixers and changed the testing inspired by futurize.

This library is a very thin wrapper around `lib2to3
<https://github.com/python/cpython/tree/master/Lib/lib2to3>`_ to utilize it
to make Python 2 code more modern with the intention of porting it over to
Python 3.

The ``python-modernize`` command works like `2to3
<https://docs.python.org/3/library/2to3.html>`_. Here's how you'd rewrite a
single file::

    python-modernize -w example.py


We recommend to run without the ``-w`` option and check the output before
writing it. We also introduce two stages, which only include a part of all
fixers. The first stage (``-1``) includes fixers modernizing python 2 code and do not
create python 3 compability. This stage should quite safe to run.
The second stage (``-2``) should produce code which is compatible between python2 and
python 3. It is not guaranteet that this fixers are working as expected.
You should check the output very carefully.

The option ``-l`` can be used to list the applied fixer.
Here is how to list the fixer for the first stage::

    python-modernize -1 -l


The default option is to run both stages.
It does not guarantee, but it attempts to spit out a codebase compatible
with Python 2.6+ or Python 3. The code that it generates has a runtime
dependency on `six <https://pypi.python.org/pypi/six>`_.

In comparison to the original project, we tried to use full import namespaces
when using functions. E.g. we just use ``import six`` and call
``six.moves.urllib.parse.urlparse(...)``. We want to make it easier to
track situations where Python 2 and Python3 compatibility is necessary. Another
reason was issues regarding the garbage collection when resolving the
dependencies. We also created a stages of fixer simliar to futurize. You dont
have to run all fixers at once.

**Testing:**
Tests can be found under ´´./tests´´. We changed to test one fixer at a time
instead of running all fixer at once. That makes it possible to test the fixers
independently.

Run tests::

    python setup.py test


**Modernize Documentation:** `python-modernize.readthedocs.io
<https://python-modernize.readthedocs.io/>`_.

See the ``LICENSE`` file for the license of ``python-modernize``.
Using this tool does not affect licensing of the modernized code.
