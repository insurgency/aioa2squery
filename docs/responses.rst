Responses
=========

Query responses are defined as :mod:`dataclasses`, which allows them to be
defined in a :wikipedia:`DRY <Don't_repeat_yourself>` and declarative way. This
also means any response object can be converted to a dictionary and serialized
which is useful for saving response data in storage systems like databases,
caches, or a data structure store like redis.

.. doctest::

    >>> from aioa2squery import A2SInfoResponse
    >>> from dataclasses import asdict
    >>> from pickle import dumps, loads
    >>> A2SInfoResponse()
    >>> ...
    >>> dumps(asdict(_))
    >>> ...
    >>> loads(_)

.. warning::

    The ping value returned with all responses is not of high accuracy. From
    extensive testing against the and should only be used for a very rough
    estimation of round-trip delay.

All client query responses return a 2 tuple of the actual response object along
with server ping in millisecond resolution.

Server Info
-----------

The following :mod:`dataclasses` wrap information from the different types of
query responses.

.. autoclass:: aioa2squery.A2SInfoResponse
    :members:

Server Players
--------------

.. autoclass:: aioa2squery.A2SPlayersResponse
    :members:
.. autoclass:: aioa2squery.A2SPlayer
    :members:

Server Rules
------------

.. autoclass:: aioa2squery.A2SRulesResponse
    :members:
.. autoclass:: aioa2squery.A2SRule
    :members:
