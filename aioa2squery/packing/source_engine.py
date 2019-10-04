from enum import unique, Enum, auto

from aioa2squery.enumerations import *
from .data_types import Byte

__all__ = (
    'ServerType',
    'ServerEnvironment',
    'ServerVisibility',
    'VAC',
)


class ServerType(TryLowercaseValueWhenMissingMixin, OrdinalByteRepresentationMixin, Byte, Enum):
    """
    Indicates the type of server
    """

    UNKNOWN = auto()
    """No particular server type"""
    DEDICATED_SERVER = ord('d')
    """:valve-wiki:`Dedicated game server <Source_Dedicated_Server>`"""
    LISTEN = ord('l')
    """Non-dedicated server (:valve-wiki:`LAN <Preventing_Players_from_Joining_a_Map>`/``sv_lan "0"``)"""
    NON_DEDICATED_SERVER = LISTEN
    """An alias for :attr:`LISTEN`"""
    SOURCETV_RELAY_PROXY = ord('p')
    """:valve-wiki:`SourceTV <SourceTV>`/HLTV Relay Proxy"""

    def __str__(self) -> str:
        if self is ServerType.DEDICATED_SERVER:
            return 'Dedicated Server'
        elif self is ServerType.NON_DEDICATED_SERVER:
            return 'Non-dedicated Server (LAN)'
        elif self is ServerType.SOURCETV_RELAY_PROXY:
            return 'SourceTV/HLTV Relay Proxy Server'

        return 'Unknown'


@unique
class ServerEnvironment(OrdinalByteRepresentationMixin, Byte, Enum):
    """Indicates the operating system of the server"""

    UNKNOWN = auto()
    """No particular operating system"""
    LINUX = ord('l')
    """Linux"""
    WINDOWS = ord('w')
    """Windows"""
    MAC = ord('m')
    """macOS"""
    OSX = ord('o')
    """OSX"""

    @classmethod
    def _missing_(cls, value):
        value = chr(value)

        if value == 'L' or value == 'W':
            return cls(ord(value.lower()))

        return super()._missing_(value)

    def __str__(self) -> str:
        if self is ServerEnvironment.LINUX:
            return 'Linux'
        elif self is ServerEnvironment.WINDOWS:
            return 'Windows'
        elif self is ServerEnvironment.MAC:
            return 'macOS'
        elif self is ServerEnvironment.OSX:
            return 'OS X'

        return 'Unknown'


class ServerVisibility(BooleanEnumMixin, SimpleMemberNameStringMixin, Byte, Enum):
    """Indicates whether the server requires a password for entry"""

    PUBLIC = 0
    """The server is publicly accessible without a password"""
    PRIVATE = 1
    """The server is private and requires a password for entry into multiplayer"""
    PASSWORDED = PRIVATE
    """An alias for :attr:`PRIVATE`"""

    def __bool__(self):
        return not super().__bool__()


class VAC(SimpleMemberNameStringMixin, Byte, Enum):
    """Specifies whether the server uses :valve-wiki:`VAC <Valve_Anti-Cheat>` (Valve Anti-Cheat)"""

    UNSECURED = 0
    """Anti-cheat is disabled"""
    INSECURE = 0
    """An alias for :attr:`UNSECURED`"""
    SECURED = 1
    """Anti-cheat is active"""
