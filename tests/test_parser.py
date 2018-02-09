import pytest
import glob

from ppping.parser import PingResult, PingParserError

TXT_DIR = 'tests/txt/'


class DummyResult(object):
    def __init__(self, address, hostname, icmp_seq, ttl, time):
        self.address = address
        self.hostname = hostname
        self.icmp_seq = icmp_seq
        self.ttl = ttl
        self.time = time


class TestPingResult(object):
    def test_parser(self):

        expected = {
            'localhost': DummyResult(address='::1', hostname='localhost',
                                     icmp_seq=1, ttl=64, time=0.063),
            '8.8.8.8': DummyResult(address='8.8.8.8', hostname='8.8.8.8',
                                   icmp_seq=1, ttl=57, time=6.21),
            'google.com': DummyResult(address='172.217.27.174',
                                      hostname='kix05s07-in-f174.1e100.net',
                                      icmp_seq=1, ttl=54, time=6.19),
        }

        messages = [open(TXT_DIR + '{}.txt'.format(host), 'rt').read()
                    for host in expected.keys()]

        message_raw = [m.encode() for m in messages]

        for m, raw, e in zip(messages, message_raw, expected.values()):
            result = PingResult(m)
            assert result.raw == m
            assert result.address == e.address
            assert result.hostname == e.hostname
            assert result.icmp_seq == e.icmp_seq
            assert result.ttl == e.ttl
            assert result.time == e.time

            result = PingResult(raw)
            assert result.raw == m
            assert result.address == e.address
            assert result.hostname == e.hostname
            assert result.icmp_seq == e.icmp_seq
            assert result.ttl == e.ttl
            assert result.time == e.time

    def test_parser_error(self):

        errors = [open(g, 'rt').read()
                  for g in glob.glob(TXT_DIR + 'error*.txt')]

        for e in errors:
            with pytest.raises(PingParserError):
                PingResult(e)
