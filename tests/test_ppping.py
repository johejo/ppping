import pytest

from ppping.ppping import PPPing


class DummyScreen(object):
    def clear(self):
        pass

    def refresh(self):
        pass

    def addstr(self, y, x, string, mode):
        pass


scr = DummyScreen()
test_host = ['localhost', 'google.com', '8.8.8.8']


def test_no_host():
    p = PPPing(args=test_host, duration=3, no_host=True)
    p.run(scr)


def test_no_host_false():
    p = PPPing(args=test_host, duration=3, no_host=False)
    p.run(scr)


def test_config_no_host():
    p = PPPing(args=[], duration=3, config='ppping.conf', no_host=True)
    p.run(scr)


def test_config_no_host_false():
    p = PPPing(args=[], duration=3, config='ppping.conf', no_host=False)
    p.run(scr)


def test_failed_host():
    p = PPPing(args=['foo.bar'], duration=3, no_host=True)
    p.run(scr)


def test_scale_char():
    p = PPPing(args=['foo.bar'], duration=3, no_host=True)

    rtt = [5, 15, 25, 35, 45, 55, 65, 75]
    expected = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

    for i, e in zip(rtt, expected):
        assert p.scale_char(i) == e


def test_open_config():
    with pytest.raises(FileNotFoundError):
        PPPing(args=[], duration=3, config='nothing.conf', no_host=False)


def test_closed_network():
    p = PPPing(args=test_host, duration=3, no_host=True, closed=True)
    assert p._n_headers == 2
    assert p.info.find('Global') <= 0
    p.run(scr)


def test_connected_network():
    p = PPPing(args=test_host, duration=3, no_host=True, closed=False)
    assert p._n_headers == 3
    assert p.info.find('Global') > 0
    p.run(scr)
