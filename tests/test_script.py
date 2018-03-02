import pytest
import sys
import curses

from ppping.ppping import PPPing
from ppping.script import main, set_args


class DummyPPPingKeyboardInterrupt(PPPing):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, stdscr):
        raise KeyboardInterrupt


class DummyPPPingProcessLookupError(PPPing):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, stdscr):
        raise ProcessLookupError


def test_set_args():
    sys.argv = ['test', 'localhost', '8.8.8.8']
    args = set_args()
    assert args.args == ['localhost', '8.8.8.8']


def test_main():
    sys.argv = ['test', 'localhost', '8.8.8.8', '-d', '3']

    with pytest.raises(curses.error):
        assert main()


def test_script_no_args():
    sys.argv = ['test']
    with pytest.raises(SystemExit):
        main()


def test_quit():
    dummy = DummyPPPingKeyboardInterrupt(args=[], config='ppping.conf',
                                         duration=3, no_host=False)

    with pytest.raises(SystemExit):
        main(ppping=dummy)

    dummy = DummyPPPingProcessLookupError(args=[], config='ppping.conf',
                                          duration=3, no_host=False)
    with pytest.raises(SystemExit):
        main(ppping=dummy)
