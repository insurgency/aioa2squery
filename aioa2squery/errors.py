__all__ = (
    'ResponseError',
    'InvalidSplitModeHeader',  # Bad split mode header
    'PacketTotalTooLow',  # Bad packet total declared (too low)
    'PacketTotalTooHigh',  # Bad packet total declared (too high)
    'PacketNumberIsOutOfBounds',  # Packet number doesn't conform to bounds
    'UnexpectedSplitModeChange',  # Unexpected change in split mode between response packets
    'UnexpectedAnswerIDChange',  # Unexpected change in answer ID between response packets
    'TotalPacketsChangedFromInitial',  # Unexpected change in total number of packets declared
    'PacketNumberRepeated',  # Bad repetition on packet number for a single answer
    'IncorrectResponseMessageHeader',
)


class ResponseError(Exception):
    """Base exception for errors related to processing and parsing server query responses"""


class InvalidSplitModeHeader(ResponseError):
    """
    Query client exception raised when processing a response that contains (packet header field that indicated whether
    a response is multi-packeted or not)
    """

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f"Invalid split mode head header ({self.value})"


class PacketTotalTooLow(ResponseError):
    """TODO"""

    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"Packet total for multi-packeted response is less than 2 ({self.value})"


class PacketTotalTooHigh(ResponseError):
    """TODO"""

    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"Packet total for multi-packeted response is greater than 15 ({self.value})"


class PacketNumberIsOutOfBounds(ResponseError):
    """TODO"""

    def __init__(self, should_be, gave):
        self.max_value = should_be
        self.value = gave

    def __str__(self) -> str:
        return f"Packet number for multi-packeted response is out of bounds ({self.value})." \
            f"Should be between 2 and {self.max_value}"


class UnexpectedSplitModeChange(ResponseError):
    """TODO"""

    def __init__(self, should_be, gave):
        self.should_be = should_be
        self.gave = gave

    def __str__(self):
        return f"Response split mode changed unexpectedly from {self.should_be} to {self.gave}"


class UnexpectedAnswerIDChange(ResponseError):
    """TODO"""

    def __init__(self, should_be, gave):
        self.should_be = should_be
        self.gave = gave

    def __str__(self):
        return f"Answer ID changed unexpectedly from {self.should_be} to {self.gave}"


class PacketNumberRepeated(ResponseError):
    """TODO"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Packet number was repeated in response: {self.value}"


class TotalPacketsChangedFromInitial(ResponseError):
    """TODO"""

    def __init__(self, should_be, gave):
        self.should_be = should_be
        self.gave = gave

    def __str__(self):
        return f"Answer ID changed unexpectedly from {self.should_be} to {self.gave}"


class IncorrectResponseMessageHeader(ResponseError):
    """TODO"""

    def __init__(self, gave, should_be):
        self.should_be = should_be
        self.gave = gave

    def __str__(self) -> str:
        return f"Response message header is incorrect. Gave '{self.gave:c}', but should be '{self.should_be:c}'"
