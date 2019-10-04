from enum import unique, Enum

from ..enumerations import *
from .data_types import *

__all__ = (
    'Mod',
    'ModType',
    'ModDLL',
)


@unique
class Mod(SimpleMemberNameStringMixin, Byte, Enum):
    """TODO"""

    HALF_LIFE = 0
    """TODO"""
    HALF_LIFE_MOD = 1
    """TODO"""


@unique
class ModType(SimpleMemberNameStringMixin, Byte, Enum):
    """Indicates the type of mod"""

    SINGLE_AND_MULTIPLAYER = 0
    """Singleplayer **and** multiplayer mod"""
    MULTIPLAYER_ONLY = 1
    """Multiplayer **only** mod"""
    DONT_REALLY_KNOW = 10
    """TODO"""


@unique
class ModDLL(SimpleMemberNameStringMixin, Byte, Enum):
    """Indicates whether mod uses its own :wikipedia:`DLL <Dynamic-link_library>`"""

    USES_HALF_LIFE = 0
    """The mod uses the :valve:`Half-Life <Half-Life>` :wikipedia:`DLL <Dynamic-link_library>`"""
    USES_OWN = 1
    """It uses its own :wikipedia:`DLL <Dynamic-link_library>`"""
