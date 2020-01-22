import dataclasses
import enum

from bz2 import decompress
from dataclasses import dataclass, Field, MISSING
from datetime import timedelta
from zlib import crc32

from typing import List, Dict

from .enumerations import *
from .buffers import A2SBytesIO
from .context import *
from .errors import *
from .packing import *
from .requests import IS_NOT_SPLIT, IS_SPLIT

__all__ = (
    'response',
    'A2SQueryResponse',

    # A2S_INFO
    'A2SInfoResponse',
    # A2S_INFO_GOLDSRC
    'A2SInfoGoldSrcResponse',
    # A2S_PLAYERS
    'A2SPlayerChallengeResponse',
    'A2SPlayersResponse',
    # A2S_RULES
    'A2SRulesChallengeResponse',
    'A2SRulesResponse',
    # A2S_PING
    'A2SPingResponse',
    # A2S_SERVERQUERY_GETCHALLENGE
    'A2SServerQueryGetChallengeResponse',
)


def response(*, header: int):
    """
    Decorator to transform a :class:`A2SQueryResponse <aioa2squery.A2SQueryResponse>` class into a query response
     :mod:`dataclass <dataclasses>` with the corresponding response message ID header

    :param header: message header unique to this request type
    :type header: int

    :raises AssertionError: If ``header`` is not of type :class:`int` or decorated class does not subclass
     :class:`A2SQueryResponse <aioa2squery.A2SQueryResponse>`
    """

    # TODO: decorated without header should be base dataclass, however we lose then lose the ability to run
    #  semi-important import-time assertions

    # Check message_header was provided and is not a class/null but is indeed an integer
    assert isinstance(header, int), (
        "Response dataclasses must be decorated and pass a single argument representing the response's message header "
        "byte field"
    )

    def wrap(cls):
        assert issubclass(cls, A2SQueryResponse), f"{cls.__name__} must subclass {A2SQueryResponse.__name__}"
        # Set expected response message header value
        setattr(cls, '_message_header', header)
        # Transform into a response class into a dataclass
        cls = dataclass(cls, init=False, unsafe_hash=True)  # TODO: add back __init__ with *cmd_args, **kwargs

        return cls

    return wrap


# Function to return sorting key based on packet's response number
def _packet_number(buf: A2SBytesIO):
    # Special header processing for GoldSrc formatted responses...
    if GAME_ENGINE.get() is Engine.GOLDSRC:
        # Skip split mode header & answer ID to get the packet number for each buffer
        buf.seek(Long.BYTE_LENGTH*2)
        # Get packet's number from upper 4 bits
        return buf.read_byte() >> 4

    # Skip split mode header (long), answer ID (long), and total packets (byte) to get the packer number
    # for each buffer (Source Engine response format)
    buf.seek(Long.BYTE_LENGTH*2 + Byte.BYTE_LENGTH*1)

    return buf.read_byte()


