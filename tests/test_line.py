import pytest

from ppping.line import Line, SetLineError
from ppping.parser import PingResult

TEST_DIR = 'tests/'


class TestLine(object):
    def test_line(self):
        line = Line(0, arg='localshot', name='TEST', space=1)

        line.add_info(PingResult(open(TEST_DIR + 'txt/localhost.txt', 'rt').read()))
        line.add_char('X')

        assert line.x_pos() == 0
        assert line.y_pos() == 1

        name_len = (True, False)
        no_host = (True, False)

        # assert line.get_line('>', True, 5, 5, 5, 5, 5)
