import asyncio

from asyncio import AbstractEventLoop

from typing import Optional, Type

from .requests import (
    A2SQueryRequest,
    A2SInfoRequest,
    A2SPlayerRequest,
    A2SRulesChallengeRequest,
    A2SPingRequest,
    A2SServerQueryGetChallengeRequest,
)
from .responses import (
    A2SInfoResponse,
    A2SInfoGoldSrcResponse,
    A2SPlayerChallengeResponse,
    A2SPlayersResponse,
    A2SRulesChallengeResponse,
    A2SRulesResponse,
    A2SServerQueryGetChallengeResponse,
    A2SPingResponse,
)
from .enumerations import Engine
from .context import GAME_ENGINE

__all__ = (
    'A2SQueryProtocol',
)


class A2SQueryProtocol(asyncio.DatagramProtocol):
    def __init__(self, loop: AbstractEventLoop):
        self.loop = loop

        self.transport = None
        self.connected = self.loop.create_future()

        self.future_response: Optional[asyncio.Future] = None
        self.response_builder = None

    def connection_made(self, transport):
        # Store established transport for closing later
        self.transport = transport
        # A connection is made, proceed with protocol...
        self.connected.set_result(self.loop.time())

    def datagram_received(self, data, addr):
        try:
            if not self.response_builder.read_in_packet(data):
                return
        except Exception as exc:
            if not self.future_response.done():
                # FIXME: Figure out why was getting InvalidStateError's occasionally?!
                self.future_response.set_exception(exc)
        else:
            ping_and_response = (self.response_builder, round((self.loop.time() - self.connected.result()) * 1000))

            if not self.future_response.done():
                # FIXME: Figure out why was getting InvalidStateError's occasionally?!
                self.future_response.set_result(ping_and_response)

    async def _execute_query(self, request: A2SQueryRequest, response_cls: Type):
        # Wait to establish transport "connection" before sending anything
        await self.connected
        # Create a future for storing the eventual query response
        self.future_response = self.loop.create_future()
        # Create a new buffer to store pieces (packet bytes) of the eventual response
        self.response_builder = response_cls()
        # Send the request to the currently established transport
        for part in request:
            # Requests technically may be multi-packeted, iterate the response for each packet given the currently
            # configured query cut-off size
            self.transport.sendto(part)
        # Wait for the query response to be completely finished
        await self.future_response
        # Return completed result to calling coroutine
        return self.future_response.result()

    # def _ping(self) -> int:
    #     return round((self.loop.time() - self.connected.result()) * 1000)

    async def a2s_query_info(self):
        response_cls = A2SInfoGoldSrcResponse if GAME_ENGINE.get() is Engine.GOLDSRC else A2SInfoResponse

        return await self._execute_query(A2SInfoRequest(), response_cls)

    async def a2s_query_players(self):
        response, ping = await self._execute_query(A2SPlayerRequest(), A2SPlayerChallengeResponse)
        response, _ = await self._execute_query(A2SPlayerRequest(response.challenge), A2SPlayersResponse)

        return response, ping

    async def a2s_query_rules(self):
        response, ping = await self._execute_query(A2SRulesChallengeRequest(), A2SRulesChallengeResponse)
        response, _ = await self._execute_query(A2SRulesChallengeRequest(response.challenge), A2SRulesResponse)

        return response, ping

    async def a2a_query_ping(self):
        response_cls = A2SPingResponse if GAME_ENGINE.get() is Engine.GOLDSRC else A2SPingResponse  # FIXME
        response, ping = await self._execute_query(A2SPingRequest(), response_cls)

        return response, ping

    async def a2s_query_serverquery_get_challenge(self):
        return await self._execute_query(A2SServerQueryGetChallengeRequest(), A2SServerQueryGetChallengeResponse)
