import asyncio
import socket

from asyncio import AbstractEventLoop

from typing import Optional, Tuple, Dict

from .decorators import deprecated
from .protocol import A2SQueryProtocol
from .responses import A2SInfoResponse, A2SPlayersResponse, A2SRulesResponse
from .context import *
from .enumerations import *

__all__ = (
    'A2SQueryContext',
)


class A2SQueryContext:
    """
    Query client that handles the nuances of querying different Source engine and game versions

    :param timeout: Default timeout duration (in seconds) when making :valve-wiki:`server queries<Server_Queries>`
    :type timeout: float
    :param game_engine: Explicitly treat all query responses as being in the response format for a specific game engine
     version
    :type game_engine: aioa2squery.Engine
    :param app_id: If specified treat all responses as being in a format for this explicit
     :valve-wiki:`Steam application ID<Steam_Application_IDs>`
    :type app_id: int
    :param packet_split_size: How big to make query before splitting query request into additional packets. Steam uses
     a packet size of 1400 bytes (the default).
    :type packet_split_size: int
    :param loop: An event loop to use
    :type loop: asyncio.AbstractEventLoop
    :param use_compression: Whether or not to apply compression on multi-packeted query requests
    :type use_compression: bool
    """

    def __init__(self, game_engine: Engine = Engine.SOURCE, app_id: Optional[int] = None,
                 packet_split_size: Optional[int] = 0x04E0, timeout: Optional[float] = 10.0,
                 use_compression: bool = False, loop: Optional[AbstractEventLoop] = None):
        self.timeout = timeout
        self._loop = asyncio.get_running_loop()  # FIXME?
        self.use_compression = use_compression
        self.packet_split_size = packet_split_size

        # Set contextvars
        GAME_ENGINE.set(game_engine)
        APP_ID.set(app_id)

    async def _get_protocol(self, host, port):
        transport, protocol = await self._loop.create_datagram_endpoint(
            # Source Engine only really supports IPv4
            family=socket.AF_INET,
            protocol_factory=lambda: A2SQueryProtocol(loop=self._loop),

            remote_addr=(host, port),
        )
        protocol: A2SQueryProtocol

        return transport, protocol

    async def execute_query(self, host, port, timeout, *, func=None):
        transport, protocol = await self._get_protocol(host, port)

        try:
            func = getattr(protocol, func)
            response = await asyncio.wait_for(func(), timeout=timeout or self.timeout)
        except Exception:
            # Re-raise exception to caller after cleanup
            raise
        else:
            # If all went well return parsed response
            return response
        finally:
            # Assure client transport is closed regardless of errors while querying
            transport.close()

    async def query_info(self, host: Optional[str] = '127.0.0.1', port: Optional[int] = QueryPort.SRCDS,
                         timeout: Optional[float] = None) -> Tuple[A2SInfoResponse, int]:
        """
        Retrieve information about the server including, but not limited to: its name, the map currently being
        played, and the number of players

        .. note::
            :valve-wiki:`Rag Doll Kung Fu <Rag_Doll_Kung_Fu>` :valve-wiki:`servers <Source_Dedicated_Server>` always
            return :attr:`ServerType.UNKNOWN <aioa2squery.ServerType.UNKNOWN>` for
            :attr:`aioa2squery.A2SInfoResponse.server_type` in the response.

        .. note::
            :valve-wiki:`HLTV <SourceTV>` servers may respond with a late request that is either incomplete or incorrect
            if the number of slots is 255.

        :param host: Host of the server to query
        :param port: Port of server to query
        :param timeout: Timeout duration (in seconds) when making :valve-wiki:`server queries<Server_Queries>`

        :raises asyncio.TimeoutError: If query takes exceeds timeout duration
        :raises aioa2squery.ResponseError: If there is a problem completing, reading or parsing the response data

        :return: Basic information about the server and the estimated ping to the server in milliseconds
        :rtype: tuple[A2SInfoResponse, int]
        """

        return await self.execute_query(host, port, timeout, func='a2s_query_info')

    async def query_players(self, host: Optional[str] = '127.0.0.1', port: Optional[int] = QueryPort.SRCDS,
                            timeout: Optional[float] = None) -> Tuple[A2SPlayersResponse, int]:
        """
        Retrieve information about the players currently on the server.

        .. _uptime: https://wikipedia.org/wiki/Uptime

        .. note::
            `SourceTV`_ does not respond to this query.

        .. note::
            When a player is trying to connect to a server, they are recorded in the number of players. However, they
            will not be in the list of player information.

        .. warning::
            :valve-wiki:`Counter-Strike: Global Offensive Dedicated Server
            <Counter-Strike:_Global_Offensive_Dedicated_Servers>` by default returns only max players and server
            `uptime`_. You have to change server :valve-wiki:`CVar <ConVar>` :code:`"host_players_show"` in
            :valve-wiki:`server.cfg <Server.cfg>` to value :code:`"2"` (show full info) if you want to revert to old
            format with players list.

        :param host: Host of the server to query
        :param port: Port of server to query
        :param timeout: Timeout duration (in seconds) when making :valve-wiki:`server queries<Server_Queries>`

        :raises asyncio.TimeoutError: If query takes exceeds timeout duration
        :raises aioa2squery.ResponseError: If there is a problem completing, reading or parsing the response data

        :return: Details about each player on the server and the estimated ping to the server in milliseconds
        :rtype: A2SPlayersResponse
        """

        # if port == SOURCETV_PORT:
        #     "SourceTV does not respond to this request."

        return await self.execute_query(host, port, timeout, func='a2s_query_players')

    async def query_rules(self, host: Optional[str] = '127.0.0.1', port: Optional[int] = QueryPort.SRCDS,
                          timeout: Optional[float] = None) -> Dict:
        """
        .. warning::
            Older games, usually on :valve-wiki:`Source SDK 2007<Source_2007>`, may reply with a truncated response. In
            this case, the data may be terminated in the middle of a string or in between a name and value.

        :param host: Host of the server to query
        :param port: Port of server to query
        :param timeout: Timeout duration (in seconds) when making :valve-wiki:`server queries<Server_Queries>`

        :raises asyncio.TimeoutError: If query takes exceeds timeout duration
        :raises aioa2squery.ResponseError: If there is a problem completing, reading or parsing the response data

        :return: The rules the server is using and the estimated ping to the server in milliseconds
        :rtype: A2SPlayersResponse
        """

        return await self.execute_query(host, port, timeout, func='a2s_query_rules')

    @deprecated(message="A2A_PING is no longer supported on Counter Strike: Source and Team Fortress 2 servers, "
                        "and is considered a deprecated feature.")
    async def query_ping(self, host: Optional[str] = '127.0.0.1', port: Optional[int] = QueryPort.SRCDS,
                         timeout: Optional[float] = None) -> int:
        """
        Ping the server to see if it exists, this can be used to calculate the latency to the server.

        .. |A2A_PING| replace:: ``A2A_PING``
        .. _A2A_PING: https://wiki.teamfortress.com/wiki/Dedicated_server

        .. warning::
            According to :valve-wiki:`Valve<Valve>` (see :valve-wiki:`Talk Page <Talk:Server_queries#A2A_PING_no_longer_supported.3F>`), |A2A_PING|_ is no longer supported on :valve-wiki:`Counter Strike: Source <Counter-Strike:_Source>` and :valve-wiki:`Team Fortress 2<Team Fortress 2>` :valve-wiki:`servers <Source_Dedicated_Server>`, and is considered a deprecated feature.

        :param host: Host of the server to query
        :param port: Port of server to query
        :param timeout: Timeout duration (in seconds) when making :valve-wiki:`server queries<Server_Queries>`

        :raises asyncio.TimeoutError: If query takes exceeds timeout duration
        :raises aioa2squery.ResponseError: If there is a problem completing, reading or parsing the response data

        :return: Calculated ping (round-trip latency) to the server
        :rtype: int
        """

        # if self.app_id is AppID.COUNTER_STRIKE_SOURCE or self.app_id is AppID.:
        #     ...  # TODO: log library warning

        return await self.execute_query(host, port, timeout, func='a2a_query_ping')

    async def _query_get_challenge(self, host: Optional[str] = '127.0.0.1', port: Optional[int] = QueryPort.SRCDS,
                                   timeout: Optional[float] = None):
        """
        ``A2S_PLAYER`` and ``A2S_RULES`` queries both require a challenge number. Formerly, this number could be
        obtained via an ``A2S_SERVERQUERY_GETCHALLENGE`` request. In newer games it no longer works.

        On some engines (confirmed AppIDs: 17510, 17530, 17740, 17550, 17700) it can be used.

        :param host: Host of the server to query
        :param port: Port of server to query
        :param timeout: Timeout duration (in seconds) when making :valve-wiki:`server queries<Server_Queries>`

        :raises asyncio.TimeoutError: If query takes exceeds timeout duration
        :raises aioa2squery.ResponseError: If there is a problem completing, reading or parsing the response data

        :return: A challenge number for use in the player and rules query
        :rtype: int
        """

        return await self.execute_query(host, port, timeout, func='a2s_query_serverquery_get_challenge')
