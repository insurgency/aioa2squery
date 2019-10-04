Installing
==========

.. _PyPI: https://pypi.org
.. |git| replace:: ``git``
.. _git: https://git-scm.com
.. |pip install sub-command documentation| replace:: ``pip install`` sub-command documentation
.. _pip install sub-command documentation: https://pip.pypa.io/en/stable/reference/pip_install#git

We do **not** provide package distribution via `PyPI`_ for **any** of our
Python libraries. However, we do follow a `semantic versioning scheme
<https://semver.org>`_ with our git_ `release tags
<https://github.com/insurgency/aioa2squery/releases>`_. You can install the
library from the git repository's :github-branch:`stable <stable>` branch,
which denotes that most current stable release version of the library, or
alternatively you can pass a `tag name
<https://github.com/insurgency/aioa2squery/tags>`_ to use a specific pinned
version.

Refer to the |pip install sub-command documentation|_ for more details on
installing `Python packages <https://packaging.python.org/>`_ from
:wikipedia:`version control systems <Version_control>`.

.. note::

   You need to have git_ installed and accessible from your system ``$PATH`` in
   order to run the source cloning  operation with ``pip install
   git+protocol//...``

.. code-block:: shell

   $ # Install the library package using git over HTTPS with pip...
   $ pip3 install 'git+https://github.com/insurgency/aioa2squery.git@stable#egg=aioa2squery'
   $ # Or with Pipenv...
   $ pipenv install 'git+https://github.com/insurgency/aioa2squery.git@stable#egg=aioa2squery'

.. note::

    Our library packages only officially support the most current release
    version of CPython. Any other Python interpreter version is unsupported.

Using Virtualenv or Pipenv
--------------------------

We **highly** recommend users to make use of virtualenv or Pipenv in order to
isolate your project dependencies from that of your system Python installation.
If you have never used or are unfamiliar with virtualenv we recommend you read
the documentation regarding installing Python packages using pip and virtualenv
or the virtualenv documentation itself to get started. This allows you to avoid
bloating your system Python installation packages while simultaneously allowing
you to pin different package versions for use in in an individual project.

Verifying Package Signatures
----------------------------

We make a best effort to use cryptographic signing wherever possible. All of
our publicly distributed Python library packages are signed using `our
organization's PGP public key
<https://gist.github.com/h1nk/a05e040aae61baad1d4836b42d46b772>`_).
