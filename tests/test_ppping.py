import pytest

from ppping.ppping import PPPing


class DummyScreen(object):
    def clear(self):
        pass

    def refresh(self):
        pass

    def addstr(self, y, x, string, mode):
        pass


class TestPPPing(object):
    def test_ppping(self):
        scr = DummyScreen()

        test_host = ['localhost', 'google.com', '8.8.8.8']

        p = PPPing(args=test_host, duration=3, no_host=True)
        p.run(scr)

        p = PPPing(args=[], duration=3, config='ppping.conf', no_host=True)
        p.run(scr)

        p = PPPing(args=test_host, duration=3, no_host=False)
        p.run(scr)

        p = PPPing(args=[], duration=3, config='ppping.conf', no_host=False)
        p.run(scr)

    def test_failed_host(self):
        scr = DummyScreen()
        p = PPPing(args=['foo.bar'], duration=3, no_host=True)
        p.run(scr)

    def test_scale_char(self):
        p = PPPing(args=['foo.bar'], duration=3, no_host=True)

        rtt = [5, 15, 25, 35, 45, 55, 65, 75]
        expected = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

        for i, e in zip(rtt, expected):
            assert p.scale_char(i) == e

    def test_open_config(self):
        with pytest.raises(FileNotFoundError):
            PPPing(args=[], duration=3, config='nothing.conf', no_host=False)
