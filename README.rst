ppping
======

.. image:: https://img.shields.io/pypi/v/ppping.svg
    :target: https://pypi.python.org/pypi/ppping

.. image:: https://img.shields.io/github/license/johejo/ppping.svg
    :target: https://github.com/johejo/ppping

.. image:: https://api.codeclimate.com/v1/badges/aea7bbd42d3b4cf5b4ae/maintainability
   :target: https://codeclimate.com/github/johejo/ppping/maintainability
   :alt: Maintainability


Description
-----------

Petty Plain Ping Tool affected
`deadman <https://github.com/upa/deadman>`__

Demo
----

.. figure:: https://github.com/johejo/ppping/blob/master/demo.gif
   :alt: result

   result

Install
-------

.. code:: bash

    $ pip install ppping

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
