from contextvars import ContextVar

from .enumerations import Engine

__all__ = (
    'GAME_ENGINE',
    'APP_ID',
    'USE_REQUEST_COMPRESSION',
    'REQUEST_PACKET_SPLIT_SIZE',
)

GAME_ENGINE = ContextVar('game_engine', default=Engine.SOURCE)
APP_ID = ContextVar('app_id', default=None)
USE_REQUEST_COMPRESSION = ContextVar('use_request_compression', default=False)
REQUEST_PACKET_SPLIT_SIZE = ContextVar('request_packet_slit_size', default=1400)
