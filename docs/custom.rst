Crafting Custom Queries
=======================

Ideally the majority of library users shouldn't need to craft any custom
queries or responses, but since the query protocol is so divergent and nuanced
across many games and Source Engine versions the library provides some
low-level facilities to easily craft, send custom queries for your particular
needs without having to do any dirty monkey patching.

Firstly a bytes-buffer class is included that inherits :class:`io.BytesIO`
and provides read/write methods for the different :valve-wiki:`packet field
data types <Server_queries#Data_Types>`. This can be useful for any custom
low-level packet crafting or handling with the query protocol or even uses
outside of this library.

.. autoclass:: aioa2squery.A2SBytesIO
    :members:

Custom Query Requests & Responses
---------------------------------

.. autoclass:: aioa2squery.A2SQueryRequest
    :members:
.. autodecorator:: aioa2squery.request
.. autoclass:: aioa2squery.A2SQueryResponse
    :members:
.. autodecorator:: aioa2squery.response

dataclass Field Types
---------------------

.. autoclass:: aioa2squery.Byte
    :show-inheritance:
.. autoclass:: aioa2squery.Short
    :show-inheritance:
.. autoclass:: aioa2squery.Long
    :show-inheritance:
.. autoclass:: aioa2squery.Float
    :show-inheritance:
.. autoclass:: aioa2squery.LongLong
    :show-inheritance:
.. autoclass:: aioa2squery.String
    :show-inheritance:

Helpful Enumeration Mixins
--------------------------

If you are doing any type of custom query crafting you may want to make your
``Byte`` enumerations or whatnot.

Automatic :meth:`object.__str__` method generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: aioa2squery.enumerations.TryLowercaseValueWhenMissingMixin

Automatic :meth:`object.__repr__` method generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: aioa2squery.enumerations.OrdinalByteRepresentationMixin
