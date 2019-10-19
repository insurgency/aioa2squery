from dataclasses import fields, dataclass
from bz2 import compress
from zlib import crc32

from typing import Optional

from .buffers import *
from .packing import *

__all__ = (
    'IS_NOT_SPLIT',
    'IS_SPLIT',
    'request',
    'A2SQueryRequest',
    'A2SInfoRequest',
    'A2SPlayerRequest',
    'A2SRulesChallengeRequest',
    'A2SPingRequest',
    'A2SServerQueryGetChallengeRequest',
)

# Packet response split mode headers
IS_NOT_SPLIT = -1
IS_SPLIT = -2
# Challenge packet number to receive a challenge number
RECEIVE_A_CHALLENGE = -1


def request(*, header: int):
    """
    Decorator to transform a class into a query request :mod:`dataclass <dataclasses>`

    :param header: message header unique to this request type
    :type header: int

    :raises AssertionError: If ``header`` is not of type :class:`int` or decorated class does not subclass
     :class:`A2SQueryRequest <aioa2squery.A2SQueryRequest>`
    """

    assert isinstance(header, int), (
        "Response dataclasses must be decorated and pass a single argument representing the response's message header "
        "byte field"
    )

    def wrap(cls):
        assert issubclass(cls, A2SQueryRequest), f"{cls.__name__} must subclass {A2SQueryRequest.__name__}"

        setattr(cls, '_message_header', header)
        cls = dataclass(cls, init=False)

        return cls
    return wrap


# noinspection PyDataclass
@dataclass(init=False)
class A2SQueryRequest(A2SBytesIO):
    """Base :mod:`dataclass <dataclasses>` for constructing data that goes into a query request"""

    _message_header: Byte

    def __init__(self):
        super().__init__()

        # Write split mode header into request buffer
        self.write_long(IS_NOT_SPLIT)

        for field in fields(self):
            # Get the appropriate write method for each dataclass field type
            write_method = '_'.join(('write', field.type.__name__)).lower()
            write_method = getattr(self, write_method)
            # Call the write method by name dynamically
            write_method(getattr(self, field.name))

    @property
    def size(self):
        """
        :return: byte length (size) of data in :meth:`py:io.BytesIO.getvalue`
        """

        return len(self.getvalue())

    @property
    def checksum(self):
        """:wikipedia:`CRC32 <Cyclic_redundancy_check>` checksum of :meth:`py:io.BytesIO.getvalue`"""

        return crc32(self.getvalue())

    @property
    def compressed_value(self):
        """:wikipedia:`BZ2 <Bzip2>` compressed value of :meth:`py:io.BytesIO.getvalue`"""

        return compress(self.getvalue())

    def __len__(self):
        # TODO: make cut-off value variable
        return len(self.getvalue()) // 1000 + 1

    def __iter__(self):
        self.n = 0

        return self

    def __next__(self):
        if self.n == 0:
            self.n += 1

            return self.getvalue()
        else:
            raise StopIteration

        # if self.n <= len(self):
        #     if len(self) > 1:
        #         multi_part_header = A2SBytesIO()
        #         multi_part_header.write_long(IS_SPLIT)
        #
        #     part.write_long(IS_SPLIT)
        #
        #     return part.getvalue()
        #
        #     if self.n == 0:
        #         pass
        #
        #     return self.getvalue()[]
        #
        #     self.n += 1


@dataclass(init=False)
class _ChallengeNumberMixin:
    challenge: Long = RECEIVE_A_CHALLENGE

    def __init__(self, challenge: Optional[int] = None):
        if challenge is not None:
            # noinspection PyTypeChecker
            self.challenge = challenge

        super().__init__()


@request(header=ord('T'))  # 0x54
class A2SInfoRequest(A2SQueryRequest):
    payload: String = 'Source Engine Query'


@request(header=ord('U'))  # 0x55
class A2SPlayerRequest(_ChallengeNumberMixin, A2SQueryRequest):
    pass


@request(header=ord('V'))  # 0x56
class A2SRulesChallengeRequest(_ChallengeNumberMixin, A2SQueryRequest):
    pass


@request(header=ord('i'))  # 0x69
class A2SPingRequest(A2SQueryRequest):
    pass


@request(header=ord('W'))  # 0x57
class A2SServerQueryGetChallengeRequest(A2SQueryRequest):
    pass
