from enum import IntEnum
from unittest import TestCase

from aioa2squery import (
    TheShipGameMode,
    ServerType,
    ServerEnvironment,
    ServerVisibility,
    OrdinalByteRepresentationMixin,
)


class TestEnumerationMixins(TestCase):
    def test_ordinal_byte_representation_mixin(self):
        class SomeEnum(OrdinalByteRepresentationMixin, IntEnum):
            MEMBER = ord('X')

        self.assertEqual("<SomeEnum.MEMBER: 'X'>", repr(SomeEnum.MEMBER))


class TestEnumerationBehaviors(TestCase):
    def test_server_environment_goldsource_to_lower(self):
        self.assertIs(ServerEnvironment.WINDOWS, ServerEnvironment(ord('W')))

    def test_server_type_goldsource_to_lower(self):
        self.assertIs(ServerType.DEDICATED_SERVER, ServerType(ord('D')))

    def test_server_environment_goldsource_mac_and_osx_should_be_missing(self):
        def test_mac():
            _ = ServerEnvironment(ord('M'))

        def test_osx():
            _ = ServerEnvironment(ord('O'))

        self.assertRaises(ValueError, test_mac)
        self.assertRaises(ValueError, test_osx)

    def test_server_visibility_members_boolean_values(self):
        self.assertTrue(ServerVisibility.PUBLIC)

        self.assertFalse(ServerVisibility.PRIVATE)
        self.assertFalse(ServerVisibility.PASSWORDED)

    def test_simple_member_string_enum_mixin(self):
        self.assertEqual('Hunt', str(TheShipGameMode.HUNT))
        self.assertEqual('Team Elimination', str(TheShipGameMode.TEAM_ELIMINATION))
        self.assertEqual('VIP Team', str(TheShipGameMode.VIP_TEAM))
