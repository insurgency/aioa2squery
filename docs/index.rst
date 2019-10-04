AsyncIO Any to Server (A2S) Query Library
=========================================

This library is an :mod:`asyncio` implementation of the
:valve-wiki:`Any to Server (A2S) query protocol<Server_queries>` for querying
information from :valve-wiki:`Goldsource<Goldsource>` and
:valve-wiki:`Source Engine<Source_Engine>`
:valve-wiki:`servers<Source_Dedicated_Server>`. It provides a simplistic
:ref:`client interface <query-client>` that attempts to handle the nuances of
querying different engine and game versions while allowing users to perform
multiple concurrent queries.

Documentation Contents
----------------------

.. toctree::
    :maxdepth: 3

    installation
    examples
    client
    responses
    custom
    enumerations
    exceptions
    logging
    contributing
