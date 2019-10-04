from enum import IntFlag, unique

__all__ = (
    'ExtraDataFlag',
)


@unique
class ExtraDataFlag(IntFlag):
    GAME_ID = 0x01  # 1
    # NOTE: Lower bits 2-4 are unused/undocumented
    STEAM_ID = 0x10  # 5
    KEYWORDS = 0x20  # 6
    SOURCETV = 0x40  # 7
    GAME_PORT = 0x80  # 8
