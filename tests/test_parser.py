import pytest
import glob

from ppping.parser import PingResult, PingParserError

TEST_DIR = 'tests/'


class ExpectedResult(object):
    def __init__(self, address, hostname, icmp_seq, ttl, time):
        self.address = address
        self.hostname = hostname
        self.icmp_seq = icmp_seq
        self.ttl = ttl
        self.time = time

    def __str__(self):
        return 'host={}, address={}, icmp_sec={}, ttl={}, time={}'. \
            format(self.hostname, self.address, self.icmp_seq, self.ttl, self.time)


class TestPingResult(object):
    def test_parser(self):

        expected = {
            'localhost': ExpectedResult(address='::1', hostname='localhost', icmp_seq=1, ttl=64, time=0.063),
            '8.8.8.8': ExpectedResult(address='8.8.8.8', hostname='8.8.8.8', icmp_seq=1, ttl=57, time=6.21),
            'google.com': ExpectedResult(address='172.217.27.174', hostname='kix05s07-in-f174.1e100.net',
                                         icmp_seq=1, ttl=54, time=6.19),
        }

        test_messages = [open(TEST_DIR + 'txt/{}.txt'.format(host), 'rt').read() for host in expected.keys()]
        test_message_raw = [m.encode() for m in test_messages]

        for test_message, raw, e in zip(test_messages, test_message_raw, expected.values()):
            result = PingResult(test_message)
            assert result.raw == test_message
            assert result.address == e.address
            assert result.hostname == e.hostname
            assert result.icmp_seq == e.icmp_seq
            assert result.ttl == e.ttl
            assert result.time == e.time

            result = PingResult(raw)
            assert result.raw == test_message
            assert result.address == e.address
            assert result.hostname == e.hostname
            assert result.icmp_seq == e.icmp_seq
            assert result.ttl == e.ttl
            assert result.time == e.time

            assert str(result) == str(e)

    def test_parser_error(self):

        errors = [open(g, 'rt').read() for g in glob.glob(TEST_DIR + 'error*.txt')]

        for e in errors:
            with pytest.raises(PingParserError):
                PingResult(e)
