from dataclasses import is_dataclass
from unittest import TestCase

from aioa2squery.context import REQUEST_PACKET_SPLIT_SIZE
from aioa2squery.requests import (
    request,

    A2SQueryRequest,

    A2SInfoRequest,
    A2SPingRequest,
    A2SPlayerRequest,
    A2SRulesChallengeRequest,
    A2SServerQueryGetChallengeRequest,
)


class TestRequestDecorator(TestCase):
    def test_request_decorator_adds_message_id(self):
        @request(header=ord('X'))
        class _Test(A2SQueryRequest):
            pass

        self.assertTrue(is_dataclass(_Test))
        self.assertEqual(_Test()._message_header, ord('X'))

    def test_request_class_constructed_with_bad_decorator_fails(self):
        # FIXME
        return

        # noinspection PyUnusedLocal
        def _test():
            # Using the @request() decorator incorrectly without passing a message ID header argument should fail at
            # import-time
            @request
            class _Test(A2SQueryRequest):
                pass

        self.assertRaises(AssertionError, _test)

    def test_request_class_does_not_subclass_base(self):
        def _test():
            @request(header=ord('X'))
            class _Test:
                pass

        self.assertRaises(AssertionError, _test)

    def test_multi_packet_request_size_too_low(self):
        # FIXME
        return

        def _test():
            REQUEST_PACKET_SPLIT_SIZE.set(1)

            @request(header=ord('X'))
            class _Test(A2SQueryRequest):
                pass

        self.assertRaises(ValueError, _test)

    def test_multi_packet_request_size_too_high(self):
        # FIXME
        return

        def _test():
            REQUEST_PACKET_SPLIT_SIZE.set(1_000_000)

            @request(header=ord('X'))
            class _Test(A2SQueryRequest):
                pass

        self.assertRaises(ValueError, _test)


class TestStandardRequests(TestCase):
    def test_a2s_info_query_request(self):
        self.assertEqual(
            first=A2SInfoRequest().getvalue(),
            second=(
                b'\xFF\xFF\xFF\xFF'         # -1 (split mode header)
                b'T'                        # 'T' (message header)
                b'Source Engine Query\x00'  # request payload string
            ),
        )

    def test_a2s_players_challenge_request(self):
        self.assertEqual(
            first=A2SPlayerRequest().getvalue(),
            second=bytes.fromhex(
                'FF FF FF FF'   # -1 (split mode header)
                '55'            # 'U' (message header)
                'FF FF FF FF'   # -1 (receive challenge)
            ),
        )

    def test_a2s_player_challenge_request_with_number(self):
        self.assertEqual(
            first=A2SPlayerRequest(584425803).getvalue(),
            second=bytes.fromhex(
                'FF FF FF FF'  # -1 (split mode header)
                '55'           # 'U' (message header)
                '4B A1 D5 22'  # 584425803 (challenge number)
            ),
        )

    def test_a2s_rules_challenge_request(self):
        self.assertEqual(
            first=A2SRulesChallengeRequest().getvalue(),
            second=bytes.fromhex(
                'FF FF FF FF'    # -1 (split mode header)
                '56'             # 'V'
                'FF FF FF FF'    # -1 (receive challenge)
            ),
        )

    def test_a2s_rules_challenge_request_with_number(self):
        self.assertEqual(
            first=A2SRulesChallengeRequest(584425803).getvalue(),
            second=bytes.fromhex(
                'FF FF FF FF'    # -1 (split mode header)
                '56'             # 
                '4B A1 D5 22'    #
            )
        ),

    def test_a2s_ping_query_request(self):
        self.assertEqual(
            first=A2SPingRequest().getvalue(),
            second=bytes.fromhex(
                'FF FF FF FF'  # -1 (split mode header)
                '69'           # 'i' (message ID)
            ),
        )

    def test_a2s_serverquery_challenge_request(self):
        self.assertEqual(
            first=A2SServerQueryGetChallengeRequest().getvalue(),
            second=bytes.fromhex(
                'FF FF FF FF'  # -1 (split mode header)
                '57'           # 'W' (message ID)
            ),
        )
