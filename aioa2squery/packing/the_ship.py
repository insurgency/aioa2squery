from enum import unique, Enum

from aioa2squery.enumerations import *
from .data_types import Byte


__all__ = (
    'TheShipGameMode',
)


@unique
class TheShipGameMode(SimpleMemberNameStringMixin, Byte, Enum):
    """
    Gamemodes for :valve-wiki:`The Ship <The_Ship>`
    """

    HUNT = 0
    """Hunt"""
    ELIMINATION = 1
    """Elimination"""
    DUEL = 2
    """Duel"""
    DEATHMATCH = 3
    """Deathmatch"""
    VIP_TEAM = 4
    """VIP Team"""
    TEAM_ELIMINATION = 5
    """Team Elimination"""

    def __str__(self):
        if self is TheShipGameMode.VIP_TEAM:
            return 'VIP Team'

        return super().__str__()
