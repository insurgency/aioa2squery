import dataclasses

from dataclasses import dataclass
from datetime import timedelta

from typing import Optional

from .data_types import *

__all__ = (
    'A2SPlayer',
    'A2SRule',
)


@dataclass
class A2SPlayer:
    """
    A :mod:`dataclass <dataclasses>` that represents a player
    """

    name: String
    """Name of the player"""
    score: Long
    """Player's score (usually "frags" or "kills")"""
    duration: Float  # TODO: make timedelta
    """Time duration player has been connected to the server"""

    # Special dataclass fields for The Ship:
    deaths: Optional[Long] = None
    """Player's deaths (:valve-wiki:`The Ship <The_Ship>` Only)"""
    money: Optional[Long] = None
    """Player's money (:valve-wiki:`The Ship <The_Ship>` Only)"""

    def __str__(self) -> str:
        return self.name


@dataclass
class A2SRule:
    """
    Represents a single server :valve-wiki:`configuration<CFG>` :valve-wiki:`rule<ConVar>` as contained in the elements
    of :attr:`rules <A2SRulesResponse.rules>` list attribute of a :class:`A2SRulesResponse`
    """

    name: String
    """Name of the rule"""
    value: String
    """Value of the rule"""
