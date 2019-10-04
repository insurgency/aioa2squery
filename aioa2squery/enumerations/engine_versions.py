from enum import Enum, auto

__all__ = (
    'Engine',
)


class Engine(Enum):
    """Enumeration representing the different Source Engine versions"""

    GOLDSRC = auto()
    """:valve-wiki:`Goldsource <GoldSrc>`"""
    GOLDSOURCE = GOLDSRC
    """An alias for :attr:`GOLDSRC`"""
    SOURCE = auto()
    """:valve-wiki:`Source <Source>`"""
