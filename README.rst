=====
Meizi
=====

*Meizi* provides two commands:

- ``mz download`` for downloading nice albums.
- ``mz serve`` for starting a simple web server to serve the albums.

Install
=======

You need to have **Python 3.8+**.

.. code-block:: bash

    $ pip install meizi

Usage
=====

You can run ``mz download`` in one terminal, and run ``mz serve`` in
another terminal.

Then open http://localhost:1310 in your browser.

Commands
========

.. code-block::

    $ mz download --help
    Usage: mz download [OPTIONS]

      Download albums.

    Options:
      --max-workers INTEGER  The number of threads for downloading.  [default: 2]
      --data-dir PATH        The directory to save albums.  [default:
                             /Users/xzmeng/.meizi]
      --help                 Show this message and exit.


.. code-block::

    $ mz serve --help
    Usage: mz serve [OPTIONS]

      Run a local http server.

    Options:
      --data-dir PATH  The directory to read albums.  [default:
                       /Users/xzmeng/.meizi]
      --port INTEGER   The port of the http server.  [default: 1310]
      --help           Show this message and exit.