@dataclass(init=False)
class A2SQueryResponse:
    _split_mode_header: Long = dataclasses.field(repr=False)
    _message_header: Byte = dataclasses.field(repr=False)

    def __init__(self, **kwargs):
        for field in dataclasses.fields(self):
            if field.name != '_message_header' and field.default is MISSING:
                # Default all dataclass member variables to null
                setattr(self, field.name, None)

        self._received_packets: List[A2SBytesIO] = list()
        self._total_packets = 1
        self._answer_id = None
        self._compression_was_used = False

    # def __getitem__(self, item):
    #     return getattr(self, item)

    def __missing__(self, key: str):
        try:
            if not isinstance(key, str) or key.startswith('_') or key not in (f.name for f in dataclasses.fields(self)):
                raise ValueError

            return getattr(self, key)
        except (ValueError, AttributeError):
            raise KeyError(key)

    def marshal_field_data(self, assembled_response: A2SBytesIO, field: Field):
        """
        Called for every :mod:`dataclass <dataclasses>` :class:`Field <dataclasses.Field>` in response to unpack
        response.

        :param assembled_response: Assembled response payload bytes
        :type assembled_response: aioa2squery.A2SBytesIO
        :param field: current :mod:`dataclass <dataclasses>` field to parse data into
        :type field: dataclasses.Field
        """

        if field.name == '_message_header':
            message_header = assembled_response.read_byte()

            if message_header != self._message_header:
                raise IncorrectResponseMessageHeader(message_header, self._message_header)

            return

        # Store the field's type
        field_type = field.type

        # For dataclass fields that are annotated as enumeration types use the mixed-in type of the enum
        if issubclass(field.type, enum.Enum):
            field_type = field.type.__base__

        # if isinstance(field.type, Iterable):
        #     ...  # FIXME: Handle iterable types

        # Dynamically get the name of the appropriate buffer read method
        read_method = '_'.join(('read', field_type.__name__)).lower()
        # read_long_long() has a different method name than usual
        read_method = read_method.replace('longlong', 'long_long')
        read_method = getattr(assembled_response, read_method)

        # Set the dataclass field to the read value
        if issubclass(field.type, enum.Enum):
            # For enums get the appropriate member
            setattr(self, field.name, field.type(read_method()))
        else:
            setattr(self, field.name, read_method())

    def _assemble_response(self):
        """
        Assemble any multi-packeted response and marshal out data into dataclass fields
        """

        assembled_response = A2SBytesIO()

        # Sort the received packets if the response was multi-packeted
        if len(self._received_packets) >= 2:
            self._received_packets = sorted(self._received_packets, key=_packet_number)

        # Make an iterator over the list of previously received packet buffers
        received_packets = iter(self._received_packets)
        # Start with the first packet to get the special head fields like checksum and assembled response size
        first_packet = next(received_packets)

        if len(self._received_packets) == 1:
            assembled_response = first_packet
        else:  # Else we're assembling a multi-packet response...
            # Only new Source Engine format can have response compression (not GoldSrc)
            if self._compression_was_used:
                # Start reading from the beginning of the first packet
                first_packet.seek(0)
                # Skip split mode header, answer ID, total packets, packet number
                first_packet.seek(Long.BYTE_LENGTH * 2 + Byte.BYTE_LENGTH * 2)

                # Skip response cut-off size field if it has it
                if APP_ID.get() not in APPS_NO_PACKET_SIZE_FIELD:
                    # TODO: check if it has 0x04E0 as the next value
                    _ = first_packet.read_short()

                assembled_size = first_packet.read_long()
                assembled_checksum = first_packet.read_long()
                # Write the rest of the first packet (the payload) into the assembled buffer
                assembled_response.write(first_packet.read())

                assembled_response = bytes()
                for packet in received_packets:
                    assembled_response += packet.getvalue()

                assembled_response = decompress(assembled_response)
                assert len(assembled_response) == assembled_size, "Assembled size is not what was expected"
                assert crc32(assembled_response) == assembled_checksum, "Bad response checksum"
            else:
                for packet in self._received_packets:
                    # Skip to payload section of response packets

                    if GAME_ENGINE.get() is Engine.GOLDSRC:
                        packet.seek(Long.BYTE_LENGTH*2 + Byte.BYTE_LENGTH)
                    else:
                        packet.seek(Long.BYTE_LENGTH*2 + Byte.BYTE_LENGTH*2 + Short.BYTE_LENGTH)

                    # Append each payload out to buffer
                    assembled_response.write(packet.read())

        # Read from beginning of response payload
        assembled_response.seek(0)

        # Loop over all response dataclass fields
        for _field in dataclasses.fields(self):
            self.marshal_field_data(assembled_response, _field)

    # FIXME: Currently uses a lot of messy branching and repetition, please attempt to improve later
    def read_in_packet(self, packet_data: bytes) -> bool:
        """
        Read in a single received packet in order to assemble and parse a full query response

        :param packet_data: Data from an individual response packet
        :type packet_data: bytes

        :raises aioa2squery.InvalidSplitModeHeader: If packet split mode header is invalid

        :return: ``True`` if response is complete, ``False`` if response in incomplete
        :rtype: bool
        """

        # Create an A2S query bytes buffer from the raw packet bytes
        packet_data = A2SBytesIO(packet_data)
        # Get split mode header of response: every query packet should have one regardless of the engine query format
        split_mode_header = packet_data.read_long()

        # Check to make sure split mode header is valid (either IS split or is NOT split)
        if split_mode_header != IS_NOT_SPLIT and split_mode_header != IS_SPLIT:
            # TODO: Why does this reply happen a lot on the halflife port?
            #  b'\x08\x08\x01\x12\x19Invalid/unknown MsgID 255'/302057480?
            raise InvalidSplitModeHeader(split_mode_header)

        # Check if we've received any packets already, if not this is the first packet being read in for this response
        if not self._received_packets:
            # Store split mode header from the first packet received in this query response
            self._split_mode_header = split_mode_header

            if split_mode_header == IS_NOT_SPLIT:
                # If the response is only a single packet assemble the complete response it and return...
                self._received_packets.append(packet_data)
                self._assemble_response()

                return True

            # Otherwise this is a multi-packeted query response...

            # Store unique number assigned by server per answer
            self._answer_id = packet_data.read_long()

            if GAME_ENGINE.get() is Engine.SOURCE:
                # Only game servers using the Source Engine query format CAN use compression in multi-packeted responses
                # Check the most significant bit of the answer ID to determine if response compression WAS applied
                self._compression_was_used = bool(self._answer_id >> Long.BYTE_LENGTH*8-1)

            # Now process the current packet number AND total number of packets in response
            # TODO: packet_number, total_packets = get_packet_number_and_total()
            if GAME_ENGINE.get() is Engine.GOLDSRC:
                packet_number = packet_data.read_byte()

                # For GoldSrc the lower 4 bits of this field represent the current packet number of this response
                self._total_packets = packet_number & 0x0F  # Mask out lower bits to get the upper portion
                # And the upper 4 bits represent the total number of packets in the response
                packet_number >>= 4
            else:
                # Otherwise for the standard Source Engine query format the total number of packets and the current
                # packet number are simply 2 separate header fields:
                self._total_packets = packet_data.read_byte()  # Store the total packets for this response
                packet_number = packet_data.read_byte()

            # Perform a sanity check to ensure the total number of packets declared is at least greater than 1 for
            # a multi-packeted response
            if not self._total_packets > 1:
                raise PacketTotalTooLow(self._total_packets)
            elif not self._total_packets <= 15:
                # FIXME: not all servers seem to conform to this upper limit?
                pass  # raise PacketTotalTooHigh(self._total_packets)

            # The number of the first packet in a response is 0, therefore all packet numbers must be greater than
            # or equal to zero and less than the total number of packets declared for a response
            if not 0 <= packet_number < self._total_packets:  # FIXME: logic repetition again!
                raise PacketNumberIsOutOfBounds(self._total_packets, packet_number)

            # This initial packet of this multi-packet response is valid, append it and proceed to collect additional
            # response packets
            self._received_packets.append(packet_data)

            # We're not done quite yet!
            return False

        # Else handle subsequent packets in multi-packeted response...

        # Assure split mode header hasn't changed since the initially received packet
        if split_mode_header != self._split_mode_header:
            raise UnexpectedSplitModeChange(self._split_mode_header, split_mode_header)

        # Assure answer ID is the same as initial ID
        answer_id = packet_data.read_long()
        if answer_id != self._answer_id:
            raise UnexpectedAnswerIDChange(self._answer_id, answer_id)

        # FIXME: repetition of logic, super not good!
        if GAME_ENGINE.get() is Engine.GOLDSRC:
            # Read out a byte from the current buffer being read in to get the packet number response header field
            packet_number = packet_data.read_byte()
            # And total packets in this response Lower 4 bits to get the total packets
            total_packets = packet_number & 0x0F

            # Get packet number from upper 4 bits
            packet_number >>= 4
        else:
            total_packets = packet_data.read_byte()
            packet_number = packet_data.read_byte()

        # Check that total packets for this response hasn't changed from initially declared value
        if total_packets != self._total_packets:
            raise TotalPacketsChangedFromInitial(self._total_packets, total_packets)

        # FIXME: logic repetition again!
        # Ensure the packet number is not lower or higher than it should be
        if not 0 <= packet_number < self._total_packets:
            raise PacketNumberIsOutOfBounds(self._total_packets, packet_number)

        # Loop through previous response packets...
        for previous_packet in self._received_packets:
            # And pull out packet numbers from each buffer
            previous_packet_number = _packet_number(previous_packet)

            # Make sure packet number is not a repeat
            if packet_number == previous_packet_number:
                raise PacketNumberRepeated(packet_number)

        # Add packet buffer to previous ones
        self._received_packets.append(packet_data)

        # We have received as many packet buffers as we needed to complete this response
        if len(self._received_packets) == self._total_packets:
            # Assemble response and return...
            self._assemble_response()

            return True

        # Otherwise we need to continue reading in packets...
        return False


