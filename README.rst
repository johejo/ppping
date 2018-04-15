ppping
======

.. image:: https://travis-ci.org/johejo/ppping.svg?branch=master
    :target: https://travis-ci.org/johejo/ppping

.. image:: https://img.shields.io/pypi/v/ppping.svg
    :target: https://pypi.python.org/pypi/ppping

.. image:: https://img.shields.io/github/license/johejo/ppping.svg
    :target: https://raw.githubusercontent.com/johejo/ppping/master/LICENSE

.. image:: https://api.codeclimate.com/v1/badges/aea7bbd42d3b4cf5b4ae/maintainability
   :target: https://codeclimate.com/github/johejo/ppping/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/aea7bbd42d3b4cf5b4ae/test_coverage
   :target: https://codeclimate.com/github/johejo/ppping/test_coverage
   :alt: Test Coverage



Description
-----------

ping monitoring tool written in Python affected
`deadman <https://github.com/upa/deadman>`__

Demo
----

.. figure:: https://github.com/johejo/ppping/blob/master/demo.gif
   :alt: result

Environment
-----------

ppping works using python's curses

List of environments actually checking the operation

- Linux distribution (Ubuntu, ArchLinux)
- Windows Subsystem for Linux (Ubuntu)
- UNIX (macOS)

Requirements
------------

- Python 3.5 or later
- cURL (optional: used to acquire global IP)

Install
-------

From PyPi
~~~~~~~~~~~~~~~~~~~~~~~
.. code:: bash

    $ pip install -U ppping

Standalone (recommended)
~~~~~~~~~~

Download standalone script to a directory that is convenient for you (e.g. "~/.local/bin/" or "/usr/local/bin/")

.. code:: bash

    $ curl "https://raw.githubusercontent.com/johejo/ppping/master/standalone/ppping" -O
    $ chmod +x ppping


Usage
-----

Simple Usage
~~~~~~~~~~~~

.. code:: bash

    $ ppping foo.com bar.org WW.XX.YY.ZZ ...

Future help

.. code:: bash

    $ ppping --help

Config File Usage
~~~~~~~~~~~~~~~~~

.. code:: bash

    $ ppping -c [CONFIG_FILE]

This is a sample of configuration file.

::

    [Hosts]
    google: www.google.com
    google DNS: 8.8.8.8
    GitHub: www.github.com

License
-------

MIT
