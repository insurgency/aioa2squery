import io

from struct import pack, unpack

from .packing import *

__all__ = (
    'STRING_TERMINATOR',
    'A2SBytesIO',
)


STRING_TERMINATOR = b'\x00'


class A2SBytesIO(io.BytesIO):
    """
    A bytes buffer that inherits includes methods for reading and writing :valve-wiki:`A2S query packet fields data
    types <Server_queries#Data_Types>`
    """

    # Byte

    def read_byte(self) -> int:
        """
        Read an 8-bit character (``unsigned char``) from the current buffer

        :return: An 8-bit character (``unsigned char``) value read from the current buffer
        :rtype: Byte
        """

        return unpack('<B', self.read(Byte.BYTE_LENGTH))[0]

    def write_byte(self, value: int):
        """
        Write an 8-bit character (``unsigned char``) to the current buffer

        :param value: value to be written to the buffer
        :type value: int
        """

        self.write(pack('<B', value))

    # Short

    def read_short(self) -> int:
        """
        Read a 16-bit signed integer (``short``) from the current buffer

        :return: A 16-bit signed integer (``short``) value read from the current buffer
        :rtype: Short
        """

        return unpack('<h', self.read(Short.BYTE_LENGTH))[0]

    def write_short(self, value: int):
        """
        Write a 16-bit signed integer (``short``) to the current buffer

        :param value: value to be written to the buffer
        :type value: int
        """

        self.write(pack('<h', value))

    # Long

    def read_long(self) -> int:
        """
        Read a 32-bit signed integer (``int``) from the current buffer

        :return: A 32-bit signed integer (``int``) value read from the current buffer
        :rtype: Long
        """

        return unpack('<l', self.read(Long.BYTE_LENGTH))[0]

    def write_long(self, value: int):
        """
        Write a 32-bit signed integer (``int``) to the current buffer

        :param value: value to be written to the buffer
        """

        self.write(pack('<l', value))

    # Long Long

    def read_long_long(self) -> int:
        """
        Read a 64-bit unsigned integer (``unsigned long long``) from the current buffer

        :return: A 64-bit unsigned integer (``unsigned long long``) value read from the current buffer
        :rtype: LongLong
        """

        return unpack('Q', self.read(LongLong.BYTE_LENGTH))[0]

    def write_long_long(self, value: int):
        """
        Write a 64-bit unsigned integer (``unsigned long long``) to the current buffer

        :param value: value to be written to the buffer
        :type value: int
        """

        self.write(pack('Q', value))

    # Float

    def read_float(self) -> float:
        """
        Read a 32-bit floating point (``float``) from the current buffer

        :return: A 32-bit floating point (``float``) value read from the current buffer
        :rtype: float
        """

        return unpack('<f', self.read(Float.BYTE_LENGTH))[0]

    def write_float(self, value: float):
        """
        Write a 32-bit floating point (``float``) to the current buffer

        :param value: value to be written to the buffer
        :type value: Float
        """

        self.write(pack('<f', value))

    # String

    def read_string(self) -> str:
        """
        Read a variable-length UTF-8 encoded string from the current buffer

        :return: A string value read from the current buffer
        :rtype: String
        """

        # Start with the entire buffer value and the current buffer position
        value, start = self.getvalue(), self.tell()

        try:
            # Retrieve the index of the next string termination occurrence in the buffer
            end = value.index(STRING_TERMINATOR, start)
        except ValueError:
            # If the string terminator was unable to be found then response buffer was likely terminated in the
            # middle of a string. In this scenario just read until the end of the buffer to get as much of the original
            # string as possible...
            end = len(self.getvalue())

        # Slice the buffer value from starting index until the next terminator to form a string subsection
        value = value[start:end]
        # Resume by seeking to the index after the string terminator
        self.seek(end + 1)

        # TODO: perhaps it would be better to re-raise Unicode decode errors as a library specific exception?
        return value.decode(errors='ignore')

    def write_string(self, value: str):
        """
        Write a variable-length UTF-8 encoded string to the current buffer

        :param value: value to be written to the buffer
        :type value: str
        """

        self.write(value.encode() + STRING_TERMINATOR)
