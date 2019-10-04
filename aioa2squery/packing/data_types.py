"""Data packing field types."""

__all__ = (
    'Byte',
    'Short',
    'Long',
    'Float',
    'LongLong',
    'String',
)


class Byte(int):
    """An 8-bit character (``unsigned char``)."""

    BYTE_LENGTH = 1


class Short(int):
    """A 16-bit signed integer (``short``)."""

    BYTE_LENGTH = 2


class Long(int):
    """A 32-bit signed integer (``int``)."""

    BYTE_LENGTH = 4


class Float(float):
    """A 32-bit floating point (``float``)."""

    BYTE_LENGTH = 4


class LongLong(int):
    """A 64-bit unsigned integer (``unsigned long long``)."""

    BYTE_LENGTH = 8


class String(str):
    """A string (``std::string``)."""

    BYTE_LENGTH = None
