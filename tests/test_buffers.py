import struct

from unittest import TestCase
from random import getrandbits, uniform, choices
from string import ascii_uppercase, digits

from aioa2squery import A2SBytesIO


def random_string():
    return ''.join(choices(ascii_uppercase + digits, k=100))


class TestA2SQueryIO(TestCase):
    def setUp(self):
        self.buffer = A2SBytesIO()

    # Byte

    def test_write_and_read_normal_byte(self):
        original_value = getrandbits(8)

        self.buffer.write_short(original_value)
        self.buffer.seek(0)
        unpacked_value = self.buffer.read_short()

        self.assertEqual(unpacked_value, original_value)

    def test_write_byte_too_big(self):
        self.assertRaises(struct.error, self.buffer.write_byte, 0xFF + 1)

    # Short

    def test_write_and_read_normal_short(self):
        original_value = -2**15+1

        self.buffer.write_short(original_value)
        self.buffer.seek(0)
        unpacked_value = self.buffer.read_short()

        self.assertEqual(unpacked_value, original_value)

    # Long

    def test_write_and_read_normal_long(self):
        original_value = -2**31+1

        self.buffer.write_long(original_value)
        self.buffer.seek(0)
        unpacked_value = self.buffer.read_long()

        self.assertEqual(unpacked_value, original_value)

    # Long Long

    def test_write_and_read_long_long(self):
        original_value = 2**64-1

        self.buffer.write_long_long(original_value)
        self.buffer.seek(0)
        unpacked_value = self.buffer.read_long_long()

        self.assertEqual(unpacked_value, original_value)

    # Float

    def test_write_and_read_normal_float(self):
        original_value = uniform(-1000, 1000)

        self.buffer.write_float(original_value)
        self.buffer.seek(0)
        unpacked_value = self.buffer.read_float()

        self.assertAlmostEqual(unpacked_value, original_value, places=3)

    # String

    def test_write_and_read_normal_string(self):
        original_value = random_string()

        self.buffer.write_string(original_value)
        self.buffer.seek(0)
        unpacked_value = self.buffer.read_string()

        self.assertEqual(unpacked_value, original_value)

    def test_write_many_different_and_read_string(self):
        original_value1 = random_string()
        original_value2 = random_string()

        self.buffer.write_float(-0.14)
        self.buffer.write_string(original_value1)
        self.buffer.write_float(2.5)
        self.buffer.write_short(123)
        self.buffer.write_string(original_value2)
        self.buffer.write_short(7)

        self.buffer.seek(0)
        _ = self.buffer.read_float()
        self.assertEqual(
            first=self.buffer.read_string(),
            second=original_value1,
        )
        _ = self.buffer.read_float()
        _ = self.buffer.read_short()
        self.assertEqual(
            first=self.buffer.read_string(),
            second=original_value2,
        )

    def test_write_unterminated_string(self):
        original_value = random_string()

        self.buffer.write_short(3)
        self.buffer.write(original_value.encode())

        self.buffer.seek(0)
        _ = self.buffer.read_short()
        self.assertEqual(
            first=self.buffer.read_string(),
            second=original_value,
        )

    def test_read_multiple_empty_strings(self):
        for _ in range(3):
            self.buffer.write_string('')

        self.buffer.seek(0)

        for _ in range(3):
            self.assertEqual(
                first=self.buffer.read_string(),
                second='',
            )
