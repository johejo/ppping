from ppping.line import Line
from ppping.parser import PingResult

TXT_DIR = 'tests/txt/'


class TestLine(object):
    def test_line(self):
        line = Line(0, arg='localhost', space=1)

        with open(TXT_DIR + 'localhost.txt', 'rt') as f:
            ping_message = f.read()

        line.add_info(PingResult(ping_message))
        line.add_char('▁')

        assert line.x_pos() == 0
        assert line.y_pos() == 1

        expected = '>localhost  localhost ::1     0.06 ▁'
        assert line.get_line('>', False, 10, 0, 9, 7, 4) == expected

        for _ in range(5):
            line.add_char('▁')

        line.reduce(result_len=5)

        expected = '>localhost                 ::1     0.06 ▁▁▁▁▁'
        assert line.get_line('>', True, 14, 10, 9, 7, 4) == expected

    def test_get_line(self):

        with open(TXT_DIR + 'localhost.txt', 'rt') as f:
            ping_message = f.read()

        line = Line(0, arg='localhost', space=1)

        line.add_info(PingResult(ping_message))
        line.add_char('▁')

        expected = '>localhost  ::1     0.06 ▁'
        assert line.get_line('>', True, 10, 0, 9, 7, 4) == expected

        line = Line(0, arg='localhost', space=1)

        line.add_info(PingResult(ping_message))
        line.add_char('▁')

        expected = '>localhost             localhost ::1     0.06 ▁'
        assert line.get_line('>', False, 10, 10, 9, 7, 4) == expected
