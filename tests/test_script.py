import pytest
import sys
import curses

from ppping.script import main, set_args


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