@response(header=ord('I'))  # 0x69
class A2SInfoResponse(A2SQueryResponse):
    """
    Information about the server including, but not limited to: its :attr:`name`, the :attr:`map` currently being
    played, and the number of :attr:`players`
    """

    protocol: Byte
    """Protocol version used by the server"""
    name: String
    """:valve-wiki:`Name <Hostname>` of the server"""
    map: String
    """Map the server has currently loaded"""
    folder: String
    """Name of the folder containing the game files"""
    game: String
    """Full name of the game"""
    app_id: Short
    """:valve-wiki:`Steam Application ID <Steam_Application_IDs>` of the game"""
    players: Byte
    """Number of players on the server"""
    max_players: Byte
    """Maximum number of players the server reports it can hold"""
    bots: Byte
    """Number of :valve-wiki:`bots <Server-Side_Bots>` on the server"""
    server_type: ServerType
    """Indicates the type of server"""
    server_environment: ServerEnvironment
    """Indicates the operating system of the server"""
    server_visibility: ServerVisibility
    """Indicates whether the server requires a password"""
    vac: VAC
    """Specifies whether the server uses :valve-wiki:`VAC <Valve_Anti-Cheat>`"""

    # These fields only exist in a response if the server is running The Ship

    """Indicates the game mode (:valve-wiki:`The Ship<The_Ship>` only)"""
    mode: TheShipGameMode
    """The number of witnesses necessary to have a player arrested (:valve-wiki:`The Ship<The_Ship>` only)"""
    witnesses: Byte
    """Time (in seconds) before a player is arrested while being witnessed (:valve-wiki:`The Ship<The_Ship>` only)"""
    duration: Byte

    version: String
    """Version of the game installed on the server"""

    _extra_data_flag: Byte  # TODO: make this IntFlag/Flag/ExtraDataFlag type
    """If present, this specifies which additional data fields will be included"""

    port: Short
    """The server's game port number"""
    steam_id: LongLong
    """Server's :valve-wiki:`SteamID<SteamID>`"""
    sourcetv_port: Short
    """Spectator port number for :valve-wiki:`SourceTV<SourceTV>`"""
    sourcetv_name: String
    """Name of the spectator server for :valve-wiki:`SourceTV<SourceTV>`"""
    keywords: String
    """Tags that describe the game according to the server (for future use)"""
    game_id: LongLong
    """
    The server's 64-bit GameID. If this is present, a more accurate :valve-wiki:`AppID<Steam_Application_IDs>` is 
    present in the low 24 bits. The earlier :valve-wiki:`AppID<Steam_Application_IDs>` could have been truncated as it 
    was forced into 16-bit storage.
    """

    def marshal_field_data(self, assembled_response: A2SBytesIO, field: Field):
        # Skip fields specific for the The Ship if that's not the current App ID we're querying for
        if field.name in ('mode', 'witnesses', 'duration') and APP_ID.get() != AppID.THE_SHIP:
            return
        # Special processing of Extra Data Flag (EDF) field
        elif field.name == '_extra_data_flag':
            # If the current file position is not the end it means that there is an EDF present
            if len(assembled_response.getvalue()) > assembled_response.tell():
                # Read out the next byte and store the bit field into the EDF
                self._extra_data_flag = assembled_response.read_byte()
            else:
                # Otherwise just set the EDF as having no flags if there is no next EDF byte to read
                self._extra_data_flag = 0x00
        # Port
        elif field.name == 'port':
            if self._extra_data_flag & ExtraDataFlag.GAME_PORT:
                self.port = assembled_response.read_short()
        # SteamID
        elif field.name == 'steam_id':
            if self._extra_data_flag & ExtraDataFlag.STEAM_ID:
                self.steam_id = assembled_response.read_long_long()
        # SourceTV Port & Name
        elif field.name == 'sourcetv_port':
            if self._extra_data_flag & ExtraDataFlag.SOURCETV:
                self.sourcetv_name = assembled_response.read_short()
        elif field.name == 'sourcetv_name':
            if self._extra_data_flag & ExtraDataFlag.SOURCETV:
                self.sourcetv_name = assembled_response.read_string()
        # Keywords (Tags)
        elif field.name == 'keywords':
            if self._extra_data_flag & ExtraDataFlag.KEYWORDS:
                self.keywords = assembled_response.read_string()
        # GameID
        elif field.name == 'game_id':
            if self._extra_data_flag & ExtraDataFlag.GAME_ID:
                self.game_id = assembled_response.read_long_long()
        # Otherwise...
        else:
            # Fallback to handling field normally...
            super().marshal_field_data(assembled_response, field)


