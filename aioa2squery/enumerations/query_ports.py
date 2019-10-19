from enum import IntEnum

__all__ = (
    'QueryPort',
)


class QueryPort(IntEnum):
    """Common server query port numbers"""

    SRCDS = 27_015
    """Default :valve-wiki:`Source Dedicated Server <Source Dedicated Server>` port number"""
    SOURCETV = 27_020
    """Default :valve-wiki:`SourceTV <SourceTV>` port number"""
    HLTV = SOURCETV
    """An alias for :attr:`SOURCETV`"""
    INSURGENCY_SANDSTORM_QUERY_PORT = 27_131
    """
    Standard Insurgency Sandstorm ``-QueryPort`` number per the official `Basic Server Setup Guide
    <https://steamcommunity.com/app/581320/discussions/1/1750106661705710565/>`_
    """
