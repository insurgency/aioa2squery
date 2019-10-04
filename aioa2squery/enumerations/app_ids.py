from collections import namedtuple
from enum import IntEnum


__all__ = (
    'AppID',
    'GOLDSOURCE_APPS_USE_NEW_INFO',
    'APPS_NO_PACKET_SIZE_FIELD',
    # 'APPS_RESPONSE_COMPRESSION_UNSUPPORTED',
)

# App = namedtuple('App', ())


class AppID(IntEnum):
    """
    An enumeration of common :valve-wiki:`Steam Application IDs <Steam_Application_IDs>` that handle queries
    differently. Can be used with the ``app_id`` parameter of the
    :class:`A2SQueryContext <aioa2squery.A2SQueryContext>` constructor.
    """

    # Is GoldSrc Engine
    # Uses Source info response format
    # Doesn't respond to A2S_PLAYER or A2S_SERVERQUERY_GETCHALLENGE?
    # AppID #
    # Release date

    HALF_LIFE = 70
    """:steam-app:`Half-Life 1 <70>`"""
    HALF_LIFE_1 = HALF_LIFE
    """An alias for :attr:`HALF_LIFE`"""
    # TEAM_FORTRESS_CLASSIC = namedtuple
    # TEAM_FORTRESS = TEAM_FORTRESS_CLASSIC
    # TEAM_FORTRESS_1 = TEAM_FORTRESS_1
    INSURGENCY = 222880
    """:steam-app:`Insurgency <>`"""
    INSURGENCY_SOURCE = INSURGENCY
    """An alias for :attr:`INSURGENCY`"""
    SOURCE_SDK_BASE_2006 = 215
    """:steam-app:`Source SDK Base 2006 <215>`"""
    COUNTER_STRIKE_SOURCE = 240
    """:steam-app:`Counter-Strike: Source <240>`"""
    RAG_DOLL_KUNG_FU = 1002
    """:steam-app:`Rag Doll Kung Fu <1002>`"""
    SIN_EPISODES_EMERGENCE = 1300
    """:steam-app:`SiN Episodes: Emergence <1300>`"""
    SIN_MULTIPLAYER = 1309
    """:steam-app:`SiN Multiplayer <1309>`"""
    SIN_1_MULTIPLAYER = 1309
    """An alias for :attr:`SIN_MULTIPLAYER`"""
    ETERNAL_SILENCE = 17550
    """:steam-app:`Eternal Silence <17550>`"""
    INSURGENCY_MODERN_INFANTRY_COMBAT = 17700
    """:steam-app:`Insurgency: Modern Infantry Combat <17700>`"""
    THE_SHIP = 2400
    """:steam-app:`The Ship <2400>`"""
    THE_SHIP_MURDER_PARTY = THE_SHIP
    """An alias for :attr:`THE_SHIP`"""
    LEFT_4_DEAD_2 = 550
    """:steam-app:`Left 4 Dead 2 <550>`"""


#: Pre-:valve-wiki:`orange box <Orange_Box>` games that use the updated Source Engine response protocol format for
# ``A2S_INFO`` queries
GOLDSOURCE_APPS_USE_NEW_INFO = frozenset({
    AppID.SIN_1_MULTIPLAYER,
    AppID.RAG_DOLL_KUNG_FU,
})
#: :valve-wiki:`App IDs <Steam_Application_IDs>` which are known not to contain a packet cut-off size field in
# multi-packeted responses
APPS_NO_PACKET_SIZE_FIELD = frozenset({
    AppID.SOURCE_SDK_BASE_2006,
    # FIXME: 240 when protocol = 7? AppID.COUNTER_STRIKE_SOURCE,
    AppID.ETERNAL_SILENCE,
    AppID.INSURGENCY_MODERN_INFANTRY_COMBAT,
})
#: :valve-wiki:`App IDs <Steam_Application_IDs>` which directly violate the query protocol specification by skipping
# compression headers even when responses are marked as compressed
# APPS_RESPONSE_COMPRESSION_UNSUPPORTED = frozenset({
#     AppID.LEFT_4_DEAD_2,
# })