@response(header=ord('m'))  # 0x6D
class A2SInfoGoldSrcResponse(A2SQueryResponse):
    address: String
    """IP address and port of the server (typically delimited with a colon, i.e. ``ip:port``)"""
    name: String
    """Name of the server"""
    map: String
    """Map the server has currently loaded"""
    folder: String
    """Name of the folder containing the game files"""
    game: String
    """Full name of the game"""
    players: Byte
    """Number of players on the server"""
    max_players: Byte
    """Maximum number of players the server reports it can hold"""
    protocol: Byte
    """Protocol version used by the server"""
    server_type: ServerType
    """Indicates the type of server"""
    server_environment: ServerEnvironment
    """Indicates the operating system of the server"""
    server_visibility: ServerVisibility
    """Indicates whether the server requires a password"""
    mod: Mod
    """Indicates whether the game is a mod"""

    # These fields are only present in the response if "Mod" is 1 (true):
    mod_link: String
    """URL to mod website"""
    mod_download_link: String
    """URL to download the mod"""
    _null: Byte = dataclasses.field(repr=False)  # NULL byte (0x00)
    """FIXME"""
    mod_version: Long
    """Version of mod installed on server"""
    mod_size: Long
    """Space (in bytes) the mod takes up"""
    mod_type: ModType
    """Indicates the type of mod"""
    mod_dll: ModDLL
    """Indicates whether mod uses its own :wikipedia:`DLL <Dynamic-link_library>`"""

    vac: VAC
    """Specifies whether the server uses VAC"""
    bots: Byte
    """Number of bots on the server"""

    def read_in_packet(self, packet_data: bytes) -> bool:
        if not packet_data.startswith(b'\xff\xff\xff\xff' + b'm'):
            # FIXME: Half-life 1 sends 3 responses!
            return False

        return super().read_in_packet(packet_data)

    def marshal_field_data(self, assembled_response: A2SBytesIO, field: Field):
        if (field.name.startswith('mod_') or field.name == '_null') and not self.mod:
            # Skip fields that are only present in response if "mod" field is not 1
            return
        else:
            # Otherwise fallback to handling field normally...
            super().marshal_field_data(assembled_response, field)


