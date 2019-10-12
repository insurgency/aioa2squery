Examples
========

This page shows several brief code examples for making different types of
server queries and also demonstrates how the :ref:`query client <query-client>`
can be used to execute queries concurrently.

Simple Individual Queries
-------------------------

The following code examples show how to perform the different types of query
requests available in the `protocol
<https://developer.valvesoftware.com/wiki/Server_queries#Requests>`_ as well as
access data from the corresponding response objects.

Querying Server Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This query retrieves basic information about the server such as the
:valve-wiki:`hostname <Hostname>` of the server and the name of the current
:valve-wiki:`map <Map>` being played.

.. testcode::

    import asyncio
    from aioa2squery import A2SQueryContext

    async def main():
        client = A2SQueryContext()

        try:
            response, ping = await client.query_info('example.com')
        except asyncio.TimeoutError:
            print("Query timed out")
        else:
            print(f"{response.name}: {response.game}")

    asyncio.run(main())

.. testoutput::
   :hide:
   :options: +ELLIPSIS

   ...

Querying Online Players
^^^^^^^^^^^^^^^^^^^^^^^

This query response returns a list of player objects.

.. note::

    .. code-block:: python

        # These two values are not necessarily the same number!
        len(A2SPlayersResponse) != len(A2SPlayersResponse.players)

.. testcode::

    import asyncio
    from aioa2squery import A2SQueryContext

    async def main():
        client = A2SQueryContext()

        try:
            response, _ = await client.query_players('example.com')
        except asyncio.TimeoutError:
            print("Query timed out")
            return

        for player in sorted(response, key=lambda p: p.score, reverse=True):
            print(player, player.score)

    asyncio.run(main())

.. testoutput::
   :hide:
   :options: +ELLIPSIS

   ...

Querying Server Configuration Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import asyncio
    from aioa2squery import A2SQueryContext

    async def main():
        client = A2SQueryContext()

        try:
            rules_list = client.query_rules()
        except asyncio.TimeoutError:
            print("Query timed out")
            return

        try:
            # Rules responses implement dict-like behavior for key lookups
            bomb_time = int(rules_list['mp_c4timer'])
        except KeyError, ValueError:
            print("Unable to determine the server's bomb timer")
        else:
            print("The bomb takes", bomb_time, "seconds to explode")

    asyncio.run(main())


Multiple Concurrent Queries
---------------------------

Now let's actually leverage :mod:`asyncio` to execute multiple concurrent
queries. Here we're querying a few ports across a single host:

.. code-block:: python

    import asyncio

    from aioa2squery import A2SQueryContext

    async def main():
        client = A2SQueryContext()
        host = '127.0.0.1'

        queries = list()

        for i range(27050, 27053):
            queries.append(client.query_info(host, i))

        # Schedule query calls concurrently and capture exceptions
        completed, _ = await asyncio.wait(*queries, return_when=ALL_COMPLETED)

        # Show results for each ping
        for task in completed:
            if not task.exception():
                response, ping = task.result()
                print(f'Name: {response.name} ({ping}ms)')

    asyncio.run(main())

Querying A /22 Network
----------------------

In the following example we'll *attempt* to query all of the hosts on a
contiguous :math:`/22` network prefix allocated to `Valve Corporation
<https://whois.arin.net/rest/net/NET-208-78-164-0-1>`_. We'll iterate over an
:class:`IPv4Network <ipaddress.IPv4Network>` that we create with the
:obj:`ip_network <ipaddress.ip_network>` function and query several hosts
concurrently using the default :valve-wiki:`Source Dedicated Server
<Source_Dedicated_Server>` port of :math:`27015`.

Since we're going to be querying such a large network block
(:math:`2^{32-22}=1024` hosts) we may want to limit the concurrent execution of
our queries in order to avoid exceeding any socket/open :wikipedia:`file
descriptor<File_descriptor>` resource limits. Additionally, we'll reduce the
memory consumption by scheduling subsequent queries as previous ones complete
or timeout, rather than eagerly creating `all` 1,024 :class:`Task
<asyncio.Task>` objects beforehand.

All of this can be achieved fairly easily using some of
:mod:`asyncio`'s built-in :ref:`synchronization primitives <asyncio-sync>`:

.. testcode::

    import asyncio
    from functools import partial
    from aioa2squery import A2SQueryContext
    from ipaddress import ip_network
    
    # Set for tracking currently running queries
    query_tasks = set()
    
    async def start():
        # A query client instance is needed as always
        query_client = A2SQueryContext(timeout=1.5)
        # Using a semaphore we can limit the concurrency of our queries
        sem = asyncio.Semaphore(25)
        
        # Callback function for printing completed query results
        def print_query_result(host, query_task):
            # Print results for queries that completed without errors...
            if not query_task.exception():
                response, _ = query_task.result()
                players = "{0.players}/{0.max_players}".format(response)
                print(f"{host}: {response.name} ({players})")
        
            # Remove finished task and release semaphore
            query_tasks.remove(query_task)
            sem.release()
        
        # Loop over hosts in this IPv4 network
        for ip in ip_network('208.78.164.0/22'):
            # Suspend loop while we're unable to queue additional queries
            await sem.acquire()
            
            # Schedule the query as a task
            query = query_client.query_info(str(ip))
            task = asyncio.create_task(query)
            # Attach our done callback for printing task results
            task.add_done_callback(partial(print_query_result, ip))
            # Add the task to the set
            query_tasks.add(task)
        
        # Await remaining tasks to complete
        await asyncio.gather(*query_tasks, return_exceptions=True)
    
    asyncio.run(start())


.. testoutput::
   :hide:
   :options: +ELLIPSIS

   ...

We can watch the execution behavior of the semaphore mechanism by monitoring
the total number of open socket file descriptors while the script is running:

.. code-block:: shell

    $ # The bound of our semaphore limits the amount of open sockets
    $ sudo watch "lsof -n -i4UDP:27015 | wc -l"

We can also roughly estimate the `expected` execution time given the
concurrency, number of tasks, and the configured timeout duration:

.. code-block:: python

    >>> round(1_024 * 1.5 / 25)
    >>> 61 # Should take a maximum of a little less than a minute to complete
    >>> # Testing this using a simple timing benchmark:
    >>> loop = asyncio.get_even_loop(); before = loop.time()
    >>> loop.run_until_complete(start()); after = loop.time()
    >>> print("Completed in", round(after - before), "seconds")
    >>> ...

.. TODO: make into doctest

.. note::

    The library includes a more full-fledged version of the above code as a
    single command:

.. command-output:: python3 -m aioa2squery query --help
    :cwd: ../

.. image:: _static/images/demo.svg
    :align: center

This is also available from a pre-built `Docker <https://www.docker.com>`_
image for your convenience:

.. code-block:: shell

    $ docker run -it --rm docker.pkg.github.com/insurgency/aioa2squery/a2squery
    query --help

    ...

Constructing a Primitive Query Server
-------------------------------------

We can leverage a lot of the library to create a little static demo query
server, that would perhaps be useful for testing purposes. This could even
be extended to build a reverse proxy server.

.. TODO
