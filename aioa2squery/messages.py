from dataclasses import dataclass

from .buffers import A2SBytesIO
from .packing import Byte, Long

__all__ = (
    'A2SQueryMessage',
)


@dataclass(init=False)
class A2SQueryMessage(A2SBytesIO):
    _split_mode_header: Long
    _message_header: Byte

    def __bytes__(self) -> bytes:
        return self.getvalue()