@response(header=ord('A'))  # 0x41
class A2SPlayerChallengeResponse(A2SQueryResponse):
    challenge: Long
    """Challenge number"""


@response(header=ord('D'))  # 0x44
class A2SPlayersResponse(A2SQueryResponse):
    """
    Represents details about each player on the server as returned by :meth:`A2SQueryContext.query_players`

    .. note:
        When a player is trying to connect to a server, they are recorded in the number of players. However, they will
        not be in the list of player information. i.e.
        :code:`len(A2SPlayersResponse()) != len(A2SPlayersResponse().players)`
    """

    _players: Byte
    players: List[A2SPlayer] = dataclasses.field(default_factory=list)
    """:class:`List <list>` of :class:`A2SPlayers <A2SPlayer>` on the server"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # TODO: fix dataclasses.field since we're overriding init in A2SQueryResponse
        self.players = list()

    def marshal_field_data(self, assembled_response: A2SBytesIO, field: Field):
        if field.name == 'players':
            # Is there one more byte that can be read from current buffer position?
            while len(assembled_response.getvalue()) - assembled_response.tell() >= 1:
                # Index is basically useless?
                _ = assembled_response.read_byte()

                # TODO: Fix type hinting
                next_player_chunk = A2SPlayer(
                    name=assembled_response.read_string(),
                    score=assembled_response.read_long(),
                    duration=timedelta(seconds=assembled_response.read_float()),
                )
                self.players.append(next_player_chunk)
        else:
            super().marshal_field_data(assembled_response, field)

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def __len__(self):
        return self._players or len(self.players)

    def __bool__(self) -> bool:
        return bool(len(self))


@response(header=ord('A'))  # 0x41
class A2SRulesChallengeResponse(A2SQueryResponse):
    challenge: Long
    """Challenge number"""


@response(header=ord('E'))  # 0x45
class A2SRulesResponse(A2SQueryResponse):
    """
    Represents a list of :valve-wiki:`server <Source_Dedicated_Server>` :valve-wiki:`configuration<CFG>`
    :valve-wiki:`rules<ConVar>` as returned by :meth:`A2SQueryContext.query_rules`.

    This class is dict-like and rules can be TODO
    """

    _rules: Short
    """
    Number of :valve-wiki:`server <Source_Dedicated_Server>` :valve-wiki:`configuration <CFG>`
    :valve-wiki:`rules <ConVar>`
     """
    rules: Dict = dataclasses.field(default_factory=dict)
    """
    :class:`Dictionary <dict>` ``name`` to ``value`` mapping of :valve-wiki:`server <Source_Dedicated_Server>`
    :valve-wiki:`configuration<CFG>` :valve-wiki:`rules<ConVar>`
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rules = dict()

    def __getitem__(self, key):
        return self.rules[key]

    def marshal_field_data(self, assembled_response: A2SBytesIO, field: Field):
        if field.name == 'rules':
            # Is there one more byte that can be read from current buffer position?
            while len(assembled_response.getvalue()) - assembled_response.tell() >= 1:
                name = assembled_response.read_string()
                value = assembled_response.read_string()

                # Get each rules name and value and store it in the dictionary
                self.rules[name] = value
        else:
            # Otherwise handle field data normally...
            super().marshal_field_data(assembled_response, field)


@response(header=ord('j'))  # 0x6A
class A2SPingResponse(A2SQueryResponse):
    _payload: String

    def __init__(self):
        if GAME_ENGINE.get() is Engine.SOURCE:
            self._payload = ''
        elif GAME_ENGINE.get() is Engine.GOLDSRC:
            self._payload = '0' * 14 + '.'

        super().__init__()


@response(header=ord('A'))  # 0x41
class A2SServerQueryGetChallengeResponse(A2SQueryResponse):
    challenge: Long
    """The challenge number to use"""
